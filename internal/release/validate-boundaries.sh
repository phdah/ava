#!/bin/sh

set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

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
  CHANGELOG.md \
  version.txt \
  release-please-config.json \
  .release-please-manifest.json \
  .github/workflows/conventional-pr-title.yml \
  .github/workflows/release-please.yml \
  distribution/index.md \
  distribution/paths.md \
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
  templates/project-scaffolds/index.md \
  internal/release/index.md \
  internal/release/procedure.md \
  internal/release/release-please.md \
  internal/release/installer.md \
  internal/release/conformance.md \
  internal/release/qualification-automation.md \
  internal/release/assemble.sh \
  internal/release/assemble.py \
  internal/release/conformance.py \
  internal/release/conformance_common.py \
  internal/release/conformance_repository.py \
  internal/release/conformance_installed.py \
  internal/release/conformance_release.py \
  internal/release/_qualification_runner_core.py \
  internal/release/_qualification_automation_core.py \
  internal/release/qualification_runner.py \
  internal/release/qualification_automation.py \
  internal/release/qualification_phase_runner.py \
  internal/release/qualification_phase_automation.py \
  internal/release/qualification_phase_gate.py \
  internal/release/qualify-release.sh \
  internal/release/accept-release-qualification.sh \
  internal/release/qualification-opencode.sh \
  internal/release/validate-installed-paths.py \
  internal/release/validate_pr_title.py \
  internal/release/ava-install.sh \
  internal/release/installer/00.py \
  internal/release/installer/01.py \
  internal/release/installer/02.py \
  internal/release/installer/03.py \
  internal/release/installer/04.py \
  internal/release/installer/05.py \
  internal/release/installer/06.py \
  internal/release/installer/07.py \
  internal/release/test.sh \
  internal/release/fixtures/conformance-matrix.json \
  internal/release/fixtures/release-please-policy.json \
  internal/release/fixtures/synthetic-qualification-vault/index.md \
  internal/release/fixtures/synthetic-qualification-vault/blueprint.md \
  internal/release/fixtures/synthetic-qualification-vault/blueprint.json \
  internal/release/fixtures/synthetic-qualification-vault/checkpoint.py \
  internal/release/fixtures/synthetic-qualification-vault/checkpoints.md \
  internal/release/fixtures/synthetic-qualification-vault/fixture.py \
  internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json \
  internal/release/fixtures/synthetic-qualification-vault/requirements.lock \
  internal/release/fixtures/synthetic-qualification-vault/oracle.schema.json \
  internal/release/fixtures/synthetic-qualification-vault/run-manifest.schema.json \
  internal/release/tests/test_installed_paths.py \
  internal/release/tests/test_installer.py \
  internal/release/tests/test_installer_conformance.py \
  internal/release/tests/test_conformance.py \
  internal/release/tests/test_conformance_matrix.py \
  internal/release/tests/test_release_please.py \
  internal/release/tests/test_synthetic_qualification_vault.py \
  internal/release/tests/test_qualification_checkpoints.py \
  internal/release/tests/test_qualification_runner.py \
  internal/release/tests/test_qualification_phases.py
do
  require_file "$path"
done

[ ! -e "$ROOT/internal/release/qualify-synthetic.sh" ] || fail "legacy qualification shell entry point remains: internal/release/qualify-synthetic.sh"
[ ! -e "$ROOT/internal/release/qualification-runner.md" ] || fail "legacy full-matrix qualification procedure remains: internal/release/qualification-runner.md"

grep -F 'use internal/release/qualify-release.sh' "$ROOT/internal/release/qualification_runner.py" >/dev/null || fail "qualification runner facade does not reject standalone execution"
grep -F 'use internal/release/qualify-release.sh' "$ROOT/internal/release/qualification_automation.py" >/dev/null || fail "qualification automation facade does not reject standalone execution"

for path in templates/base templates/project-scaffolds internal/release/installer internal/release/fixtures
do
  require_dir "$path"
done

for path in "$ROOT"/templates/* "$ROOT"/templates/.[!.]* "$ROOT"/templates/..?*
do
  [ -e "$path" ] || continue
  case "$path" in
    "$ROOT/templates/index.md"|\
    "$ROOT/templates/base"|\
    "$ROOT/templates/project-scaffolds") ;;
    *) fail "unexpected templates root entry: ${path#"$ROOT/"}" ;;
  esac
done

for old_path in \
  templates/distribution-and-ownership.md \
  templates/versioning-and-compatibility.md \
  templates/github-release-assets.md \
  templates/upgrade-and-migration.md \
  templates/release-guidance.md \
  templates/schemas \
  templates/host-bootstraps
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

stale_pattern='templates/(distribution-and-ownership|versioning-and-compatibility|github-release-assets|upgrade-and-migration|release-guidance)\.md|templates/schemas/'

find "$ROOT" \( -path "$ROOT/.git" -o -name __pycache__ \) -prune -o -type f -print | while IFS= read -r file
do
  [ "$file" = "$ROOT/internal/release/validate-boundaries.sh" ] && continue
  if grep -En "$stale_pattern" "$file" >/dev/null 2>&1; then
    printf 'ERROR: stale distribution reference in %s\n' "${file#"$ROOT/"}" >&2
    exit 1
  fi
done

for source_root in templates/base templates/project-scaffolds
do
  find "$ROOT/$source_root" -type f -print | while IFS= read -r file
  do
    if grep -En '\]\([^)]*internal/|resource:[[:space:]]*/?internal/' "$file" >/dev/null 2>&1; then
      printf 'ERROR: release source depends on internal content: %s\n' "${file#"$ROOT/"}" >&2
      exit 1
    fi
  done
done

sh -n "$ROOT/internal/release/assemble.sh"
sh -n "$ROOT/internal/release/ava-install.sh"
sh -n "$ROOT/internal/release/qualify-release.sh"
sh -n "$ROOT/internal/release/accept-release-qualification.sh"
sh -n "$ROOT/internal/release/qualification-opencode.sh"
sh -n "$ROOT/internal/release/test.sh"
python3 -m py_compile \
  "$ROOT/internal/release/assemble.py" \
  "$ROOT/internal/release/conformance.py" \
  "$ROOT/internal/release/conformance_common.py" \
  "$ROOT/internal/release/conformance_repository.py" \
  "$ROOT/internal/release/conformance_installed.py" \
  "$ROOT/internal/release/conformance_release.py" \
  "$ROOT/internal/release/_qualification_runner_core.py" \
  "$ROOT/internal/release/_qualification_automation_core.py" \
  "$ROOT/internal/release/qualification_runner.py" \
  "$ROOT/internal/release/qualification_automation.py" \
  "$ROOT/internal/release/qualification_phase_runner.py" \
  "$ROOT/internal/release/qualification_phase_automation.py" \
  "$ROOT/internal/release/qualification_phase_gate.py" \
  "$ROOT/internal/release/fixtures/synthetic-qualification-vault/checkpoint.py" \
  "$ROOT/internal/release/fixtures/synthetic-qualification-vault/fixture.py" \
  "$ROOT/internal/release/validate-installed-paths.py" \
  "$ROOT/internal/release/validate_pr_title.py"
python3 "$ROOT/internal/release/validate-installed-paths.py" --root "$ROOT"
python3 "$ROOT/internal/release/conformance.py" --root "$ROOT" --mode repository --format text

printf 'Repository boundaries valid.\n'
