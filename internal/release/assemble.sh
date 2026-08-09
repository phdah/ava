#!/bin/sh
set -eu
ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
python3 "$ROOT/internal/release/validate-installed-paths.py" --root "$ROOT"
if [ -n "${AVA_UPGRADE_CATALOG:-}" ]; then
  exec python3 "$ROOT/internal/release/assemble_reviewed.py" \
    --root "$ROOT" \
    --upgrade-catalog "$AVA_UPGRADE_CATALOG" \
    "$@"
fi
exec python3 "$ROOT/internal/release/assemble.py" --root "$ROOT" "$@"
