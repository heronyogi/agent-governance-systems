from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.validate_catalog import ROOT, canonical_json_sha256, validate_catalog


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def copy_catalog(tmp_path: Path) -> Path:
    target = tmp_path / "catalog"
    for directory in ("manifests", "registry", "schemas", "trials"):
        shutil.copytree(ROOT / directory, target / directory)
    return target


def test_catalog_is_valid() -> None:
    assert validate_catalog() == []


def test_unregistered_manifest_is_rejected(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    source = catalog / "manifests/agent-context-integrity.json"
    extra = json.loads(source.read_text(encoding="utf-8"))
    extra["system_id"] = "unregistered-system"
    extra["repository"]["url"] = "https://github.com/example/unregistered-system"
    write_json(catalog / "manifests/unregistered-system.json", extra)

    assert "unregistered manifest" in "\n".join(validate_catalog(catalog))


def test_unknown_relationship_is_rejected(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "manifests/agent-context-integrity.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["relationships"][0]["system_id"] = "missing-system"
    write_json(path, manifest)

    assert "unknown relationship target" in "\n".join(validate_catalog(catalog))


def test_repository_mismatch_is_rejected(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "registry/systems.v0.1.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["systems"][0]["repository_url"] = "https://github.com/example/wrong"
    write_json(path, registry)

    assert "repository URL mismatch" in "\n".join(validate_catalog(catalog))


def test_nonreciprocal_sibling_is_rejected(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "manifests/agent-context-integrity.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["relationships"] = []
    write_json(path, manifest)

    assert "nonreciprocal sibling relationship" in "\n".join(validate_catalog(catalog))


def test_active_system_requires_activation_binding(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "registry/systems.v0.1.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["systems"][0].pop("activation")
    write_json(path, registry)

    assert "'activation' is a required property" in "\n".join(validate_catalog(catalog))


def test_candidate_system_forbids_activation_binding(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "registry/systems.v0.1.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["systems"][0]["adoption"] = "candidate"
    write_json(path, registry)

    errors = validate_catalog(catalog)
    assert any("activation" in error for error in errors)


def test_activation_digest_binds_catalog_manifest(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "manifests/agent-authority-integrity.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["name"] = "Changed after activation"
    write_json(path, manifest)

    assert "activation manifest digest mismatch" in "\n".join(validate_catalog(catalog))


def test_trial_freeze_detects_changed_artifact(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "trials/FET-001/protocol.v0.1.md"
    path.write_text(path.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")

    assert "frozen artifact digest mismatch" in "\n".join(validate_catalog(catalog))


def test_trial_detects_changed_envelope(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "trials/FET-001/fixtures/development-cases.v0.1.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["cases"][0]["envelope"]["limitations"].append("Changed after freeze")
    write_json(path, document)

    assert "envelope digest mismatch for FET001-DEV-001" in "\n".join(
        validate_catalog(catalog)
    )


def test_modified_digest_fixture_must_remain_mismatched(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "trials/FET-001/fixtures/development-cases.v0.1.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    case = next(
        item for item in document["cases"] if item["family"] == "MODIFIED_DIGEST"
    )
    case["envelope_sha256"] = canonical_json_sha256(case["envelope"])
    write_json(path, document)

    assert "modified-digest fixture unexpectedly matches" in "\n".join(
        validate_catalog(catalog)
    )


def test_duplicate_trial_case_is_rejected(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "trials/FET-001/fixtures/development-cases.v0.1.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["cases"].append(document["cases"][0])
    write_json(path, document)

    assert "duplicate FET-001 case_id" in "\n".join(validate_catalog(catalog))


def test_mutation_family_coverage_is_exact(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "trials/FET-001/fixtures/mutations.v0.1.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["mutations"].pop()
    write_json(path, document)

    assert "mutation family coverage mismatch" in "\n".join(validate_catalog(catalog))


def test_ready_cannot_be_promoted_to_permission(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "trials/FET-001/fixtures/development-cases.v0.1.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    case = next(
        item
        for item in document["cases"]
        if item["family"] == "READY_ABSENT_PERMISSION"
    )
    case["expected"]["authority_disposition"] = "ALLOW_FEDERATED"
    case["expected"]["committed_effects"] = ["publish-release"]
    write_json(path, document)

    assert "expected outcome mismatch for FET001-DEV-001" in "\n".join(
        validate_catalog(catalog)
    )


def test_context_envelope_rejects_downstream_permission(tmp_path: Path) -> None:
    catalog = copy_catalog(tmp_path)
    path = catalog / "trials/FET-001/fixtures/development-cases.v0.1.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    case = document["cases"][0]
    case["envelope"]["downstream_permission"] = "GRANTED"
    case["envelope_sha256"] = canonical_json_sha256(case["envelope"])
    write_json(path, document)

    assert "downstream_permission" in "\n".join(validate_catalog(catalog))
