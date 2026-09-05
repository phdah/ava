"""Release-local adjacent-edge records and recursive upgrade composition."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from internal.release.adjacent_edges import (
    AdjacentEdgeError,
    compose_guidance,
    normalize_edge,
    normalize_guidance,
    resolve_unique_path,
    validate_catalog,
    version_key,
)


# Stable 1.0.0 is the root of the permanent upgrade ledger. It is a first
# release, not an upgrade from any prerelease or synthetic published source.
BOOTSTRAP_VERSION = "1.0.0"
CATALOG_DIRECTORY = Path("internal/release/catalogs")
RELEASE_RECORD_FIELDS = {
    "catalog_schema",
    "target_version",
    "edge",
    "guidance",
    "retired_sources",
}
RETIREMENT_FIELDS = {"version", "reason"}


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AdjacentEdgeError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AdjacentEdgeError(f"{path} must contain a JSON object")
    return value


def catalog_path(root: Path, version: str) -> Path:
    version_key(version)
    return root / CATALOG_DIRECTORY / f"{version}.json"


def _normalize_retirements(value: object) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise AdjacentEdgeError("retired_sources must be a list")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != RETIREMENT_FIELDS:
            raise AdjacentEdgeError(
                f"retired_sources[{index}] must contain exactly version and reason"
            )
        version = item["version"]
        reason = item["reason"]
        if not isinstance(version, str):
            raise AdjacentEdgeError(
                f"retired_sources[{index}].version must be a string"
            )
        version_key(version)
        if not isinstance(reason, str) or not reason.strip():
            raise AdjacentEdgeError(
                f"retired_sources[{index}].reason must be non-empty"
            )
        if version in seen:
            raise AdjacentEdgeError(f"duplicate retired source: {version}")
        seen.add(version)
        result.append({"version": version, "reason": reason.strip()})
    return sorted(result, key=lambda item: version_key(item["version"]))


def validate_release_record(
    record: Mapping[str, Any],
    *,
    target_version: str | None = None,
) -> dict[str, Any]:
    if not isinstance(record, Mapping):
        raise AdjacentEdgeError("release catalog record must be an object")
    if set(record) != RELEASE_RECORD_FIELDS or record.get("catalog_schema") != 1:
        raise AdjacentEdgeError(
            "release catalog record fields and catalog_schema must match schema 1"
        )

    target = record.get("target_version")
    if not isinstance(target, str):
        raise AdjacentEdgeError("target_version must be a string")
    version_key(target)
    if target_version is not None and target != target_version:
        raise AdjacentEdgeError(
            f"release catalog target {target!r} does not match {target_version!r}"
        )

    edge = normalize_edge(record.get("edge"), "edge")
    if edge["to"] != target:
        raise AdjacentEdgeError(
            "release catalog edge.to must equal the record target_version"
        )

    raw_guidance = record.get("guidance")
    if not isinstance(raw_guidance, list):
        raise AdjacentEdgeError("guidance must be a list")
    guidance = [
        normalize_guidance(item, f"guidance[{index}]")
        for index, item in enumerate(raw_guidance)
    ]
    paths = [item["path"] for item in guidance]
    ids = [item["guidance_id"] for item in guidance]
    if len(paths) != len(set(paths)) or len(ids) != len(set(ids)):
        raise AdjacentEdgeError("guidance paths and IDs must be unique")
    if set(paths) != set(edge["guidance_paths"]):
        raise AdjacentEdgeError(
            "the release record must contain exactly the guidance referenced by its edge"
        )
    for item in guidance:
        if (
            item["from_version"] != edge["from"]
            or item["to_version"] != edge["to"]
        ):
            raise AdjacentEdgeError(
                f"guidance transition does not match the release edge: {item['path']}"
            )

    retirements = _normalize_retirements(record.get("retired_sources"))
    retired_versions = {item["version"] for item in retirements}
    if edge["from"] in retired_versions and edge["from"] != BOOTSTRAP_VERSION:
        raise AdjacentEdgeError(
            "the immediately previous release cannot be retired by its own edge"
        )
    if any(version_key(item["version"]) >= version_key(target) for item in retirements):
        raise AdjacentEdgeError(
            "retired sources must be older than the release target"
        )

    return {
        "catalog_schema": 1,
        "target_version": target,
        "edge": edge,
        "guidance": sorted(guidance, key=lambda item: item["path"]),
        "retired_sources": retirements,
    }


def read_release_record(root: Path, version: str) -> dict[str, Any]:
    return validate_release_record(
        read_json_object(catalog_path(root, version)),
        target_version=version,
    )


def initial_catalog(version: str = BOOTSTRAP_VERSION) -> dict[str, Any]:
    version_key(version)
    return validate_catalog(
        {
            "catalog_schema": 1,
            "target_version": version,
            "supported_sources": [],
            "edges": [],
            "guidance": [],
        }
    )


def append_release(
    previous_catalog: Mapping[str, Any],
    record: Mapping[str, Any],
) -> dict[str, Any]:
    previous = validate_catalog(dict(previous_catalog))
    current = validate_release_record(record)
    edge = current["edge"]
    if edge["from"] != previous["target_version"]:
        raise AdjacentEdgeError(
            "the release record edge must start at the immediately previous release: "
            f"expected {previous['target_version']} -> {current['target_version']}, "
            f"got {edge['from']} -> {edge['to']}"
        )

    inherited_sources = set(previous["supported_sources"]) | {
        previous["target_version"]
    }
    retired = {item["version"] for item in current["retired_sources"]}
    unknown = retired - inherited_sources
    if unknown:
        raise AdjacentEdgeError(
            "release retires sources that are not inherited: "
            + ", ".join(sorted(unknown, key=version_key))
        )
    supported = inherited_sources - retired

    return validate_catalog(
        {
            "catalog_schema": 1,
            "target_version": current["target_version"],
            "supported_sources": sorted(supported, key=version_key),
            "edges": [*previous["edges"], edge],
            "guidance": [*previous["guidance"], *current["guidance"]],
        }
    )


def read_release_chain(
    root: Path,
    target_version: str,
    *,
    root_version: str = BOOTSTRAP_VERSION,
) -> tuple[dict[str, Any], ...]:
    version_key(target_version)
    version_key(root_version)
    if version_key(target_version) <= version_key(root_version):
        if target_version == root_version:
            return ()
        raise AdjacentEdgeError(
            f"target {target_version} predates bootstrap root {root_version}"
        )

    reverse_records: list[dict[str, Any]] = []
    current = target_version
    visited: set[str] = set()
    while current != root_version:
        if current in visited:
            raise AdjacentEdgeError(
                f"cycle detected while following release records from {target_version}"
            )
        visited.add(current)
        path = catalog_path(root, current)
        if not path.is_file():
            raise AdjacentEdgeError(
                f"missing release catalog record for {current}: {path}"
            )
        record = read_release_record(root, current)
        reverse_records.append(record)
        current = record["edge"]["from"]
        if version_key(current) < version_key(root_version):
            raise AdjacentEdgeError(
                f"release chain for {target_version} passes before bootstrap root {root_version}"
            )

    reverse_records.reverse()
    return tuple(reverse_records)


def read_catalog(
    root: Path,
    target_version: str,
    *,
    root_version: str = BOOTSTRAP_VERSION,
) -> dict[str, Any]:
    catalog = initial_catalog(root_version)
    for record in read_release_chain(root, target_version, root_version=root_version):
        catalog = append_release(catalog, record)
    return catalog


def _safe_relative(value: str, location: str) -> Path:
    candidate = PurePosixPath(value)
    if (
        candidate.is_absolute()
        or not candidate.parts
        or any(part in ("", ".", "..") for part in candidate.parts)
    ):
        raise AdjacentEdgeError(f"{location} must be a safe relative path")
    return Path(*candidate.parts)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise AdjacentEdgeError(f"cannot read guidance artifact {path}: {exc}") from exc
    return digest.hexdigest()


def validate_guidance_artifacts(
    catalog_or_record: Mapping[str, Any],
    guidance_root: Path,
) -> None:
    if "edge" in catalog_or_record:
        guidance = validate_release_record(catalog_or_record)["guidance"]
    else:
        guidance = validate_catalog(dict(catalog_or_record))["guidance"]
    root = guidance_root.resolve()
    for item in guidance:
        relative = _safe_relative(item["path"], f"guidance {item['guidance_id']} path")
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise AdjacentEdgeError(
                f"guidance artifact is missing or not a regular file: {item['path']}"
            )
        if sha256_file(path) != item["sha256"]:
            raise AdjacentEdgeError(
                f"guidance artifact digest changed: {item['guidance_id']}"
            )


def validate_release_delta(
    previous_catalog: Mapping[str, Any],
    current_record: Mapping[str, Any],
    *,
    guidance_root: Path | None = None,
) -> dict[str, Any]:
    previous = validate_catalog(dict(previous_catalog))
    current = validate_release_record(current_record)
    result = append_release(previous, current)
    if guidance_root is not None:
        validate_guidance_artifacts(previous, guidance_root)
        validate_guidance_artifacts(current, guidance_root)
    return result


def manifest_edges(catalog: Mapping[str, Any]) -> list[dict[str, Any]]:
    normalized = validate_catalog(dict(catalog))
    target = normalized["target_version"]
    result: list[dict[str, Any]] = []
    for source in normalized["supported_sources"]:
        path = resolve_unique_path(normalized["edges"], source, target)
        migrations: list[str] = []
        seen_migrations: set[str] = set()
        for edge in path:
            for migration_id in edge["migration_ids"]:
                if migration_id in seen_migrations:
                    raise AdjacentEdgeError(
                        f"migration is referenced more than once on {source} -> {target}: "
                        f"{migration_id}"
                    )
                seen_migrations.add(migration_id)
                migrations.append(migration_id)
        guidance = compose_guidance(path, normalized["guidance"])
        result.append(
            {
                "from": source,
                "to": target,
                "mode": "direct",
                "intermediates": [],
                "carry_unresolved_semantic_state": all(
                    edge["carry_unresolved_semantic_state"] for edge in path
                ),
                "migration_ids": migrations,
                "guidance_paths": [item["path"] for item in guidance],
                "semantic_review_required": any(
                    edge["semantic_review_required"] for edge in path
                ),
            }
        )
    return result
