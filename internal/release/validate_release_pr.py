from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from internal.release.adjacent_edges import AdjacentEdgeError, version_key
from internal.release.release_catalog import (
    read_catalog,
    read_release_record,
    validate_release_delta,
)


SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(alpha|beta|rc)\.([1-9][0-9]*))?$"
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
        raise ReleasePrValidationError(
            f"{path} contains an invalid Ava version: {version!r}"
        )
    return version


def derive_channel(version: str) -> str:
    match = SEMVER_RE.fullmatch(version)
    if match is None:
        raise ReleasePrValidationError(f"invalid Ava version: {version!r}")
    return match.group(4) or "stable"


def validate_release_please_channel(
    config: dict[str, Any],
    target_version: str,
) -> None:
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


def _read_upgrade_policy(root: Path) -> dict[str, Any]:
    path = root / "internal/release/fixtures/release-upgrade-policy.json"
    policy = _read_json(path)
    required = {
        "schema_version",
        "initial_release_version",
        "protected_direct_sources",
    }
    if set(policy) != required or policy.get("schema_version") != 1:
        raise ReleasePrValidationError(f"{path} has invalid schema 1 fields")
    initial = policy["initial_release_version"]
    protected = policy["protected_direct_sources"]
    if not isinstance(initial, str) or not SEMVER_RE.fullmatch(initial):
        raise ReleasePrValidationError(f"{path} has invalid initial_release_version")
    if (
        not isinstance(protected, list)
        or not all(isinstance(item, str) and SEMVER_RE.fullmatch(item) for item in protected)
        or len(protected) != len(set(protected))
    ):
        raise ReleasePrValidationError(f"{path} has invalid protected source list")
    return policy


def validate_catalog_change_scope(
    root: Path,
    base_revision: str,
    target_version: str,
) -> None:
    try:
        completed = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                base_revision,
                "--",
                "internal/release/catalogs",
            ],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ReleasePrValidationError(
            f"cannot compare release catalog files with {base_revision}: {exc}"
        ) from exc
    changed_json = {
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip().endswith(".json")
    }
    expected = f"internal/release/catalogs/{target_version}.json"
    if changed_json != {expected}:
        raise ReleasePrValidationError(
            "a release PR may add only its own release-local catalog record; "
            f"expected {expected}, changed {sorted(changed_json)}"
        )


def validate_release_pr(
    root: Path,
    previous_version: str,
    *,
    base_revision: str | None = None,
) -> str:
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

    validate_release_please_channel(
        _read_json(root / "release-please-config.json"),
        target_version,
    )
    policy = _read_upgrade_policy(root)
    if previous_version == "0.0.0" and target_version != policy["initial_release_version"]:
        raise ReleasePrValidationError(
            f"first release target must be {policy['initial_release_version']}, "
            f"got {target_version}"
        )

    legacy_impact = root / "internal/release/upgrade-impact.json"
    if legacy_impact.exists():
        raise ReleasePrValidationError(
            "upgrade-impact.json is archival compatibility data and is not a valid "
            "authoring input. Author one release-local adjacent edge record."
        )

    try:
        previous_catalog = read_catalog(root, previous_version)
        current_record = read_release_record(root, target_version)
        protected_retirements = {
            item["version"]
            for item in current_record["retired_sources"]
        } & set(policy["protected_direct_sources"])
        if protected_retirements:
            raise ReleasePrValidationError(
                "protected supported sources require a separate policy change before "
                "retirement: "
                + ", ".join(sorted(protected_retirements, key=version_key))
            )
        expected_catalog = validate_release_delta(
            previous_catalog,
            current_record,
            guidance_root=root / "internal/release/guidance",
        )
        recursive_catalog = read_catalog(root, target_version)
        if recursive_catalog != expected_catalog:
            raise ReleasePrValidationError(
                "the target record does not recursively compose to the reviewed release delta"
            )
    except AdjacentEdgeError as exc:
        raise ReleasePrValidationError(str(exc)) from exc

    if base_revision:
        validate_catalog_change_scope(root, base_revision, target_version)

    return (
        f"release PR identity and recursive adjacent edge valid for "
        f"{previous_version} -> {target_version}; "
        f"channel: {derive_channel(target_version)}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate release identity and one release-local edge record."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--previous-version", required=True)
    parser.add_argument("--base-revision")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        message = validate_release_pr(
            args.root,
            args.previous_version,
            base_revision=args.base_revision,
        )
    except ReleasePrValidationError as exc:
        print(f"release PR policy invalid: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
