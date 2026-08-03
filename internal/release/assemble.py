#!/usr/bin/env python3
"""Build deterministic Ava GitHub Release assets from repository sources."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import tarfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Iterable

ASSET_NAMES = (
    "ava-install.sh",
    "ava-base.tar.gz",
    "ava-guidance.tar.gz",
    "ava-migrations.tar.gz",
    "ava-release.json",
    "ava-release-notes.md",
    "SHA256SUMS",
)
VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(alpha|beta|rc)\.([1-9][0-9]*))?$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class AssemblyError(RuntimeError):
    pass


@dataclass(frozen=True)
class Payload:
    archive_path: str
    destination: str
    ownership: str
    operation: str
    role: str
    data: bytes


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_version(value: str) -> str:
    value = value.removeprefix("v")
    if not VERSION_RE.fullmatch(value):
        raise AssemblyError(f"invalid Ava version: {value}")
    return value


def derive_channel(version: str) -> str:
    match = VERSION_RE.fullmatch(version)
    assert match
    return match.group(4) or "stable"


def safe_relative(path: str) -> str:
    candidate = PurePosixPath(path)
    if candidate.is_absolute() or not candidate.parts or any(part in ("", ".", "..") for part in candidate.parts):
        raise AssemblyError(f"unsafe relative path: {path}")
    return candidate.as_posix()


def iter_files(root: Path) -> Iterable[Path]:
    if not root.is_dir():
        return []
    return sorted((path for path in root.rglob("*") if path.is_file()), key=lambda p: p.relative_to(root).as_posix().encode())


def read_payloads(root: Path, host_bootstraps: list[str]) -> list[Payload]:
    base = root / "templates" / "base"
    scaffolds = root / "templates" / "project-scaffolds"
    if not base.is_dir():
        raise AssemblyError("missing templates/base")
    if not scaffolds.is_dir():
        raise AssemblyError("missing templates/project-scaffolds")

    result: list[Payload] = []
    for path in iter_files(base):
        rel = path.relative_to(base).as_posix()
        data = path.read_bytes()
        if rel == "AGENTS.md":
            result.append(Payload("base/AGENTS.md", "/AGENTS.md", "ava-managed", "replace-managed", "router", data))
        elif rel == "index.md" or rel.startswith(("roles/", "workflows/", "shared/")):
            result.append(Payload(f"base/{rel}", f"/.ava/base/{rel}", "ava-managed", "replace-managed", "base", data))
        elif rel.startswith(("knowledge/", "inbox/")):
            # These remain source-format examples, not release payload. The explicit
            # project-scaffold tree owns installed project paths.
            continue
        else:
            raise AssemblyError(f"unclassified templates/base source: {rel}")

    for path in iter_files(scaffolds):
        rel = path.relative_to(scaffolds).as_posix()
        result.append(Payload(f"scaffolds/{rel}", f"/{rel}", "project-owned", "create-if-absent", "scaffold", path.read_bytes()))

    seen_destinations = {item.destination for item in result}
    for mapping in host_bootstraps:
        if "=" not in mapping:
            raise AssemblyError("host bootstrap must use SOURCE=DESTINATION")
        source, destination = mapping.split("=", 1)
        source_rel = safe_relative(source)
        if not destination.startswith("/") or destination == "/" or ".." in PurePosixPath(destination).parts:
            raise AssemblyError(f"unsafe host bootstrap destination: {destination}")
        source_path = root / "templates" / "host-bootstraps" / source_rel
        if not source_path.is_file():
            raise AssemblyError(f"missing host bootstrap source: {source}")
        if destination in seen_destinations:
            raise AssemblyError(f"duplicate installed destination: {destination}")
        result.append(Payload(f"bootstraps/{source_rel}", destination, "ava-managed", "replace-managed", "bootstrap", source_path.read_bytes()))
        seen_destinations.add(destination)

    destinations = [item.destination for item in result]
    archive_paths = [item.archive_path for item in result]
    if len(destinations) != len(set(destinations)):
        raise AssemblyError("duplicate installed destination")
    if len(archive_paths) != len(set(archive_paths)):
        raise AssemblyError("duplicate archive path")
    return sorted(result, key=lambda item: item.archive_path.encode())


def asset_identity(name: str, role: str, version: str, channel: str, revision: str) -> bytes:
    return (json.dumps({
        "asset_schema": 1,
        "asset_name": name,
        "asset_role": role,
        "ava_version": version,
        "tag": f"v{version}",
        "channel": channel,
        "source_repository": "phdah/ava",
        "source_revision": revision,
    }, indent=2, sort_keys=True) + "\n").encode()


def write_reproducible_tar(path: Path, files: dict[str, bytes], epoch: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=epoch) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for name in sorted(files, key=lambda value: value.encode()):
                    safe_relative(name)
                    data = files[name]
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    info.mode = 0o644
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    info.mtime = epoch
                    archive.addfile(info, io.BytesIO(data))


def load_migrations(directory: Path | None, version: str) -> tuple[dict[str, bytes], list[dict]]:
    if directory is None:
        return {}, []
    descriptors: list[dict] = []
    files: dict[str, bytes] = {}
    descriptor_paths = set(directory.glob("*.json"))
    for file_path in iter_files(directory):
        if file_path in descriptor_paths:
            continue
        relative = file_path.relative_to(directory).as_posix()
        safe_relative(relative)
        files[relative] = file_path.read_bytes()
    for descriptor_path in sorted(descriptor_paths, key=lambda p: p.name.encode()):
        descriptor = json.loads(descriptor_path.read_text())
        required = {"id", "from", "to", "order", "depends_on", "apply_path", "verify_path", "idempotent"}
        if set(descriptor) != required:
            raise AssemblyError(f"invalid migration descriptor fields: {descriptor_path}")
        if descriptor["to"] != version or descriptor["idempotent"] is not True:
            raise AssemblyError(f"invalid migration target or idempotency: {descriptor_path}")
        for key in ("apply_path", "verify_path"):
            rel = safe_relative(descriptor[key])
            file_path = directory / rel
            if not file_path.is_file():
                raise AssemblyError(f"missing migration file: {rel}")
            files[rel] = file_path.read_bytes()
        descriptor_bytes = (json.dumps(descriptor, indent=2, sort_keys=True) + "\n").encode()
        descriptor_archive_path = f"descriptors/{descriptor['id']}.json"
        files[descriptor_archive_path] = descriptor_bytes
        descriptors.append({
            **descriptor,
            "descriptor_sha256": sha256_bytes(descriptor_bytes),
        })
    ids = [item["id"] for item in descriptors]
    if len(ids) != len(set(ids)):
        raise AssemblyError("duplicate migration id")
    return files, descriptors


def parse_upgrade_edges(values: list[str], migrations: list[dict], guidance_paths: list[str]) -> list[dict]:
    migration_by_from: dict[str, list[str]] = {}
    for migration in migrations:
        migration_by_from.setdefault(migration["from"], []).append(migration["id"])
    edges: list[dict] = []
    for value in values:
        # FROM or FROM:INTERMEDIATE,INTERMEDIATE
        source, separator, intermediates_raw = value.partition(":")
        source = canonical_version(source)
        intermediates = [canonical_version(item) for item in intermediates_raw.split(",") if item] if separator else []
        edges.append({
            "from": source,
            "to": "__TARGET__",
            "mode": "chained" if intermediates else "direct",
            "intermediates": intermediates,
            "carry_unresolved_semantic_state": False,
            "migration_ids": sorted(migration_by_from.get(source, [])),
            "guidance_paths": guidance_paths,
        })
    return edges


def build(args: argparse.Namespace) -> None:
    root = args.root.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    version = canonical_version(args.version)
    channel = derive_channel(version)
    if args.channel and args.channel != channel:
        raise AssemblyError(f"channel {args.channel} does not match version {version}")
    if not SHA_RE.fullmatch(args.source_revision):
        raise AssemblyError("source revision must be a full 40-character lowercase Git SHA")
    epoch = args.source_date_epoch
    published_at = args.published_at or datetime.fromtimestamp(epoch, timezone.utc).isoformat().replace("+00:00", "Z")

    payloads = read_payloads(root, args.host_bootstrap)
    base_files = {"ava-asset.json": asset_identity("ava-base.tar.gz", "base", version, channel, args.source_revision)}
    for payload in payloads:
        base_files[payload.archive_path] = payload.data
    write_reproducible_tar(output / "ava-base.tar.gz", base_files, epoch)

    guidance_files: dict[str, bytes] = {
        "ava-asset.json": asset_identity("ava-guidance.tar.gz", "guidance", version, channel, args.source_revision)
    }
    guidance_entries: list[dict] = []
    if args.guidance_dir:
        for path in iter_files(args.guidance_dir):
            rel = path.relative_to(args.guidance_dir).as_posix()
            safe_relative(rel)
            data = path.read_bytes()
            guidance_files[rel] = data
            guidance_entries.append({"path": rel, "sha256": sha256_bytes(data)})
    write_reproducible_tar(output / "ava-guidance.tar.gz", guidance_files, epoch)

    migration_files, migration_steps = load_migrations(args.migrations_dir, version)
    migration_archive = {
        "ava-asset.json": asset_identity("ava-migrations.tar.gz", "migrations", version, channel, args.source_revision),
        **migration_files,
    }
    write_reproducible_tar(output / "ava-migrations.tar.gz", migration_archive, epoch)

    installer_source = (root / "internal" / "release" / "ava-install.sh").read_text()
    installer_fragments = root / "internal" / "release" / "installer"
    fragments = [path.read_text() for path in sorted(installer_fragments.glob("*.py"), key=lambda path: path.name)]
    if not fragments:
        raise AssemblyError("missing installer Python source fragments")
    installer_source = installer_source.replace("@AVA_INSTALLER_PYTHON@", "".join(fragments).rstrip())
    replacements = {
        "@AVA_VERSION@": version,
        "@AVA_TAG@": f"v{version}",
        "@AVA_CHANNEL@": channel,
        "@AVA_SOURCE_REVISION@": args.source_revision,
    }
    for old, new in replacements.items():
        installer_source = installer_source.replace(old, new)
    if "@AVA_" in installer_source:
        raise AssemblyError("unresolved installer identity placeholder")
    (output / "ava-install.sh").write_text(installer_source)
    os.chmod(output / "ava-install.sh", 0o755)

    if args.release_notes:
        notes_body = args.release_notes.read_text()
    else:
        notes_body = "No additional release notes were supplied."
    release_notes = (
        "---\n"
        f"ava_version: \"{version}\"\n"
        f"tag: \"v{version}\"\n"
        f"channel: \"{channel}\"\n"
        f"source_revision: \"{args.source_revision}\"\n"
        f"semantic_review_required: {str(args.semantic_review_required).lower()}\n"
        "---\n\n"
        f"# Ava {version}\n\n{notes_body.rstrip()}\n"
    )
    (output / "ava-release-notes.md").write_text(release_notes)

    guidance_paths = [item["path"] for item in guidance_entries]
    edges = parse_upgrade_edges(args.upgrade_from, migration_steps, guidance_paths)
    for edge in edges:
        edge["to"] = version

    installed_files = [{
        "source_asset": "ava-base.tar.gz",
        "source_path": payload.archive_path,
        "destination": payload.destination,
        "ownership": payload.ownership,
        "operation": payload.operation,
        "role": payload.role,
        "sha256": sha256_bytes(payload.data),
    } for payload in payloads]

    def hashed_asset(name: str, role: str, media_type: str) -> dict:
        path = output / name
        return {
            "name": name,
            "role": role,
            "media_type": media_type,
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        }

    release_manifest = {
        "release_schema": 1,
        "ava_version": version,
        "tag": f"v{version}",
        "channel": channel,
        "source_repository": "phdah/ava",
        "source_revision": args.source_revision,
        "published_at": published_at,
        "installer_protocol": 1,
        "okf_version": "0.2",
        "manifest_schema": 1,
        "semantic_review_required": args.semantic_review_required,
        "assets": [
            hashed_asset("ava-install.sh", "installer", "text/x-shellscript"),
            hashed_asset("ava-base.tar.gz", "base", "application/gzip"),
            hashed_asset("ava-guidance.tar.gz", "guidance", "application/gzip"),
            hashed_asset("ava-migrations.tar.gz", "migrations", "application/gzip"),
            {"name": "ava-release.json", "role": "release-manifest", "media_type": "application/json"},
            hashed_asset("ava-release-notes.md", "release-notes", "text/markdown"),
            {"name": "SHA256SUMS", "role": "checksums", "media_type": "text/plain"},
        ],
        "installed_files": installed_files,
        "upgrade_paths": {"edges": edges},
        "guidance": {"entries": guidance_entries},
        "migrations": {
            "files": [{"path": path, "sha256": sha256_bytes(data)} for path, data in sorted(migration_files.items())],
            "steps": migration_steps,
        },
    }
    release_bytes = (json.dumps(release_manifest, indent=2, sort_keys=True) + "\n").encode()
    (output / "ava-release.json").write_bytes(release_bytes)

    checksum_lines = []
    for name in ASSET_NAMES[:-1]:
        checksum_lines.append(f"{sha256_file(output / name)}  {name}\n")
    (output / "SHA256SUMS").write_text("".join(checksum_lines))

    generated = set(ASSET_NAMES)
    actual = {path.name for path in output.iterdir() if path.is_file()}
    if actual != generated:
        raise AssemblyError(f"unexpected output files: {sorted(actual ^ generated)}")
    print(f"Built Ava release v{version} in {output}")


def parse_args() -> argparse.Namespace:
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
    parser.add_argument("--host-bootstrap", action="append", default=[])
    parser.add_argument("--semantic-review-required", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        build(parse_args())
    except (AssemblyError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
