#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
TMP=${RUNNER_TEMP:-${TMPDIR:-/tmp}}
WORK=$(mktemp -d "$TMP/ava-project-backlog.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

ASSETS="$WORK/assets"
TARGET="$WORK/project"
mkdir -p "$ASSETS" "$TARGET"

version=$(cat "$ROOT/version.txt")
revision=$(git -C "$ROOT" rev-parse HEAD)
epoch=$(git -C "$ROOT" show -s --format=%ct HEAD)

PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" python3 "$ROOT/internal/release/assemble.py" \
  --root "$ROOT" \
  --output "$ASSETS" \
  --version "$version" \
  --source-revision "$revision" \
  --source-date-epoch "$epoch"

sh "$ASSETS/ava-install.sh" --target "$TARGET" --asset-dir "$ASSETS"

test -f "$TARGET/backlog.config.yml"
test -f "$TARGET/backlog/tasks/.gitkeep"
test -f "$TARGET/backlog/completed/.gitkeep"

grep -q '^backlog_directory: backlog$' "$TARGET/backlog.config.yml"
grep -q '^remote_operations: false$' "$TARGET/backlog.config.yml"
grep -q '^auto_commit: false$' "$TARGET/backlog.config.yml"

cd "$TARGET"
npx -y backlog.md@1.50.1 instructions overview >/dev/null
npx -y backlog.md@1.50.1 task create "Installed lifecycle probe" -d "Verify Ava project task scaffold" >/dev/null
probe_id=$(npx -y backlog.md@1.50.1 task list --json | jq -r '.tasks[] | select(.title == "Installed lifecycle probe") | .id' | head -n 1)
test -n "$probe_id"

npx -y backlog.md@1.50.1 task edit "$probe_id" -s "In Progress" >/dev/null

probe_file=$(find backlog/tasks -type f ! -name .gitkeep -print -quit)
test -n "$probe_file"
python3 - "$probe_file" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text()
updated, count = re.subn(r'(?m)^status:\s*.*$', 'status: "To Do"', text, count=1)
if count != 1:
    raise SystemExit("task status field not found")
path.write_text(updated)
PY

npx -y backlog.md@1.50.1 task "$probe_id" --json | jq -e '.task.status == "To Do"' >/dev/null
npx -y backlog.md@1.50.1 task edit "$probe_id" -s "Done" >/dev/null
