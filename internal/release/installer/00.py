from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

REPOSITORY = "phdah/ava"
PROTOCOL = 1
ASSETS = (
    "ava-install.sh",
    "ava-base.tar.gz",
    "ava-guidance.tar.gz",
    "ava-migrations.tar.gz",
    "ava-release.json",
    "ava-release-notes.md",
    "SHA256SUMS",
)
VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(alpha|beta|rc)\.([1-9][0-9]*))?$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


class AvaError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass
class Bundle:
    version: str
    tag: str
    directory: Path
    manifest: dict[str, Any]
    manifest_sha256: str
    base: Path
    guidance: Path
    migrations: Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_version(value: str) -> str:
    value = value.removeprefix("v")
    if not VERSION_RE.fullmatch(value):
        raise AvaError("INVALID_VERSION", f"invalid Ava version: {value}")
    return value


def derive_channel(version: str) -> str:
    match = VERSION_RE.fullmatch(version)
    assert match
    return match.group(4) or "stable"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, data: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent.is_symlink():
        raise AvaError("UNSAFE_PATH", f"parent is a symlink: {path.parent}")
    temp = path.parent / f".{path.name}.ava-tmp-{uuid.uuid4().hex}"
    try:
        with temp.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp, mode)
        os.replace(temp, path)
        try:
            directory_fd = os.open(path.parent, os.O_DIRECTORY)
        except (AttributeError, OSError):
            return
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temp.unlink(missing_ok=True)


def atomic_json(path: Path, value: Any) -> None:
    atomic_write(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


def safe_relative(value: str) -> str:
    if "\x00" in value or "\\" in value:
        raise AvaError("UNSAFE_PATH", f"unsafe relative path: {value}")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in ("", ".", "..") for part in path.parts):
        raise AvaError("UNSAFE_PATH", f"unsafe relative path: {value}")
    return path.as_posix()


def destination_relative(value: str) -> str:
    if "\x00" in value or "\\" in value or not value.startswith("/") or value == "/":
        raise AvaError("UNSAFE_PATH", f"unsafe installed path: {value}")
    path = PurePosixPath(value)
    if any(part in ("", ".", "..") for part in path.parts[1:]):
        raise AvaError("UNSAFE_PATH", f"unsafe installed path: {value}")
    return PurePosixPath(*path.parts[1:]).as_posix()


def safe_live_path(root: Path, destination: str, *, permit_missing: bool = True) -> Path:
    relative = destination_relative(destination)
    current = root
    for part in PurePosixPath(relative).parts:
        if current.exists() and current.is_symlink():
            raise AvaError("SYMLINK_ESCAPE", f"symlink in installed path: {current}")
        current = current / part
    if current.exists() and current.is_symlink():
        raise AvaError("SYMLINK_ESCAPE", f"installed path is a symlink: {destination}")
    ancestor = current
    while not ancestor.exists():
        parent = ancestor.parent
        if parent == ancestor:
            break
        ancestor = parent
    if ancestor.is_symlink():
        raise AvaError("SYMLINK_ESCAPE", f"symlink ancestor for installed path: {destination}")
    try:
        resolved_ancestor = ancestor.resolve(strict=True)
    except FileNotFoundError:
        resolved_ancestor = root
    if os.path.commonpath((str(root), str(resolved_ancestor))) != str(root):
        raise AvaError("PATH_ESCAPE", f"installed path escapes target root: {destination}")
    if not permit_missing and not current.exists():
        raise AvaError("MISSING_PATH", f"missing installed path: {destination}")
    return current


def remove_empty_parents(path: Path, stop: Path) -> None:
    parent = path.parent
    while parent != stop and parent != parent.parent:
        try:
            parent.rmdir()
        except OSError:
            return
        parent = parent.parent


def parse_checksums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9._-]+)", line)
        if not match:
            raise AvaError("INVALID_CHECKSUM_FILE", f"invalid SHA256SUMS line {line_number}")
        digest, name = match.groups()
        if name in checksums:
            raise AvaError("INVALID_CHECKSUM_FILE", f"duplicate checksum entry: {name}")
        checksums[name] = digest
    expected = set(ASSETS) - {"SHA256SUMS"}
    if set(checksums) != expected:
        raise AvaError("INVALID_CHECKSUM_FILE", f"checksum inventory mismatch: expected {sorted(expected)}")
    return checksums


def require_exact_keys(value: dict[str, Any], keys: set[str], context: str) -> None:
    if set(value) != keys:
        missing = sorted(keys - set(value))
        extra = sorted(set(value) - keys)
        raise AvaError("INVALID_MANIFEST", f"{context} fields mismatch, missing={missing}, extra={extra}")


