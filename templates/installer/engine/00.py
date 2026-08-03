from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import uuid
from dataclasses import dataclass
from typing import Any

ASSETS = pathlib.Path(sys.argv[1])
TARGET = pathlib.Path(sys.argv[2])
DRY_RUN = sys.argv[3] == '1'
ADOPT_AGENTS = sys.argv[4] == '1'
BOOTSTRAP = sys.argv[5].lstrip('/')
EXPECTED = {
    'ava_version': os.environ['AVA_VERSION'],
    'tag': os.environ['AVA_TAG'],
    'channel': os.environ['AVA_CHANNEL'],
    'source_revision': os.environ['AVA_SOURCE_REVISION'],
    'source_repository': os.environ['AVA_REPOSITORY'],
}
RELEASE_SHA = os.environ['RELEASE_SHA']


class AvaError(Exception):
    def __init__(self, code: str, message: str, *, stage: str = 'preflight', path: str | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.stage = stage
        self.path = path


def fail(code: str, message: str, *, stage: str = 'preflight', path: str | None = None) -> None:
    raise AvaError(code, message, stage=stage, path=path)


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f'.{path.name}.tmp-{os.getpid()}')
    with temp.open('w', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def rel_path(value: str, *, field: str) -> pathlib.PurePosixPath:
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or not value or '\\' in value or any(part in ('', '.', '..') for part in path.parts):
        fail('UNSAFE_PATH', f'unsafe {field}: {value}', path=value)
    return path


def destination(value: str) -> pathlib.PurePosixPath:
    if not value.startswith('/') or '\\' in value:
        fail('UNSAFE_PATH', f'destination must be an absolute POSIX path: {value}', path=value)
    path = pathlib.PurePosixPath(value[1:])
    if not path.parts or any(part in ('', '.', '..') for part in path.parts):
        fail('UNSAFE_PATH', f'unsafe destination: {value}', path=value)
    return path


def target_path(relative: pathlib.PurePosixPath) -> pathlib.Path:
    candidate = TARGET.joinpath(*relative.parts)
    current = TARGET
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            fail('SYMLINK_PATH', 'managed path traverses a symlink', path='/' + str(relative))
    if candidate.is_symlink():
        fail('SYMLINK_PATH', 'managed destination is a symlink', path='/' + str(relative))
    try:
        resolved_parent = candidate.parent.resolve(strict=False)
        root = TARGET.resolve(strict=False)
        resolved_parent.relative_to(root)
    except ValueError:
        fail('PATH_ESCAPE', 'destination resolves outside target root', path='/' + str(relative))
    return candidate


def load_json(path: pathlib.Path, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(code, f'cannot read valid JSON from {path.name}: {exc}')
    if not isinstance(value, dict):
        fail(code, f'{path.name} must contain a JSON object')
    return value


def validate_archive(path: pathlib.Path, expected_name: str, workspace: pathlib.Path) -> pathlib.Path:
    extract_root = workspace / expected_name.removesuffix('.tar.gz')
    extract_root.mkdir(parents=True)
    try:
        with tarfile.open(path, 'r:gz') as archive:
            seen: set[str] = set()
            for member in archive.getmembers():
                normalized = rel_path(member.name.rstrip('/'), field='archive entry')
                name = str(normalized)
                if name in seen:
                    fail('UNSAFE_ARCHIVE', f'duplicate archive entry: {name}')
                seen.add(name)
                if member.issym() or member.islnk() or member.isdev() or member.isfifo():
                    fail('UNSAFE_ARCHIVE', f'unsupported archive entry type: {name}')
                if not (member.isfile() or member.isdir()):
                    fail('UNSAFE_ARCHIVE', f'unsupported archive entry type: {name}')
            for member in archive.getmembers():
                destination = extract_root / rel_path(member.name.rstrip('/'), field='archive entry')
                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    fail('UNSAFE_ARCHIVE', f'cannot read archive entry: {member.name}')
                with source, destination.open('xb') as output:
                    shutil.copyfileobj(source, output)
                destination.chmod(member.mode & 0o777)
    except (tarfile.TarError, OSError) as exc:
        fail('INVALID_ARCHIVE', f'cannot validate {expected_name}: {exc}')
    identity = load_json(extract_root / 'ava-asset.json', 'INVALID_ASSET_IDENTITY')
    if identity.get('asset_name') != expected_name:
        fail('ASSET_IDENTITY_MISMATCH', f'{expected_name} contains identity for {identity.get("asset_name")}')
    for key, expected in EXPECTED.items():
        if identity.get(key) != expected:
            fail('ASSET_IDENTITY_MISMATCH', f'{expected_name} {key} differs from installer identity')
    return extract_root


@dataclass
class Change:
    path: str
    operation: str
