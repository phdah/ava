#!/bin/sh
set -eu

REAL_OPENCODE=${AVA_QUALIFICATION_OPENCODE:-opencode}

if [ "$#" -eq 4 ] \
  && [ "$1" = "session" ] \
  && [ "$2" = "list" ] \
  && [ "$3" = "--format" ] \
  && [ "$4" = "json" ]; then
  exec "$REAL_OPENCODE" db --format json \
    "SELECT id, parent_id AS parentID, directory FROM session ORDER BY id;"
fi

if [ "$#" -ge 2 ] && [ "$1" = "run" ]; then
  exec python3 - "$REAL_OPENCODE" "$@" <<'PY'
import os
import sys

real = sys.argv[1]
args = sys.argv[2:]
if "--" not in args:
    args.insert(len(args) - 1, "--")
os.execvp(real, [real, *args])
PY
fi

exec "$REAL_OPENCODE" "$@"
