#!/bin/sh

set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

require_file() {
  [ -f "$ROOT/$1" ] || fail "missing required file: $1"
}

require_dir() {
  [ -d "$ROOT/$1" ] || fail "missing required directory: $1"
}

for path in \
  distribution/index.md \
  distribution/ownership.md \
  distribution/versioning.md \
  distribution/releases.md \
  distribution/upgrades.md \
  distribution/guidance.md \
  distribution/schemas/index.md \
  distribution/schemas/manifest.schema.json \
  distribution/schemas/release.schema.json \
  distribution/schemas/upgrade.schema.json \
  distribution/schemas/guidance.schema.json \
  templates/index.md \
  templates/base/index.md \
  templates/base/base-index.md \
  templates/base/scaffold/index.md \
  templates/installer/index.md \
  templates/installer/ava-install.sh \
  internal/release/index.md \
  internal/release/procedure.md \
  internal/release/build-assets.sh \
  internal/release/test-installer.sh
do
  require_file "$path"
done

require_dir templates/base
require_dir templates/installer/engine

for path in "$ROOT"/templates/* "$ROOT"/templates/.[!.]* "$ROOT"/templates/..?*
do
  [ -e "$path" ] || continue
  case "$path" in
    "$ROOT/templates/index.md"|"$ROOT/templates/base"|"$ROOT/templates/installer") ;;
    *) fail "unexpected templates root entry: ${path#"$ROOT/"}" ;;
  esac
done

for old_path in \
  templates/distribution-and-ownership.md \
  templates/versioning-and-compatibility.md \
  templates/github-release-assets.md \
  templates/upgrade-and-migration.md \
  templates/release-guidance.md \
  templates/schemas
do
  [ ! -e "$ROOT/$old_path" ] || fail "obsolete distribution location remains: $old_path"
done

for schema in manifest release upgrade guidance
do
  file="$ROOT/distribution/schemas/$schema.schema.json"
  expected="https://github.com/phdah/ava/blob/main/distribution/schemas/$schema.schema.json"
  grep -F '"$id":' "$file" >/dev/null || fail "schema has no id: ${file#"$ROOT/"}"
  grep -F "$expected" "$file" >/dev/null || fail "schema id is not canonical: ${file#"$ROOT/"}"
done

for script in \
  templates/installer/ava-install.sh \
  internal/release/build-assets.sh \
  internal/release/test-installer.sh \
  internal/release/validate-boundaries.sh
do
  sh -n "$ROOT/$script" || fail "invalid POSIX shell syntax: $script"
done

python3 - "$ROOT/templates/installer/engine" <<'PY' || exit 1
import pathlib, sys
root = pathlib.Path(sys.argv[1])
parts = sorted(path for path in root.rglob('*') if path.is_file())
if not parts:
    raise SystemExit('ERROR: installer engine has no source fragments')
compile(b''.join(path.read_bytes() for path in parts), 'installer/engine.py', 'exec')
PY

stale_pattern='templates/(distribution-and-ownership|versioning-and-compatibility|github-release-assets|upgrade-and-migration|release-guidance)\.md|templates/schemas/'

find "$ROOT" -path "$ROOT/.git" -prune -o -type f -print | while IFS= read -r file
do
  [ "$file" = "$ROOT/internal/release/validate-boundaries.sh" ] && continue
  if grep -En "$stale_pattern" "$file" >/dev/null 2>&1; then
    printf 'ERROR: stale distribution reference in %s\n' "${file#"$ROOT/"}" >&2
    exit 1
  fi
done

find "$ROOT/templates/base" -type f -print | while IFS= read -r file
do
  if grep -En '\]\([^)]*internal/|resource:[[:space:]]*/?internal/' "$file" >/dev/null 2>&1; then
    printf 'ERROR: release source depends on internal content: %s\n' "${file#"$ROOT/"}" >&2
    exit 1
  fi
done

printf 'Repository boundaries valid.\n'
