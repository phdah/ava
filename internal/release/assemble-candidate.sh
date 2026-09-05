#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd -P)
cd "$ROOT"

phase=edge-dependent
while [ "$#" -gt 0 ]; do
  case "$1" in
    --phase)
      [ "$#" -ge 2 ] || { echo "ERROR: --phase requires a value" >&2; exit 2; }
      phase=$2
      shift 2
      ;;
    --phase=*)
      phase=${1#*=}
      shift
      ;;
    *)
      echo "ERROR: unsupported candidate assembly argument: $1" >&2
      exit 2
      ;;
  esac
done
case "$phase" in
  edge-independent|edge-dependent) ;;
  *)
    echo "ERROR: --phase must be edge-independent or edge-dependent" >&2
    exit 2
    ;;
esac

if [ -n "$(git status --porcelain)" ]; then
  echo "ERROR: Ava repository must be clean before candidate assembly" >&2
  exit 1
fi

version=$(cat version.txt)
revision=$(git rev-parse HEAD)
source_date_epoch=$(git show -s --format=%ct "$revision")
published_at=$(SOURCE_DATE_EPOCH="$source_date_epoch" python3 -c 'import datetime, os; print(datetime.datetime.fromtimestamp(int(os.environ["SOURCE_DATE_EPOCH"]), datetime.timezone.utc).isoformat().replace("+00:00", "Z"))')

case "$version" in
  *-alpha.*) channel=alpha ;;
  *-beta.*) channel=beta ;;
  *-rc.*) channel=rc ;;
  *-*)
    echo "ERROR: unsupported prerelease version: $version" >&2
    exit 1
    ;;
  *) channel=stable ;;
esac

catalog="$ROOT/internal/release/catalogs/$version.json"
root_release=false
if [ "$version" = "1.0.0" ]; then
  root_release=true
fi
if [ "$phase" = edge-dependent ] && [ "$root_release" = false ] && [ ! -f "$catalog" ]; then
  echo "ERROR: missing adjacent release catalog: $catalog" >&2
  exit 1
fi
if [ "$root_release" = true ] && [ -f "$catalog" ]; then
  echo "ERROR: root release 1.0.0 must not define an upgrade edge catalog" >&2
  exit 1
fi

output_parent=${AVA_CANDIDATE_ROOT:-${TMPDIR:-/tmp}}
output_parent=$(python3 -c 'import pathlib, sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$output_parent")
case "$output_parent" in
  "$ROOT"|"$ROOT"/*)
    echo "ERROR: candidate output must be outside the Ava repository" >&2
    exit 1
    ;;
esac
mkdir -p "$output_parent"

short_revision=$(printf '%s' "$revision" | cut -c1-7)
if [ "$phase" = edge-independent ]; then
  output="$output_parent/ava-$version-$short_revision-edge-independent"
else
  output="$output_parent/ava-$version-$short_revision"
fi
if [ -e "$output" ]; then
  echo "ERROR: candidate output already exists: $output" >&2
  exit 1
fi

assemble_without_edge() {
  unset AVA_UPGRADE_CATALOG
  "$ROOT/internal/release/assemble.sh" \
    --output "$output" \
    --version "$version" \
    --channel "$channel" \
    --source-revision "$revision" \
    --source-date-epoch "$source_date_epoch" \
    --published-at "$published_at" \
    --release-notes "$ROOT/CHANGELOG.md" >&2
}

if [ "$phase" = edge-independent ] || [ "$root_release" = true ]; then
  assemble_without_edge
else
  AVA_UPGRADE_CATALOG="$catalog" \
    "$ROOT/internal/release/assemble.sh" \
    --output "$output" \
    --version "$version" \
    --channel "$channel" \
    --source-revision "$revision" \
    --source-date-epoch "$source_date_epoch" \
    --published-at "$published_at" \
    --release-notes "$ROOT/CHANGELOG.md" >&2
fi

printf '%s\n' "$output"
