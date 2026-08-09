#!/usr/bin/env python3
"""Append one reviewed adjacent edge to an immutable release catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from internal.release.adjacent_edges import (
    AdjacentEdgeError,
    canonical_json,
    inherit_catalog,
)


def read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AdjacentEdgeError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AdjacentEdgeError(f"{path} must contain a JSON object")
    return value


def read_guidance(paths: list[Path]) -> list[dict[str, Any]]:
    return [read_object(path) for path in paths]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose a target release catalog from an immutable prior catalog and one new edge."
    )
    parser.add_argument("--previous-catalog", type=Path, required=True)
    parser.add_argument("--new-edge", type=Path, required=True)
    parser.add_argument("--new-guidance", type=Path, action="append", default=[])
    parser.add_argument("--retired-source", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        catalog = inherit_catalog(
            read_object(args.previous_catalog),
            read_object(args.new_edge),
            retired_sources=args.retired_source,
            new_guidance=read_guidance(args.new_guidance),
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
