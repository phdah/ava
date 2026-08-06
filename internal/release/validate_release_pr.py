from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from internal.release.validate_upgrade_impact import (
    SEMVER_RE,
    UpgradeImpactValidationError,
    derive_channel,
    read_upgrade_policy,
    retired_source_assessments,
    source_assessments,
    version_key,
)


class ReleasePrValidationError(ValueError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleasePrValidationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleasePrValidationError(f"{path} must contain a JSON object")
    return value


def _read_version(path: Path) -> str:
    try:
        version = path.read_text().strip()
    except OSError as exc:
        raise ReleasePrValidationError(f"cannot read {path}: {exc}") from exc
    if not SEMVER_RE.fullmatch(version):
        raise ReleasePrValidationError(f"{path} contains an invalid Ava version: {version!r}")
    return version


def validate_release_please_channel(config: dict[str, Any], target_version: str) -> None:
    channel = derive_channel(target_version)
    prerelease = config.get("prerelease")
    versioning = config.get("versioning")
    prerelease_type = config.get("prerelease-type")

    if channel == "stable":
        if prerelease is not False or versioning != "default" or prerelease_type is not None:
            raise ReleasePrValidationError(
                "stable release requires release-please prerelease=false, "
                "versioning='default', and no prerelease-type"
            )
        return

    if prerelease is not True or versioning != "prerelease" or prerelease_type != channel:
        raise ReleasePrValidationError(
            f"{channel} release requires release-please prerelease=true, "
            f"versioning='prerelease', and prerelease-type='{channel}'"
        )


def validate_release_pr(root: Path, previous_version: str) -> str:
    root = root.resolve()
    if not SEMVER_RE.fullmatch(previous_version):
        raise ReleasePrValidationError(
            f"invalid previous Ava version supplied by the workflow: {previous_version!r}"
        )

    target_version = _read_version(root / "version.txt")
    manifest = _read_json(root / ".release-please-manifest.json")
    if manifest.get(".") != target_version:
        raise ReleasePrValidationError(
            ".release-please-manifest.json and version.txt disagree: "
            f"{manifest.get('.')!r} != {target_version!r}"
        )

    if version_key(target_version) <= version_key(previous_version):
        raise ReleasePrValidationError(
            f"release PR must advance Ava from {previous_version} to a newer version, "
            f"got {target_version}"
        )

    config = _read_json(root / "release-please-config.json")
    try:
        validate_release_please_channel(config, target_version)
        policy = read_upgrade_policy(root)
    except UpgradeImpactValidationError as exc:
        raise ReleasePrValidationError(str(exc)) from exc

    if previous_version == "0.0.0" and target_version != policy["initial_release_version"]:
        raise ReleasePrValidationError(
            f"first release target must be {policy['initial_release_version']}, "
            f"got {target_version}"
        )

    impact = _read_json(root / "internal/release/upgrade-impact.json")
    try:
        source_assessments(impact)
        retired_source_assessments(impact)
    except UpgradeImpactValidationError as exc:
        raise ReleasePrValidationError(str(exc)) from exc
    if impact.get("target_version") != target_version:
        raise ReleasePrValidationError(
            f"upgrade-impact.json target {impact.get('target_version')!r} does not match "
            f"release PR target {target_version!r}"
        )

    return (
        f"release PR identity valid for {previous_version} -> {target_version}; "
        f"channel: {derive_channel(target_version)}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate release-please identity, channel, and reviewed release state."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--previous-version", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        message = validate_release_pr(args.root, args.previous_version)
    except ReleasePrValidationError as exc:
        print(f"release PR policy invalid: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
