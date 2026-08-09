#!/usr/bin/env python3
"""Append one reviewed adjacent edge to an immutable release catalog."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from internal.release.adjacent_edges import (
    AdjacentEdgeError,
    canonical_json,
    inherit_catalog,
)
from internal.release.release_catalog import (
    read_json_object,
    validate_release_delta,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose a target catalog from inherited history and one new edge."
    )
    parser.add_argument("--previous-catalog", type=Path, required=True)
    parser.add_argument("--new-edge", type=Path, required=True)
    parser.add_argument("--new-guidance", type=Path, action="append", default=[])
    parser.add_argument("--retired-source", action="append", default=[])
    parser.add_argument("--guidance-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        previous = read_json_object(args.previous_catalog)
        catalog = inherit_catalog(
            previous,
            read_json_object(args.new_edge),
            retired_sources=args.retired_source,
            new_guidance=[
                read_json_object(path)
                for path in args.new_guidance
            ],
        )
        validate_release_delta(
            previous,
            catalog,
            retired_sources={
                source: "Explicitly supplied to the catalog composer."
                for source in args.retired_source
            },
            guidance_root=args.guidance_root,
        )
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical_json(catalog))
    except (AdjacentEdgeError, OSError) as exc:
        print(f"cannot compose adjacent upgrade catalog: {exc}", file=sys.stderr)
        return 1
    print(f"wrote adjacent upgrade catalog for {catalog['target_version']} to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
