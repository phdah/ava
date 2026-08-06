from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(alpha|beta|rc)\.([1-9][0-9]*))?$"
)
RETAINED_VALUE = "all-unlisted-managed-payload-files"
SOURCE_FIELDS = {
    "from",
    "managed_changes",
    "migration_ids",
    "migration_assessment",
    "guidance_paths",
    "semantic_review_required",
    "semantic_assessment",
    "release_note_versions",
    "release_note_assessment",
}
MANAGED_CHANGE_FIELDS = {"retained", "replaced", "created", "deleted"}


class UpgradeImpactValidationError(ValueError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise UpgradeImpactValidationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise UpgradeImpactValidationError(f"{path} must contain a JSON object")
    return value


def _read_version(path: Path) -> str:
    try:
        value = path.read_text().strip()
    except OSError as exc:
        raise UpgradeImpactValidationError(f"cannot read {path}: {exc}") from exc
    if not SEMVER_RE.fullmatch(value):
        raise UpgradeImpactValidationError(
            f"{path} contains an invalid Ava version: {value!r}"
        )
    return value


def _read_sources(path: Path) -> list[str]:
    try:
        values = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    except OSError as exc:
        raise UpgradeImpactValidationError(f"cannot read {path}: {exc}") from exc
    if len(values) != len(set(values)):
        raise UpgradeImpactValidationError(f"{path} contains duplicate upgrade sources")
    invalid = [value for value in values if not SEMVER_RE.fullmatch(value)]
    if invalid:
        raise UpgradeImpactValidationError(
            f"{path} contains invalid Ava versions: {', '.join(sorted(invalid))}"
        )
    return values


def _version_list(value: object, location: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a non-empty list" if not allow_empty else "a list"
        raise UpgradeImpactValidationError(f"{location} must be {qualifier}")
    if not all(isinstance(item, str) and SEMVER_RE.fullmatch(item) for item in value):
        raise UpgradeImpactValidationError(f"{location} must contain valid Ava versions")
    if len(value) != len(set(value))):
        raise UpgradeImpactValidationError(f"{location} contains duplicates")
    return list(value)


def _string_list(value: object, location: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise UpgradeImpactValidationError(
            f"{location} must be a list of non-empty strings"
        )
    if len(value) != len(set(value)):
        raise UpgradeImpactValidationError(f"{location} contains duplicates")
    return list(value)


def source_assessments(impact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if impact.get("schema_version") != 1:
        raise UpgradeImpactValidationError("upgrade-impact.json.schema_version must be 1")
    target = impact.get("target_version")
    if not isinstance(target, str) or not SEMVER_RE.fullmatch(target):
        raise UpgradeImpactValidationError("upgrade-impact.json.target_version is invalid")
    values = impact.get("sources")
    if not isinstance(values, list) or not values:
        raise UpgradeImpactValidationError(
            "upgrade-impact.json.sources must be a non-empty list"
        )

    result: dict[str, dict[str, Any]] = {}
    for index, assessment in enumerate(values):
        location = f"upgrade-impact.json.sources[{index}]"
        if not isinstance(assessment, dict):
            raise UpgradeImpactValidationError(f"{location} must be an object")
        if set(assessment) != SOURCE_FIELDS:
            raise UpgradeImpactValidationError(
                f"{location} fields must be exactly {sorted(SOURCE_FIELDS)}"
            )
        source = assessment["from"]
        if not isinstance(source, str) or not SEMVER_RE.fullmatch(source):
            raise UpgradeImpactValidationError(f"{location}.from is invalid")
        if source in result:
            raise UpgradeImpactValidationError(f"duplicate impact assessment for {source}")

        changes = assessment["managed_changes"]
        if not isinstance(changes, dict) or set(changes) != MANAGED_CHANGE_FIELDS:
            raise UpgradeImpactValidationError(
                f"{location}.managed_changes fields must be exactly "
                f"{sorted(MANAGED_CHANGE_FIELDS)}"
            )
        if changes["retained"] != RETAINED_VALUE:
            raise UpgradeImpactValidationError(
                f"{location}.managed_changes.retained must be {RETAINED_VALUE!r}"
            )
        for name in ("replaced", "created", "deleted"):
            paths = _string_list(changes[name], f"{location}.managed_changes.{name}")
            for path in paths:
                candidate = PurePosixPath(path)
                if not candidate.is_absolute() or ".." in candidate.parts:
                    raise UpgradeImpactValidationError(
                        f"{location}.managed_changes.{name} contains unsafe "
                        f"installed path {path!r}"
                    )
            changes[name] = paths

        assessment["migration_ids"] = _string_list(
            assessment["migration_ids"], f"{location}.migration_ids"
        )
        assessment["guidance_paths"] = _string_list(
            assessment["guidance_paths"], f"{location}.guidance_paths"
        )
        for field in (
            "migration_assessment",
            "semantic_assessment",
            "release_note_assessment",
        ):
            if not isinstance(assessment[field], str) or not assessment[field].strip():
                raise UpgradeImpactValidationError(
                    f"{location}.{field} must be non-empty"
                )
        if not isinstance(assessment["semantic_review_required"], bool):
            raise UpgradeImpactValidationError(
                f"{location}.semantic_review_required must be boolean"
            )
        assessment["release_note_versions"] = _version_list(
            assessment["release_note_versions"],
            f"{location}.release_note_versions",
            allow_empty=False,
        )
        result[source] = assessment
    return result


def repository_path_to_installed(path: str) -> str | None:
    prefix = "templates/base/"
    if not path.startswith(prefix):
        return None
    relative = path.removeprefix(prefix)
    if relative == "AGENTS.md":
        return "/AGENTS.md"
    if relative == "index.md" or relative.startswith(
        ("roles/", "workflows/", "shared/")
    ):
        return f"/.ava/base/{relative}"
    return None


def managed_delta(root: Path, source: str) -> dict[str, list[str]]:
    command = [
        "git",
        "-C",
        str(root),
        "diff",
        "--name-status",
        f"v{source}..HEAD",
        "--",
        "templates/base",
    ]
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise UpgradeImpactValidationError(
            f"cannot compare v{source} with HEAD: {result.stderr.strip()}"
        )

    delta = {"replaced": [], "created": [], "deleted": []}
    for line in result.stdout.splitlines():
        fields = line.split("\t")
        status = fields[0]
        if status.startswith("R") and len(fields) == 3:
            old = repository_path_to_installed(fields[1])
            new = repository_path_to_installed(fields[2])
            if old:
                delta["deleted"].append(old)
            if new:
                delta["created"].append(new)
            continue
        if len(fields) != 2:
            raise UpgradeImpactValidationError(f"unexpected git diff record: {line!r}")
        destination = repository_path_to_installed(fields[1])
        if destination is None:
            continue
        if status == "M":
            delta["replaced"].append(destination)
        elif status == "A":
            delta["created"].append(destination)
        elif status == "D":
            delta["deleted"].append(destination)
        else:
            raise UpgradeImpactValidationError(
                f"unsupported managed payload change status {status!r} for {fields[1]}"
            )
    return {name: sorted(paths) for name, paths in delta.items()}


def validate_release_note_coverage(
    changelog: str,
    assessments: dict[str, dict[str, Any]],
) -> None:
    headings = set(re.findall(r"(?m)^## \[([^]]+)\]", changelog))
    for source, assessment in assessments.items():
        missing = sorted(set(assessment["release_note_versions"]) - headings)
        if missing:
            raise UpgradeImpactValidationError(
                f"release notes for {source} require missing changelog versions: "
                + ", ".join(missing)
            )


def validate_upgrade_impact(
    root: Path,
    previous_version: str,
    *,
    verify_managed_delta: bool,
) -> str:
    root = root.resolve()
    if not SEMVER_RE.fullmatch(previous_version):
        raise UpgradeImpactValidationError(
            f"invalid previous Ava version supplied by the workflow: {previous_version!r}"
        )

    target = _read_version(root / "version.txt")
    sources = set(_read_sources(root / "internal/release/upgrade-sources.txt"))
    impact = _read_json(root / "internal/release/upgrade-impact.json")
    assessments = source_assessments(impact)
    policy = _read_json(root / "internal/release/fixtures/alpha-qualification.json")

    if impact["target_version"] != target:
        raise UpgradeImpactValidationError(
            f"upgrade-impact.json target {impact['target_version']} does not match "
            f"version.txt {target}"
        )
    if set(assessments) != sources:
        raise UpgradeImpactValidationError(
            "upgrade-impact.json sources do not exactly match upgrade-sources.txt: "
            f"impact={sorted(assessments)}, declared={sorted(sources)}"
        )

    support = policy.get("prerelease_support")
    if not isinstance(support, dict):
        raise UpgradeImpactValidationError(
            "alpha-qualification.json.prerelease_support must be an object"
        )
    protected = set(
        _version_list(
            support.get("protected_direct_sources"),
            "alpha-qualification.json.prerelease_support.protected_direct_sources",
        )
    )
    required = protected | {previous_version}
    omitted = sorted(required - sources)
    if omitted:
        raise UpgradeImpactValidationError(
            "upgrade source declaration strands protected installed prereleases: "
            + ", ".join(omitted)
        )

    try:
        changelog = (root / "CHANGELOG.md").read_text()
    except OSError as exc:
        raise UpgradeImpactValidationError(f"cannot read CHANGELOG.md: {exc}") from exc
    validate_release_note_coverage(changelog, assessments)

    if verify_managed_delta:
        for source, assessment in assessments.items():
            actual = managed_delta(root, source)
            declared = assessment["managed_changes"]
            for field in ("replaced", "created", "deleted"):
                if actual[field] != sorted(declared[field]):
                    raise UpgradeImpactValidationError(
                        f"managed {field} paths for {source} disagree with "
                        f"v{source}..HEAD: declared={sorted(declared[field])}, "
                        f"actual={actual[field]}"
                    )

    return (
        f"reviewed upgrade impact valid for {target}; protected direct sources: "
        f"{', '.join(sorted(sources))}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate reviewed per-source upgrade impact for a release pull request."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--previous-version", required=True)
    parser.add_argument("--skip-managed-delta", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        message = validate_upgrade_impact(
            args.root,
            args.previous_version,
            verify_managed_delta=not args.skip_managed_delta,
        )
    except UpgradeImpactValidationError as exc:
        print(f"upgrade impact invalid: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
