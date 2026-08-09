#!/usr/bin/env python3
"""Validate one release record and its recursively linked upgrade chain."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from internal.release.adjacent_edges import AdjacentEdgeError, resolve_upgrade
from internal.release.release_catalog import (
    catalog_path,
    read_catalog,
    read_initial_version,
    read_release_record,
    validate_guidance_artifacts,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate recursive release-local adjacent-edge composition."
    )
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--initial-version")
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


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = args.root.resolve()
        target_version = args.catalog.stem
        expected = catalog_path(root, target_version).resolve()
        if args.catalog.resolve() != expected:
            raise AdjacentEdgeError(
                f"catalog must be the target record at {expected}"
            )
        record = read_release_record(root, target_version)
        initial = args.initial_version or read_initial_version(root)
        catalog = read_catalog(
            root,
            target_version,
            initial_version=initial,
        )
        guidance_root = (
            args.guidance_root.resolve()
            if args.guidance_root
            else root / "internal/release/guidance"
        )
        validate_guidance_artifacts(catalog, guidance_root)

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
        "previous_version": record["edge"]["from"],
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
            f"release-local adjacent chain valid for {catalog['target_version']}; "
            f"sources={len(catalog['supported_sources'])}, "
            f"edges={len(catalog['edges'])}, guidance={len(catalog['guidance'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
