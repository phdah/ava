#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
cd "$ROOT"

stage=${1:-}
case "$stage" in
  pre-edge|final) ;;
  *)
    printf 'usage: %s pre-edge|final\n' "$0" >&2
    exit 2
    ;;
esac

command -v gh >/dev/null 2>&1 || {
  printf 'GitHub CLI is required to acquire immutable source assets\n' >&2
  exit 2
}

run_parent=${AVA_QUALIFICATION_RUN_PARENT:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/ava-release-qualification}
mkdir -p "$run_parent"
run_root=$(mktemp -d "$run_parent/run.XXXXXX")
mkdir -p "$run_root/assets/source" "$run_root/fixture" "$run_root/test-project" "$run_root/execution"

pair_json=$(python3 - <<'PY'
import json
from internal.release import qualification_state as state
config, catalog, _ = state.load_configuration(state.REPOSITORY_ROOT)
pair = state.active_pair(config, catalog)
print(json.dumps({"repository": config["repository"], "pair": pair}, sort_keys=True))
PY
)
repository=$(printf '%s' "$pair_json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["repository"])')
source_tag=$(printf '%s' "$pair_json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["pair"]["source"]["tag"])')

printf 'qualification stage: %s\n' "$stage"
printf 'qualification executor: %s\n' "${AVA_QUALIFICATION_EXECUTOR:-direct-shell}"
printf 'source release: %s\n' "$source_tag"

gh release download "$source_tag" -R "$repository" --dir "$run_root/assets/source"
gh release verify "$source_tag" -R "$repository" --format json >/dev/null
for asset in ava-install.sh ava-base.tar.gz ava-guidance.tar.gz ava-migrations.tar.gz ava-release.json ava-release-notes.md SHA256SUMS
do
  gh release verify-asset "$source_tag" "$run_root/assets/source/$asset" -R "$repository" --format json >/dev/null
done

fixture_log=$(TMPDIR="$run_root/fixture" internal/release/generate-synthetic-qualification-vault.sh)
printf '%s\n' "$fixture_log"
qualification_root=$(printf '%s\n' "$fixture_log" | sed -n 's/^synthetic qualification vault ready: //p' | tail -n 1)
[ -n "$qualification_root" ] && [ -d "$qualification_root" ] || {
  printf 'could not resolve generated qualification root\n' >&2
  exit 2
}

cat > "$run_root/test-project/index.md" <<'EOF'
# Qualification test boundary

Repository-external byte-integrity sentinel.
EOF
cat > "$run_root/test-project/sentinel.json" <<'EOF'
{"purpose":"qualification-test-boundary","schema_version":1}
EOF

case "$stage" in
  pre-edge) assembly_phase=edge-independent ;;
  final) assembly_phase=edge-dependent ;;
esac

target_assets=$(internal/release/assemble-candidate.sh --phase "$assembly_phase")

internal/release/qualify-release.sh "$stage" \
  --qualification-root "$qualification_root" \
  --execution-root "$run_root/execution" \
  --source-assets "$run_root/assets/source" \
  --target-assets "$target_assets" \
  --test-project "$run_root/test-project"

printf 'qualification run root: %s\n' "$run_root"
