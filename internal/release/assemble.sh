#!/bin/sh
set -eu
ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
python3 "$ROOT/internal/release/validate-installed-paths.py" --root "$ROOT"
exec python3 "$ROOT/internal/release/assemble.py" --root "$ROOT" "$@"
