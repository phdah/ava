#!/usr/bin/env python3
"""Author one immutable release-local adjacent-edge record."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from internal.release.adjacent_edges import (
    AdjacentEdgeError,
    canonical_json,
    normalize_edge,
)
from internal.release.release_catalog import (
    read_json_object,
    validate_guidance_artifacts,
    validate_release_record,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Author one previous-release-to-target release record."
    )
    parser.add_argument("--previous-version", required=True)
    parser.add_argument("--new-edge", type=Path, required=True)
    parser.add_argument("--new-guidance", type=Path, action="append", default=[])
    parser.add_argument(
        "--retired-source",
        action="append",
        default=[],
        metavar="VERSION=REASON",
    )
    parser.add_argument("--guidance-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def retirement(value: str) -> dict[str, str]:
    version, separator, reason = value.partition("=")
    if not separator or not version or not reason.strip():
        raise AdjacentEdgeError(
            "--retired-source must use VERSION=REASON with a non-empty reason"
        )
    return {"version": version, "reason": reason.strip()}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        edge = normalize_edge(read_json_object(args.new_edge), "new_edge")
        if edge["from"] != args.previous_version:
            raise AdjacentEdgeError(
                "new edge must start at --previous-version: "
                f"expected {args.previous_version}, got {edge['from']}"
            )
        record = validate_release_record(
            {
                "catalog_schema": 1,
                "target_version": edge["to"],
                "edge": edge,
                "guidance": [
                    read_json_object(path)
                    for path in args.new_guidance
                ],
                "retired_sources": [
                    retirement(value)
                    for value in args.retired_source
                ],
            }
        )
        if args.guidance_root:
            validate_guidance_artifacts(record, args.guidance_root)
        output = args.output.resolve()
        if output.stem != record["target_version"]:
            raise AdjacentEdgeError(
                "output filename must equal the target version"
            )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical_json(record))
    except (AdjacentEdgeError, OSError) as exc:
        print(f"cannot compose adjacent release record: {exc}", file=sys.stderr)
        return 1
    print(
        f"wrote release-local edge {edge['from']} -> {edge['to']} to {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
