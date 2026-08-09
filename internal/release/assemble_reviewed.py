#!/usr/bin/env python3
"""Assemble a release from the canonical adjacent-edge catalog."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from internal.release import assemble
from internal.release.adjacent_edges import AdjacentEdgeError, validate_catalog
from internal.release.release_catalog import (
    manifest_edges,
    read_json_object,
    validate_guidance_artifacts,
)


class ReviewedAssemblyError(RuntimeError):
    pass


def apply_reviewed_catalog(
    output: Path,
    catalog: dict[str, object],
    target_version: str,
) -> None:
    try:
        normalized = validate_catalog(catalog)
        projections = manifest_edges(normalized)
    except AdjacentEdgeError as exc:
        raise ReviewedAssemblyError(str(exc)) from exc
    if normalized["target_version"] != target_version:
        raise ReviewedAssemblyError(
            f"reviewed catalog target {normalized['target_version']} "
            f"does not match {target_version}"
        )

    manifest_path = output / "ava-release.json"
    manifest = json.loads(manifest_path.read_text())
    assembled_sources = {
        edge["from"]
        for edge in manifest["upgrade_paths"]["edges"]
    }
    reviewed_sources = {
        edge["from"]
        for edge in projections
    }
    if assembled_sources != reviewed_sources:
        raise ReviewedAssemblyError(
            "assembled edge sources do not match the reviewed catalog: "
            f"assembled={sorted(assembled_sources)}, "
            f"reviewed={sorted(reviewed_sources)}"
        )

    migration_ids = {
        step["id"]
        for step in manifest["migrations"]["steps"]
    }
    guidance_paths = {
        entry["path"]
        for entry in manifest["guidance"]["entries"]
    }
    for edge in projections:
        unknown_migrations = sorted(set(edge["migration_ids"]) - migration_ids)
        unknown_guidance = sorted(set(edge["guidance_paths"]) - guidance_paths)
        if unknown_migrations:
            raise ReviewedAssemblyError(
                f"catalog migrations for {edge['from']} are absent from release assets: "
                + ", ".join(unknown_migrations)
            )
        if unknown_guidance:
            raise ReviewedAssemblyError(
                f"catalog guidance for {edge['from']} is absent from release assets: "
                + ", ".join(unknown_guidance)
            )

    manifest["upgrade_paths"]["edges"] = projections
    manifest["semantic_review_required"] = any(
        edge["semantic_review_required"]
        for edge in projections
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    checksum_lines = [
        f"{assemble.sha256_file(output / name)}  {name}\n"
        for name in assemble.ASSET_NAMES[:-1]
    ]
    (output / "SHA256SUMS").write_text("".join(checksum_lines))


def stage_guidance(
    catalog: dict[str, object],
    guidance_root: Path,
    destination: Path,
) -> None:
    try:
        normalized = validate_catalog(catalog)
        validate_guidance_artifacts(normalized, guidance_root)
    except AdjacentEdgeError as exc:
        raise ReviewedAssemblyError(str(exc)) from exc
    for item in normalized["guidance"]:
        source = guidance_root / item["path"]
        target = destination / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--channel", choices=("stable", "rc", "beta", "alpha"))
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--source-date-epoch", type=int, required=True)
    parser.add_argument("--published-at")
    parser.add_argument("--release-notes", type=Path)
    parser.add_argument("--guidance-root", type=Path)
    parser.add_argument("--migrations-dir", type=Path)
    parser.add_argument("--upgrade-from", action="append", default=[])
    parser.add_argument("--semantic-review-required", action="store_true")
    parser.add_argument("--upgrade-catalog", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    catalog_path = args.upgrade_catalog.resolve()
    guidance_root = (
        args.guidance_root.resolve()
        if args.guidance_root
        else root / "internal/release/guidance"
    )
    try:
        catalog = validate_catalog(read_json_object(catalog_path))
    except AdjacentEdgeError as exc:
        raise ReviewedAssemblyError(str(exc)) from exc

    target_version = assemble.canonical_version(args.version)
    if catalog["target_version"] != target_version:
        raise ReviewedAssemblyError(
            f"catalog target {catalog['target_version']} does not match {target_version}"
        )

    supplied_sources = set(args.upgrade_from)
    reviewed_sources = set(catalog["supported_sources"])
    if supplied_sources and supplied_sources != reviewed_sources:
        raise ReviewedAssemblyError(
            "command-line upgrade sources disagree with the reviewed catalog: "
            f"command={sorted(supplied_sources)}, reviewed={sorted(reviewed_sources)}"
        )

    del args.upgrade_catalog
    del args.guidance_root
    args.upgrade_from = list(catalog["supported_sources"])
    args.semantic_review_required = any(
        edge["semantic_review_required"]
        for edge in catalog["edges"]
    )

    with tempfile.TemporaryDirectory(prefix="ava-guidance-") as temporary:
        staging = Path(temporary)
        stage_guidance(catalog, guidance_root, staging)
        args.guidance_dir = staging
        assemble.build(args)

    apply_reviewed_catalog(
        args.output.resolve(),
        catalog,
        target_version,
    )
    print(f"Applied reviewed adjacent catalog from {catalog_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        ReviewedAssemblyError,
        assemble.AssemblyError,
        AdjacentEdgeError,
        OSError,
        json.JSONDecodeError,
    ) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
