#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

if [ "${1:-}" = "--validate-config-only" ]; then
  shift
  set -- validate-config "$@"
fi

exec python3 "$ROOT/internal/release/qualification.py" \
  --repository-root "$ROOT" \
  "$@"
