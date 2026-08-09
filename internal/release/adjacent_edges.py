"""Deterministic adjacent-edge release catalog validation and composition."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(alpha|beta|rc)\.([1-9][0-9]*))?$"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EDGE_FIELDS = {
    "from",
    "to",
    "carry_unresolved_semantic_state",
    "migration_ids",
    "guidance_paths",
    "semantic_review_required",
    "edge_sha256",
}
GUIDANCE_FIELDS = {
    "guidance_id",
    "path",
    "from_version",
    "to_version",
    "supersedes",
    "sha256",
}


class AdjacentEdgeError(ValueError):
    """Raised when an adjacent-edge catalog cannot be proven safe."""


@dataclass(frozen=True)
class ResolvedUpgrade:
    """Resolved deterministic and semantic work for one target release."""

    managed_path: tuple[dict[str, Any], ...]
    semantic_path: tuple[dict[str, Any], ...]
    effective_guidance: tuple[dict[str, Any], ...]
    semantic_review_required: bool
    may_advance_compatibility_mechanically: bool


def version_key(value: str) -> tuple[int, int, int, int, int]:
    match = SEMVER_RE.fullmatch(value)
    if match is None:
        raise AdjacentEdgeError(f"invalid Ava version: {value!r}")
    rank = {"alpha": 0, "beta": 1, "rc": 2, None: 3}[match.group(4)]
    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        rank,
        int(match.group(5) or 0),
    )


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def edge_digest(edge: Mapping[str, Any]) -> str:
    payload = {key: edge[key] for key in sorted(EDGE_FIELDS - {"edge_sha256"})}
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def _string_list(value: object, location: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise AdjacentEdgeError(f"{location} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise AdjacentEdgeError(f"{location} contains duplicates")
    return list(value)


def normalize_edge(value: object, location: str = "edge") -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != EDGE_FIELDS:
        raise AdjacentEdgeError(f"{location} fields must be exactly {sorted(EDGE_FIELDS)}")
    source = value["from"]
    target = value["to"]
    if not isinstance(source, str) or not isinstance(target, str):
        raise AdjacentEdgeError(f"{location} endpoints must be strings")
    if version_key(source) >= version_key(target):
        raise AdjacentEdgeError(f"{location} must advance from an older release to a newer release")
    carry = value["carry_unresolved_semantic_state"]
    semantic = value["semantic_review_required"]
    if not isinstance(carry, bool) or not isinstance(semantic, bool):
        raise AdjacentEdgeError(f"{location} carry and semantic decisions must be boolean")
    migrations = _string_list(value["migration_ids"], f"{location}.migration_ids")
    guidance = _string_list(value["guidance_paths"], f"{location}.guidance_paths")
    if semantic and not guidance:
        raise AdjacentEdgeError(f"{location} requires semantic review but has no guidance")
    if not semantic and guidance:
        raise AdjacentEdgeError(f"{location} has guidance without semantic review")
    digest = value["edge_sha256"]
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise AdjacentEdgeError(f"{location}.edge_sha256 must be a lowercase SHA-256 digest")
    normalized = {
        "from": source,
        "to": target,
        "carry_unresolved_semantic_state": carry,
        "migration_ids": migrations,
        "guidance_paths": guidance,
        "semantic_review_required": semantic,
        "edge_sha256": digest,
    }
    if edge_digest(normalized) != digest:
        raise AdjacentEdgeError(f"{location}.edge_sha256 does not match its edge content")
    return normalized


def make_edge(
    source: str,
    target: str,
    *,
    carry_unresolved_semantic_state: bool = False,
    migration_ids: Sequence[str] = (),
    guidance_paths: Sequence[str] = (),
    semantic_review_required: bool = False,
) -> dict[str, Any]:
    edge: dict[str, Any] = {
        "from": source,
        "to": target,
        "carry_unresolved_semantic_state": carry_unresolved_semantic_state,
        "migration_ids": list(migration_ids),
        "guidance_paths": list(guidance_paths),
        "semantic_review_required": semantic_review_required,
        "edge_sha256": "0" * 64,
    }
    edge["edge_sha256"] = edge_digest(edge)
    return normalize_edge(edge)


def _adjacency(edges: Sequence[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        result.setdefault(edge["from"], []).append(edge)
    for values in result.values():
        values.sort(key=lambda item: (version_key(item["to"]), item["edge_sha256"]))
    return result


def resolve_unique_path(
    edges: Sequence[Mapping[str, Any]], source: str, target: str
) -> tuple[dict[str, Any], ...]:
    version_key(source)
    version_key(target)
    if source == target:
        return ()
    normalized = [normalize_edge(dict(edge), f"edges[{index}]") for index, edge in enumerate(edges)]
    adjacency = _adjacency(normalized)
    paths: list[tuple[dict[str, Any], ...]] = []

    def walk(current: str, path: tuple[dict[str, Any], ...], visited: frozenset[str]) -> None:
        if len(paths) > 1:
            return
        for edge in adjacency.get(current, []):
            next_version = edge["to"]
            if next_version in visited:
                raise AdjacentEdgeError(f"cycle detected while resolving {source} to {target}")
            next_path = (*path, edge)
            if next_version == target:
                paths.append(next_path)
                continue
            if version_key(next_version) >= version_key(target):
                continue
            walk(next_version, next_path, visited | {next_version})

    walk(source, (), frozenset({source}))
    if not paths:
        raise AdjacentEdgeError(f"no upgrade path from {source} to {target}")
    if len(paths) != 1:
        raise AdjacentEdgeError(f"ambiguous upgrade paths from {source} to {target}")
    return paths[0]


def validate_catalog(catalog: object) -> dict[str, Any]:
    if not isinstance(catalog, dict):
        raise AdjacentEdgeError("upgrade catalog must be an object")
    required = {"catalog_schema", "target_version", "supported_sources", "edges", "guidance"}
    if set(catalog) != required:
        raise AdjacentEdgeError(f"upgrade catalog fields must be exactly {sorted(required)}")
    if catalog["catalog_schema"] != 1:
        raise AdjacentEdgeError("upgrade catalog schema must be 1")
    target = catalog["target_version"]
    if not isinstance(target, str):
        raise AdjacentEdgeError("target_version must be a string")
    version_key(target)
    supported = _string_list(catalog["supported_sources"], "supported_sources")
    if any(version_key(source) >= version_key(target) for source in supported):
        raise AdjacentEdgeError("every supported source must be older than the target")
    raw_edges = catalog["edges"]
    if not isinstance(raw_edges, list):
        raise AdjacentEdgeError("edges must be a list")
    edges = [normalize_edge(item, f"edges[{index}]") for index, item in enumerate(raw_edges)]
    identities = [(edge["from"], edge["to"]) for edge in edges]
    if len(identities) != len(set(identities)):
        raise AdjacentEdgeError("upgrade catalog contains duplicate edge endpoints")
    digests = [edge["edge_sha256"] for edge in edges]
    if len(digests) != len(set(digests)):
        raise AdjacentEdgeError("upgrade catalog contains duplicate edge digests")
    for source in supported:
        resolve_unique_path(edges, source, target)

    raw_guidance = catalog["guidance"]
    if not isinstance(raw_guidance, list):
        raise AdjacentEdgeError("guidance must be a list")
    guidance = [normalize_guidance(item, f"guidance[{index}]") for index, item in enumerate(raw_guidance)]
    paths = [item["path"] for item in guidance]
    ids = [item["guidance_id"] for item in guidance]
    if len(paths) != len(set(paths)) or len(ids) != len(set(ids)):
        raise AdjacentEdgeError("guidance paths and IDs must be unique")
    guidance_by_path = {item["path"]: item for item in guidance}
    for edge in edges:
        for path in edge["guidance_paths"]:
            item = guidance_by_path.get(path)
            if item is None:
                raise AdjacentEdgeError(f"edge references missing guidance: {path}")
            if item["from_version"] != edge["from"] or item["to_version"] != edge["to"]:
                raise AdjacentEdgeError(f"guidance transition does not match edge: {path}")
    return {
        "catalog_schema": 1,
        "target_version": target,
        "supported_sources": sorted(supported, key=version_key),
        "edges": sorted(edges, key=lambda item: (version_key(item["from"]), version_key(item["to"]))),
        "guidance": sorted(guidance, key=lambda item: item["path"]),
    }


def normalize_guidance(value: object, location: str = "guidance") -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != GUIDANCE_FIELDS:
        raise AdjacentEdgeError(f"{location} fields must be exactly {sorted(GUIDANCE_FIELDS)}")
    guidance_id = value["guidance_id"]
    path = value["path"]
    source = value["from_version"]
    target = value["to_version"]
    digest = value["sha256"]
    if not all(isinstance(item, str) and item for item in (guidance_id, path, source, target)):
        raise AdjacentEdgeError(f"{location} identity fields must be non-empty strings")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise AdjacentEdgeError(f"{location}.sha256 must be a lowercase SHA-256 digest")
    if version_key(source) >= version_key(target):
        raise AdjacentEdgeError(f"{location} transition must advance")
    supersedes = _string_list(value["supersedes"], f"{location}.supersedes")
    if guidance_id in supersedes:
        raise AdjacentEdgeError(f"{location} cannot supersede itself")
    return {
        "guidance_id": guidance_id,
        "path": path,
        "from_version": source,
        "to_version": target,
        "supersedes": supersedes,
        "sha256": digest,
    }


def compose_guidance(
    path: Sequence[Mapping[str, Any]], guidance: Iterable[Mapping[str, Any]]
) -> tuple[dict[str, Any], ...]:
    guidance_values = [normalize_guidance(dict(item), f"guidance[{index}]") for index, item in enumerate(guidance)]
    by_path = {item["path"]: item for item in guidance_values}
    if len(by_path) != len(guidance_values):
        raise AdjacentEdgeError("guidance paths must be unique")
    active: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for edge_index, raw_edge in enumerate(path):
        edge = normalize_edge(dict(raw_edge), f"path[{edge_index}]")
        for guidance_path in edge["guidance_paths"]:
            item = by_path.get(guidance_path)
            if item is None:
                raise AdjacentEdgeError(f"path references missing guidance: {guidance_path}")
            if item["guidance_id"] in seen_ids:
                raise AdjacentEdgeError(f"guidance is referenced more than once: {item['guidance_id']}")
            if item["from_version"] != edge["from"] or item["to_version"] != edge["to"]:
                raise AdjacentEdgeError(f"guidance transition does not match path edge: {guidance_path}")
            active_ids = {entry["guidance_id"] for entry in active}
            missing = set(item["supersedes"]) - active_ids
            if missing:
                raise AdjacentEdgeError(
                    "guidance supersedes IDs that are not active: " + ", ".join(sorted(missing))
                )
            if item["supersedes"]:
                active = [entry for entry in active if entry["guidance_id"] not in item["supersedes"]]
            active.append(item)
            seen_ids.add(item["guidance_id"])
    return tuple(active)


def resolve_upgrade(
    catalog: Mapping[str, Any],
    *,
    installed_version: str,
    compatible_through: str,
    semantic_status: str,
) -> ResolvedUpgrade:
    normalized = validate_catalog(dict(catalog))
    target = normalized["target_version"]
    if installed_version not in normalized["supported_sources"]:
        raise AdjacentEdgeError(f"installed version is not a supported source: {installed_version}")
    managed_path = resolve_unique_path(normalized["edges"], installed_version, target)
    semantic_path = resolve_unique_path(normalized["edges"], compatible_through, target)
    incomplete = semantic_status != "complete"
    if incomplete and not all(edge["carry_unresolved_semantic_state"] for edge in semantic_path):
        raise AdjacentEdgeError("semantic path does not permit carrying unresolved semantic state")
    effective_guidance = compose_guidance(semantic_path, normalized["guidance"])
    semantic_required = incomplete or any(edge["semantic_review_required"] for edge in semantic_path)
    return ResolvedUpgrade(
        managed_path=managed_path,
        semantic_path=semantic_path,
        effective_guidance=effective_guidance,
        semantic_review_required=semantic_required,
        may_advance_compatibility_mechanically=not semantic_required,
    )


def inherit_catalog(
    previous: Mapping[str, Any],
    new_edge: Mapping[str, Any],
    *,
    supported_sources: Sequence[str] | None = None,
    retired_sources: Sequence[str] = (),
    new_guidance: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    prior = validate_catalog(dict(previous))
    edge = normalize_edge(dict(new_edge), "new_edge")
    if edge["from"] != prior["target_version"]:
        raise AdjacentEdgeError("new adjacent edge must start at the previous catalog target")
    retired = set(retired_sources)
    unknown_retired = retired - set(prior["supported_sources"])
    if unknown_retired:
        raise AdjacentEdgeError("cannot retire unknown supported sources: " + ", ".join(sorted(unknown_retired)))
    if supported_sources is None:
        supported = [
            source for source in (*prior["supported_sources"], prior["target_version"])
            if source not in retired
        ]
    else:
        supported = list(supported_sources)
        expected_retained = set(prior["supported_sources"]) - retired
        if not expected_retained.issubset(supported):
            omitted = expected_retained - set(supported)
            raise AdjacentEdgeError("inherited supported sources were omitted: " + ", ".join(sorted(omitted)))
        if prior["target_version"] not in supported:
            raise AdjacentEdgeError("previous target must become a supported source")
    catalog = {
        "catalog_schema": 1,
        "target_version": edge["to"],
        "supported_sources": sorted(set(supported), key=version_key),
        "edges": [*prior["edges"], edge],
        "guidance": [*prior["guidance"], *(dict(item) for item in new_guidance)],
    }
    result = validate_catalog(catalog)
    inherited_by_digest = {item["edge_sha256"]: item for item in result["edges"]}
    for old_edge in prior["edges"]:
        if inherited_by_digest.get(old_edge["edge_sha256"]) != old_edge:
            raise AdjacentEdgeError("an inherited edge changed while extending the catalog")
    return result
