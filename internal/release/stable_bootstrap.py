#!/usr/bin/env python3
"""One-time stable bootstrap support for the alpha.19 -> 1.0.0 cutover."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "internal/release/stable-bootstrap.json"
INVENTORY_PATH = ROOT / "internal/release/history/alpha-reset-inventory.json"
EXPECTED_ASSETS = {
    "SHA256SUMS",
    "ava-base.tar.gz",
    "ava-guidance.tar.gz",
    "ava-install.sh",
    "ava-migrations.tar.gz",
    "ava-release-notes.md",
    "ava-release.json",
}


class StableBootstrapError(RuntimeError):
    pass


def _json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StableBootstrapError(f"cannot read {path}: {exc}") from exc


def _run(args: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise StableBootstrapError(
            f"command failed ({result.returncode}): {' '.join(args)}\n{result.stderr.strip()}"
        )
    return result.stdout.strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_bootstrap(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    config_path = root / "internal/release/stable-bootstrap.json"
    config = _json(config_path)
    required = {
        "alpha_reset_requested",
        "enabled",
        "schema_version",
        "source_evidence_path",
        "source_revision",
        "source_tag",
        "source_version",
        "target_version",
    }
    if not isinstance(config, dict) or set(config) != required or config.get("schema_version") != 1:
        raise StableBootstrapError(f"{config_path} has invalid schema")
    if config.get("enabled") is not True:
        raise StableBootstrapError("stable bootstrap is disabled")
    if config.get("source_version") != "1.0.0-alpha.19" or config.get("target_version") != "1.0.0":
        raise StableBootstrapError("stable bootstrap is not bounded to alpha.19 -> 1.0.0")
    if config.get("source_tag") != "v1.0.0-alpha.19":
        raise StableBootstrapError("stable bootstrap source tag is not exact alpha.19")
    evidence_path = root / config["source_evidence_path"]
    evidence = _json(evidence_path)
    published = evidence.get("published_final_alpha") if isinstance(evidence, dict) else None
    if not isinstance(published, dict):
        raise StableBootstrapError("final-alpha evidence is missing published identity")
    if published.get("version") != config["source_version"]:
        raise StableBootstrapError("bootstrap source version disagrees with final-alpha evidence")
    if published.get("tag") != config["source_tag"]:
        raise StableBootstrapError("bootstrap source tag disagrees with final-alpha evidence")
    if published.get("tag_revision") != config["source_revision"]:
        raise StableBootstrapError("bootstrap source revision disagrees with final-alpha evidence")
    digests = published.get("asset_sha256")
    if not isinstance(digests, dict) or set(digests) != EXPECTED_ASSETS:
        raise StableBootstrapError("final-alpha evidence has an invalid asset inventory")
    return config, evidence


def reconstruct_source_assets(root: Path, output: Path) -> None:
    config, evidence = load_bootstrap(root)
    published = evidence["published_final_alpha"]
    expected = published["asset_sha256"]
    output = output.resolve()
    if output.exists() and any(output.iterdir()):
        raise StableBootstrapError(f"source asset output must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    source_revision = config["source_revision"]
    _run(["git", "-C", str(root), "cat-file", "-e", f"{source_revision}^{{commit}}"])
    epoch = _run(["git", "-C", str(root), "show", "-s", "--format=%ct", source_revision])
    published_at = (
        datetime.fromtimestamp(int(epoch), timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    temp_parent = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir()))
    with tempfile.TemporaryDirectory(prefix="ava-stable-bootstrap-", dir=temp_parent) as temp:
        temp_root = Path(temp)
        worktree = temp_root / "source"
        assembled = temp_root / "assets"
        _run(["git", "-C", str(root), "worktree", "add", "--detach", str(worktree), source_revision])
        try:
            env = os.environ.copy()
            env["AVA_UPGRADE_CATALOG"] = str(
                worktree / f"internal/release/catalogs/{config['source_version']}.json"
            )
            _run(
                [
                    str(worktree / "internal/release/assemble.sh"),
                    "--output",
                    str(assembled),
                    "--version",
                    config["source_version"],
                    "--channel",
                    "alpha",
                    "--source-revision",
                    source_revision,
                    "--source-date-epoch",
                    epoch,
                    "--published-at",
                    published_at,
                    "--release-notes",
                    str(worktree / "CHANGELOG.md"),
                ],
                cwd=worktree,
                env=env,
            )
            actual_names = {path.name for path in assembled.iterdir() if path.is_file()}
            if actual_names != EXPECTED_ASSETS:
                raise StableBootstrapError(
                    f"reconstructed alpha.19 assets differ in shape: {sorted(actual_names)}"
                )
            for name in sorted(EXPECTED_ASSETS):
                digest = _sha256(assembled / name)
                if digest != expected[name]:
                    raise StableBootstrapError(
                        f"reconstructed alpha.19 digest mismatch for {name}: {digest} != {expected[name]}"
                    )
                shutil.copy2(assembled / name, output / name)
        finally:
            _run(["git", "-C", str(root), "worktree", "remove", "--force", str(worktree)])

    print(f"reconstructed verified final-alpha source assets: {output}")


def _flatten_pages(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise StableBootstrapError("GitHub API payload must be an array")
    if all(isinstance(item, dict) for item in value):
        return list(value)
    records: list[dict[str, Any]] = []
    for page in value:
        if not isinstance(page, list):
            raise StableBootstrapError("GitHub API paginated payload is invalid")
        if not all(isinstance(item, dict) for item in page):
            raise StableBootstrapError("GitHub API payload contains a non-object record")
        records.extend(page)
    return records


def verify_alpha_reset(root: Path, releases_json: Path, refs_json: Path) -> None:
    config, _ = load_bootstrap(root)
    if config.get("alpha_reset_requested") is not True:
        raise StableBootstrapError("alpha reset was not explicitly requested in bootstrap state")
    inventory = _json(root / "internal/release/history/alpha-reset-inventory.json")
    expected_releases = inventory.get("release_objects")
    expected_refs = inventory.get("tag_refs")
    if not isinstance(expected_releases, list) or not isinstance(expected_refs, list):
        raise StableBootstrapError("alpha reset inventory is invalid")

    live_releases = _flatten_pages(_json(releases_json))
    if len(live_releases) != len(expected_releases):
        raise StableBootstrapError(
            f"release inventory changed: expected {len(expected_releases)}, found {len(live_releases)}"
        )
    expected_release_map = {item["release_id"]: item for item in expected_releases}
    live_release_map = {item.get("id"): item for item in live_releases}
    if set(live_release_map) != set(expected_release_map):
        raise StableBootstrapError("GitHub Release ids no longer match the frozen alpha inventory")
    for release_id, expected in expected_release_map.items():
        live = live_release_map[release_id]
        checks = {
            "tag_name": expected["tag_name"],
            "target_commitish": expected["target_commitish"],
            "draft": expected["draft"],
            "prerelease": expected["prerelease"],
            "immutable": expected["immutable"],
        }
        for field, value in checks.items():
            if live.get(field) != value:
                raise StableBootstrapError(
                    f"GitHub Release {release_id} field {field} changed: {live.get(field)!r} != {value!r}"
                )

    live_refs = _flatten_pages(_json(refs_json))
    expected_ref_map = {item["ref"]: item["revision"] for item in expected_refs}
    live_ref_map = {
        item.get("ref"): (item.get("object") or {}).get("sha")
        for item in live_refs
    }
    if live_ref_map != expected_ref_map:
        raise StableBootstrapError("alpha tag refs no longer match the frozen inventory")
    print(
        f"alpha reset inventory verified: {len(live_releases)} releases, {len(live_refs)} tags"
    )


def verify_alpha_empty(releases_json: Path, refs_json: Path) -> None:
    releases = _flatten_pages(_json(releases_json))
    refs = _flatten_pages(_json(refs_json))
    alpha_releases = [item for item in releases if str(item.get("tag_name", "")).startswith("v1.0.0-alpha.")]
    alpha_refs = [item for item in refs if str(item.get("ref", "")).startswith("refs/tags/v1.0.0-alpha.")]
    if alpha_releases or alpha_refs:
        raise StableBootstrapError(
            f"alpha reset incomplete: {len(alpha_releases)} releases, {len(alpha_refs)} tags remain"
        )
    print("alpha public history reset verified: no alpha Releases or tags remain")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    source = sub.add_parser("source-assets")
    source.add_argument("--output", type=Path, required=True)
    verify = sub.add_parser("verify-alpha-reset")
    verify.add_argument("--releases-json", type=Path, required=True)
    verify.add_argument("--refs-json", type=Path, required=True)
    empty = sub.add_parser("verify-alpha-empty")
    empty.add_argument("--releases-json", type=Path, required=True)
    empty.add_argument("--refs-json", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "source-assets":
            reconstruct_source_assets(args.root.resolve(), args.output)
        elif args.command == "verify-alpha-reset":
            verify_alpha_reset(args.root.resolve(), args.releases_json, args.refs_json)
        elif args.command == "verify-alpha-empty":
            verify_alpha_empty(args.releases_json, args.refs_json)
        else:
            raise StableBootstrapError(f"unsupported command: {args.command}")
    except StableBootstrapError as exc:
        print(f"stable bootstrap invalid: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
