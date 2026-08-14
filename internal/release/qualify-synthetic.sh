#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

set +e
python3 "$ROOT/internal/release/qualification_runner.py" \
  --repository-root "$ROOT" \
  "$@"
RUNNER_STATUS=$?
set -e

if [ "$RUNNER_STATUS" -ne 0 ]; then
  exit "$RUNNER_STATUS"
fi

exec python3 "$ROOT/internal/release/qualification_postconditions.py" \
  --repository-root "$ROOT" \
  "$@"
