#!/bin/sh

set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
TMP=${TMPDIR:-/tmp}/ava-installer-test.$$
DIST1="$ROOT/.ava-test-dist-1.$$"
DIST2="$ROOT/.ava-test-dist-2.$$"

cleanup() {
  rm -rf "$TMP" "$DIST1" "$DIST2"
}
trap cleanup EXIT HUP INT TERM

fail() {
  printf 'TEST FAILED: %s\n' "$*" >&2
  exit 1
}

expect_failure() {
  code=$1
  shift
  stderr="$TMP/stderr"
  if "$@" >"$TMP/stdout" 2>"$stderr"; then
    fail "command unexpectedly succeeded: $*"
  fi
  grep -F "code=$code" "$stderr" >/dev/null || {
    cat "$stderr" >&2
    fail "expected error code $code"
  }
}

mkdir -p "$TMP"
revision=$(git -C "$ROOT" rev-parse HEAD)
epoch=$(git -C "$ROOT" show -s --format=%ct "$revision")
published_at=2026-01-01T00:00:00Z

"$ROOT/internal/release/build-assets.sh" \
  --version 0.0.1-alpha.1 \
  --source-revision "$revision" \
  --source-date-epoch "$epoch" \
  --published-at "$published_at" \
  --output "${DIST1#"$ROOT/"}" >/dev/null

"$ROOT/internal/release/build-assets.sh" \
  --version 0.0.1-beta.1 \
  --upgrade-from 0.0.1-alpha.1 \
  --source-revision "$revision" \
  --source-date-epoch "$epoch" \
  --published-at "$published_at" \
  --output "${DIST2#"$ROOT/"}" >/dev/null

TARGET="$TMP/project"
"$DIST1/ava-install.sh" --assets-dir "$DIST1" --target "$TARGET" --dry-run >"$TMP/plan"
[ ! -e "$TARGET" ] || fail 'dry-run mutated the target'
grep -F 'operation=create ownership=ava-managed path=/AGENTS.md' "$TMP/plan" >/dev/null || fail 'dry-run omitted managed router plan'
grep -F 'operation=create ownership=project-owned path=/roles/index.md' "$TMP/plan" >/dev/null || fail 'dry-run omitted project scaffold plan'

"$DIST1/ava-install.sh" --assets-dir "$DIST1" --target "$TARGET" >/dev/null
[ -f "$TARGET/AGENTS.md" ] || fail 'router was not installed'
[ -f "$TARGET/.ava/base/index.md" ] || fail 'managed base index was not installed'
[ -f "$TARGET/.ava/state/manifest.json" ] || fail 'installed manifest was not created'
[ -f "$TARGET/.ava/state/upgrade.json" ] || fail 'upgrade journal was not created'
[ -f "$TARGET/roles/index.md" ] || fail 'project scaffold was not created'

python3 - "$TARGET" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
manifest = json.loads((root / '.ava/state/manifest.json').read_text())
upgrade = json.loads((root / '.ava/state/upgrade.json').read_text())
assert manifest['ava_version'] == '0.0.1-alpha.1'
assert manifest['semantic_compatibility']['status'] == 'complete'
assert upgrade['status'] == 'complete'
assert any(item['path'] == '/AGENTS.md' and item['kind'] == 'payload' for item in manifest['managed_files'])
assert not any(item['path'] == '/roles/index.md' for item in manifest['managed_files'])
PY

printf '# Project-specific roles\n' >"$TARGET/roles/index.md"
"$DIST2/ava-install.sh" --assets-dir "$DIST2" --target "$TARGET" >/dev/null
grep -F '# Project-specific roles' "$TARGET/roles/index.md" >/dev/null || fail 'upgrade replaced project-owned scaffold'
python3 - "$TARGET" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
manifest = json.loads((root / '.ava/state/manifest.json').read_text())
assert manifest['ava_version'] == '0.0.1-beta.1'
PY

printf '\nlocal modification\n' >>"$TARGET/.ava/base/index.md"
expect_failure MANAGED_FILE_CONFLICT "$DIST2/ava-install.sh" --assets-dir "$DIST2" --target "$TARGET"

COLLISION="$TMP/collision"
mkdir -p "$COLLISION"
printf '# Existing router\n' >"$COLLISION/AGENTS.md"
expect_failure AGENTS_COLLISION "$DIST1/ava-install.sh" --assets-dir "$DIST1" --target "$COLLISION"
"$DIST1/ava-install.sh" --assets-dir "$DIST1" --target "$COLLISION" --adopt-agents >/dev/null
grep -F '# Ava' "$COLLISION/AGENTS.md" >/dev/null || fail 'explicit router adoption did not replace AGENTS.md'

UNRECOGNIZED="$TMP/unrecognized"
mkdir -p "$UNRECOGNIZED/.ava"
expect_failure UNRECOGNIZED_AVA "$DIST1/ava-install.sh" --assets-dir "$DIST1" --target "$UNRECOGNIZED"

BAD="$TMP/bad-assets"
cp -R "$DIST1" "$BAD"
python3 - "$BAD" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
release_path = root / 'ava-release.json'
release = json.loads(release_path.read_text())
release['installed_files'][0]['destination'] = '/../outside'
release_path.write_text(json.dumps(release, indent=2, sort_keys=True) + '\n')
records = []
for line in (root / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split(None, 1)
    name = name.lstrip('*')
    if name == 'ava-release.json':
        digest = hashlib.sha256(release_path.read_bytes()).hexdigest()
    records.append(f'{digest}  {name}')
(root / 'SHA256SUMS').write_text('\n'.join(records) + '\n')
PY
expect_failure UNSAFE_PATH "$BAD/ava-install.sh" --assets-dir "$BAD" --target "$TMP/unsafe"
[ ! -e "$TMP/outside" ] || fail 'unsafe mapping wrote outside target root'

printf 'Installer smoke tests passed.\n'
