#!/bin/sh
set -eux

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
test -f "$TARGET/backlog/index.md"
test -f "$TARGET/backlog/tasks/index.md"
test ! -d "$TARGET/backlog/completed"
test ! -e "$TARGET/backlog/tasks/.gitkeep"

grep -q '^backlog_directory: backlog$' "$TARGET/backlog.config.yml"
grep -Fq 'statuses: ["To Do", "In Progress", "Won'"'"'t Fix", "Done"]' "$TARGET/backlog.config.yml"
grep -q '^remote_operations: false$' "$TARGET/backlog.config.yml"
grep -q '^auto_commit: false$' "$TARGET/backlog.config.yml"

cd "$TARGET"
npx -y backlog.md@1.50.1 instructions overview >/dev/null

# Verify canonical next-task selection uses readiness first and ordinal ordering second.
npx -y backlog.md@1.50.1 task create "Ordering blocker" --ordinal 10 >/dev/null
blocker_id=$(npx -y backlog.md@1.50.1 task list --json | jq -r '.tasks[] | select(.title == "Ordering blocker") | .id' | head -n 1)
test -n "$blocker_id"
npx -y backlog.md@1.50.1 task create "Blocked lower ordinal" --ordinal 1 --depends-on "$blocker_id" >/dev/null
npx -y backlog.md@1.50.1 task create "Ready next ordinal" --ordinal 2 >/dev/null
next_json=$(npx -y backlog.md@1.50.1 task list --status "To Do" --ready --sort ordinal --limit 1 --json)
printf '%s\n' "$next_json"
next_title=$(printf '%s\n' "$next_json" | jq -r '.tasks[0].title')
test "$next_title" = "Ready next ordinal"

# Verify Done dependencies become ready without moving task files.
npx -y backlog.md@1.50.1 task edit "$blocker_id" -s "Done" >/dev/null
unblocked_json=$(npx -y backlog.md@1.50.1 task list --status "To Do" --ready --sort ordinal --limit 1 --json)
printf '%s\n' "$unblocked_json"
unblocked_title=$(printf '%s\n' "$unblocked_json" | jq -r '.tasks[0].title')
test "$unblocked_title" = "Blocked lower ordinal"
test ! -d backlog/completed

# Verify direct native Markdown edits remain compatible and terminal tasks remain in tasks/.
npx -y backlog.md@1.50.1 task create "Installed lifecycle probe" -d "Verify Ava project task scaffold" >/dev/null
probe_id=$(npx -y backlog.md@1.50.1 task list --json | jq -r '.tasks[] | select(.title == "Installed lifecycle probe") | .id' | head -n 1)
test -n "$probe_id"
npx -y backlog.md@1.50.1 task edit "$probe_id" -s "In Progress" >/dev/null

probe_file=$(find backlog/tasks -type f -name 'task-*.md' | while IFS= read -r path; do
  grep -q '^title: "Installed lifecycle probe"$' "$path" && { printf '%s\n' "$path"; break; }
done)
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
test -f "$probe_file"
test ! -d backlog/completed
npx -y backlog.md@1.50.1 task "$probe_id" --json | jq -e '.task.status == "Done"' >/dev/null

npx -y backlog.md@1.50.1 task create "Won't fix lifecycle probe" >/dev/null
wont_fix_id=$(npx -y backlog.md@1.50.1 task list --json | jq -r '.tasks[] | select(.title == "Won'"'"'t fix lifecycle probe") | .id' | head -n 1)
test -n "$wont_fix_id"
npx -y backlog.md@1.50.1 task edit "$wont_fix_id" -s "Won't Fix" >/dev/null
npx -y backlog.md@1.50.1 task "$wont_fix_id" --json | jq -e '.task.status == "Won'"'"'t Fix"' >/dev/null
test ! -d backlog/completed
