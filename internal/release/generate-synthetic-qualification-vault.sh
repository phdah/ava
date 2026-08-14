#!/bin/sh
set -eu

if [ "$#" -ne 0 ]; then
  printf 'usage: %s\n' "$0" >&2
  exit 2
fi

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
FIXTURE="$ROOT/internal/release/fixtures/synthetic-qualification-vault/fixture.py"
TEMP_ROOT=${TMPDIR:-/tmp}

if [ ! -d "$TEMP_ROOT" ]; then
  printf 'temporary directory does not exist: %s\n' "$TEMP_ROOT" >&2
  exit 1
fi

OUTPUT=$(mktemp -d "$TEMP_ROOT/ava-synthetic-qualification-vault.XXXXXX")
printf 'generating synthetic qualification vault: %s\n' "$OUTPUT"

python3 "$FIXTURE" generate "$OUTPUT"
python3 "$FIXTURE" install-pinned-images "$OUTPUT"
python3 "$FIXTURE" finalize-images "$OUTPUT"
python3 "$FIXTURE" verify "$OUTPUT"
python3 "$FIXTURE" materialize-variants "$OUTPUT"

printf 'synthetic qualification vault ready: %s\n' "$OUTPUT"
