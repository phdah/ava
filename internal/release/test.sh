#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)

sh -n "$ROOT/internal/release/assemble.sh"
sh -n "$ROOT/internal/release/ava-install.sh"
python3 -m py_compile \
  "$ROOT/internal/release/assemble.py" \
  "$ROOT/internal/release/validate-installed-paths.py"
python3 "$ROOT/internal/release/validate-installed-paths.py" --root "$ROOT"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  internal.release.tests.test_installed_paths \
  internal.release.tests.test_installer
