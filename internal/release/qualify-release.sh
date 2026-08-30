#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
: "${AVA_QUALIFICATION_OPENCODE:=opencode}"
export AVA_QUALIFICATION_OPENCODE

resolve_path() {
  python3 - "$1" <<'PY'
from pathlib import Path
import sys

print(Path(sys.argv[1]).expanduser().resolve())
PY
}

run_root_parent=
source_assets=
target_assets=
validate_config_only=false
pending_option=
for arg in "$@"; do
  if [ -n "$pending_option" ]; then
    case "$pending_option" in
      run-root-parent) run_root_parent=$arg ;;
      source-assets) source_assets=$arg ;;
      target-assets) target_assets=$arg ;;
    esac
    pending_option=
    continue
  fi
  case "$arg" in
    --validate-config-only) validate_config_only=true ;;
    --run-root-parent) pending_option=run-root-parent ;;
    --run-root-parent=*) run_root_parent=${arg#*=} ;;
    --source-assets) pending_option=source-assets ;;
    --source-assets=*) source_assets=${arg#*=} ;;
    --target-assets) pending_option=target-assets ;;
    --target-assets=*) target_assets=${arg#*=} ;;
  esac
done
if [ -n "$pending_option" ]; then
  printf '%s\n' "qualify-release.sh: missing value for --$pending_option" >&2
  exit 2
fi

if [ "$validate_config_only" = false ]; then
  requested_parent=${run_root_parent:-${TMPDIR:-/tmp}}
  requested_parent=$(resolve_path "$requested_parent")
  case "$requested_parent" in
    "$ROOT"|"$ROOT"/*)
      printf '%s\n' "qualify-release.sh: run root parent must be outside the Ava repository" >&2
      exit 2
      ;;
  esac
  mkdir -p "$requested_parent"
  operation_parent=$(mktemp -d "$requested_parent/ava-qualification-operation.XXXXXX")
  set -- "$@" --run-root-parent "$operation_parent"

  AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS=$(
    python3 - "$ROOT" "$operation_parent" "$source_assets" "$target_assets" <<'PY'
import json
from pathlib import Path
import sys

repository_root = Path(sys.argv[1]).resolve()
roots: list[Path] = []
for raw in sys.argv[2:]:
    if not raw:
        continue
    candidate = Path(raw).expanduser().resolve()
    if candidate == Path("/"):
        raise SystemExit("qualification OpenCode permission root must not be filesystem root")
    if candidate == repository_root or candidate.is_relative_to(repository_root):
        continue
    if any(candidate == root or candidate.is_relative_to(root) for root in roots):
        continue
    roots = [root for root in roots if not root.is_relative_to(candidate)]
    roots.append(candidate)

if not roots:
    raise SystemExit("qualification OpenCode permission scope is empty")
print(json.dumps([str(root) for root in roots], separators=(",", ":")))
PY
  )
  export AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS
fi

exec python3 "$ROOT/internal/release/qualification_automation.py" \
  "$@" \
  --repository-root "$ROOT" \
  --opencode "$ROOT/internal/release/qualification-opencode.sh"
