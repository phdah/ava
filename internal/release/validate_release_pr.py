from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

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
        raise ReleasePrValidationError(f"{path} contains an invalid Ava version: {version!r}")
    return version


def _read_upgrade_sources(path: Path) -> list[str]:
    try:
        sources = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    except OSError as exc:
        raise ReleasePrValidationError(f"cannot read {path}: {exc}") from exc

    invalid = [source for source in sources if not SEMVER_RE.fullmatch(source)]
    if invalid:
        raise ReleasePrValidationError(
            f"{path} contains invalid Ava versions: {', '.join(sorted(invalid))}"
        )
    if len(sources) != len(set(sources)):
        raise ReleasePrValidationError(f"{path} contains duplicate upgrade sources")
    return sources


def _transition_sources(
    transitions: object,
    *,
    target_version: str,
    location: str,
) -> set[str]:
    if not isinstance(transitions, list):
        raise ReleasePrValidationError(f"{location} must be a list")

    sources: set[str] = set()
    for index, transition in enumerate(transitions):
        if not isinstance(transition, dict):
            raise ReleasePrValidationError(f"{location}[{index}] must be an object")
        if transition.get("to") != target_version:
            continue
        source = transition.get("from")
        if not isinstance(source, str) or not SEMVER_RE.fullmatch(source):
            raise ReleasePrValidationError(
                f"{location}[{index}].from is not a valid Ava version"
            )
        if transition.get("must_be_declared") is not True:
            raise ReleasePrValidationError(
                f"{location}[{index}] must set must_be_declared to true"
            )
        sources.add(source)
    return sources


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

    actual_sources = set(_read_upgrade_sources(root / "internal/release/upgrade-sources.txt"))
    policy = _read_json(root / "internal/release/fixtures/alpha-qualification.json")
    matrix = _read_json(root / "internal/release/fixtures/conformance-matrix.json")

    prerelease_support = policy.get("prerelease_support")
    if not isinstance(prerelease_support, dict):
        raise ReleasePrValidationError(
            "alpha-qualification.json.prerelease_support must be an object"
        )
    first_alpha = prerelease_support.get("first_alpha")
    if not isinstance(first_alpha, dict) or not isinstance(first_alpha.get("version"), str):
        raise ReleasePrValidationError(
            "alpha-qualification.json.prerelease_support.first_alpha.version is required"
        )
    first_alpha_version = first_alpha["version"]

    policy_sources = _transition_sources(
        prerelease_support.get("transitions"),
        target_version=target_version,
        location="alpha-qualification.json.prerelease_support.transitions",
    )
    matrix_sources = _transition_sources(
        matrix.get("prerelease_transitions"),
        target_version=target_version,
        location="conformance-matrix.json.prerelease_transitions",
    )

    if target_version == first_alpha_version:
        if actual_sources:
            raise ReleasePrValidationError(
                f"first alpha {target_version} must not declare upgrade sources"
            )
        if policy_sources or matrix_sources:
            raise ReleasePrValidationError(
                f"first alpha {target_version} must not declare upgrade transitions"
            )
        return f"release PR policy valid for first alpha {target_version}"

    if previous_version == target_version:
        raise ReleasePrValidationError(
            f"release PR does not advance the Ava version from {previous_version}"
        )
    if previous_version not in actual_sources:
        raise ReleasePrValidationError(
            f"upgrade-sources.txt must include the current main version {previous_version} "
            f"when preparing {target_version}"
        )

    target_is_prerelease = SEMVER_RE.fullmatch(target_version).group(4) is not None
    if target_is_prerelease and not policy_sources:
        raise ReleasePrValidationError(
            f"alpha-qualification.json declares no transition to prerelease {target_version}"
        )
    if target_is_prerelease and not matrix_sources:
        raise ReleasePrValidationError(
            f"conformance-matrix.json declares no transition to prerelease {target_version}"
        )

    if policy_sources or matrix_sources:
        if policy_sources != matrix_sources:
            raise ReleasePrValidationError(
                "release transition fixtures disagree for "
                f"{target_version}: policy={sorted(policy_sources)}, "
                f"matrix={sorted(matrix_sources)}"
            )
        if actual_sources != policy_sources:
            raise ReleasePrValidationError(
                "upgrade-sources.txt does not exactly match the declared transitions for "
                f"{target_version}: actual={sorted(actual_sources)}, "
                f"expected={sorted(policy_sources)}"
            )

    return (
        f"release PR policy valid for {previous_version} -> {target_version}; "
        f"upgrade sources: {', '.join(sorted(actual_sources))}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate release-only upgrade edge declarations for a release-please PR."
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
