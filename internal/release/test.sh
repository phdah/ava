#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)

sh -n "$ROOT/internal/release/assemble.sh"
sh -n "$ROOT/internal/release/ava-install.sh"
python3 -m py_compile "$ROOT/internal/release/assemble.py"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v internal.release.tests.test_installer
