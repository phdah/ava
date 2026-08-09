"""Policy helpers for the retained adjacent-edge ledger boundary."""

from __future__ import annotations

import json
from pathlib import Path

from internal.release.adjacent_edges import AdjacentEdgeError, version_key


POLICY_PATH = Path("internal/release/fixtures/release-upgrade-policy.json")


def read_upgrade_policy(root: Path) -> dict[str, object]:
    path = root / POLICY_PATH
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AdjacentEdgeError(f"cannot read valid upgrade policy from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AdjacentEdgeError(f"{path} must contain a JSON object")
    required = {
        "schema_version",
        "initial_release_version",
        "protected_direct_sources",
    }
    if set(value) != required or value.get("schema_version") != 1:
        raise AdjacentEdgeError(f"{path} has invalid schema 1 fields")
    initial = value.get("initial_release_version")
    protected = value.get("protected_direct_sources")
    if not isinstance(initial, str):
        raise AdjacentEdgeError(f"{path} initial_release_version must be a string")
    version_key(initial)
    if (
        not isinstance(protected, list)
        or not all(isinstance(item, str) for item in protected)
        or len(protected) != len(set(protected))
    ):
        raise AdjacentEdgeError(f"{path} protected_direct_sources must be unique versions")
    for version in protected:
        version_key(version)
    return {
        "schema_version": 1,
        "initial_release_version": initial,
        "protected_direct_sources": list(protected),
    }


def catalog_root_version(root: Path) -> str:
    policy = read_upgrade_policy(root)
    protected = policy["protected_direct_sources"]
    if protected:
        return min(protected, key=version_key)
    return policy["initial_release_version"]
