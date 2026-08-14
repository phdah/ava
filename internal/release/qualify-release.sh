#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
: "${AVA_QUALIFICATION_OPENCODE:=opencode}"
export AVA_QUALIFICATION_OPENCODE

exec python3 "$ROOT/internal/release/qualification_automation.py" \
  "$@" \
  --repository-root "$ROOT" \
  --opencode "$ROOT/internal/release/qualification-opencode.sh"
