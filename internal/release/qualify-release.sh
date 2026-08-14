#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

exec python3 "$ROOT/internal/release/qualification_automation.py" \
  --repository-root "$ROOT" \
  "$@"
