#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)

for arg in "$@"; do
  case "$arg" in
    --run-root-parent|--run-root-parent=*)
      echo "qualify-release-detached.sh owns --run-root-parent; set AVA_QUALIFICATION_RUN_ROOT_PARENT instead" >&2
      exit 2
      ;;
  esac
done

for command_name in nohup setsid; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "required command not found: $command_name" >&2
    exit 2
  fi
done

umask 077
parent=${AVA_QUALIFICATION_RUN_ROOT_PARENT:-${TMPDIR:-/tmp}}
mkdir -p "$parent"
launch_id="$(date -u +%Y%m%dT%H%M%SZ)-$$"
launch_root="$parent/ava-qualification-launch-$launch_id"
mkdir "$launch_root"
log_path="$launch_root/qualification.log"
pid_path="$launch_root/pid"
: > "$log_path"

nohup setsid sh -c '
  pid_path=$1
  shift
  printf "%s\n" "$$" > "$pid_path"
  exec "$@"
' sh "$pid_path" sh "$ROOT/internal/release/qualify-release.sh" "$@" \
  --run-root-parent "$launch_root" >>"$log_path" 2>&1 </dev/null &
bootstrap_pid=$!

attempt=0
while [ ! -s "$pid_path" ] && [ "$attempt" -lt 10 ]; do
  if ! kill -0 "$bootstrap_pid" 2>/dev/null; then
    break
  fi
  sleep 0.05
  attempt=$((attempt + 1))
done

if [ ! -s "$pid_path" ]; then
  echo "detached qualification failed to start; see $log_path" >&2
  exit 1
fi

pid=$(cat "$pid_path")
if ! kill -0 "$pid" 2>/dev/null; then
  echo "detached qualification exited during launch; see $log_path" >&2
  exit 1
fi

evidence_root=""
attempt=0
while [ "$attempt" -lt 10 ]; do
  for candidate in "$launch_root"/ava-qualification-*; do
    if [ -d "$candidate" ]; then
      evidence_root=$candidate
      break
    fi
  done
  if [ -n "$evidence_root" ] || ! kill -0 "$pid" 2>/dev/null; then
    break
  fi
  sleep 0.05
  attempt=$((attempt + 1))
done

printf "qualification PID: %s\n" "$pid"
printf "detached log: %s\n" "$log_path"
printf "launch root: %s\n" "$launch_root"
if [ -n "$evidence_root" ]; then
  printf "external evidence: %s\n" "$evidence_root"
else
  printf "external evidence: pending under %s\n" "$launch_root"
fi
