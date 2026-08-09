"""Strict release-authoring rules for adjacent upgrade catalogs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from internal.release.adjacent_edges import (
    AdjacentEdgeError,
    compose_guidance,
    normalize_edge,
    normalize_guidance,
    resolve_unique_path,
    validate_catalog,
    version_key,
)


CATALOG_DIRECTORY = Path("internal/release/catalogs")
GUIDANCE_DIRECTORY = Path("internal/release/guidance")
RETIREMENTS_PATH = Path("internal/release/catalog-retirements.json")


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


def read_catalog(root: Path, version: str) -> dict[str, Any]:
    path = catalog_path(root, version)
    catalog = validate_catalog(read_json_object(path))
    if catalog["target_version"] != version:
        raise AdjacentEdgeError(
            f"{path} target {catalog['target_version']!r} does not match its filename"
        )
    return catalog


def read_retirements(root: Path, target_version: str) -> dict[str, str]:
    path = root / RETIREMENTS_PATH
    value = read_json_object(path)
    if set(value) != {"schema_version", "target_version", "retired_sources"}:
        raise AdjacentEdgeError(
            "catalog-retirements.json fields must be schema_version, target_version, "
            "and retired_sources"
        )
    if value["schema_version"] != 1:
        raise AdjacentEdgeError("catalog-retirements.json schema_version must be 1")
    if value["target_version"] != target_version:
        raise AdjacentEdgeError(
            "catalog-retirements.json target does not match the proposed release"
        )
    entries = value["retired_sources"]
    if not isinstance(entries, list):
        raise AdjacentEdgeError("retired_sources must be a list")
    result: dict[str, str] = {}
    for index, item in enumerate(entries):
        if not isinstance(item, dict) or set(item) != {"version", "reason"}:
            raise AdjacentEdgeError(
                f"retired_sources[{index}] must contain exactly version and reason"
            )
        version = item["version"]
        reason = item["reason"]
        if not isinstance(version, str):
            raise AdjacentEdgeError(f"retired_sources[{index}].version must be a string")
        version_key(version)
        if not isinstance(reason, str) or not reason.strip():
            raise AdjacentEdgeError(
                f"retired_sources[{index}].reason must be non-empty"
            )
        if version in result:
            raise AdjacentEdgeError(f"duplicate retired source: {version}")
        result[version] = reason.strip()
    return result


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
    catalog: Mapping[str, Any], guidance_root: Path
) -> None:
    normalized = validate_catalog(dict(catalog))
    root = guidance_root.resolve()
    for item in normalized["guidance"]:
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
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    retired_sources: Mapping[str, str] | None = None,
    guidance_root: Path | None = None,
) -> dict[str, Any]:
    prior = validate_catalog(dict(previous))
    retired = dict(retired_sources or {})

    if not isinstance(current, Mapping):
        raise AdjacentEdgeError("proposed upgrade catalog must be an object")
    required = {"catalog_schema", "target_version", "supported_sources", "edges", "guidance"}
    if set(current) != required or current.get("catalog_schema") != 1:
        raise AdjacentEdgeError(
            "proposed upgrade catalog fields and catalog_schema must match schema 1"
        )
    current_target = current.get("target_version")
    if not isinstance(current_target, str):
        raise AdjacentEdgeError("proposed catalog target_version must be a string")
    version_key(current_target)
    raw_sources = current.get("supported_sources")
    if (
        not isinstance(raw_sources, list)
        or not all(isinstance(item, str) and item for item in raw_sources)
        or len(raw_sources) != len(set(raw_sources))
    ):
        raise AdjacentEdgeError("proposed catalog supported_sources must be unique versions")
    for source in raw_sources:
        version_key(source)
    raw_edges = current.get("edges")
    raw_guidance = current.get("guidance")
    if not isinstance(raw_edges, list) or not isinstance(raw_guidance, list):
        raise AdjacentEdgeError("proposed catalog edges and guidance must be lists")
    target_edges_list = [
        normalize_edge(item, f"proposed edges[{index}]")
        for index, item in enumerate(raw_edges)
    ]
    target_guidance_list = [
        normalize_guidance(item, f"proposed guidance[{index}]")
        for index, item in enumerate(raw_guidance)
    ]
    edge_identities = [(item["from"], item["to"]) for item in target_edges_list]
    if len(edge_identities) != len(set(edge_identities)):
        raise AdjacentEdgeError("proposed catalog contains duplicate edge endpoints")
    guidance_ids = [item["guidance_id"] for item in target_guidance_list]
    if len(guidance_ids) != len(set(guidance_ids)):
        raise AdjacentEdgeError("proposed catalog contains duplicate guidance IDs")

    if version_key(current_target) <= version_key(prior["target_version"]):
        raise AdjacentEdgeError("proposed catalog target must advance beyond the inherited target")

    target_edges = {
        (edge["from"], edge["to"]): edge
        for edge in target_edges_list
    }
    target_guidance = {
        item["guidance_id"]: item
        for item in target_guidance_list
    }

    prior_edges = {
        (edge["from"], edge["to"]): edge
        for edge in prior["edges"]
    }
    for identity, edge in prior_edges.items():
        if identity not in target_edges:
            raise AdjacentEdgeError(
                f"proposed catalog omits inherited edge {identity[0]} -> {identity[1]}"
            )
        if target_edges[identity] != edge:
            raise AdjacentEdgeError(
                f"proposed catalog mutates inherited edge {identity[0]} -> {identity[1]}"
            )

    new_edge_identities = sorted(set(target_edges) - set(prior_edges))
    if len(new_edge_identities) != 1:
        raise AdjacentEdgeError(
            "a release must inherit its catalog unchanged and author exactly one new adjacent edge"
        )
    new_identity = new_edge_identities[0]
    expected_identity = (prior["target_version"], current_target)
    if new_identity != expected_identity:
        raise AdjacentEdgeError(
            "the single new edge must be the immediately previous release to the "
            f"proposed target: expected {expected_identity[0]} -> {expected_identity[1]}, "
            f"got {new_identity[0]} -> {new_identity[1]}"
        )
    new_edge = target_edges[new_identity]

    prior_guidance = {
        item["guidance_id"]: item
        for item in prior["guidance"]
    }
    for guidance_id, item in prior_guidance.items():
        if guidance_id not in target_guidance:
            raise AdjacentEdgeError(
                f"proposed catalog omits inherited guidance {guidance_id}"
            )
        if target_guidance[guidance_id] != item:
            raise AdjacentEdgeError(
                f"proposed catalog mutates inherited guidance {guidance_id}"
            )

    new_guidance_ids = sorted(set(target_guidance) - set(prior_guidance))
    new_guidance = [target_guidance[item] for item in new_guidance_ids]
    new_guidance_paths = {item["path"] for item in new_guidance}
    if set(new_edge["guidance_paths"]) != new_guidance_paths:
        raise AdjacentEdgeError(
            "the new edge must reference exactly the guidance authored for that edge; "
            "do not copy cumulative guidance from an older obligation"
        )
    for item in new_guidance:
        if (
            item["from_version"] != new_edge["from"]
            or item["to_version"] != new_edge["to"]
        ):
            raise AdjacentEdgeError(
                f"new guidance {item['guidance_id']} is not scoped to the new adjacent edge"
            )

    prior_sources = set(prior["supported_sources"])
    unknown_retirements = set(retired) - prior_sources
    if unknown_retirements:
        raise AdjacentEdgeError(
            "retirement names unknown inherited sources: "
            + ", ".join(sorted(unknown_retirements, key=version_key))
        )
    current_sources = set(raw_sources)
    expected_sources = (prior_sources - set(retired)) | {prior["target_version"]}
    if current_sources != expected_sources:
        omitted = expected_sources - current_sources
        added = current_sources - expected_sources
        details: list[str] = []
        if omitted:
            details.append(
                "silently omitted " + ", ".join(sorted(omitted, key=version_key))
            )
        if added:
            details.append(
                "added non-adjacent entry points "
                + ", ".join(sorted(added, key=version_key))
            )
        raise AdjacentEdgeError(
            "supported_sources must retain inherited entries, apply only explicit "
            "retirements, and add the previous target: "
            + "; ".join(details)
        )

    target = validate_catalog(
        {
            "catalog_schema": 1,
            "target_version": current_target,
            "supported_sources": raw_sources,
            "edges": target_edges_list,
            "guidance": target_guidance_list,
        }
    )
    for source in target["supported_sources"]:
        resolve_unique_path(target["edges"], source, target["target_version"])

    if guidance_root is not None:
        validate_guidance_artifacts(prior, guidance_root)
        validate_guidance_artifacts(target, guidance_root)

    return target


def validate_initial_catalog(
    catalog: Mapping[str, Any],
    *,
    target_version: str,
    guidance_root: Path | None = None,
) -> dict[str, Any]:
    normalized = validate_catalog(dict(catalog))
    if normalized["target_version"] != target_version:
        raise AdjacentEdgeError("initial catalog target does not match the release")
    if normalized["supported_sources"] or normalized["edges"] or normalized["guidance"]:
        raise AdjacentEdgeError(
            "the initial release catalog must not declare upgrade history"
        )
    if guidance_root is not None:
        validate_guidance_artifacts(normalized, guidance_root)
    return normalized


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
