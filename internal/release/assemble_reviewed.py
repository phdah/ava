#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from internal.release import assemble
from internal.release.validate_upgrade_impact import (
    UpgradeImpactValidationError,
    source_assessments,
    version_key,
)


class ReviewedAssemblyError(RuntimeError):
    pass


def apply_reviewed_impact(output: Path, impact_path: Path, target_version: str) -> None:
    try:
        impact = json.loads(impact_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewedAssemblyError(f"cannot read reviewed upgrade impact: {exc}") from exc
    try:
        assessments = source_assessments(
            impact,
            require_semantic_evidence=True,
        )
    except UpgradeImpactValidationError as exc:
        raise ReviewedAssemblyError(str(exc)) from exc
    if impact["target_version"] != target_version:
        raise ReviewedAssemblyError(
            f"reviewed impact target {impact['target_version']} does not match {target_version}"
        )

    manifest_path = output / "ava-release.json"
    manifest = json.loads(manifest_path.read_text())
    edges = manifest["upgrade_paths"]["edges"]
    edge_by_source = {edge["from"]: edge for edge in edges}
    if set(edge_by_source) != set(assessments):
        raise ReviewedAssemblyError(
            "assembled edge sources do not match reviewed impact: "
            f"assembled={sorted(edge_by_source)}, reviewed={sorted(assessments)}"
        )

    migration_ids = {step["id"] for step in manifest["migrations"]["steps"]}
    guidance_paths = {entry["path"] for entry in manifest["guidance"]["entries"]}
    for source, assessment in assessments.items():
        unknown_migrations = sorted(set(assessment["migration_ids"]) - migration_ids)
        unknown_guidance = sorted(set(assessment["guidance_paths"]) - guidance_paths)
        if unknown_migrations:
            raise ReviewedAssemblyError(
                f"reviewed migration IDs for {source} are absent from release assets: "
                + ", ".join(unknown_migrations)
            )
        if unknown_guidance:
            raise ReviewedAssemblyError(
                f"reviewed guidance paths for {source} are absent from release assets: "
                + ", ".join(unknown_guidance)
            )
        edge = edge_by_source[source]
        edge["migration_ids"] = list(assessment["migration_ids"])
        edge["guidance_paths"] = list(assessment["guidance_paths"])
        edge["semantic_review_required"] = assessment["semantic_review_required"]

    manifest["semantic_review_required"] = any(
        assessment["semantic_review_required"] for assessment in assessments.values()
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    checksum_lines = [
        f"{assemble.sha256_file(output / name)}  {name}\n"
        for name in assemble.ASSET_NAMES[:-1]
    ]
    (output / "SHA256SUMS").write_text("".join(checksum_lines))


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
    parser.add_argument("--guidance-dir", type=Path)
    parser.add_argument("--migrations-dir", type=Path)
    parser.add_argument("--upgrade-from", action="append", default=[])
    parser.add_argument("--semantic-review-required", action="store_true")
    parser.add_argument("--upgrade-impact", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    impact_path = args.upgrade_impact
    del args.upgrade_impact
    try:
        impact = json.loads(impact_path.read_text())
        assessments = source_assessments(
            impact,
            require_semantic_evidence=True,
        )
    except (OSError, json.JSONDecodeError, UpgradeImpactValidationError) as exc:
        raise ReviewedAssemblyError(f"cannot read reviewed upgrade impact: {exc}") from exc

    supplied_sources = set(args.upgrade_from)
    reviewed_sources = set(assessments)
    if supplied_sources and supplied_sources != reviewed_sources:
        raise ReviewedAssemblyError(
            "command-line upgrade sources disagree with reviewed impact: "
            f"command={sorted(supplied_sources)}, reviewed={sorted(reviewed_sources)}"
        )
    args.upgrade_from = sorted(reviewed_sources, key=version_key)
    args.semantic_review_required = any(
        assessment["semantic_review_required"] for assessment in assessments.values()
    )
    assemble.build(args)
    apply_reviewed_impact(
        args.output.resolve(),
        impact_path.resolve(),
        assemble.canonical_version(args.version),
    )
    print(f"Applied reviewed upgrade impact from {impact_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        ReviewedAssemblyError,
        assemble.AssemblyError,
        OSError,
        json.JSONDecodeError,
    ) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
