from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.validate_catalog import ROOT, validate_catalog


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def copy_catalog(tmp_path: Path) -> Path:
    target = tmp_path / "catalog"
    for directory in ("manifests", "registry", "schemas"):
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
