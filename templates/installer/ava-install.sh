#!/bin/sh

set -eu

AVA_VERSION='@AVA_VERSION@'
AVA_TAG='@AVA_TAG@'
AVA_CHANNEL='@AVA_CHANNEL@'
AVA_SOURCE_REVISION='@AVA_SOURCE_REVISION@'
AVA_REPOSITORY='phdah/ava'
AVA_INSTALLER_PROTOCOL='1'

usage() {
  cat <<'USAGE'
Usage: ava-install.sh [options]

Install or upgrade Ava in a project directory.

Options:
  --target DIR          Project root. Defaults to the current directory.
  --version VERSION     Require this installer to match VERSION or vVERSION.
  --dry-run             Validate and print the complete plan without mutation.
  --verified            Require GitHub immutable-release verification.
  --adopt-agents        Explicitly authorize replacing an existing /AGENTS.md.
  --bootstrap PATH      Install one optional host bootstrap by destination path.
  --assets-dir DIR      Read already-downloaded release assets from DIR.
  -h, --help            Show this help.

Version selection is performed by the immutable installer URL. Use the latest
stable URL for stable selection or download this script from an exact vX.Y.Z tag.
USAGE
}

fail() {
  code=$1
  shift
  printf 'AVA_ERROR code=%s stage=bootstrap message=%s\n' "$code" "$*" >&2
  exit 1
}

need() {
  command -v "$1" >/dev/null 2>&1 || fail MISSING_COMMAND "required command not found: $1"
}

hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    fail MISSING_COMMAND 'required command not found: sha256sum or shasum'
  fi
}

TARGET=.
DRY_RUN=0
VERIFIED=0
ADOPT_AGENTS=0
BOOTSTRAP=
ASSETS_DIR=
REQUESTED_VERSION=

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      [ "$#" -ge 2 ] || fail INVALID_ARGUMENT '--target requires a directory'
      TARGET=$2
      shift 2
      ;;
    --version)
      [ "$#" -ge 2 ] || fail INVALID_ARGUMENT '--version requires a value'
      REQUESTED_VERSION=$2
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --verified)
      VERIFIED=1
      shift
      ;;
    --adopt-agents)
      ADOPT_AGENTS=1
      shift
      ;;
    --bootstrap)
      [ "$#" -ge 2 ] || fail INVALID_ARGUMENT '--bootstrap requires a destination path'
      BOOTSTRAP=$2
      shift 2
      ;;
    --assets-dir)
      [ "$#" -ge 2 ] || fail INVALID_ARGUMENT '--assets-dir requires a directory'
      ASSETS_DIR=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail INVALID_ARGUMENT "unknown option: $1"
      ;;
  esac
done

case "$AVA_VERSION:$AVA_TAG:$AVA_SOURCE_REVISION" in
  *@*) fail UNBUILT_INSTALLER 'this source template must be assembled into a release installer before use' ;;
esac

if [ -n "$REQUESTED_VERSION" ]; then
  case "$REQUESTED_VERSION" in v*) requested_tag=$REQUESTED_VERSION ;; *) requested_tag=v$REQUESTED_VERSION ;; esac
  [ "$requested_tag" = "$AVA_TAG" ] || fail VERSION_MISMATCH "installer is $AVA_TAG, requested $requested_tag"
fi

need python3

TARGET=$(python3 - "$TARGET" <<'PY'
import os, pathlib, sys
p = pathlib.Path(sys.argv[1]).expanduser()
if p.exists() and p.is_symlink():
    raise SystemExit('target root must not be a symlink')
print(os.path.abspath(str(p)))
PY
) || fail UNSAFE_TARGET 'could not normalize target directory'

TARGET_CREATED=0
if [ ! -e "$TARGET" ]; then
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$TARGET" || fail TARGET_CREATE_FAILED "cannot create target: $TARGET"
    TARGET_CREATED=1
  fi
elif [ ! -d "$TARGET" ]; then
  fail INVALID_TARGET "target is not a directory: $TARGET"
fi

WORK=
cleanup() {
  status=$?
  if [ -n "$WORK" ] && [ -d "$WORK" ]; then
    rm -rf "$WORK"
  fi
  if [ "$status" -ne 0 ] && [ "$TARGET_CREATED" -eq 1 ] && [ -d "$TARGET" ]; then
    rmdir "$TARGET" 2>/dev/null || true
  fi
  exit "$status"
}
trap cleanup EXIT HUP INT TERM

if [ -n "$ASSETS_DIR" ]; then
  ASSETS_DIR=$(python3 - "$ASSETS_DIR" <<'PY'
import os, pathlib, sys
p = pathlib.Path(sys.argv[1]).expanduser()
if not p.is_dir():
    raise SystemExit(1)
print(os.path.abspath(str(p)))
PY
) || fail INVALID_ASSETS_DIR 'assets directory does not exist'
else
  [ "$DRY_RUN" -eq 0 ] || fail DRY_RUN_DOWNLOAD 'dry-run without --assets-dir would create a download workspace in the target'
  need curl
  WORK="$TARGET/.ava-install.$$"
  [ ! -e "$WORK" ] || fail WORKSPACE_EXISTS "temporary workspace already exists: $WORK"
  mkdir -m 700 "$WORK"
  ASSETS_DIR=$WORK
  base_url="https://github.com/$AVA_REPOSITORY/releases/download/$AVA_TAG"
  for asset in ava-release.json SHA256SUMS ava-base.tar.gz ava-guidance.tar.gz ava-migrations.tar.gz; do
    curl -fsSL "$base_url/$asset" -o "$ASSETS_DIR/$asset" || fail DOWNLOAD_FAILED "could not download $asset"
  done
fi

for asset in ava-release.json SHA256SUMS ava-base.tar.gz ava-guidance.tar.gz ava-migrations.tar.gz; do
  [ -f "$ASSETS_DIR/$asset" ] || fail MISSING_ASSET "missing release asset: $asset"
done

if [ "$VERIFIED" -eq 1 ]; then
  need gh
  case "$0" in
    -|sh|*/sh) fail VERIFIED_STDIN 'verified mode requires an installer file downloaded from the pinned release' ;;
  esac
  [ -f "$0" ] || fail VERIFIED_STDIN 'verified mode requires a local installer file'
  gh release verify "$AVA_TAG" --repo "$AVA_REPOSITORY" >/dev/null || fail ATTESTATION_FAILED "release verification failed for $AVA_TAG"
  gh release verify-asset "$AVA_TAG" "$0" --repo "$AVA_REPOSITORY" >/dev/null || fail ATTESTATION_FAILED 'installer asset verification failed'
fi

python3 - "$ASSETS_DIR/SHA256SUMS" "$ASSETS_DIR" <<'PY'
import hashlib, pathlib, re, sys
sums = pathlib.Path(sys.argv[1])
root = pathlib.Path(sys.argv[2])
records = {}
for number, line in enumerate(sums.read_text(encoding='utf-8').splitlines(), 1):
    match = re.fullmatch(r'([0-9a-f]{64})[ \t]+\*?([^/\\]+)', line)
    if not match:
        raise SystemExit(f'AVA_ERROR code=INVALID_CHECKSUMS stage=bootstrap message=invalid SHA256SUMS line {number}')
    digest, name = match.groups()
    if name in records:
        raise SystemExit(f'AVA_ERROR code=INVALID_CHECKSUMS stage=bootstrap message=duplicate checksum for {name}')
    records[name] = digest
required = {'ava-release.json', 'ava-base.tar.gz', 'ava-guidance.tar.gz', 'ava-migrations.tar.gz'}
missing = sorted(required - records.keys())
if missing:
    raise SystemExit('AVA_ERROR code=INVALID_CHECKSUMS stage=bootstrap message=missing checksums: ' + ', '.join(missing))
for name in sorted(required):
    path = root / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != records[name]:
        raise SystemExit(f'AVA_ERROR code=CHECKSUM_MISMATCH stage=bootstrap path={name} message=expected {records[name]}, got {digest}')
PY

RELEASE_SHA=$(hash_file "$ASSETS_DIR/ava-release.json")
export AVA_VERSION AVA_TAG AVA_CHANNEL AVA_SOURCE_REVISION AVA_REPOSITORY AVA_INSTALLER_PROTOCOL RELEASE_SHA

python3 - "$ASSETS_DIR/ava-base.tar.gz" "$ASSETS_DIR" "$TARGET" "$DRY_RUN" "$ADOPT_AGENTS" "$BOOTSTRAP" <<'PYENGINE'
import pathlib, sys, tarfile
archive_path = pathlib.Path(sys.argv[1])
with tarfile.open(archive_path, 'r:gz') as archive:
    matches = [member for member in archive.getmembers() if member.name == 'installer/engine.py']
    if len(matches) != 1 or not matches[0].isfile():
        raise SystemExit('AVA_ERROR code=INVALID_INSTALLER_ENGINE stage=bootstrap message=missing regular installer/engine.py')
    source = archive.extractfile(matches[0])
    if source is None:
        raise SystemExit('AVA_ERROR code=INVALID_INSTALLER_ENGINE stage=bootstrap message=cannot read installer engine')
    code = source.read()
sys.argv = ['installer/engine.py', *sys.argv[2:]]
exec(compile(code, 'installer/engine.py', 'exec'), {'__name__': '__main__'})
PYENGINE
