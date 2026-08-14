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

exec "$REAL_OPENCODE" "$@"
