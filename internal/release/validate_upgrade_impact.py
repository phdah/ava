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
SOURCE_FIELDS_V1 = {
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
SOURCE_FIELDS_V2 = SOURCE_FIELDS_V1 | {"semantic_impact_evidence"}
MANAGED_CHANGE_FIELDS = {"retained", "replaced", "created", "deleted"}
SEMANTIC_EVIDENCE_FIELDS = {"managed_path", "project_owned_impact", "reason"}
RETIREMENT_FIELDS = {"version", "reason"}
POLICY_FIELDS = {"schema_version", "initial_release_version", "protected_direct_sources"}


class UpgradeImpactValidationError(ValueError):
    pass


def version_key(value: str) -> tuple[int, int, int, int, int]:
    match = SEMVER_RE.fullmatch(value)
    if not match:
        raise UpgradeImpactValidationError(f"invalid Ava version: {value!r}")
    channel = match.group(4)
    channel_rank = {"alpha": 0, "beta": 1, "rc": 2, None: 3}[channel]
    prerelease_number = int(match.group(5) or 0)
    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        channel_rank,
        prerelease_number,
    )


def derive_channel(value: str) -> str:
    match = SEMVER_RE.fullmatch(value)
    if not match:
        raise UpgradeImpactValidationError(f"invalid Ava version: {value!r}")
    return match.group(4) or "stable"


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
        raise UpgradeImpactValidationError(f"{path} contains an invalid Ava version: {value!r}")
    return value


def _version_list(value: object, location: str) -> list[str]:
    if not isinstance(value, list):
        raise UpgradeImpactValidationError(f"{location} must be a list")
    if not all(isinstance(item, str) and SEMVER_RE.fullmatch(item) for item in value):
        raise UpgradeImpactValidationError(f"{location} must contain valid Ava versions")
    if len(value) != len(set(value)):
        raise UpgradeImpactValidationError(f"{location} contains duplicates")
    return list(value)


def _string_list(value: object, location: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise UpgradeImpactValidationError(f"{location} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise UpgradeImpactValidationError(f"{location} contains duplicates")
    return list(value)


def _installed_path(value: object, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise UpgradeImpactValidationError(f"{location} must be a non-empty installed path")
    candidate = PurePosixPath(value)
    if not candidate.is_absolute() or ".." in candidate.parts:
        raise UpgradeImpactValidationError(f"{location} contains unsafe installed path {value!r}")
    return value


def _semantic_evidence(
    value: object,
    location: str,
    changed_paths: set[str],
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise UpgradeImpactValidationError(f"{location} must be a list")

    evidence: list[dict[str, Any]] = []
    paths: list[str] = []
    for index, item in enumerate(value):
        item_location = f"{location}[{index}]"
        if not isinstance(item, dict) or set(item) != SEMANTIC_EVIDENCE_FIELDS:
            raise UpgradeImpactValidationError(
                f"{item_location} fields must be exactly {sorted(SEMANTIC_EVIDENCE_FIELDS)}"
            )
        path = _installed_path(item["managed_path"], f"{item_location}.managed_path")
        impact = item["project_owned_impact"]
        reason = item["reason"]
        if not isinstance(impact, bool):
            raise UpgradeImpactValidationError(
                f"{item_location}.project_owned_impact must be boolean"
            )
        if not isinstance(reason, str) or not reason.strip():
            raise UpgradeImpactValidationError(f"{item_location}.reason must be non-empty")
        paths.append(path)
        evidence.append(
            {
                "managed_path": path,
                "project_owned_impact": impact,
                "reason": reason,
            }
        )

    if len(paths) != len(set(paths)):
        raise UpgradeImpactValidationError(f"{location} contains duplicate managed paths")
    evidence_paths = set(paths)
    if evidence_paths != changed_paths:
        missing = sorted(changed_paths - evidence_paths)
        extra = sorted(evidence_paths - changed_paths)
        details: list[str] = []
        if missing:
            details.append("missing=" + ", ".join(missing))
        if extra:
            details.append("unexpected=" + ", ".join(extra))
        raise UpgradeImpactValidationError(
            f"{location} must account for every created, replaced, or deleted managed path"
            + (": " + "; ".join(details) if details else "")
        )
    return evidence


def source_assessments(
    impact: dict[str, Any],
    *,
    require_semantic_evidence: bool = False,
) -> dict[str, dict[str, Any]]:
    allowed_fields = {"schema_version", "target_version", "retired_sources", "sources"}
    if set(impact) != allowed_fields:
        raise UpgradeImpactValidationError(
            f"upgrade-impact.json fields must be exactly {sorted(allowed_fields)}"
        )
    schema_version = impact.get("schema_version")
    if schema_version not in {1, 2}:
        raise UpgradeImpactValidationError("upgrade-impact.json.schema_version must be 1 or 2")
    if require_semantic_evidence and schema_version != 2:
        raise UpgradeImpactValidationError(
            "current release upgrade-impact.json must use schema_version 2 with semantic impact evidence"
        )

    target = impact.get("target_version")
    if not isinstance(target, str) or not SEMVER_RE.fullmatch(target):
        raise UpgradeImpactValidationError("upgrade-impact.json.target_version is invalid")
    values = impact.get("sources")
    if not isinstance(values, list):
        raise UpgradeImpactValidationError("upgrade-impact.json.sources must be a list")

    source_fields = SOURCE_FIELDS_V2 if schema_version == 2 else SOURCE_FIELDS_V1
    result: dict[str, dict[str, Any]] = {}
    for index, assessment in enumerate(values):
        location = f"upgrade-impact.json.sources[{index}]"
        if not isinstance(assessment, dict):
            raise UpgradeImpactValidationError(f"{location} must be an object")
        if set(assessment) != source_fields:
            raise UpgradeImpactValidationError(
                f"{location} fields must be exactly {sorted(source_fields)}"
            )
        source = assessment["from"]
        if not isinstance(source, str) or not SEMVER_RE.fullmatch(source):
            raise UpgradeImpactValidationError(f"{location}.from is invalid")
        if source in result:
            raise UpgradeImpactValidationError(f"duplicate impact assessment for {source}")
        if version_key(source) >= version_key(target):
            raise UpgradeImpactValidationError(
                f"{location}.from must be older than target version {target}"
            )

        changes = assessment["managed_changes"]
        if not isinstance(changes, dict) or set(changes) != MANAGED_CHANGE_FIELDS:
            raise UpgradeImpactValidationError(
                f"{location}.managed_changes fields must be exactly {sorted(MANAGED_CHANGE_FIELDS)}"
            )
        if changes["retained"] != RETAINED_VALUE:
            raise UpgradeImpactValidationError(
                f"{location}.managed_changes.retained must be {RETAINED_VALUE!r}"
            )
        changed_paths: set[str] = set()
        for name in ("replaced", "created", "deleted"):
            paths = _string_list(changes[name], f"{location}.managed_changes.{name}")
            for path in paths:
                _installed_path(path, f"{location}.managed_changes.{name}")
                if path in changed_paths:
                    raise UpgradeImpactValidationError(
                        f"{location}.managed_changes declares {path!r} in more than one change class"
                    )
                changed_paths.add(path)
            changes[name] = paths

        assessment["migration_ids"] = _string_list(
            assessment["migration_ids"], f"{location}.migration_ids"
        )
        assessment["guidance_paths"] = _string_list(
            assessment["guidance_paths"], f"{location}.guidance_paths"
        )
        for path in assessment["guidance_paths"]:
            candidate = PurePosixPath(path)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise UpgradeImpactValidationError(
                    f"{location}.guidance_paths contains unsafe relative path {path!r}"
                )
        for field in (
            "migration_assessment",
            "semantic_assessment",
            "release_note_assessment",
        ):
            if not isinstance(assessment[field], str) or not assessment[field].strip():
                raise UpgradeImpactValidationError(f"{location}.{field} must be non-empty")
        if not isinstance(assessment["semantic_review_required"], bool):
            raise UpgradeImpactValidationError(
                f"{location}.semantic_review_required must be boolean"
            )

        if schema_version == 2:
            evidence = _semantic_evidence(
                assessment["semantic_impact_evidence"],
                f"{location}.semantic_impact_evidence",
                changed_paths,
            )
            assessment["semantic_impact_evidence"] = evidence
            evidenced_requirement = any(
                item["project_owned_impact"] for item in evidence
            )
            if assessment["semantic_review_required"] != evidenced_requirement:
                raise UpgradeImpactValidationError(
                    f"{location}.semantic_review_required must equal the path-by-path semantic impact evidence"
                )
            if evidenced_requirement and not assessment["guidance_paths"]:
                raise UpgradeImpactValidationError(
                    f"{location} requires project-owned semantic review but declares no guidance_paths"
                )
            if not evidenced_requirement and assessment["guidance_paths"]:
                raise UpgradeImpactValidationError(
                    f"{location} declares guidance_paths without project-owned semantic impact"
                )

        assessment["release_note_versions"] = _version_list(
            assessment["release_note_versions"],
            f"{location}.release_note_versions",
        )
        result[source] = assessment
    return result


def retired_source_assessments(impact: dict[str, Any]) -> dict[str, str]:
    values = impact.get("retired_sources")
    if not isinstance(values, list):
        raise UpgradeImpactValidationError("upgrade-impact.json.retired_sources must be a list")
    result: dict[str, str] = {}
    for index, retirement in enumerate(values):
        location = f"upgrade-impact.json.retired_sources[{index}]"
        if not isinstance(retirement, dict) or set(retirement) != RETIREMENT_FIELDS:
            raise UpgradeImpactValidationError(
                f"{location} fields must be exactly {sorted(RETIREMENT_FIELDS)}"
            )
        version = retirement["version"]
        reason = retirement["reason"]
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            raise UpgradeImpactValidationError(f"{location}.version is invalid")
        if version in result:
            raise UpgradeImpactValidationError(f"duplicate retirement for {version}")
        if not isinstance(reason, str) or not reason.strip():
            raise UpgradeImpactValidationError(f"{location}.reason must be non-empty")
        result[version] = reason
    return result


def read_upgrade_policy(root: Path) -> dict[str, Any]:
    path = root / "internal/release/fixtures/release-upgrade-policy.json"
    policy = _read_json(path)
    if set(policy) != POLICY_FIELDS:
        raise UpgradeImpactValidationError(
            f"{path} fields must be exactly {sorted(POLICY_FIELDS)}"
        )
    if policy.get("schema_version") != 1:
        raise UpgradeImpactValidationError(f"{path}.schema_version must be 1")
    initial = policy.get("initial_release_version")
    if not isinstance(initial, str) or not SEMVER_RE.fullmatch(initial):
        raise UpgradeImpactValidationError(f"{path}.initial_release_version is invalid")
    policy["protected_direct_sources"] = _version_list(
        policy.get("protected_direct_sources"),
        f"{path}.protected_direct_sources",
    )
    return policy


def _git_show(root: Path, revision: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def previous_direct_sources(root: Path, previous_version: str) -> set[str]:
    tag = f"v{previous_version}"
    reviewed = _git_show(root, tag, "internal/release/upgrade-impact.json")
    if reviewed is not None:
        try:
            impact = json.loads(reviewed)
        except json.JSONDecodeError as exc:
            raise UpgradeImpactValidationError(
                f"cannot parse previous release impact from {tag}: {exc}"
            ) from exc
        if not isinstance(impact, dict):
            raise UpgradeImpactValidationError(
                f"previous release impact from {tag} must be an object"
            )
        if impact.get("target_version") != previous_version:
            raise UpgradeImpactValidationError(
                f"previous release impact target does not match {previous_version}"
            )
        return set(source_assessments(impact))

    legacy = _git_show(root, tag, "internal/release/upgrade-sources.txt")
    if legacy is None:
        return set()
    values = [line.strip() for line in legacy.splitlines() if line.strip()]
    if len(values) != len(set(values)):
        raise UpgradeImpactValidationError(
            f"legacy upgrade sources in {tag} contain duplicates"
        )
    invalid = [value for value in values if not SEMVER_RE.fullmatch(value)]
    if invalid:
        raise UpgradeImpactValidationError(
            f"legacy upgrade sources in {tag} contain invalid versions: "
            + ", ".join(sorted(invalid))
        )
    return set(values)


def required_direct_sources(root: Path, previous_version: str) -> tuple[set[str], set[str]]:
    policy = read_upgrade_policy(root)
    if previous_version == "0.0.0":
        return set(), set(policy["protected_direct_sources"])
    inherited = previous_direct_sources(root, previous_version)
    protected = set(policy["protected_direct_sources"])
    return inherited | protected | {previous_version}, protected


def repository_path_to_installed(path: str) -> str | None:
    prefix = "templates/base/"
    if not path.startswith(prefix):
        return None
    relative = path.removeprefix(prefix)
    if relative == "AGENTS.md":
        return "/AGENTS.md"
    if relative == "index.md" or relative.startswith(("roles/", "workflows/", "shared/")):
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
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


def changelog_versions(changelog: str) -> list[str]:
    values = re.findall(r"(?m)^## \[([^]]+)\]", changelog)
    return sorted(
        {value for value in values if SEMVER_RE.fullmatch(value)},
        key=version_key,
    )


def validate_release_note_coverage(
    changelog: str,
    target: str,
    assessments: dict[str, dict[str, Any]],
) -> None:
    available = changelog_versions(changelog)
    for source, assessment in assessments.items():
        expected = [
            version
            for version in available
            if version_key(source) < version_key(version) <= version_key(target)
        ]
        declared = assessment["release_note_versions"]
        if declared != expected:
            raise UpgradeImpactValidationError(
                f"release-note versions for {source} must exactly cover every release through "
                f"{target}: declared={declared}, expected={expected}"
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
    impact = _read_json(root / "internal/release/upgrade-impact.json")
    assessments = source_assessments(impact, require_semantic_evidence=True)
    retirements = retired_source_assessments(impact)
    policy = read_upgrade_policy(root)

    if impact["target_version"] != target:
        raise UpgradeImpactValidationError(
            f"upgrade-impact.json target {impact['target_version']} does not match version.txt {target}"
        )

    if previous_version == "0.0.0":
        if target != policy["initial_release_version"]:
            raise UpgradeImpactValidationError(
                f"first release target must be {policy['initial_release_version']}, got {target}"
            )
        if assessments or retirements:
            raise UpgradeImpactValidationError(
                "first release must not declare upgrade sources or retired sources"
            )
    else:
        required, protected = required_direct_sources(root, previous_version)
        retired = set(retirements)
        unknown_retirements = sorted(retired - required, key=version_key)
        if unknown_retirements:
            raise UpgradeImpactValidationError(
                "retired sources were not inherited or required: "
                + ", ".join(unknown_retirements)
            )
        protected_retirements = sorted(retired & protected, key=version_key)
        if protected_retirements:
            raise UpgradeImpactValidationError(
                "protected direct sources require a separate policy change before retirement: "
                + ", ".join(protected_retirements)
            )
        required -= retired
        omitted = sorted(required - set(assessments), key=version_key)
        if omitted:
            raise UpgradeImpactValidationError(
                "upgrade impact strands required direct sources: " + ", ".join(omitted)
            )
        still_declared = sorted(retired & set(assessments), key=version_key)
        if still_declared:
            raise UpgradeImpactValidationError(
                "retired sources must not also be declared as upgrade sources: "
                + ", ".join(still_declared)
            )

    try:
        changelog = (root / "CHANGELOG.md").read_text()
    except OSError as exc:
        raise UpgradeImpactValidationError(f"cannot read CHANGELOG.md: {exc}") from exc
    validate_release_note_coverage(changelog, target, assessments)

    if verify_managed_delta:
        for source, assessment in assessments.items():
            actual = managed_delta(root, source)
            declared = assessment["managed_changes"]
            for field in ("replaced", "created", "deleted"):
                if actual[field] != sorted(declared[field]):
                    raise UpgradeImpactValidationError(
                        f"managed {field} paths for {source} disagree with v{source}..HEAD: "
                        f"declared={sorted(declared[field])}, actual={actual[field]}"
                    )

    sources = sorted(assessments, key=version_key)
    return (
        f"reviewed upgrade impact valid for {target} ({derive_channel(target)}); "
        f"direct sources: {', '.join(sources) if sources else 'none'}"
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
