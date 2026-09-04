#!/usr/bin/env python3
"""Durable release-publication identity and retry planning."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(alpha|beta|rc)\.([1-9][0-9]*))?$"
)


class PublicationError(ValueError):
    pass


@dataclass(frozen=True)
class PublicationIdentity:
    version: str
    tag: str
    source_revision: str
    previous_revision: str
    previous_version: str
    channel: str
    source_date_epoch: str
    published_at: str


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise PublicationError(
            f"git {' '.join(args)} failed: {result.stderr.strip()}"
        )
    return result


def _version(value: str, *, label: str) -> str:
    value = value.strip()
    if VERSION_RE.fullmatch(value) is None:
        raise PublicationError(f"{label} is not a canonical Ava version: {value!r}")
    return value


def derive_channel(version: str) -> str:
    match = VERSION_RE.fullmatch(version)
    if match is None:
        raise PublicationError(f"invalid Ava version: {version!r}")
    return match.group(4) or "stable"


def _published_at(source_date_epoch: str) -> str:
    return (
        datetime.fromtimestamp(int(source_date_epoch), timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def resolve_identity(
    root: Path,
    *,
    requested_tag: str | None = None,
) -> PublicationIdentity | None:
    root = root.resolve()
    head = _git(root, "rev-parse", "HEAD").stdout.strip()
    version = _version(
        (root / "version.txt").read_text(encoding="utf-8"),
        label="version.txt",
    )
    expected_tag = f"v{version}"
    tag = requested_tag.strip() if requested_tag else expected_tag

    if tag != expected_tag:
        raise PublicationError(
            f"requested release tag {tag!r} does not match checked-out version "
            f"{expected_tag!r}"
        )

    tag_ref = _git(root, "rev-parse", "--verify", f"refs/tags/{tag}", check=False)
    if tag_ref.returncode != 0:
        if requested_tag:
            raise PublicationError(f"requested release tag does not exist: {tag}")
        return None

    source_revision = _git(root, "rev-list", "-n", "1", tag).stdout.strip()
    if source_revision != head:
        if requested_tag:
            raise PublicationError(
                f"requested release tag {tag} points to {source_revision}, "
                f"but the checked-out revision is {head}"
            )
        return None

    previous_revision = _git(root, "rev-parse", "HEAD^").stdout.strip()
    previous_version = _version(
        _git(root, "show", f"{previous_revision}:version.txt").stdout,
        label=f"{previous_revision}:version.txt",
    )
    source_date_epoch = _git(
        root,
        "show",
        "-s",
        "--format=%ct",
        source_revision,
    ).stdout.strip()

    return PublicationIdentity(
        version=version,
        tag=tag,
        source_revision=source_revision,
        previous_revision=previous_revision,
        previous_version=previous_version,
        channel=derive_channel(version),
        source_date_epoch=source_date_epoch,
        published_at=_published_at(source_date_epoch),
    )


def extract_release_notes(changelog: str, version: str) -> str:
    marker = re.compile(rf"^## \[{re.escape(version)}\].*$", re.MULTILINE)
    match = marker.search(changelog)
    if match is None:
        raise PublicationError(f"CHANGELOG.md has no release section for {version}")
    next_match = re.search(r"^## \[", changelog[match.end():], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(changelog)
    return changelog[match.start():end].rstrip() + "\n"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def _release_assets(release: dict[str, Any]) -> dict[str, dict[str, Any]]:
    assets = release.get("assets")
    if not isinstance(assets, list):
        raise PublicationError("GitHub Release assets must be an array")
    result: dict[str, dict[str, Any]] = {}
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get("name"), str):
            raise PublicationError("GitHub Release contains an invalid asset record")
        name = asset["name"]
        if name in result:
            raise PublicationError(f"GitHub Release contains duplicate asset {name!r}")
        result[name] = asset
    return result


def _release_id(release: dict[str, Any]) -> int:
    release_id = release.get("id")
    if not isinstance(release_id, int) or release_id <= 0:
        raise PublicationError("GitHub Release id must be a positive integer")
    return release_id


def plan_assets(
    release_dir: Path,
    release: dict[str, Any] | None,
    *,
    identity: PublicationIdentity,
    expected_body: str,
) -> tuple[str, list[Path], bool]:
    release_dir = release_dir.resolve()
    expected_paths = sorted(path for path in release_dir.iterdir() if path.is_file())
    if not expected_paths:
        raise PublicationError(f"release directory is empty: {release_dir}")
    expected = {path.name: path for path in expected_paths}

    if release is None:
        return "missing", expected_paths, False

    checks = {
        "tag_name": identity.tag,
        "name": identity.tag,
        "target_commitish": identity.source_revision,
        "prerelease": identity.channel != "stable",
    }
    for field, expected_value in checks.items():
        if release.get(field) != expected_value:
            raise PublicationError(
                f"GitHub Release {field} mismatch: "
                f"{release.get(field)!r} != {expected_value!r}"
            )
    body = release.get("body")
    if not isinstance(body, str) or body.rstrip() != expected_body.rstrip():
        raise PublicationError(
            "GitHub Release notes do not match the target CHANGELOG section"
        )

    remote = _release_assets(release)
    unexpected = sorted(set(remote) - set(expected))
    if unexpected:
        raise PublicationError(
            "GitHub Release contains unexpected assets: " + ", ".join(unexpected)
        )

    missing: list[Path] = []
    for name, path in expected.items():
        asset = remote.get(name)
        if asset is None:
            missing.append(path)
            continue
        expected_digest = _sha256(path)
        if asset.get("digest") != expected_digest:
            raise PublicationError(
                f"GitHub Release asset digest mismatch for {name}: "
                f"{asset.get('digest')!r} != {expected_digest!r}"
            )

    draft = release.get("draft")
    if not isinstance(draft, bool):
        raise PublicationError("GitHub Release draft state is invalid")
    if not draft and missing:
        raise PublicationError(
            "published GitHub Release is missing expected assets: "
            + ", ".join(path.name for path in missing)
        )
    return (
        "draft" if draft else "published",
        missing,
        not draft and not missing,
    )


def select_release(
    release_dir: Path,
    releases: list[dict[str, Any]],
    *,
    identity: PublicationIdentity,
    expected_body: str,
) -> tuple[dict[str, Any] | None, str, list[int]]:
    """Select one exact release and identify only safe redundant draft duplicates."""

    matches = [release for release in releases if release.get("tag_name") == identity.tag]
    if not matches:
        return None, "missing", []

    candidates: list[tuple[dict[str, Any], int, str, int]] = []
    for release in matches:
        release_id = _release_id(release)
        state, missing, _complete = plan_assets(
            release_dir,
            release,
            identity=identity,
            expected_body=expected_body,
        )
        candidates.append((release, release_id, state, len(missing)))

    published = [candidate for candidate in candidates if candidate[2] == "published"]
    if published:
        if len(candidates) != 1:
            raise PublicationError(
                f"multiple GitHub Releases reference {identity.tag}; "
                "published state is never deduplicated automatically"
            )
        release, _release_id_value, state, _missing_count = published[0]
        return release, state, []

    # All matching releases are exact, compatible drafts at this point. Preserve the
    # most complete draft; on a tie preserve the oldest release id. Redundant drafts
    # can then be deleted without discarding any unique or mismatched release state.
    selected = min(candidates, key=lambda candidate: (candidate[3], candidate[1]))
    release, selected_id, state, _missing_count = selected
    redundant_ids = sorted(
        candidate[1] for candidate in candidates if candidate[1] != selected_id
    )
    return release, state, redundant_ids


def stage_missing_assets(paths: list[Path], upload_dir: Path) -> None:
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
    upload_dir.mkdir(parents=True)
    for path in paths:
        shutil.copy2(path, upload_dir / path.name)


def _write_outputs(values: dict[str, str]) -> None:
    import os

    path_value = os.environ.get("GITHUB_OUTPUT")
    if not path_value:
        return
    with Path(path_value).open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            if "\n" in value:
                raise PublicationError(f"workflow output {key} must be single-line")
            handle.write(f"{key}={value}\n")


def _identity_from_args(args: argparse.Namespace) -> PublicationIdentity:
    return PublicationIdentity(
        version=_version(args.version, label="--version"),
        tag=args.tag,
        source_revision=args.source_revision,
        previous_revision=args.previous_revision,
        previous_version=_version(
            args.previous_version,
            label="--previous-version",
        ),
        channel=derive_channel(args.version),
        source_date_epoch=args.source_date_epoch,
        published_at=args.published_at,
    )


def _release_records(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise PublicationError("GitHub Releases JSON must contain an array")
    if all(isinstance(item, dict) for item in value):
        return list(value)

    releases: list[dict[str, Any]] = []
    for page in value:
        if not isinstance(page, list):
            raise PublicationError("paginated GitHub Releases JSON is invalid")
        for release in page:
            if not isinstance(release, dict):
                raise PublicationError("GitHub Releases JSON contains an invalid record")
            releases.append(release)
    return releases


def _identity_command(args: argparse.Namespace) -> int:
    identity = resolve_identity(args.root, requested_tag=args.tag or None)
    if identity is None:
        _write_outputs({"eligible": "false"})
        print("no release tag targets the checked-out revision")
        return 0
    values = {
        "eligible": "true",
        "version": identity.version,
        "tag": identity.tag,
        "source_revision": identity.source_revision,
        "previous_revision": identity.previous_revision,
        "previous_version": identity.previous_version,
        "channel": identity.channel,
        "source_date_epoch": identity.source_date_epoch,
        "published_at": identity.published_at,
    }
    _write_outputs(values)
    print(
        f"durable publication identity: {identity.previous_version} -> "
        f"{identity.version} ({identity.tag} @ {identity.source_revision})"
    )
    return 0


def _notes_command(args: argparse.Namespace) -> int:
    version = _version(args.version, label="--version")
    notes = extract_release_notes(
        args.changelog.read_text(encoding="utf-8"),
        version,
    )
    args.output.write_text(notes, encoding="utf-8")
    print(f"wrote release notes for {version}: {args.output}")
    return 0


def _select_command(args: argparse.Namespace) -> int:
    identity = _identity_from_args(args)
    releases = _release_records(
        json.loads(args.releases_json.read_text(encoding="utf-8"))
    )
    expected_body = args.notes.read_text(encoding="utf-8")
    selected, state, redundant_ids = select_release(
        args.release_dir,
        releases,
        identity=identity,
        expected_body=expected_body,
    )

    args.redundant_ids.write_text(
        "".join(f"{release_id}\n" for release_id in redundant_ids),
        encoding="utf-8",
    )
    if selected is None:
        args.selected_json.unlink(missing_ok=True)
        release_id = ""
    else:
        release_id = str(_release_id(selected))
        args.selected_json.write_text(
            json.dumps(selected, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    _write_outputs(
        {
            "release_state": state,
            "release_id": release_id,
            "redundant_count": str(len(redundant_ids)),
        }
    )
    print(
        f"selected release state: {state}; redundant compatible drafts: "
        f"{len(redundant_ids)}"
    )
    return 0


def _plan_command(args: argparse.Namespace) -> int:
    identity = _identity_from_args(args)
    release = None
    if args.release_json and args.release_json.exists():
        value = json.loads(args.release_json.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise PublicationError("GitHub Release JSON must contain an object")
        release = value
    expected_body = args.notes.read_text(encoding="utf-8")
    state, missing, complete = plan_assets(
        args.release_dir,
        release,
        identity=identity,
        expected_body=expected_body,
    )
    stage_missing_assets(missing, args.upload_dir)
    _write_outputs(
        {
            "release_state": state,
            "missing_count": str(len(missing)),
            "complete": "true" if complete else "false",
        }
    )
    print(
        f"release state: {state}; assets to upload: {len(missing)}"
    )
    return 0


def _add_identity_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--version", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--previous-revision", required=True)
    parser.add_argument("--previous-version", required=True)
    parser.add_argument("--source-date-epoch", required=True)
    parser.add_argument("--published-at", required=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    identity = subparsers.add_parser("identity")
    identity.add_argument("--tag", default="")

    notes = subparsers.add_parser("notes")
    notes.add_argument("--version", required=True)
    notes.add_argument("--changelog", type=Path, default=Path("CHANGELOG.md"))
    notes.add_argument("--output", type=Path, required=True)

    select = subparsers.add_parser("select")
    select.add_argument("--release-dir", type=Path, required=True)
    select.add_argument("--releases-json", type=Path, required=True)
    select.add_argument("--selected-json", type=Path, required=True)
    select.add_argument("--redundant-ids", type=Path, required=True)
    select.add_argument("--notes", type=Path, required=True)
    _add_identity_arguments(select)

    plan = subparsers.add_parser("plan")
    plan.add_argument("--release-dir", type=Path, required=True)
    plan.add_argument("--release-json", type=Path)
    plan.add_argument("--upload-dir", type=Path, required=True)
    plan.add_argument("--notes", type=Path, required=True)
    _add_identity_arguments(plan)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "identity":
            return _identity_command(args)
        if args.command == "notes":
            return _notes_command(args)
        if args.command == "select":
            return _select_command(args)
        return _plan_command(args)
    except (OSError, json.JSONDecodeError, PublicationError) as exc:
        print(f"release publication invalid: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
