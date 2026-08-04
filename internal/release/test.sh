#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)

sh -n "$ROOT/internal/release/assemble.sh"
sh -n "$ROOT/internal/release/ava-install.sh"
python3 -m py_compile \
  "$ROOT/internal/release/assemble.py" \
  "$ROOT/internal/release/conformance.py" \
  "$ROOT/internal/release/conformance_common.py" \
  "$ROOT/internal/release/conformance_repository.py" \
  "$ROOT/internal/release/conformance_installed.py" \
  "$ROOT/internal/release/conformance_release.py" \
  "$ROOT/internal/release/validate-installed-paths.py"
python3 "$ROOT/internal/release/validate-installed-paths.py" --root "$ROOT"
python3 "$ROOT/internal/release/conformance.py" \
  --root "$ROOT" \
  --mode repository \
  --format text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  internal.release.tests.test_installed_paths \
  internal.release.tests.test_installer \
  internal.release.tests.test_installer_conformance \
  internal.release.tests.test_host_config \
  internal.release.tests.test_document_update_metadata_fixtures \
  internal.release.tests.test_ava_maintenance \
  internal.release.tests.test_conformance \
  internal.release.tests.test_conformance_matrix
