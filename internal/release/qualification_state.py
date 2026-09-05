"""Current deterministic release qualification state helpers."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from internal.release import qualification_runner

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = REPOSITORY_ROOT / "internal/release/qualification"
SCHEMA_ROOT = STATE_ROOT / "schemas"
MATRIX_PATH = REPOSITORY_ROOT / "internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json"
RELEASE_ASSETS = qualification_runner.RELEASE_ASSETS
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PAIR_STATUSES = {
    "not-run",
    "running",
    "failed",
    "needs-review",
    "awaiting-user-signoff",
    "accepted",
    "rejected",
}
BOOTSTRAP_VERSION = "0.0.0"
FIRST_RELEASE_VERSION = "1.0.0"


class QualificationStateError(RuntimeError):
    pass


class CommandResult:
    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_inventory(root: Path, *, exclude: Iterable[Path] = ()) -> list[dict[str, Any]]:
    excluded = tuple(path.resolve() for path in exclude)
    records: list[dict[str, Any]] = []
    if not root.exists():
        return records
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(root).as_posix().encode(),
    ):
        resolved = path.resolve()
        if any(resolved == base or resolved.is_relative_to(base) for base in excluded):
            continue
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    return records


def tree_digest(root: Path, *, exclude: Iterable[Path] = ()) -> str:
    return sha256_text(canonical_json(tree_inventory(root, exclude=exclude)))


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationStateError(f"cannot read JSON {path}: {exc}") from exc


def _type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def validate_schema(value: Any, schema: dict[str, Any], *, label: str, path: str = "$") -> None:
    expected = schema.get("type")
    if isinstance(expected, str) and not _type_ok(value, expected):
        raise QualificationStateError(f"{label}: {path} must be {expected}")
    if isinstance(expected, list) and not any(_type_ok(value, item) for item in expected):
        raise QualificationStateError(f"{label}: {path} has invalid type")
    if "const" in schema and value != schema["const"]:
        raise QualificationStateError(f"{label}: {path} must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise QualificationStateError(f"{label}: {path} must be one of {schema['enum']}")
    if isinstance(value, str):
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, value) is None:
            raise QualificationStateError(f"{label}: {path} does not match required pattern")
        if "minLength" in schema and len(value) < schema["minLength"]:
            raise QualificationStateError(f"{label}: {path} is too short")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise QualificationStateError(f"{label}: {path} has too few items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                raise QualificationStateError(f"{label}: {path} contains duplicate items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema(item, item_schema, label=label, path=f"{path}[{index}]")
    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                raise QualificationStateError(f"{label}: {path}.{required} is required")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, item in value.items():
                if key in properties:
                    validate_schema(item, properties[key], label=label, path=f"{path}.{key}")
                elif schema.get("additionalProperties") is False:
                    raise QualificationStateError(f"{label}: unexpected field {path}.{key}")


def run_command(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
) -> CommandResult:
    result = subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    command = CommandResult(result.returncode, result.stdout, result.stderr)
    if check and result.returncode != 0:
        raise QualificationStateError(
            f"command failed ({result.returncode}): {' '.join(args)}\n{result.stderr.strip()}"
        )
    return command


def require_clean_repository(repository_root: Path) -> None:
    result = run_command(
        ["git", "-C", str(repository_root), "status", "--porcelain"],
        check=False,
    )
    if result.returncode != 0:
        raise QualificationStateError(
            f"cannot inspect repository cleanliness: {result.stderr.strip()}"
        )
    if result.stdout.strip():
        raise QualificationStateError(
            "Ava repository must be clean before qualification starts"
        )


def repository_revision(repository_root: Path) -> str:
    result = run_command(["git", "-C", str(repository_root), "rev-parse", "HEAD"])
    revision = result.stdout.strip()
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise QualificationStateError(f"invalid repository revision: {revision!r}")
    return revision


def release_asset_digests(directory: Path) -> dict[str, str]:
    return {name: sha256_file(directory / name) for name in RELEASE_ASSETS}


def matrix_digest(repository_root: Path) -> str:
    return sha256_file(
        repository_root
        / "internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json"
    )


def reject_mutable_tag(tag: str) -> None:
    if not tag or tag.lower() == "latest" or "/" in tag:
        raise QualificationStateError(
            f"release tag must be exact and immutable, got {tag!r}"
        )


def validate_catalog_selection(selection: dict[str, Any], *, label: str) -> None:
    kind = selection.get("kind")
    version = selection.get("version")
    if kind == "bootstrap":
        if selection != {"kind": "bootstrap", "version": BOOTSTRAP_VERSION}:
            raise QualificationStateError(
                f"{label} bootstrap selection must be exactly the internal {BOOTSTRAP_VERSION} sentinel"
            )
        return

    tag = selection.get("tag")
    if kind not in {"published", "local"}:
        raise QualificationStateError(
            f"{label} kind must be bootstrap, published, or local"
        )
    if not isinstance(version, str) or not version:
        raise QualificationStateError(f"{label} version is required")
    if tag != f"v{version}":
        raise QualificationStateError(f"{label} tag must be the exact v-prefixed version")
    reject_mutable_tag(tag)
    if kind == "published":
        revision = selection.get("source_revision")
        manifest_digest = selection.get("release_manifest_sha256")
        digests = selection.get("asset_sha256")
        if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
            raise QualificationStateError(f"{label} published source revision is required")
        if not isinstance(manifest_digest, str) or SHA256_RE.fullmatch(manifest_digest) is None:
            raise QualificationStateError(
                f"{label} published release manifest digest is required"
            )
        if not isinstance(digests, dict) or set(digests) != set(RELEASE_ASSETS):
            raise QualificationStateError(
                f"{label} published asset digest inventory must contain exactly seven assets"
            )
        if any(
            not isinstance(value, str) or SHA256_RE.fullmatch(value) is None
            for value in digests.values()
        ):
            raise QualificationStateError(
                f"{label} published asset digest inventory is invalid"
            )


def load_configuration(
    repository_root: Path = REPOSITORY_ROOT,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    state_root = repository_root / "internal/release/qualification"
    schema_root = state_root / "schemas"

    def validated(name: str, schema_name: str) -> Any:
        value = load_json(state_root / name)
        schema = load_json(schema_root / schema_name)
        validate_schema(value, schema, label=name)
        return value

    config = validated("config.json", "config.schema.json")
    catalog = validated("pair-catalog.json", "pair-catalog.schema.json")
    current = validated("current-state.json", "current-state.schema.json")
    pair_ids = [pair["id"] for pair in catalog["pairs"]]
    if len(pair_ids) != len(set(pair_ids)):
        raise QualificationStateError("pair catalog contains duplicate IDs")
    if config["active_pair"] not in pair_ids:
        raise QualificationStateError("active pair is not present in pair catalog")
    if set(current["pairs"]) != set(pair_ids):
        raise QualificationStateError("current state pair inventory differs from pair catalog")
    if current.get("active_pair") != config["active_pair"]:
        raise QualificationStateError(
            "current state active pair differs from qualification configuration"
        )
    catalog_by_id = {pair["id"]: pair for pair in catalog["pairs"]}
    for pair_id, pair_state in current["pairs"].items():
        if not isinstance(pair_state, dict):
            raise QualificationStateError(
                f"current state for {pair_id} must be an object"
            )
        if pair_state.get("historical") is not catalog_by_id[pair_id]["historical"]:
            raise QualificationStateError(
                f"current state historical flag differs for {pair_id}"
            )
        if pair_state.get("status") not in PAIR_STATUSES:
            raise QualificationStateError(
                f"current state has invalid status for {pair_id}"
            )
    for pair in catalog["pairs"]:
        validate_catalog_selection(pair["source"], label=f"{pair['id']} source")
        validate_catalog_selection(pair["target"], label=f"{pair['id']} target")
        if pair["source"].get("kind") == "bootstrap":
            if pair["target"].get("kind") != "local" or pair["target"].get("version") != FIRST_RELEASE_VERSION:
                raise QualificationStateError(
                    "bootstrap qualification may target only the local first stable 1.0.0 release"
                )
    return config, catalog, current


def active_pair(config: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    matches = [pair for pair in catalog["pairs"] if pair["id"] == config["active_pair"]]
    if len(matches) != 1:
        raise QualificationStateError(
            "checked-in active release pair must resolve exactly once"
        )
    return matches[0]


def utc_run_id(pair_id: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{stamp}-{pair_id}"
