#!/usr/bin/env python3
"""Validate a proposed self-contained adjacent upgrade edge catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from internal.release.adjacent_edges import (
    AdjacentEdgeError,
    resolve_upgrade,
    validate_catalog,
)


def read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AdjacentEdgeError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AdjacentEdgeError(f"{path} must contain a JSON object")
    return value


def validate_inheritance(
    previous: dict[str, Any],
    current: dict[str, Any],
    retired_sources: set[str],
) -> None:
    prior = validate_catalog(previous)
    target = validate_catalog(current)
    if target["target_version"] == prior["target_version"]:
        raise AdjacentEdgeError("current catalog must advance beyond the previous target")

    prior_edges = {edge["edge_sha256"]: edge for edge in prior["edges"]}
    current_edges = {edge["edge_sha256"]: edge for edge in target["edges"]}
    missing_edges = sorted(set(prior_edges) - set(current_edges))
    if missing_edges:
        raise AdjacentEdgeError(
            "current catalog omits or alters inherited edge digests: "
            + ", ".join(missing_edges)
        )
    for digest, edge in prior_edges.items():
        if current_edges[digest] != edge:
            raise AdjacentEdgeError(f"inherited edge content changed: {digest}")

    prior_guidance = {item["guidance_id"]: item for item in prior["guidance"]}
    current_guidance = {item["guidance_id"]: item for item in target["guidance"]}
    missing_guidance = sorted(set(prior_guidance) - set(current_guidance))
    if missing_guidance:
        raise AdjacentEdgeError(
            "current catalog omits inherited guidance IDs: "
            + ", ".join(missing_guidance)
        )
    for guidance_id, item in prior_guidance.items():
        if current_guidance[guidance_id] != item:
            raise AdjacentEdgeError(f"inherited guidance changed: {guidance_id}")

    unknown_retirements = retired_sources - set(prior["supported_sources"])
    if unknown_retirements:
        raise AdjacentEdgeError(
            "retirement names unknown prior sources: "
            + ", ".join(sorted(unknown_retirements))
        )
    required_sources = set(prior["supported_sources"]) - retired_sources
    omitted = required_sources - set(target["supported_sources"])
    if omitted:
        raise AdjacentEdgeError(
            "current catalog silently drops inherited supported sources: "
            + ", ".join(sorted(omitted))
        )
    if prior["target_version"] not in target["supported_sources"]:
        raise AdjacentEdgeError("previous target must become a supported source")

    new_edges = [
        edge for edge in target["edges"]
        if edge["edge_sha256"] not in prior_edges
    ]
    if len(new_edges) != 1:
        raise AdjacentEdgeError("a normal release must append exactly one new adjacent edge")
    new_edge = new_edges[0]
    if new_edge["from"] != prior["target_version"]:
        raise AdjacentEdgeError("new edge must start at the previous catalog target")
    if new_edge["to"] != target["target_version"]:
        raise AdjacentEdgeError("new edge must end at the current catalog target")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate deterministic adjacent-edge release catalog composition."
    )
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--previous-catalog", type=Path)
    parser.add_argument("--retired-source", action="append", default=[])
    parser.add_argument("--installed-version")
    parser.add_argument("--compatible-through")
    parser.add_argument(
        "--semantic-status",
        choices=("complete", "pending", "partial", "blocked"),
        default="complete",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        raw = read_object(args.catalog)
        catalog = validate_catalog(raw)
        if args.previous_catalog:
            validate_inheritance(
                read_object(args.previous_catalog),
                catalog,
                set(args.retired_source),
            )
        resolution = None
        if bool(args.installed_version) != bool(args.compatible_through):
            raise AdjacentEdgeError(
                "--installed-version and --compatible-through must be supplied together"
            )
        if args.installed_version:
            resolution = resolve_upgrade(
                catalog,
                installed_version=args.installed_version,
                compatible_through=args.compatible_through,
                semantic_status=args.semantic_status,
            )
    except AdjacentEdgeError as exc:
        print(f"adjacent upgrade catalog invalid: {exc}", file=sys.stderr)
        return 1

    result: dict[str, Any] = {
        "target_version": catalog["target_version"],
        "supported_sources": catalog["supported_sources"],
        "edge_count": len(catalog["edges"]),
        "guidance_count": len(catalog["guidance"]),
    }
    if resolution is not None:
        result["resolution"] = {
            "managed_edges": [edge["edge_sha256"] for edge in resolution.managed_path],
            "semantic_edges": [edge["edge_sha256"] for edge in resolution.semantic_path],
            "guidance_ids": [item["guidance_id"] for item in resolution.effective_guidance],
            "semantic_review_required": resolution.semantic_review_required,
            "may_advance_compatibility_mechanically": (
                resolution.may_advance_compatibility_mechanically
            ),
        }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"adjacent upgrade catalog valid for {catalog['target_version']}; "
            f"sources={len(catalog['supported_sources'])}, "
            f"edges={len(catalog['edges'])}, guidance={len(catalog['guidance'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
