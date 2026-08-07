from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

FET001_CASE_FAMILIES = {
    "READY_ABSENT_PERMISSION",
    "READY_PURPOSE_MISMATCH",
    "REJECTED_CONTEXT_INDEPENDENT_PATH",
    "EXPIRED_READY",
    "MODIFIED_DIGEST",
    "READY_MATCHING_PERMISSION",
    "READY_REVOKED_PERMISSION",
    "HOLD_NO_AUTHORITY",
}

FET001_EXPECTED_OUTCOMES = {
    "READY_ABSENT_PERMISSION": ("ACCEPTED", "DENY_FEDERATED", set()),
    "READY_PURPOSE_MISMATCH": ("REJECTED_SCOPE", "DENY_FEDERATED", set()),
    "REJECTED_CONTEXT_INDEPENDENT_PATH": (
        "REJECTED_CONTEXT",
        "ALLOW_INDEPENDENT",
        {"open-review-ticket"},
    ),
    "EXPIRED_READY": ("REJECTED_EXPIRED", "DENY_FEDERATED", set()),
    "MODIFIED_DIGEST": ("REJECTED_INTEGRITY", "DENY_FEDERATED", set()),
    "READY_MATCHING_PERMISSION": (
        "ACCEPTED",
        "ALLOW_FEDERATED",
        {"publish-release"},
    ),
    "READY_REVOKED_PERMISSION": ("ACCEPTED", "DENY_FEDERATED", set()),
    "HOLD_NO_AUTHORITY": ("REJECTED_CONTEXT", "DENY_FEDERATED", set()),
}

FET001_BASELINE = {
    "agent-governance-systems": "bfe416d0d91e5fbad5459a888d8d277ae7099b85",
    "agent-context-proof": "7fb35d3ff9ef31ffec46672510fdf87795c1de78",
    "agent-authority-benchmark": "2506171db41a804f6c4418f0be607f7747d7420f",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_errors(instance: object, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(
        validator.iter_errors(instance), key=lambda item: list(item.path)
    ):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{label}:{location}: {error.message}")
    return errors


def canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_fet001(root: Path) -> list[str]:
    trial_root = root / "trials/FET-001"
    required_paths = [
        trial_root / "README.md",
        trial_root / "protocol.v0.1.md",
        trial_root / "protocol.v0.1.json",
        trial_root / "fixtures/development-cases.v0.1.json",
        trial_root / "fixtures/mutations.v0.1.json",
        trial_root / "freeze-manifest.v0.1.json",
        trial_root / "schemas/context-envelope.v0.1.schema.json",
        trial_root / "schemas/case.v0.1.schema.json",
        trial_root / "schemas/mutation.v0.1.schema.json",
        trial_root / "schemas/report.v0.1.schema.json",
        trial_root / "schemas/protocol.v0.1.schema.json",
        trial_root / "schemas/freeze-manifest.v0.1.schema.json",
    ]
    missing = [path for path in required_paths if not path.is_file()]
    if missing:
        return [
            f"missing FET-001 artifact: {path.relative_to(root)}" for path in missing
        ]

    protocol = load_json(trial_root / "protocol.v0.1.json")
    protocol_text = (trial_root / "protocol.v0.1.md").read_text(encoding="utf-8")
    cases_document = load_json(trial_root / "fixtures/development-cases.v0.1.json")
    mutations_document = load_json(trial_root / "fixtures/mutations.v0.1.json")
    freeze = load_json(trial_root / "freeze-manifest.v0.1.json")

    schema_names = {
        "protocol": "protocol.v0.1.schema.json",
        "envelope": "context-envelope.v0.1.schema.json",
        "case": "case.v0.1.schema.json",
        "mutation": "mutation.v0.1.schema.json",
        "report": "report.v0.1.schema.json",
        "freeze": "freeze-manifest.v0.1.schema.json",
    }
    schemas = {
        name: load_json(trial_root / "schemas" / filename)
        for name, filename in schema_names.items()
    }
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)

    errors = schema_errors(protocol, schemas["protocol"], "FET-001 protocol")
    errors.extend(schema_errors(freeze, schemas["freeze"], "FET-001 freeze"))

    cases = cases_document.get("cases", [])
    if set(cases_document) != {"schema_version", "trial_id", "fixture_class", "cases"}:
        errors.append("FET-001 case document has an unexpected top-level field")
    if cases_document.get("schema_version") != "0.1.0":
        errors.append("FET-001 case document schema_version mismatch")
    if cases_document.get("trial_id") != "FET-001":
        errors.append("FET-001 case document trial_id mismatch")
    if cases_document.get("fixture_class") != "public-development":
        errors.append("FET-001 cases must remain public development fixtures")

    case_ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    for case_id in sorted({value for value in case_ids if case_ids.count(value) > 1}):
        errors.append(f"duplicate FET-001 case_id: {case_id}")
    families = {case.get("family") for case in cases if isinstance(case, dict)}
    if families != FET001_CASE_FAMILIES:
        errors.append("FET-001 case family coverage mismatch")

    protocol_rule_ids = {rule.get("id") for rule in protocol.get("rules", [])}
    expected_rule_ids = {f"FET-R{number:02d}" for number in range(1, 13)}
    if protocol_rule_ids != expected_rule_ids:
        errors.append("FET-001 protocol rule coverage mismatch")
    for rule_id in expected_rule_ids:
        if rule_id not in protocol_text:
            errors.append(f"FET-001 normative protocol omits {rule_id}")
    if protocol.get("proposition") not in protocol_text:
        errors.append("FET-001 normative and machine propositions differ")
    for disposition in protocol.get("federated_route_dispositions", []) + protocol.get(
        "authority_dispositions", []
    ):
        if disposition not in protocol_text:
            errors.append(
                f"FET-001 normative protocol omits disposition: {disposition}"
            )
    for case in cases:
        case_id = case.get("case_id", "<unknown>")
        errors.extend(schema_errors(case, schemas["case"], str(case_id)))
        envelope = case.get("envelope", {})
        errors.extend(
            schema_errors(envelope, schemas["envelope"], f"{case_id} envelope")
        )
        actual_digest = canonical_json_sha256(envelope)
        declared_digest = case.get("envelope_sha256")
        if case.get("family") == "MODIFIED_DIGEST":
            if actual_digest == declared_digest:
                errors.append(
                    f"modified-digest fixture unexpectedly matches: {case_id}"
                )
        elif actual_digest != declared_digest:
            errors.append(f"envelope digest mismatch for {case_id}")

        expected_outcome = FET001_EXPECTED_OUTCOMES.get(case.get("family"))
        if expected_outcome is not None:
            declared_outcome = (
                case.get("expected", {}).get("federated_route"),
                case.get("expected", {}).get("authority_disposition"),
                set(case.get("expected", {}).get("committed_effects", [])),
            )
            if declared_outcome != expected_outcome:
                errors.append(f"FET-001 expected outcome mismatch for {case_id}")

        if not set(case.get("rules", [])).issubset(protocol_rule_ids):
            errors.append(f"unknown protocol rule in {case_id}")

        try:
            created = parse_timestamp(envelope["created_at"])
            expires = parse_timestamp(envelope["expires_at"])
            evaluated = parse_timestamp(case["evaluation_time"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"invalid temporal boundary in {case_id}")
        else:
            if not created < expires:
                errors.append(f"non-increasing envelope validity interval in {case_id}")
            is_expired = evaluated >= expires
            expected_route = case.get("expected", {}).get("federated_route")
            if case.get("family") == "EXPIRED_READY" and not is_expired:
                errors.append(f"expired fixture is not expired: {case_id}")
            if is_expired and expected_route != "REJECTED_EXPIRED":
                errors.append(f"expired fixture lacks rejected outcome: {case_id}")

        purpose_id = envelope.get("purpose", {}).get("id")
        effect_purpose = case.get("requested_effect", {}).get("purpose_id")
        expected_route = case.get("expected", {}).get("federated_route")
        if purpose_id != effect_purpose and expected_route != "REJECTED_SCOPE":
            errors.append(f"purpose mismatch lacks rejected outcome: {case_id}")

        decision = envelope.get("decision")
        trust_state = envelope.get("trust", {}).get("state")
        if (
            decision != "READY" or trust_state != "verified"
        ) and expected_route not in {
            "REJECTED_CONTEXT",
            "REJECTED_EXPIRED",
        }:
            errors.append(f"insufficient Context lacks rejected outcome: {case_id}")

        authority_state = case.get("consumer_authority", {}).get("state")
        authority_disposition = case.get("expected", {}).get("authority_disposition")
        if authority_disposition == "ALLOW_FEDERATED" and authority_state != "GRANTED":
            errors.append(f"federated allow lacks granted authority: {case_id}")
        if authority_state in {"ABSENT", "DENIED", "REVOKED"} and (
            authority_disposition == "ALLOW_FEDERATED"
        ):
            errors.append(f"restricted authority has federated allow: {case_id}")
        independent = case.get("independent_path", {})
        if authority_disposition == "ALLOW_INDEPENDENT" and not (
            independent.get("available") and independent.get("authorized")
        ):
            errors.append(f"independent allow lacks independent authority: {case_id}")

    mutations = mutations_document.get("mutations", [])
    if set(mutations_document) != {"schema_version", "trial_id", "mutations"}:
        errors.append("FET-001 mutation document has an unexpected top-level field")
    if mutations_document.get("schema_version") != "0.1.0":
        errors.append("FET-001 mutation document schema_version mismatch")
    if mutations_document.get("trial_id") != "FET-001":
        errors.append("FET-001 mutation document trial_id mismatch")

    mutation_ids = [
        mutation.get("mutation_id")
        for mutation in mutations
        if isinstance(mutation, dict)
    ]
    for mutation_id in sorted(
        {value for value in mutation_ids if mutation_ids.count(value) > 1}
    ):
        errors.append(f"duplicate FET-001 mutation_id: {mutation_id}")
    mutation_families = {
        mutation.get("family") for mutation in mutations if isinstance(mutation, dict)
    }
    if mutation_families != set(protocol.get("required_mutation_families", [])):
        errors.append("FET-001 mutation family coverage mismatch")
    for mutation in mutations:
        mutation_id = mutation.get("mutation_id", "<unknown>")
        errors.extend(schema_errors(mutation, schemas["mutation"], str(mutation_id)))
        if not set(mutation.get("violated_rules", [])).issubset(protocol_rule_ids):
            errors.append(f"unknown protocol rule in {mutation_id}")

    report_schema = schemas["report"]
    if report_schema.get("properties", {}).get("dimension_results") is None:
        errors.append("FET-001 report schema lacks separated dimension results")

    protocol_baseline = {
        item["name"]: item["commit"]
        for item in protocol.get("baseline", {}).get("repositories", [])
    }
    freeze_baseline = {
        item["name"]: item["commit"]
        for item in freeze.get("baseline", {}).get("repositories", [])
    }
    if protocol_baseline != FET001_BASELINE or freeze_baseline != FET001_BASELINE:
        errors.append("FET-001 federation baseline mismatch")
    if protocol.get("implementation_gate", {}).get("state") != "closed":
        errors.append("FET-001 protocol implementation gate is not closed")
    if freeze.get("implementation_gate") != "closed":
        errors.append("FET-001 freeze implementation gate is not closed")

    frozen_entries = {
        item.get("path"): item.get("sha256") for item in freeze.get("artifacts", [])
    }
    actual_frozen_paths = {
        str(path.relative_to(root))
        for path in trial_root.rglob("*")
        if path.is_file() and path.name != "freeze-manifest.v0.1.json"
    }
    if set(frozen_entries) != actual_frozen_paths:
        errors.append("FET-001 frozen artifact set mismatch")
    for relative_path, declared_digest in frozen_entries.items():
        artifact_path = root / relative_path
        if not artifact_path.is_file():
            continue
        actual_digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        if actual_digest != declared_digest:
            errors.append(f"frozen artifact digest mismatch: {relative_path}")

    return sorted(set(errors))


def validate_fet001_implementation_gate(
    root: Path, registry: dict[str, Any]
) -> list[str]:
    schema_path = root / "schemas/trial-implementation-gate.v0.1.schema.json"
    gate_path = root / "gates/FET-001/implementation-gate.v0.1.json"
    readme_path = root / "gates/FET-001/README.md"
    missing = [
        path.relative_to(root)
        for path in (schema_path, gate_path, readme_path)
        if not path.is_file()
    ]
    if missing:
        return [
            f"missing FET-001 implementation-gate artifact: {path}" for path in missing
        ]

    schema = load_json(schema_path)
    gate = load_json(gate_path)
    Draft202012Validator.check_schema(schema)
    errors = schema_errors(gate, schema, "FET-001 implementation gate")

    expected_protocol_binding = {
        "pull_request": "https://github.com/heronyogi/agent-governance-systems/pull/2",
        "protocol_source_commit": "ec522b8a190d51e33309e08dbc74bbc2c4e22051",
        "protocol_merge_commit": "83ef57c750eee4da56f6c358c85e9effa45d21b7",
        "freeze_manifest_sha256": (
            "1636497fa8b67bf3452f673d7b233bee428e257715722b56f6d1b237c008b4a2"
        ),
        "post_merge_check": (
            "https://github.com/heronyogi/agent-governance-systems/"
            "actions/runs/31220113497"
        ),
    }
    if gate.get("protocol_binding") != expected_protocol_binding:
        errors.append("FET-001 implementation gate protocol binding mismatch")

    freeze_path = root / "trials/FET-001/freeze-manifest.v0.1.json"
    freeze_digest = hashlib.sha256(freeze_path.read_bytes()).hexdigest()
    if gate.get("protocol_binding", {}).get("freeze_manifest_sha256") != freeze_digest:
        errors.append("FET-001 implementation gate freeze digest mismatch")

    review = gate.get("review_record", {})
    for count_name in (
        "conversation_comments",
        "reviews",
        "review_threads",
        "unresolved_review_threads",
        "change_requests",
    ):
        if review.get(count_name) != 0:
            errors.append(f"FET-001 gate review count mismatch: {count_name}")
    if review.get("independent_review") is not False:
        errors.append("FET-001 gate must not claim independent review")
    if review.get("blocking_ambiguities") != []:
        errors.append("FET-001 gate has unresolved blocking ambiguity")

    registry_by_id = {
        entry.get("system_id"): entry
        for entry in registry.get("systems", [])
        if isinstance(entry, dict)
    }
    expected_tracks = {
        "PRODUCER": "agent-context-integrity",
        "CONSUMER": "agent-authority-integrity",
    }
    tracks = {
        track.get("track_id"): track
        for track in gate.get("implementation_tracks", [])
        if isinstance(track, dict)
    }
    if set(tracks) != set(expected_tracks):
        errors.append("FET-001 implementation track coverage mismatch")
    for track_id, system_id in expected_tracks.items():
        track = tracks.get(track_id, {})
        entry = registry_by_id.get(system_id, {})
        if track.get("system_id") != system_id:
            errors.append(f"FET-001 {track_id.lower()} system mismatch")
        if track.get("repository_url") != entry.get("repository_url"):
            errors.append(f"FET-001 {track_id.lower()} repository mismatch")
        expected_commit = entry.get("activation", {}).get("source_commit")
        if track.get("base_commit") != expected_commit:
            errors.append(f"FET-001 {track_id.lower()} base commit mismatch")

        authorized_text = " ".join(track.get("authorized_changes", [])).lower()
        prohibited_authorizations = (
            "live model",
            "provider api",
            "production data",
            "production traffic",
            "real external side effect",
            "claim a fet-001 experimental",
            "publish sealed",
        )
        if any(phrase in authorized_text for phrase in prohibited_authorizations):
            errors.append(
                f"FET-001 {track_id.lower()} authorized scope exceeds the gate"
            )

    required_non_authorizations = {
        "Live model or provider API calls",
        "Production data, credentials, or external side effects",
        "Publication of sealed or independently authored cases",
        "A FET-001 experimental, safety, or production claim",
        "Modification of the frozen FET-001 protocol packet",
        "Opening the development-execution gate",
    }
    if not required_non_authorizations.issubset(
        set(gate.get("non_authorizations", []))
    ):
        errors.append("FET-001 implementation gate non-authorization mismatch")
    if gate.get("next_gate", {}).get("state") != "closed":
        errors.append("FET-001 development-execution gate is not closed")

    return sorted(set(errors))


def validate_catalog(root: Path = ROOT) -> list[str]:
    manifest_schema = load_json(root / "schemas/system-manifest.v0.1.schema.json")
    registry_schema = load_json(root / "schemas/system-registry.v0.1.schema.json")
    Draft202012Validator.check_schema(manifest_schema)
    Draft202012Validator.check_schema(registry_schema)

    registry_path = root / "registry/systems.v0.1.json"
    registry = load_json(registry_path)
    errors = schema_errors(registry, registry_schema, registry_path.name)

    manifest_paths = sorted((root / "manifests").glob("*.json"))
    manifests: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in manifest_paths:
        manifest = load_json(path)
        errors.extend(schema_errors(manifest, manifest_schema, path.name))
        system_id = manifest.get("system_id")
        if not isinstance(system_id, str):
            continue
        if system_id in manifests:
            errors.append(f"duplicate manifest system_id: {system_id}")
        manifests[system_id] = (path, manifest)
        if path.stem != system_id:
            errors.append(f"manifest filename does not match system_id: {path.name}")

    entries = registry.get("systems", [])
    entry_ids = [entry.get("system_id") for entry in entries if isinstance(entry, dict)]
    duplicates = sorted(
        {system_id for system_id in entry_ids if entry_ids.count(system_id) > 1}
    )
    for system_id in duplicates:
        errors.append(f"duplicate registry system_id: {system_id}")

    registered_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        system_id = entry.get("system_id")
        path_value = entry.get("catalog_manifest")
        if isinstance(path_value, str):
            registered_paths.add(path_value)
        if system_id not in manifests:
            errors.append(f"registry references missing manifest: {system_id}")
            continue
        _, manifest = manifests[system_id]
        if entry.get("repository_url") != manifest.get("repository", {}).get("url"):
            errors.append(f"repository URL mismatch for {system_id}")
        if entry.get("source_manifest") != manifest.get("repository", {}).get(
            "manifest_path"
        ):
            errors.append(f"source manifest path mismatch for {system_id}")
        expected_path = str(manifests[system_id][0].relative_to(root))
        if path_value != expected_path:
            errors.append(f"catalog manifest path mismatch for {system_id}")
        activation = entry.get("activation")
        if isinstance(activation, dict):
            manifest_digest = hashlib.sha256(
                manifests[system_id][0].read_bytes()
            ).hexdigest()
            if activation.get("source_manifest_sha256") != manifest_digest:
                errors.append(f"activation manifest digest mismatch for {system_id}")

    actual_paths = {str(path.relative_to(root)) for path in manifest_paths}
    for path in sorted(actual_paths - registered_paths):
        errors.append(f"unregistered manifest: {path}")
    for path in sorted(registered_paths - actual_paths):
        errors.append(f"registered manifest does not exist: {path}")

    known_ids = set(manifests)
    for system_id, (_, manifest) in manifests.items():
        relation_by_id = {
            relation["system_id"]: relation
            for relation in manifest.get("relationships", [])
            if isinstance(relation, dict) and "system_id" in relation
        }
        for related_id, relation in relation_by_id.items():
            if related_id not in known_ids:
                errors.append(
                    f"unknown relationship target for {system_id}: {related_id}"
                )
                continue
            if relation.get("kind") == "sibling":
                reciprocal = {
                    item.get("system_id"): item
                    for item in manifests[related_id][1].get("relationships", [])
                    if isinstance(item, dict)
                }.get(system_id)
                if reciprocal is None or reciprocal.get("kind") != "sibling":
                    errors.append(
                        "nonreciprocal sibling relationship: "
                        f"{system_id} -> {related_id}"
                    )

        dependencies = manifest.get("dependencies", {})
        for dependency_kind in ("runtime_systems", "evaluation_systems"):
            for dependency_id in dependencies.get(dependency_kind, []):
                if dependency_id == system_id:
                    errors.append(f"self dependency for {system_id}: {dependency_kind}")
                elif dependency_id not in known_ids:
                    errors.append(
                        f"unknown {dependency_kind} dependency for {system_id}: "
                        f"{dependency_id}"
                    )

        interface_ids = [
            interface.get("id")
            for direction in ("provides", "consumes")
            for interface in manifest.get("interfaces", {}).get(direction, [])
            if isinstance(interface, dict)
        ]
        for interface_id in sorted(
            {value for value in interface_ids if interface_ids.count(value) > 1}
        ):
            errors.append(f"duplicate interface id for {system_id}: {interface_id}")

    errors.extend(validate_fet001(root))
    errors.extend(validate_fet001_implementation_gate(root, registry))
    return sorted(set(errors))


def main() -> int:
    errors = validate_catalog()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    manifest_count = len(list((ROOT / "manifests").glob("*.json")))
    print(f"catalog valid: {manifest_count} systems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
