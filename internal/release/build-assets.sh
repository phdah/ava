#!/bin/sh

set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
exec python3 - "$ROOT" "$@" <<'PY'
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys
import tarfile
from typing import Any, Iterable

ROOT = pathlib.Path(sys.argv[1]).resolve()


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description='Build deterministic Ava release assets.')
    value.add_argument('--version', required=True, help='Canonical version without a leading v.')
    value.add_argument('--source-revision', help='Full source commit SHA. Defaults to git HEAD.')
    value.add_argument('--published-at', help='UTC RFC 3339 timestamp. Defaults to current time.')
    value.add_argument('--source-date-epoch', type=int, help='Normalized archive mtime. Defaults to source commit time.')
    value.add_argument('--output', default='dist', help='Output directory relative to the repository root.')
    value.add_argument('--release-notes', help='Optional Markdown release notes source.')
    value.add_argument('--upgrade-from', action='append', default=[], help='Declare a direct supported source version. Repeatable.')
    value.add_argument('--semantic-review-required', action='store_true')
    return value


args = parser().parse_args(sys.argv[2:])
version_pattern = re.compile(r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(alpha|beta|rc)\.([1-9][0-9]*))?$')
if not version_pattern.fullmatch(args.version):
    raise SystemExit(f'ERROR: invalid canonical Ava version: {args.version}')
match = version_pattern.fullmatch(args.version)
assert match
channel = match.group(4) or 'stable'
tag = 'v' + args.version


def git(*arguments: str) -> str:
    return subprocess.check_output(['git', '-C', str(ROOT), *arguments], text=True).strip()


source_revision = args.source_revision or git('rev-parse', 'HEAD')
if not re.fullmatch(r'[0-9a-f]{40}', source_revision):
    raise SystemExit('ERROR: --source-revision must be a full lowercase commit SHA')
source_date_epoch = args.source_date_epoch
if source_date_epoch is None:
    source_date_epoch = int(git('show', '-s', '--format=%ct', source_revision))
published_at = args.published_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', published_at):
    raise SystemExit('ERROR: --published-at must be UTC RFC 3339 without fractional seconds')

for source in args.upgrade_from:
    if not version_pattern.fullmatch(source):
        raise SystemExit(f'ERROR: invalid --upgrade-from version: {source}')
    if source == args.version:
        raise SystemExit('ERROR: --upgrade-from must differ from the target version')

output = pathlib.Path(args.output)
if not output.is_absolute():
    output = ROOT / output
output = output.resolve()
try:
    output.relative_to(ROOT)
except ValueError:
    raise SystemExit('ERROR: output directory must be inside the repository root')
if output.exists() and any(output.iterdir()):
    raise SystemExit(f'ERROR: output directory is not empty: {output}')
output.mkdir(parents=True, exist_ok=True)

required = [
    ROOT / 'templates/installer/ava-install.sh',
    ROOT / 'templates/installer/engine',
    ROOT / 'templates/base/AGENTS.md',
    ROOT / 'templates/base/base-index.md',
    ROOT / 'templates/base/roles',
    ROOT / 'templates/base/workflows',
    ROOT / 'templates/base/shared',
    ROOT / 'templates/base/knowledge',
    ROOT / 'templates/base/inbox',
    ROOT / 'templates/base/scaffold',
]
for path in required:
    if not path.exists():
        raise SystemExit(f'ERROR: missing release source: {path.relative_to(ROOT)}')

identity = {
    'asset_schema': 1,
    'ava_version': args.version,
    'tag': tag,
    'channel': channel,
    'source_repository': 'phdah/ava',
    'source_revision': source_revision,
}


def sha_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha_file(path: pathlib.Path) -> str:
    return sha_bytes(path.read_bytes())


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def regular_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(root.rglob('*'), key=lambda value: value.as_posix().encode()):
        if path.is_symlink():
            raise SystemExit(f'ERROR: symlink is not allowed in release source: {path.relative_to(ROOT)}')
        if path.is_file():
            yield path


def read_source(path: pathlib.Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f'ERROR: release source is not a regular file: {path.relative_to(ROOT)}')
    return path.read_bytes()


def add_file(entries: dict[str, tuple[bytes, int]], name: str, content: bytes, mode: int = 0o644) -> None:
    pure = pathlib.PurePosixPath(name)
    if pure.is_absolute() or '..' in pure.parts or '.' in pure.parts or '\\' in name:
        raise SystemExit(f'ERROR: unsafe archive path: {name}')
    if name in entries:
        raise SystemExit(f'ERROR: duplicate archive path: {name}')
    entries[name] = (content, mode)


def archive_bytes(name: str, role: str, entries: dict[str, tuple[bytes, int]]) -> bytes:
    content = dict(entries)
    asset_identity = dict(identity, asset_name=name, asset_role=role)
    add_file(content, 'ava-asset.json', json_bytes(asset_identity))
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode='w', format=tarfile.PAX_FORMAT) as archive:
        directories: set[str] = set()
        for file_name in content:
            parent = pathlib.PurePosixPath(file_name).parent
            while str(parent) != '.':
                directories.add(str(parent) + '/')
                parent = parent.parent
        for directory in sorted(directories, key=lambda value: value.encode()):
            info = tarfile.TarInfo(directory)
            info.type = tarfile.DIRTYPE
            info.mode = 0o755
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            info.mtime = source_date_epoch
            info.pax_headers = {}
            archive.addfile(info)
        for file_name in sorted(content, key=lambda value: value.encode()):
            data, mode = content[file_name]
            info = tarfile.TarInfo(file_name)
            info.size = len(data)
            info.mode = mode
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            info.mtime = source_date_epoch
            info.pax_headers = {}
            archive.addfile(info, io.BytesIO(data))
    compressed = io.BytesIO()
    with gzip.GzipFile(filename='', mode='wb', fileobj=compressed, mtime=source_date_epoch, compresslevel=9) as handle:
        handle.write(raw.getvalue())
    return compressed.getvalue()


base_entries: dict[str, tuple[bytes, int]] = {}
engine_source = b''.join(read_source(path) for path in regular_files(ROOT / 'templates/installer/engine'))
add_file(base_entries, 'installer/engine.py', engine_source)
installed_files: list[dict[str, Any]] = []


def mapped(source: pathlib.Path, archive_path: str, destination: str, ownership: str, operation: str, role: str, mode: int = 0o644) -> None:
    content = read_source(source)
    add_file(base_entries, archive_path, content, mode)
    installed_files.append({
        'source_asset': 'ava-base.tar.gz',
        'source_path': archive_path,
        'destination': destination,
        'ownership': ownership,
        'operation': operation,
        'role': role,
        'sha256': sha_bytes(content),
    })


mapped(ROOT / 'templates/base/AGENTS.md', 'managed/AGENTS.md', '/AGENTS.md', 'ava-managed', 'replace-managed', 'router')
mapped(ROOT / 'templates/base/base-index.md', 'managed/.ava/base/index.md', '/.ava/base/index.md', 'ava-managed', 'replace-managed', 'base')
for directory in ('roles', 'workflows', 'shared'):
    source_root = ROOT / 'templates/base' / directory
    for source in regular_files(source_root):
        relative = source.relative_to(source_root).as_posix()
        mapped(source, f'managed/.ava/base/{directory}/{relative}', f'/.ava/base/{directory}/{relative}', 'ava-managed', 'replace-managed', 'base')

bootstrap_root = ROOT / 'templates/base/bootstrap'
if bootstrap_root.exists():
    for source in regular_files(bootstrap_root):
        relative = source.relative_to(bootstrap_root).as_posix()
        mapped(source, f'managed/bootstrap/{relative}', f'/{relative}', 'ava-managed', 'replace-managed', 'bootstrap')

scaffold_root = ROOT / 'templates/base/scaffold'
for source in regular_files(scaffold_root):
    relative = source.relative_to(scaffold_root).as_posix()
    if relative == 'index.md':
        continue
    destination = '/index.md' if relative == 'project-index.md' else f'/{relative}'
    mapped(source, f'scaffold/{relative}', destination, 'project-owned', 'create-if-absent', 'scaffold')
for directory in ('knowledge', 'inbox'):
    source_root = ROOT / 'templates/base' / directory
    for source in regular_files(source_root):
        relative = source.relative_to(source_root).as_posix()
        mapped(source, f'scaffold/{directory}/{relative}', f'/{directory}/{relative}', 'project-owned', 'create-if-absent', 'scaffold')

manifest_template = json_bytes({'generated_by': 'ava-install.sh', 'schema': 'manifest.schema.json'})
upgrade_template = json_bytes({'generated_by': 'ava-install.sh', 'schema': 'upgrade.schema.json'})
for archive_path, destination, content in (
    ('state/manifest.template.json', '/.ava/state/manifest.json', manifest_template),
    ('state/upgrade.template.json', '/.ava/state/upgrade.json', upgrade_template),
):
    add_file(base_entries, archive_path, content)
    installed_files.append({
        'source_asset': 'ava-base.tar.gz',
        'source_path': archive_path,
        'destination': destination,
        'ownership': 'ava-managed',
        'operation': 'replace-managed',
        'role': 'state',
        'sha256': sha_bytes(content),
    })

(output / 'ava-base.tar.gz').write_bytes(archive_bytes('ava-base.tar.gz', 'base', base_entries))

empty_inventory = {'entries': []}
guidance_entries = {'inventory.json': (json_bytes(empty_inventory), 0o644)}
(output / 'ava-guidance.tar.gz').write_bytes(archive_bytes('ava-guidance.tar.gz', 'guidance', guidance_entries))

migration_inventory = {'files': [], 'steps': []}
migration_entries = {'inventory.json': (json_bytes(migration_inventory), 0o644)}
(output / 'ava-migrations.tar.gz').write_bytes(archive_bytes('ava-migrations.tar.gz', 'migrations', migration_entries))

installer_source = (ROOT / 'templates/installer/ava-install.sh').read_text(encoding='utf-8')
replacements = {
    '@AVA_VERSION@': args.version,
    '@AVA_TAG@': tag,
    '@AVA_CHANNEL@': channel,
    '@AVA_SOURCE_REVISION@': source_revision,
}
for old, new in replacements.items():
    installer_source = installer_source.replace(old, new)
if '@AVA_' in installer_source:
    raise SystemExit('ERROR: installer contains unresolved release placeholders')
installer_path = output / 'ava-install.sh'
installer_path.write_text(installer_source, encoding='utf-8', newline='\n')
installer_path.chmod(0o755)

if args.release_notes:
    notes_body = pathlib.Path(args.release_notes).read_text(encoding='utf-8')
else:
    notes_body = '# Ava release\n\nRelease notes are completed during the publication task.\n'
notes = (
    '---\n'
    f'ava_version: "{args.version}"\n'
    f'tag: "{tag}"\n'
    f'channel: "{channel}"\n'
    'source_repository: "phdah/ava"\n'
    f'source_revision: "{source_revision}"\n'
    '---\n\n'
    + notes_body.lstrip()
)
(output / 'ava-release-notes.md').write_text(notes, encoding='utf-8', newline='\n')

hashed_assets = []
for name, role, media_type in (
    ('ava-install.sh', 'installer', 'text/x-shellscript'),
    ('ava-base.tar.gz', 'base', 'application/gzip'),
    ('ava-guidance.tar.gz', 'guidance', 'application/gzip'),
    ('ava-migrations.tar.gz', 'migrations', 'application/gzip'),
):
    path = output / name
    hashed_assets.append({'name': name, 'role': role, 'media_type': media_type, 'size': path.stat().st_size, 'sha256': sha_file(path)})
notes_path = output / 'ava-release-notes.md'
notes_asset = {'name': notes_path.name, 'role': 'release-notes', 'media_type': 'text/markdown', 'size': notes_path.stat().st_size, 'sha256': sha_file(notes_path)}

release_manifest = {
    'release_schema': 1,
    'ava_version': args.version,
    'tag': tag,
    'channel': channel,
    'source_repository': 'phdah/ava',
    'source_revision': source_revision,
    'published_at': published_at,
    'installer_protocol': 1,
    'okf_version': '0.2',
    'manifest_schema': 1,
    'semantic_review_required': args.semantic_review_required,
    'assets': [
        hashed_assets[0],
        hashed_assets[1],
        hashed_assets[2],
        hashed_assets[3],
        {'name': 'ava-release.json', 'role': 'release-manifest', 'media_type': 'application/json'},
        notes_asset,
        {'name': 'SHA256SUMS', 'role': 'checksums', 'media_type': 'text/plain'},
    ],
    'installed_files': sorted(installed_files, key=lambda item: item['destination'].encode()),
    'upgrade_paths': {
        'edges': [
            {
                'from': source,
                'to': args.version,
                'mode': 'direct',
                'intermediates': [],
                'carry_unresolved_semantic_state': False,
                'migration_ids': [],
                'guidance_paths': [],
            }
            for source in args.upgrade_from
        ]
    },
    'guidance': {'entries': []},
    'migrations': {'files': [], 'steps': []},
}
(output / 'ava-release.json').write_bytes(json_bytes(release_manifest))

checksum_names = [
    'ava-install.sh',
    'ava-base.tar.gz',
    'ava-guidance.tar.gz',
    'ava-migrations.tar.gz',
    'ava-release.json',
    'ava-release-notes.md',
]
checksums = ''.join(f'{sha_file(output / name)}  {name}\n' for name in checksum_names)
(output / 'SHA256SUMS').write_text(checksums, encoding='ascii', newline='\n')

print(f'Built Ava {args.version} release assets in {output.relative_to(ROOT)}')
for name in [*checksum_names, 'SHA256SUMS']:
    print(f'  {name}')
PY
