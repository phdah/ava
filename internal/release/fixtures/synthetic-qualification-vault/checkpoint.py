#!/usr/bin/env python3
"""Create authentic interrupted Ava upgrade transactions for qualification."""

from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any


HEREDOC_MARKER = 'exec python3 - "$@" <<\'PY\'\n'
TERMINATOR = "\nPY\n"


class CheckpointError(RuntimeError):
    pass


class CheckpointReached(BaseException):
    """Intentional non-Exception interruption that bypasses installer rollback."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckpointError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CheckpointError(f"expected JSON object at {path}")
    return value


def installer_namespace(installer: Path) -> dict[str, Any]:
    try:
        text = installer.read_text(encoding="utf-8")
    except OSError as exc:
        raise CheckpointError(f"cannot read assembled installer: {installer}") from exc
    if HEREDOC_MARKER not in text:
        raise CheckpointError("assembled installer does not contain the canonical Python heredoc")
    source = text.split(HEREDOC_MARKER, 1)[1]
    if TERMINATOR not in source:
        raise CheckpointError("assembled installer Python heredoc is not terminated")
    source, trailing = source.rsplit(TERMINATOR, 1)
    if trailing.strip():
        raise CheckpointError("assembled installer contains unexpected content after its Python heredoc")

    tree = ast.parse(source, filename=str(installer))
    if not tree.body or not isinstance(tree.body[-1], ast.Try):
        raise CheckpointError("assembled installer has no canonical execution wrapper")
    wrapper = tree.body[-1]
    if not wrapper.body or not isinstance(wrapper.body[0], ast.Raise):
        raise CheckpointError("assembled installer execution wrapper is not recognized")
    raised = wrapper.body[0].exc
    if not (
        isinstance(raised, ast.Call)
        and isinstance(raised.func, ast.Name)
        and raised.func.id == "SystemExit"
        and raised.args
        and isinstance(raised.args[0], ast.Call)
        and isinstance(raised.args[0].func, ast.Name)
        and raised.args[0].func.id == "main"
    ):
        raise CheckpointError("assembled installer execution wrapper does not invoke main through SystemExit")
    tree.body.pop()
    ast.fix_missing_locations(tree)

    module_name = f"_ava_qualification_installer_{hashlib.sha256(str(installer).encode()).hexdigest()[:16]}"
    module = ModuleType(module_name)
    module.__file__ = str(installer)
    sys.modules[module_name] = module
    try:
        exec(compile(tree, str(installer), "exec"), module.__dict__)
    except Exception as exc:
        sys.modules.pop(module_name, None)
        raise CheckpointError(f"cannot load assembled installer Python payload: {exc}") from exc
    return module.__dict__


def release_managed_paths(release: dict[str, Any]) -> set[str]:
    items = release.get("installed_files")
    if not isinstance(items, list):
        raise CheckpointError("target release manifest has no installed_files array")
    return {
        item["destination"]
        for item in items
        if isinstance(item, dict)
        and item.get("ownership") == "ava-managed"
        and isinstance(item.get("destination"), str)
    }


def installed_managed_paths(manifest: dict[str, Any]) -> set[str]:
    items = manifest.get("managed_files")
    if not isinstance(items, list):
        raise CheckpointError("installed manifest has no managed_files array")
    return {
        item["path"]
        for item in items
        if isinstance(item, dict)
        and item.get("kind") == "payload"
        and isinstance(item.get("path"), str)
    }


def project_inventory(root: Path, excluded_managed_paths: set[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root).as_posix()
        if relative == ".ava" or relative.startswith(".ava/"):
            continue
        destination = f"/{relative}"
        if destination in excluded_managed_paths:
            continue
        result[relative] = sha256_file(path)
    return result


def transaction_root(root: Path, journal: dict[str, Any]) -> Path:
    staging = journal.get("staging")
    if not isinstance(staging, dict):
        raise CheckpointError("checkpoint journal has no staging object")
    backup = staging.get("backup")
    if not isinstance(backup, str) or not backup.startswith("/"):
        raise CheckpointError("checkpoint journal has no canonical backup path")
    backup_path = root / backup.removeprefix("/")
    if not backup_path.is_dir():
        raise CheckpointError("checkpoint backup directory is missing")
    result = backup_path.parent
    for required in (result / "plan.json", result / "workspace" / "manifest.json"):
        if not required.is_file():
            raise CheckpointError(f"checkpoint transaction is missing {required.relative_to(root)}")
    return result


def validate_checkpoint(
    mode: str,
    root: Path,
    source_manifest: dict[str, Any],
    target_release: dict[str, Any],
    project_before: dict[str, str],
    excluded_managed_paths: set[str],
) -> dict[str, Any]:
    manifest = read_json(root / ".ava/state/manifest.json")
    journal = read_json(root / ".ava/state/upgrade.json")
    if manifest.get("ava_version") != source_manifest.get("ava_version"):
        raise CheckpointError("live installed manifest advanced before the checkpoint")
    if journal.get("status") != "active":
        raise CheckpointError("checkpoint journal is not active")
    staging = journal.get("staging")
    if not isinstance(staging, dict) or staging.get("managed_commit_complete") is not False:
        raise CheckpointError("checkpoint is not an incomplete managed transaction")

    if mode == "abort":
        if journal.get("stage") != "staged" or staging.get("live_mutation_started") is not False:
            raise CheckpointError("abort checkpoint is not pre-live-mutation staged state")
        if "abort" not in journal.get("allowed_operations", []):
            raise CheckpointError("abort checkpoint does not permit abort")
    else:
        if journal.get("stage") != "validating" or staging.get("live_mutation_started") is not True:
            raise CheckpointError("resume checkpoint is not an interrupted validating state")
        if "resume" not in journal.get("allowed_operations", []):
            raise CheckpointError("resume checkpoint does not permit resume")

    txn_root = transaction_root(root, journal)
    candidate = read_json(txn_root / "workspace/manifest.json")
    if candidate.get("ava_version") != target_release.get("ava_version"):
        raise CheckpointError("candidate manifest does not match the selected target release")

    plan = read_json(txn_root / "plan.json")
    operations = plan.get("operations")
    if not isinstance(operations, list):
        raise CheckpointError("transaction plan has no operations array")
    for operation in operations:
        if not isinstance(operation, dict) or not isinstance(operation.get("path"), str):
            raise CheckpointError("transaction plan contains an invalid managed operation")
        path = root / operation["path"].removeprefix("/")
        actual = sha256_file(path) if path.is_file() else None
        allowed = {
            operation.get("previous_sha256"),
            operation.get("current_sha256"),
            operation.get("target_sha256"),
        }
        if operation.get("operation") == "delete":
            allowed.add(None)
        if actual not in allowed:
            raise CheckpointError(f"managed path is outside transaction checksums: {operation['path']}")

    project_after = project_inventory(root, excluded_managed_paths)
    if project_after != project_before:
        raise CheckpointError("checkpoint creation changed project-owned files")

    return {
        "checkpoint": mode,
        "source_version": source_manifest.get("ava_version"),
        "target_version": target_release.get("ava_version"),
        "transaction_id": journal.get("transaction_id"),
        "status": journal.get("status"),
        "stage": journal.get("stage"),
        "live_mutation_started": staging.get("live_mutation_started"),
        "managed_commit_complete": staging.get("managed_commit_complete"),
        "allowed_operations": journal.get("allowed_operations"),
        "transaction_relative": txn_root.relative_to(root).as_posix(),
        "project_owned_sha256": project_after,
    }


def create_checkpoint(mode: str, target: Path, asset_dir: Path) -> dict[str, Any]:
    target = target.expanduser().resolve()
    asset_dir = asset_dir.expanduser().resolve()
    installer = asset_dir / "ava-install.sh"
    release_path = asset_dir / "ava-release.json"
    if not installer.is_file() or not release_path.is_file():
        raise CheckpointError("asset directory must contain assembled ava-install.sh and ava-release.json")
    source_manifest = read_json(target / ".ava/state/manifest.json")
    source_journal = read_json(target / ".ava/state/upgrade.json")
    if source_journal.get("status") not in {"idle", "complete", "rolled-back", "aborted"}:
        raise CheckpointError("source project already has a non-terminal upgrade transaction")
    semantic = source_manifest.get("semantic_compatibility")
    if not isinstance(semantic, dict) or semantic.get("status") != "complete":
        raise CheckpointError("source project semantic compatibility must be complete")
    target_release = read_json(release_path)
    target_version = target_release.get("ava_version")
    if not isinstance(target_version, str) or target_version == source_manifest.get("ava_version"):
        raise CheckpointError("target assets must describe a different Ava version")

    excluded_managed_paths = installed_managed_paths(source_manifest) | release_managed_paths(target_release)
    project_before = project_inventory(target, excluded_managed_paths)
    namespace = installer_namespace(installer)
    original_atomic_json = namespace.get("atomic_json")
    if not callable(original_atomic_json) or not callable(namespace.get("perform_install")):
        raise CheckpointError("assembled installer does not expose expected transaction functions")
    upgrade_path = target / ".ava/state/upgrade.json"
    manifest_path = target / ".ava/state/manifest.json"

    def checkpoint_atomic_json(path: Path, value: Any) -> None:
        if mode == "resume" and path == manifest_path:
            journal = read_json(upgrade_path)
            staging = journal.get("staging")
            if (
                journal.get("stage") == "validating"
                and isinstance(staging, dict)
                and staging.get("live_mutation_started") is True
                and staging.get("managed_commit_complete") is False
            ):
                raise CheckpointReached()
        original_atomic_json(path, value)
        if mode == "abort" and path == upgrade_path and isinstance(value, dict):
            staging = value.get("staging")
            if (
                value.get("stage") == "staged"
                and isinstance(staging, dict)
                and staging.get("live_mutation_started") is False
                and staging.get("managed_commit_complete") is False
            ):
                raise CheckpointReached()

    namespace["atomic_json"] = checkpoint_atomic_json
    args = SimpleNamespace(
        target=target,
        version=target_version,
        asset_dir=asset_dir,
        dry_run=False,
        json=False,
        verified=False,
        adopt_existing_agents=False,
        host_entrypoint=None,
        resume=False,
        abort=False,
        rollback=False,
        finalize=False,
    )
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            namespace["perform_install"](args)
    except CheckpointReached:
        pass
    except Exception as exc:
        code = getattr(exc, "code", exc.__class__.__name__)
        message = getattr(exc, "message", str(exc))
        raise CheckpointError(f"installer rejected checkpoint setup [{code}]: {message}") from exc
    else:
        raise CheckpointError("target upgrade completed before the requested qualification checkpoint")

    return validate_checkpoint(
        mode,
        target,
        source_manifest,
        target_release,
        project_before,
        excluded_managed_paths,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", choices=("abort", "resume"))
    parser.add_argument("--target", type=Path, required=True, help="Existing source-version Ava project.")
    parser.add_argument("--asset-dir", type=Path, required=True, help="Exact assembled target release asset directory.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = create_checkpoint(args.checkpoint, args.target, args.asset_dir)
    except (CheckpointError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"qualification checkpoint error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
