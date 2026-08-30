#!/bin/sh
set -eu

REAL_OPENCODE=${AVA_QUALIFICATION_OPENCODE:-opencode}

buffer_json_command() {
  output=$(mktemp "${TMPDIR:-/tmp}/ava-qualification-opencode.XXXXXX")
  trap 'rm -f "$output"' EXIT HUP INT TERM
  "$@" > "$output"
  cat "$output"
}

qualification_config_content() {
  python3 - <<'PY'
import json
import os
from pathlib import Path
import sys

roots_raw = os.environ.get("AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS", "")
if not roots_raw:
    raise SystemExit("qualification OpenCode run is missing AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS")
try:
    roots = json.loads(roots_raw)
except json.JSONDecodeError as exc:
    raise SystemExit(f"invalid qualification OpenCode external-root JSON: {exc}") from exc
if not isinstance(roots, list) or not roots:
    raise SystemExit("qualification OpenCode external-root scope must be a non-empty JSON array")

raw_config = os.environ.get("OPENCODE_CONFIG_CONTENT", "")
if raw_config.strip():
    try:
        config = json.loads(raw_config)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid existing OPENCODE_CONFIG_CONTENT: {exc}") from exc
    if not isinstance(config, dict):
        raise SystemExit("existing OPENCODE_CONFIG_CONTENT must be a JSON object")
else:
    config = {}

permission = config.get("permission")
if permission is None:
    permission = {}
elif isinstance(permission, str):
    permission = {"*": permission}
elif isinstance(permission, dict):
    permission = dict(permission)
else:
    raise SystemExit("existing OpenCode permission config must be a string or object")

external = permission.get("external_directory")
if external is None:
    external = {}
elif isinstance(external, str):
    external = {"*": external}
elif isinstance(external, dict):
    external = dict(external)
else:
    raise SystemExit("existing OpenCode external_directory permission must be a string or object")

for value in roots:
    if not isinstance(value, str) or not value:
        raise SystemExit("qualification OpenCode external roots must be non-empty strings")
    root = Path(value).expanduser().resolve()
    if not root.is_absolute() or root == Path("/"):
        raise SystemExit(f"unsafe qualification OpenCode external root: {value!r}")
    pattern = f"{root.as_posix().rstrip('/')}/**"
    external.pop(pattern, None)
    external[pattern] = "allow"

permission["external_directory"] = external
config["permission"] = permission
sys.stdout.write(json.dumps(config, separators=(",", ":")))
PY
}

if [ "$#" -eq 4 ] \
  && [ "$1" = "session" ] \
  && [ "$2" = "list" ] \
  && [ "$3" = "--format" ] \
  && [ "$4" = "json" ]; then
  buffer_json_command "$REAL_OPENCODE" db --format json \
    "SELECT id, parent_id AS parentID, directory FROM session ORDER BY id;"
  exit 0
fi

if [ "$#" -ge 2 ] && [ "$1" = "export" ]; then
  buffer_json_command "$REAL_OPENCODE" "$@"
  exit 0
fi

if [ "$#" -ge 2 ] && [ "$1" = "run" ]; then
  OPENCODE_CONFIG_CONTENT=$(qualification_config_content)
  export OPENCODE_CONFIG_CONTENT
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
