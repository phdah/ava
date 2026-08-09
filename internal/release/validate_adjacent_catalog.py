#!/usr/bin/env python3
"""Validate an adjacent catalog and, for a release, its exact inherited delta."""

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
from internal.release.release_catalog import (
    read_json_object,
    read_retirements,
    validate_guidance_artifacts,
    validate_release_delta,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate deterministic adjacent-edge release catalog composition."
    )
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--previous-catalog", type=Path)
    parser.add_argument("--retirements", type=Path)
    parser.add_argument("--guidance-root", type=Path)
    parser.add_argument("--installed-version")
    parser.add_argument("--compatible-through")
    parser.add_argument(
        "--semantic-status",
        choices=("complete", "pending", "partial", "blocked"),
        default="complete",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def _retirements(path: Path | None, target: str) -> dict[str, str]:
    if path is None:
        return {}
    root = path.resolve().parents[2]
    expected = root / "internal/release/catalog-retirements.json"
    if path.resolve() == expected:
        return read_retirements(root, target)
    value = read_json_object(path)
    if set(value) != {"schema_version", "target_version", "retired_sources"}:
        raise AdjacentEdgeError("retirement file has invalid fields")
    if value["schema_version"] != 1 or value["target_version"] != target:
        raise AdjacentEdgeError("retirement file identity does not match the catalog")
    result: dict[str, str] = {}
    for index, item in enumerate(value["retired_sources"]):
        if not isinstance(item, dict) or set(item) != {"version", "reason"}:
            raise AdjacentEdgeError(
                f"retired_sources[{index}] must contain version and reason"
            )
        if not isinstance(item["reason"], str) or not item["reason"].strip():
            raise AdjacentEdgeError(
                f"retired_sources[{index}].reason must be non-empty"
            )
        result[item["version"]] = item["reason"].strip()
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        raw = read_json_object(args.catalog)
        target_version = raw.get("target_version")
        if not isinstance(target_version, str):
            raise AdjacentEdgeError("catalog target_version must be a string")
        if args.previous_catalog:
            catalog = validate_release_delta(
                read_json_object(args.previous_catalog),
                raw,
                retired_sources=_retirements(args.retirements, target_version),
                guidance_root=args.guidance_root,
            )
        else:
            catalog = validate_catalog(raw)
            if args.guidance_root:
                validate_guidance_artifacts(catalog, args.guidance_root)

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
            "managed_edges": [
                edge["edge_sha256"] for edge in resolution.managed_path
            ],
            "semantic_edges": [
                edge["edge_sha256"] for edge in resolution.semantic_path
            ],
            "guidance_ids": [
                item["guidance_id"] for item in resolution.effective_guidance
            ],
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
