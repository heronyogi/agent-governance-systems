from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


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
