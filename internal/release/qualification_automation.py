#!/usr/bin/env python3
"""Run hands-off repository-only Ava release qualification and record compact evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from internal.release import qualification_runner

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = REPOSITORY_ROOT / "internal/release/qualification"
RUNS_ROOT = STATE_ROOT / "runs"
CONFIG_PATH = STATE_ROOT / "config.json"
PAIR_CATALOG_PATH = STATE_ROOT / "pair-catalog.json"
CURRENT_STATE_PATH = STATE_ROOT / "current-state.json"
SCHEMA_ROOT = STATE_ROOT / "schemas"
AUDIT_PROMPT_PATH = STATE_ROOT / "audit-prompt.md"
FIXTURE_ROOT = REPOSITORY_ROOT / "internal/release/fixtures/synthetic-qualification-vault"
IMAGE_MANIFEST_PATH = FIXTURE_ROOT / "images/manifest.json"
MATRIX_PATH = FIXTURE_ROOT / "qualification-matrix.json"
GENERATOR = REPOSITORY_ROOT / "internal/release/generate-synthetic-qualification-vault.sh"
RUNNER = REPOSITORY_ROOT / "internal/release/qualify-synthetic.sh"
RELEASE_ASSETS = qualification_runner.RELEASE_ASSETS
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SESSION_ID_RE = re.compile(r"\bses_[A-Za-z0-9]+\b")
PAIR_STATUSES = {
    "not-run",
    "running",
    "failed",
    "needs-review",
    "awaiting-user-signoff",
    "accepted",
    "rejected",
}


class AutomationError(RuntimeError):
    pass


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class ResolvedRelease:
    kind: str
    identity: qualification_runner.ReleaseIdentity
    release_manifest_sha256: str
    asset_sha256: dict[str, str]
    attested: bool

    def compact(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "version": self.identity.version,
            "tag": self.identity.tag,
            "source_revision": self.identity.revision,
            "release_manifest_sha256": self.release_manifest_sha256,
            "asset_sha256": self.asset_sha256,
            "attested": self.attested,
        }


RunnerFn = Callable[..., CommandResult]


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
        raise AutomationError(f"cannot read JSON {path}: {exc}") from exc


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
        raise AutomationError(f"{label}: {path} must be {expected}")
    if isinstance(expected, list) and not any(_type_ok(value, item) for item in expected):
        raise AutomationError(f"{label}: {path} has invalid type")

    if "const" in schema and value != schema["const"]:
        raise AutomationError(f"{label}: {path} must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise AutomationError(f"{label}: {path} must be one of {schema['enum']}")
    if isinstance(value, str):
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, value) is None:
            raise AutomationError(f"{label}: {path} does not match required pattern")
        if "minLength" in schema and len(value) < schema["minLength"]:
            raise AutomationError(f"{label}: {path} is too short")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise AutomationError(f"{label}: {path} has too few items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                raise AutomationError(f"{label}: {path} contains duplicate items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema(item, item_schema, label=label, path=f"{path}[{index}]")

    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                raise AutomationError(f"{label}: {path}.{required} is required")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, item in value.items():
                if key in properties:
                    validate_schema(item, properties[key], label=label, path=f"{path}.{key}")
                elif schema.get("additionalProperties") is False:
                    raise AutomationError(f"{label}: unexpected field {path}.{key}")


def validate_file_against_schema(path: Path, schema_name: str) -> Any:
    value = load_json(path)
    schema = load_json(SCHEMA_ROOT / schema_name)
    validate_schema(value, schema, label=str(path))
    return value


def require_clean_repository(repository_root: Path) -> None:
    result = run_command(
        ["git", "-C", str(repository_root), "status", "--porcelain"],
        check=False,
    )
    if result.returncode != 0:
        raise AutomationError(f"cannot inspect repository cleanliness: {result.stderr.strip()}")
    if result.stdout.strip():
        raise AutomationError("Ava repository must be clean before qualification automation starts")


def repository_revision(repository_root: Path) -> str:
    result = run_command(["git", "-C", str(repository_root), "rev-parse", "HEAD"])
    revision = result.stdout.strip()
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise AutomationError(f"invalid repository revision: {revision!r}")
    return revision


def run_command(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> CommandResult:
    result = subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    command = CommandResult(result.returncode, result.stdout, result.stderr)
    if check and result.returncode != 0:
        raise AutomationError(
            f"command failed ({result.returncode}): {' '.join(args)}\n{result.stderr.strip()}"
        )
    return command


def reject_mutable_tag(tag: str) -> None:
    if not tag or tag.lower() == "latest" or "/" in tag:
        raise AutomationError(f"release tag must be exact and immutable, got {tag!r}")


def release_asset_digests(directory: Path) -> dict[str, str]:
    return {name: sha256_file(directory / name) for name in RELEASE_ASSETS}


def resolve_local_release(
    selection: dict[str, Any],
    directory: Path,
    *,
    label: str,
) -> ResolvedRelease:
    resolved = directory.expanduser().resolve()
    identity = qualification_runner.validate_asset_dir(resolved, label)
    expected_version = selection.get("version")
    expected_tag = selection.get("tag")
    expected_revision = selection.get("source_revision")
    if expected_version and identity.version != expected_version:
        raise AutomationError(
            f"{label} version mismatch: expected {expected_version}, got {identity.version}"
        )
    if expected_tag and identity.tag != expected_tag:
        raise AutomationError(f"{label} tag mismatch: expected {expected_tag}, got {identity.tag}")
    if expected_revision and identity.revision != expected_revision:
        raise AutomationError(
            f"{label} source revision mismatch: expected {expected_revision}, got {identity.revision}"
        )
    return ResolvedRelease(
        kind="local",
        identity=identity,
        release_manifest_sha256=sha256_file(resolved / "ava-release.json"),
        asset_sha256=release_asset_digests(resolved),
        attested=False,
    )


def acquire_published_release(
    selection: dict[str, Any],
    destination: Path,
    *,
    repository: str,
    gh: str,
    command_runner: RunnerFn = run_command,
) -> ResolvedRelease:
    tag = selection.get("tag")
    if not isinstance(tag, str):
        raise AutomationError("published release selection requires an exact tag")
    reject_mutable_tag(tag)
    if destination.exists():
        if destination.is_symlink() or any(destination.iterdir()):
            raise AutomationError(f"published asset destination must be empty: {destination}")
    else:
        destination.mkdir(parents=True)

    view = command_runner(
        [gh, "release", "view", tag, "-R", repository, "--json", "tagName,isDraft,isImmutable"],
        check=True,
    )
    try:
        release_metadata = json.loads(view.stdout)
    except json.JSONDecodeError as exc:
        raise AutomationError(f"{tag} release metadata is not JSON") from exc
    if (
        release_metadata.get("tagName") != tag
        or release_metadata.get("isDraft") is not False
        or release_metadata.get("isImmutable") is not True
    ):
        raise AutomationError(f"{tag} is not the exact published immutable release")

    command_runner(
        [gh, "release", "download", tag, "-R", repository, "--dir", str(destination)],
        check=True,
    )
    entries = list(destination.iterdir())
    actual_names = {path.name for path in entries}
    if (
        actual_names != set(RELEASE_ASSETS)
        or any(path.is_symlink() or not path.is_file() for path in entries)
    ):
        raise AutomationError(
            f"{tag} release asset inventory mismatch: expected seven normal files {sorted(RELEASE_ASSETS)}, got {sorted(actual_names)}"
        )

    verify = command_runner(
        [gh, "release", "verify", tag, "-R", repository, "--format", "json"],
        check=False,
    )
    if verify.returncode != 0:
        raise AutomationError(f"{tag} immutable release attestation verification failed")

    for name in RELEASE_ASSETS:
        asset_verify = command_runner(
            [
                gh,
                "release",
                "verify-asset",
                tag,
                str(destination / name),
                "-R",
                repository,
                "--format",
                "json",
            ],
            check=False,
        )
        if asset_verify.returncode != 0:
            raise AutomationError(f"{tag} release asset attestation failed for {name}")

    identity = qualification_runner.validate_asset_dir(destination, f"published {tag}")
    expected_version = selection.get("version")
    expected_revision = selection.get("source_revision")
    if expected_version and identity.version != expected_version:
        raise AutomationError(f"{tag} version mismatch: {identity.version}")
    if expected_revision and identity.revision != expected_revision:
        raise AutomationError(
            f"{tag} source revision mismatch: expected {expected_revision}, got {identity.revision}"
        )

    manifest_digest = sha256_file(destination / "ava-release.json")
    expected_manifest_digest = selection.get("release_manifest_sha256")
    if expected_manifest_digest and manifest_digest != expected_manifest_digest:
        raise AutomationError(f"{tag} release manifest digest differs from checked-in catalog")

    digests = release_asset_digests(destination)
    expected_digests = selection.get("asset_sha256")
    if isinstance(expected_digests, dict) and expected_digests and digests != expected_digests:
        raise AutomationError(f"{tag} release asset digests differ from checked-in catalog")

    return ResolvedRelease(
        kind="published",
        identity=identity,
        release_manifest_sha256=manifest_digest,
        asset_sha256=digests,
        attested=True,
    )


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise AutomationError(f"pinned image is not a PNG: {path}")
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def validate_pinned_images(repository_root: Path = REPOSITORY_ROOT) -> dict[str, Any]:
    manifest_path = repository_root / IMAGE_MANIFEST_PATH.relative_to(REPOSITORY_ROOT)
    manifest = load_json(manifest_path)
    images = manifest.get("images")
    if manifest.get("schema_version") != 1 or not isinstance(images, list) or len(images) != 5:
        raise AutomationError("pinned qualification image manifest must contain exactly five images")
    seen_files: set[str] = set()
    seen_destinations: set[str] = set()
    for item in images:
        if not isinstance(item, dict):
            raise AutomationError("pinned image manifest contains a non-object record")
        filename = item.get("file")
        destination = item.get("destination")
        if not isinstance(filename, str) or not isinstance(destination, str):
            raise AutomationError("pinned image manifest requires file and destination")
        if filename in seen_files or destination in seen_destinations:
            raise AutomationError("pinned image manifest contains duplicate file or destination")
        seen_files.add(filename)
        seen_destinations.add(destination)
        path = manifest_path.parent / filename
        if path.is_symlink() or not path.is_file():
            raise AutomationError(f"missing pinned qualification image: {path}")
        if item.get("media_type") != "image/png":
            raise AutomationError(f"unsupported pinned image media type for {filename}")
        if path.stat().st_size != item.get("bytes"):
            raise AutomationError(f"pinned image byte-size mismatch for {filename}")
        if sha256_file(path) != item.get("sha256"):
            raise AutomationError(f"pinned image digest mismatch for {filename}")
        width, height = png_dimensions(path)
        if width != item.get("width") or height != item.get("height"):
            raise AutomationError(f"pinned image dimensions mismatch for {filename}")
        if not destination.startswith("corpus/") or ".." in Path(destination).parts:
            raise AutomationError(f"unsafe pinned image destination for {filename}: {destination}")
    return manifest


def parse_generated_fixture(stdout: str, fixture_parent: Path) -> Path:
    prefix = "synthetic qualification vault ready: "
    matches = [line[len(prefix):] for line in stdout.splitlines() if line.startswith(prefix)]
    if len(matches) != 1:
        raise AutomationError("fixture generator did not report exactly one ready path")
    result = Path(matches[0]).expanduser().resolve()
    parent = fixture_parent.resolve()
    if not result.is_relative_to(parent) or not result.is_dir():
        raise AutomationError(f"fixture generator returned unsafe output path: {result}")
    return result


def generate_fixture(
    repository_root: Path,
    fixture_parent: Path,
    *,
    command_runner: RunnerFn = run_command,
) -> Path:
    fixture_parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TMPDIR"] = str(fixture_parent)
    result = command_runner(
        ["sh", str(repository_root / "internal/release/generate-synthetic-qualification-vault.sh")],
        cwd=repository_root,
        env=env,
        check=True,
    )
    return parse_generated_fixture(result.stdout, fixture_parent)


def create_test_project(path: Path) -> None:
    path.mkdir(parents=True)
    (path / "index.md").write_text(
        "# Qualification test boundary\n\nRepository-external byte-integrity sentinel.\n",
        encoding="utf-8",
    )
    (path / "sentinel.json").write_text(
        canonical_json({"schema_version": 1, "purpose": "qualification-test-boundary"}),
        encoding="utf-8",
    )


def opencode_version(opencode: str, *, command_runner: RunnerFn = run_command) -> str:
    result = command_runner([opencode, "--version"], check=True)
    version = result.stdout.strip() or result.stderr.strip()
    if not version:
        raise AutomationError("OpenCode version command returned no version")
    return version


def matrix_digest(repository_root: Path) -> str:
    return sha256_file(repository_root / MATRIX_PATH.relative_to(REPOSITORY_ROOT))


def execution_root_for_identity(parent: Path, identity_sha256: str) -> Path:
    if not SHA256_RE.fullmatch(identity_sha256):
        raise AutomationError("execution identity must be a SHA-256 digest")
    return parent / identity_sha256


def execution_identity(
    *,
    source: ResolvedRelease,
    target: ResolvedRelease,
    image_manifest_sha256: str,
    pinned_images: list[dict[str, Any]],
    fixture_generator_sha256: str,
    fixture_inventory_sha256: str,
    matrix_sha256: str,
    repository_revision_value: str,
    runner_sha256: str,
    automation_sha256: str,
    opencode_version_value: str,
    qualification_model: str,
    audit_model: str,
) -> tuple[str, dict[str, Any]]:
    payload = {
        "schema_version": 1,
        "source": source.compact(),
        "target": target.compact(),
        "image_manifest_sha256": image_manifest_sha256,
        "pinned_images": pinned_images,
        "fixture_generator_sha256": fixture_generator_sha256,
        "fixture_inventory_sha256": fixture_inventory_sha256,
        "matrix_sha256": matrix_sha256,
        "repository_revision": repository_revision_value,
        "runner_sha256": runner_sha256,
        "automation_sha256": automation_sha256,
        "opencode_version": opencode_version_value,
        "qualification_model": qualification_model,
        "audit_model": audit_model,
    }
    return sha256_text(canonical_json(payload)), payload


def load_configuration(repository_root: Path = REPOSITORY_ROOT) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    state_root = repository_root / STATE_ROOT.relative_to(REPOSITORY_ROOT)
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
        raise AutomationError("pair catalog contains duplicate IDs")
    if config["active_pair"] not in pair_ids:
        raise AutomationError("active pair is not present in pair catalog")
    if set(current["pairs"]) != set(pair_ids):
        raise AutomationError("current state pair inventory differs from pair catalog")
    if current.get("active_pair") != config["active_pair"]:
        raise AutomationError("current state active pair differs from qualification configuration")
    catalog_by_id = {pair["id"]: pair for pair in catalog["pairs"]}
    for pair_id, state in current["pairs"].items():
        if not isinstance(state, dict):
            raise AutomationError(f"current state for {pair_id} must be an object")
        if state.get("historical") is not catalog_by_id[pair_id]["historical"]:
            raise AutomationError(f"current state historical flag differs for {pair_id}")
        if state.get("status") not in PAIR_STATUSES:
            raise AutomationError(f"current state has invalid status for {pair_id}")
        latest_run_id = state.get("latest_run_id")
        if latest_run_id is not None and not isinstance(latest_run_id, str):
            raise AutomationError(f"current state latest_run_id is invalid for {pair_id}")
        signoff = state.get("user_signoff")
        if signoff is not None:
            if not isinstance(signoff, dict) or set(signoff) != {"identity", "time"}:
                raise AutomationError(f"current state user_signoff is invalid for {pair_id}")
            if not all(isinstance(signoff[key], str) and signoff[key] for key in ("identity", "time")):
                raise AutomationError(f"current state user_signoff is incomplete for {pair_id}")
    historical = next((pair for pair in catalog["pairs"] if pair["id"] == "alpha13-to-alpha14"), None)
    if not historical or historical.get("historical") is not True:
        raise AutomationError("historical alpha.13 to alpha.14 pair is missing")
    for pair in catalog["pairs"]:
        validate_catalog_selection(pair["source"], label=f"{pair['id']} source")
        validate_catalog_selection(pair["target"], label=f"{pair['id']} target")
    for field in ("qualification_model", "audit_model"):
        validate_model_identifier(config[field], field=field)
    return config, catalog, current


def validate_model_identifier(value: str, *, field: str) -> None:
    author, separator, model = value.partition("/")
    if not separator or not author or not model:
        raise AutomationError(
            f"{field} must be an explicit author/model identifier (any provider or tool)"
        )


def validate_catalog_selection(selection: dict[str, Any], *, label: str) -> None:
    kind = selection.get("kind")
    version = selection.get("version")
    tag = selection.get("tag")
    if kind not in {"published", "local"}:
        raise AutomationError(f"{label} kind must be published or local")
    if not isinstance(version, str) or not version:
        raise AutomationError(f"{label} version is required")
    if tag != f"v{version}":
        raise AutomationError(f"{label} tag must be the exact v-prefixed version")
    reject_mutable_tag(tag)
    if kind == "published":
        revision = selection.get("source_revision")
        manifest_digest = selection.get("release_manifest_sha256")
        digests = selection.get("asset_sha256")
        if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
            raise AutomationError(f"{label} published source revision is required")
        if not isinstance(manifest_digest, str) or SHA256_RE.fullmatch(manifest_digest) is None:
            raise AutomationError(f"{label} published release manifest digest is required")
        if not isinstance(digests, dict) or set(digests) != set(RELEASE_ASSETS):
            raise AutomationError(f"{label} published asset digest inventory must contain exactly seven assets")
        if any(not isinstance(value, str) or SHA256_RE.fullmatch(value) is None for value in digests.values()):
            raise AutomationError(f"{label} published asset digest inventory is invalid")


def active_pair(config: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    matches = [pair for pair in catalog["pairs"] if pair["id"] == config["active_pair"]]
    if len(matches) != 1:
        raise AutomationError("checked-in active release pair must resolve exactly once")
    return matches[0]


def resolve_release(
    selection: dict[str, Any],
    *,
    local_path: Path | None,
    destination: Path,
    repository: str,
    gh: str,
    label: str,
    command_runner: RunnerFn = run_command,
) -> ResolvedRelease:
    kind = selection["kind"]
    if kind == "published":
        if local_path is not None:
            raise AutomationError(f"{label} is published; do not supply a local asset directory")
        return acquire_published_release(
            selection,
            destination,
            repository=repository,
            gh=gh,
            command_runner=command_runner,
        )
    if kind == "local":
        if local_path is None:
            raise AutomationError(f"{label} requires an exact caller-supplied local asset directory")
        return resolve_local_release(selection, local_path, label=label)
    raise AutomationError(f"unsupported {label} release kind: {kind}")


def snapshot_sessions(opencode: str, *, command_runner: RunnerFn = run_command) -> list[dict[str, Any]]:
    result = command_runner([opencode, "session", "list", "--format", "json"], check=True)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AutomationError("OpenCode session list did not emit JSON") from exc
    if isinstance(payload, dict):
        payload = payload.get("sessions")
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise AutomationError("OpenCode session list JSON is not a session array")
    return payload


def _session_id(item: dict[str, Any]) -> str | None:
    for key in ("id", "sessionID", "sessionId"):
        value = item.get(key)
        if isinstance(value, str) and SESSION_ID_RE.fullmatch(value):
            return value
    return None


def _parent_id(item: dict[str, Any]) -> str | None:
    for key in ("parentID", "parentId", "parent_id"):
        value = item.get(key)
        if isinstance(value, str) and SESSION_ID_RE.fullmatch(value):
            return value
    return None


def _directory(item: dict[str, Any]) -> str | None:
    value = item.get("directory")
    return value if isinstance(value, str) and value else None


def _collect_strings(value: Any) -> list[str]:
    result: list[str] = []
    if isinstance(value, str):
        result.append(value)
    elif isinstance(value, list):
        for item in value:
            result.extend(_collect_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            result.extend(_collect_strings(item))
    return result


def _first_user_prompt(value: Any) -> str | None:
    if isinstance(value, dict):
        if value.get("role") == "user":
            text_values: list[str] = []
            parts = value.get("parts")
            if isinstance(parts, list):
                for part in parts:
                    if isinstance(part, dict) and isinstance(part.get("text"), str):
                        text_values.append(part["text"])
            if text_values:
                return "\n".join(text_values)
        for child in value.values():
            found = _first_user_prompt(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _first_user_prompt(child)
            if found:
                return found
    return None


def _model_from_export(value: Any) -> str | None:
    if isinstance(value, dict):
        provider = value.get("providerID") or value.get("providerId")
        model = value.get("modelID") or value.get("modelId")
        if isinstance(provider, str) and isinstance(model, str):
            return f"{provider}/{model}"
        for child in value.values():
            found = _model_from_export(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _model_from_export(child)
            if found:
                return found
    return None


def runner_prompt_map(execution_root: Path) -> tuple[dict[str, str], dict[str, str]]:
    scenario_for_session: dict[str, str] = {}
    prompt_for_session: dict[str, str] = {}
    scenarios_root = execution_root / "scenarios"
    if not scenarios_root.is_dir():
        return scenario_for_session, prompt_for_session
    for scenario_dir in scenarios_root.iterdir():
        if not scenario_dir.is_dir():
            continue
        log = scenario_dir / "runner-commands.jsonl"
        if not log.is_file():
            continue
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("label") != "OpenCode prompt":
                continue
            command = record.get("command")
            if not isinstance(command, list) or not command or not isinstance(command[-1], str):
                continue
            prompt = command[-1]
            combined = f"{record.get('stdout', '')}\n{record.get('stderr', '')}"
            ids = SESSION_ID_RE.findall(combined)
            for session_id in ids:
                scenario_for_session.setdefault(session_id, scenario_dir.name)
                prompt_for_session.setdefault(session_id, prompt)
    return scenario_for_session, prompt_for_session


def build_session_inventory(
    *,
    before: list[dict[str, Any]],
    after: list[dict[str, Any]],
    execution_root: Path,
    opencode: str,
    configured_model: str,
    command_runner: RunnerFn = run_command,
    allow_empty: bool = False,
) -> dict[str, Any]:
    before_ids = {_session_id(item) for item in before}
    before_ids.discard(None)
    after_by_id = {_session_id(item): item for item in after if _session_id(item)}
    new_ids = set(after_by_id) - before_ids
    direct_scenario, direct_prompt = runner_prompt_map(execution_root)
    execution_root_resolved = execution_root.resolve()

    relevant: set[str] = set()
    for session_id in new_ids:
        item = after_by_id[session_id]
        if _parent_id(item) is not None:
            continue
        belongs_to_execution = session_id in direct_scenario
        directory = _directory(item)
        if directory:
            try:
                belongs_to_execution = belongs_to_execution or Path(directory).expanduser().resolve().is_relative_to(
                    execution_root_resolved
                )
            except OSError:
                pass
        if belongs_to_execution:
            relevant.add(session_id)

    changed = True
    while changed:
        changed = False
        for session_id in new_ids:
            if session_id in relevant:
                continue
            item = after_by_id[session_id]
            parent = _parent_id(item)
            if parent in relevant:
                relevant.add(session_id)
                changed = True

    if not relevant:
        if allow_empty:
            return {"schema_version": 1, "sessions": []}
        raise AutomationError("qualification produced no discoverable OpenCode sessions")

    exports: dict[str, Any] = {}
    export_text: dict[str, str] = {}
    for session_id in sorted(relevant):
        result = command_runner([opencode, "export", session_id], check=True)
        export_text[session_id] = result.stdout
        try:
            exports[session_id] = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise AutomationError(f"OpenCode export is not JSON for {session_id}") from exc

    records: list[dict[str, Any]] = []
    for session_id in sorted(relevant):
        item = after_by_id[session_id]
        parent = _parent_id(item)
        scenario = direct_scenario.get(session_id)
        ancestor = parent
        seen: set[str] = set()
        while scenario is None and ancestor and ancestor not in seen:
            seen.add(ancestor)
            scenario = direct_scenario.get(ancestor)
            ancestor = _parent_id(after_by_id.get(ancestor, {}))

        prompt = direct_prompt.get(session_id) or _first_user_prompt(exports[session_id])
        if not prompt:
            raise AutomationError(f"cannot recover prompt for OpenCode session {session_id}")
        model = _model_from_export(exports[session_id]) or configured_model
        directory = _directory(item)
        if not directory:
            strings = _collect_strings(exports[session_id])
            directory = next(
                (value for value in strings if value.startswith("/") and Path(value).is_absolute()),
                None,
            )
        if not directory:
            raise AutomationError(f"cannot recover project root for OpenCode session {session_id}")
        resolved_directory = Path(directory).expanduser().resolve()
        if not resolved_directory.is_relative_to(execution_root_resolved):
            raise AutomationError(
                f"OpenCode session {session_id} project root is outside qualification execution root"
            )

        if scenario is None:
            for scenario_dir in (execution_root / "scenarios").iterdir():
                if scenario_dir.is_dir() and resolved_directory.is_relative_to(scenario_dir.resolve()):
                    scenario = scenario_dir.name
                    break
        if scenario is None:
            raise AutomationError(f"cannot bind OpenCode session {session_id} to a qualification scenario")

        records.append(
            {
                "session_id": session_id,
                "parent_session_id": parent,
                "scenario": scenario,
                "prompt_sha256": sha256_text(prompt),
                "model": model,
                "project_root": str(resolved_directory),
                "transcript_sha256": sha256_text(export_text[session_id]),
                "terminal_state": "completed",
            }
        )

    ids = {item["session_id"] for item in records}
    for record in records:
        parent = record["parent_session_id"]
        if parent is not None and parent not in ids:
            raise AutomationError(f"session inventory is missing current-run parent session {parent}")

    return {"schema_version": 1, "sessions": records}


def extract_audit_json(stdout: str) -> dict[str, Any]:
    candidates: list[str] = [stdout]
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        candidates.extend(_collect_strings(event))
    for candidate in reversed(candidates):
        text = candidate.strip()
        if text.startswith("```") and text.endswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1]).strip()
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("schema_version") == 1 and "findings" in value:
            return value
    raise AutomationError("audit session did not emit a machine-readable audit object")


def build_audit_prompt(
    *,
    pair_id: str,
    run_id: str,
    execution_identity_sha256: str,
    session_inventory_path: Path,
    runner_summary_path: Path,
    qualification_root: Path,
    source_assets: Path,
    target_assets: Path,
    repository_root: Path,
) -> str:
    maintained = (repository_root / AUDIT_PROMPT_PATH.relative_to(REPOSITORY_ROOT)).read_text(encoding="utf-8")
    return (
        maintained
        + "\n\n# Run inputs\n\n"
        + f"- pair_id: `{pair_id}`\n"
        + f"- run_id: `{run_id}`\n"
        + f"- execution_identity_sha256: `{execution_identity_sha256}`\n"
        + f"- session_inventory: `{session_inventory_path}`\n"
        + f"- runner_summary: `{runner_summary_path}`\n"
        + f"- qualification_root: `{qualification_root}`\n"
        + f"- source_assets: `{source_assets}`\n"
        + f"- target_assets: `{target_assets}`\n"
        + f"- release_contracts: `{repository_root / 'distribution'}` and `{repository_root / 'internal/release'}`\n"
        + "\nReturn only the JSON object required by the maintained audit-output schema.\n"
    )


def run_audit(
    *,
    opencode: str,
    audit_model: str,
    prompt: str,
    repository_root: Path,
    raw_evidence_root: Path,
    command_runner: RunnerFn = run_command,
) -> tuple[dict[str, Any], str]:
    before_repo = tree_digest(repository_root, exclude=[repository_root / ".git"])
    before_raw = tree_digest(raw_evidence_root)
    result = command_runner(
        [
            opencode,
            "run",
            "--dir",
            str(repository_root),
            "--model",
            audit_model,
            "--format",
            "json",
            "--title",
            "Ava qualification independent audit",
            prompt,
        ],
        check=False,
    )
    if result.returncode != 0:
        raise AutomationError(f"independent audit session failed: {result.stderr.strip()}")
    if tree_digest(repository_root, exclude=[repository_root / ".git"]) != before_repo:
        raise AutomationError("independent audit mutated the Ava repository")
    if tree_digest(raw_evidence_root) != before_raw:
        raise AutomationError("independent audit mutated qualification evidence")
    audit = extract_audit_json(result.stdout)
    schema = load_json(
        repository_root / SCHEMA_ROOT.relative_to(REPOSITORY_ROOT) / "audit-output.schema.json"
    )
    validate_schema(audit, schema, label="audit output")
    return audit, result.stdout


def audit_status(audit: dict[str, Any]) -> tuple[str, int]:
    severities = {item["severity"] for item in audit["findings"]}
    if {"blocker", "major"} & severities:
        return "needs-review", 1
    if audit["terminal_conclusion"] == "needs-review":
        return "needs-review", 1
    return "awaiting-user-signoff", 0


def qualification_exit(summary: dict[str, Any]) -> int:
    outcomes = summary.get("outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        return 1
    return (
        0
        if all(
            isinstance(item, dict)
            and item.get("outcome") in qualification_runner.PASSING_OUTCOMES
            for item in outcomes
        )
        else 1
    )


def write_compact_evidence(
    *,
    repository_root: Path,
    run_id: str,
    pair_id: str,
    execution_identity_sha256: str,
    execution_identity_payload: dict[str, Any],
    source: ResolvedRelease,
    target: ResolvedRelease,
    opencode_version_value: str,
    qualification_model: str,
    audit_model: str,
    qualification_root: Path,
    execution_root: Path,
    raw_evidence_root: Path,
    session_inventory: dict[str, Any] | None,
    audit: dict[str, Any] | None,
    runner_summary: dict[str, Any] | None,
    automated_state: str,
    mechanical_error: str | None,
) -> None:
    state_root = repository_root / STATE_ROOT.relative_to(REPOSITORY_ROOT)
    runs_root = state_root / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)
    current_path = state_root / "current-state.json"
    current = load_json(current_path)

    issues = audit.get("findings", []) if audit else []
    run_record = {
        "schema_version": 1,
        "run_id": run_id,
        "pair_id": pair_id,
        "execution_identity_sha256": execution_identity_sha256,
        "execution_identity": execution_identity_payload,
        "source": source.compact(),
        "target": target.compact(),
        "qualification_model": qualification_model,
        "audit_model": audit_model,
        "opencode_version": opencode_version_value,
        "qualification_root_sha256": tree_digest(qualification_root),
        "runner_summary_sha256": (
            sha256_text(canonical_json(runner_summary)) if runner_summary is not None else None
        ),
        "session_inventory_file": f"{run_id}.sessions.json" if session_inventory else None,
        "audit_report_file": f"{run_id}.audit.json" if audit else None,
        "issues_file": f"{run_id}.issues.json",
        "raw_evidence": {
            "path": str(raw_evidence_root.resolve()),
            "sha256": tree_digest(raw_evidence_root),
        },
        "automated_state": automated_state,
        "mechanical_error": mechanical_error,
        "user_signoff": None,
    }
    schema = load_json(state_root / "schemas/run-record.schema.json")
    validate_schema(run_record, schema, label="run record")

    issue_payload = {"schema_version": 1, "run_id": run_id, "issues": issues}
    (runs_root / f"{run_id}.json").write_text(canonical_json(run_record), encoding="utf-8")
    (runs_root / f"{run_id}.issues.json").write_text(canonical_json(issue_payload), encoding="utf-8")
    if session_inventory:
        schema = load_json(state_root / "schemas/session-inventory.schema.json")
        validate_schema(session_inventory, schema, label="session inventory")
        (runs_root / f"{run_id}.sessions.json").write_text(
            canonical_json(session_inventory), encoding="utf-8"
        )
    if audit:
        (runs_root / f"{run_id}.audit.json").write_text(canonical_json(audit), encoding="utf-8")

    pair_state = current["pairs"][pair_id]
    pair_state["latest_run_id"] = run_id
    pair_state["status"] = automated_state
    pair_state["user_signoff"] = None
    schema = load_json(state_root / "schemas/current-state.schema.json")
    validate_schema(current, schema, label="current qualification state")
    current_path.write_text(canonical_json(current), encoding="utf-8")


def utc_run_id(pair_id: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{stamp}-{pair_id}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--source-assets", type=Path)
    parser.add_argument("--target-assets", type=Path)
    parser.add_argument("--run-root-parent", type=Path)
    parser.add_argument("--opencode", default="opencode")
    parser.add_argument("--gh", default="gh")
    parser.add_argument(
        "--validate-config-only",
        action="store_true",
        help="validate checked-in schemas, pair catalog, state, and pinned images without running qualification",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repository_root = args.repository_root.expanduser().resolve()
    try:
        config, catalog, _ = load_configuration(repository_root)
        pinned_image_manifest = validate_pinned_images(repository_root)
        if args.validate_config_only:
            print(f"qualification configuration valid: active pair {config['active_pair']}")
            return 0
        require_clean_repository(repository_root)
        pair = active_pair(config, catalog)
        run_id = utc_run_id(pair["id"])
        parent = (
            args.run_root_parent.expanduser().resolve()
            if args.run_root_parent
            else Path(os.environ.get("TMPDIR", tempfile.gettempdir())).expanduser().resolve()
        )
        if parent == repository_root or parent.is_relative_to(repository_root):
            raise AutomationError("run root parent must be outside the Ava repository")
        run_root = parent / f"ava-qualification-{run_id}"
        run_root.mkdir(parents=True)
        assets_root = run_root / "assets"
        fixture_parent = run_root / "fixture"
        execution_parent = run_root / "execution"
        transcript_root = run_root / "transcripts"
        audit_root = run_root / "audit"
        test_project = run_root / "test-project"
        for path in (assets_root, fixture_parent, execution_parent, transcript_root, audit_root):
            path.mkdir(parents=True, exist_ok=True)
        create_test_project(test_project)

        source = resolve_release(
            pair["source"],
            local_path=args.source_assets,
            destination=assets_root / "source",
            repository=config["repository"],
            gh=args.gh,
            label="source assets",
        )
        target = resolve_release(
            pair["target"],
            local_path=args.target_assets,
            destination=assets_root / "target",
            repository=config["repository"],
            gh=args.gh,
            label="target assets",
        )
        qualification_runner.validate_upgrade_pair(source.identity, target.identity)

        qualification_root = generate_fixture(repository_root, fixture_parent)
        fixture_inventory_sha256 = tree_digest(qualification_root)
        oc_version = opencode_version(args.opencode)
        repo_revision = repository_revision(repository_root)
        identity_sha, identity_payload = execution_identity(
            source=source,
            target=target,
            image_manifest_sha256=sha256_file(
                repository_root / IMAGE_MANIFEST_PATH.relative_to(REPOSITORY_ROOT)
            ),
            pinned_images=[
                {
                    "file": item["file"],
                    "sha256": item["sha256"],
                    "destination": item["destination"],
                }
                for item in pinned_image_manifest["images"]
            ],
            fixture_generator_sha256=sha256_file(
                repository_root / "internal/release/generate-synthetic-qualification-vault.sh"
            ),
            fixture_inventory_sha256=fixture_inventory_sha256,
            matrix_sha256=matrix_digest(repository_root),
            repository_revision_value=repo_revision,
            runner_sha256=sha256_file(
                repository_root / "internal/release/qualification_runner.py"
            ),
            automation_sha256=sha256_file(
                repository_root / "internal/release/qualification_automation.py"
            ),
            opencode_version_value=oc_version,
            qualification_model=config["qualification_model"],
            audit_model=config["audit_model"],
        )
        execution_root = execution_root_for_identity(execution_parent, identity_sha)
        source_path = source.identity.directory
        target_path = target.identity.directory

        base_command = [
            "sh",
            str(repository_root / "internal/release/qualify-synthetic.sh"),
            "--qualification-root",
            str(qualification_root),
            "--execution-root",
            str(execution_root),
            "--source-assets",
            str(source_path),
            "--target-assets",
            str(target_path),
            "--test-project",
            str(test_project),
            "--opencode",
            args.opencode,
            "--model",
            config["qualification_model"],
            "--transcript-dir",
            str(transcript_root),
        ]
        run_command([*base_command, "--preflight-only"], cwd=repository_root)
        sessions_before = snapshot_sessions(args.opencode)
        runner_result = run_command(base_command, cwd=repository_root, check=False)
        summary_path = execution_root / "summary.json"
        summary = load_json(summary_path) if summary_path.is_file() else None

        session_inventory: dict[str, Any] | None = None
        audit: dict[str, Any] | None = None
        mechanical_error: str | None = None
        automated_state = "failed"
        final_exit = 1

        runner_passed = (
            runner_result.returncode == 0
            and summary is not None
            and qualification_exit(summary) == 0
        )
        if not runner_passed:
            mechanical_error = (
                f"qualification runner exited {runner_result.returncode}"
                if runner_result.returncode != 0
                else "qualification runner did not produce an all-pass summary"
            )

        try:
            sessions_after = snapshot_sessions(args.opencode)
            session_inventory = build_session_inventory(
                before=sessions_before,
                after=sessions_after,
                execution_root=execution_root,
                opencode=args.opencode,
                configured_model=config["qualification_model"],
                allow_empty=not runner_passed,
            )
        except AutomationError as exc:
            if runner_passed:
                mechanical_error = f"session inventory failed: {exc}"
                runner_passed = False
            else:
                mechanical_error = f"{mechanical_error}; session inventory failed: {exc}"

        if session_inventory is not None:
            inventory_path = audit_root / "session-inventory.json"
            inventory_path.write_text(canonical_json(session_inventory), encoding="utf-8")

        if summary is not None and session_inventory is not None and session_inventory["sessions"]:
            try:
                prompt = build_audit_prompt(
                    pair_id=pair["id"],
                    run_id=run_id,
                    execution_identity_sha256=identity_sha,
                    session_inventory_path=inventory_path,
                    runner_summary_path=summary_path,
                    qualification_root=qualification_root,
                    source_assets=source_path,
                    target_assets=target_path,
                    repository_root=repository_root,
                )
                prompt_path = audit_root / "prompt.md"
                prompt_path.write_text(prompt, encoding="utf-8")
                audit, raw_audit = run_audit(
                    opencode=args.opencode,
                    audit_model=config["audit_model"],
                    prompt=prompt,
                    repository_root=repository_root,
                    raw_evidence_root=run_root,
                )
                (audit_root / "raw.jsonl").write_text(raw_audit, encoding="utf-8")
            except AutomationError as exc:
                mechanical_error = (
                    f"{mechanical_error}; independent audit failed: {exc}"
                    if mechanical_error
                    else f"independent audit failed: {exc}"
                )
                runner_passed = False

        if runner_passed and audit is not None:
            automated_state, final_exit = audit_status(audit)
        elif runner_passed:
            mechanical_error = mechanical_error or "successful qualification produced no independent audit"
            automated_state, final_exit = "failed", 1

        write_compact_evidence(
            repository_root=repository_root,
            run_id=run_id,
            pair_id=pair["id"],
            execution_identity_sha256=identity_sha,
            execution_identity_payload=identity_payload,
            source=source,
            target=target,
            opencode_version_value=oc_version,
            qualification_model=config["qualification_model"],
            audit_model=config["audit_model"],
            qualification_root=qualification_root,
            execution_root=execution_root,
            raw_evidence_root=run_root,
            session_inventory=session_inventory,
            audit=audit,
            runner_summary=summary,
            automated_state=automated_state,
            mechanical_error=mechanical_error,
        )
        print(f"qualification run: {run_id}")
        print(f"automated state: {automated_state}")
        print(f"external evidence: {run_root}")
        print("compact evidence written to internal/release/qualification/runs/ without committing")
        return final_exit
    except (AutomationError, qualification_runner.QualificationError, OSError, ValueError, KeyError) as exc:
        print(f"release qualification automation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
