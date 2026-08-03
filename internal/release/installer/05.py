def plan_operations(root: Path, installed: dict[str, Any] | None, target_payload: dict[str, dict[str, Any]], adopt_agents: bool) -> list[dict[str, Any]]:
    previous = installed_payload(installed) if installed else {}
    operations: list[dict[str, Any]] = []
    for path in sorted(set(previous) | set(target_payload)):
        old = previous.get(path)
        new = target_payload.get(path)
        live = safe_live_path(root, path)
        current_sha = sha256_file(live) if live.is_file() else None
        if live.exists() and not live.is_file():
            raise AvaError("PATH_COLLISION", f"managed path collides with non-file: {path}")
        if old:
            if current_sha != old["sha256"]:
                raise AvaError("MANAGED_CONFLICT", f"managed file differs from installed checksum: {path}")
            operation = "retain" if new and new["sha256"] == old["sha256"] else ("replace" if new else "delete")
        elif new:
            if current_sha is None:
                operation = "create"
            elif path == "/AGENTS.md" and installed is None and adopt_agents:
                operation = "replace"
            else:
                raise AvaError("PATH_COLLISION", f"new managed path already exists: {path}")
        else:
            continue
        operations.append({
            "path": path,
            "operation": operation,
            "previous_sha256": old["sha256"] if old else None,
            "current_sha256": current_sha,
            "target_sha256": new["sha256"] if new else None,
            "classification": "unchanged" if operation == "retain" else "staged",
        })
    return operations


def plan_scaffolds(root: Path, target: Bundle, fresh: bool) -> list[dict[str, Any]]:
    if not fresh:
        return []
    result: list[dict[str, Any]] = []
    for item in target.manifest["installed_files"]:
        if item["ownership"] != "project-owned":
            continue
        path = safe_live_path(root, item["destination"])
        if path.exists():
            result.append({"path": item["destination"], "operation": "skip", "sha256": item["sha256"], "source": str(target.base / item["source_path"])})
        else:
            parent = path.parent
            while parent != root and not parent.exists():
                parent = parent.parent
            if parent.exists() and not parent.is_dir():
                raise AvaError("PATH_COLLISION", f"scaffold parent is not a directory: {item['destination']}")
            result.append({"path": item["destination"], "operation": "create", "sha256": item["sha256"], "source": str(target.base / item["source_path"])})
    return result


def print_plan(
    operations: list[dict[str, Any]],
    scaffolds: list[dict[str, Any]],
    semantic: dict[str, Any],
    host_integration: dict[str, str] | None,
    json_output: bool,
) -> None:
    records = []
    for item in operations:
        records.append({"type": "managed", "operation": item["operation"], "path": item["path"], "ownership": "ava-managed"})
    for item in scaffolds:
        records.append({"type": "scaffold", "operation": item["operation"], "path": item["path"], "ownership": "project-owned"})
    records.append({"type": "semantic", **semantic})
    if host_integration is None:
        records.append({"type": "host-integration", "entrypoint": None, "discovery": "explicit-only"})
    else:
        records.append({"type": "host-integration", **host_integration})
    if json_output:
        for record in records:
            print(json.dumps(record, sort_keys=True))
    else:
        for record in records:
            if record["type"] in {"managed", "scaffold"}:
                print(f"{record['operation'].upper():7} {record['path']} [{record['ownership']}]")
        print(f"SEMANTIC {semantic['status']} compatible_through={semantic['compatible_through']} target={semantic['target_version']}")
        if host_integration is None:
            print("HOST      explicit-only")
        else:
            print(f"HOST      {host_integration['entrypoint']} [project-owned, project-provided]")


def backup_path(backup: Path, destination: str) -> Path:
    return backup / destination_relative(destination)


def backup_live_file(root: Path, backup: Path, destination: str) -> None:
    source = safe_live_path(root, destination)
    if source.is_file():
        target = backup_path(backup, destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def restore_transaction(root: Path, plan: dict[str, Any], *, terminal: str = "rolled-back") -> None:
    backup = root / plan["backup_relative"]
    source_payload = {item["path"]: item for item in plan["source_payload"]}
    target_payload_paths = set(plan["target_payload"])
    for path in sorted(target_payload_paths - set(source_payload), key=lambda value: value.count("/"), reverse=True):
        live = safe_live_path(root, path)
        if live.is_file():
            live.unlink()
            remove_empty_parents(live, root)
    for path in sorted(source_payload):
        saved = backup_path(backup, path)
        if not saved.is_file():
            raise AvaError("ROLLBACK_FAILED", f"backup is missing source managed file: {path}")
        live = safe_live_path(root, path)
        live.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(live, saved.read_bytes())
    source_manifest_backup = backup / ".ava/state/manifest.json"
    if source_manifest_backup.is_file():
        atomic_write(root / ".ava/state/manifest.json", source_manifest_backup.read_bytes())
    source_upgrade_backup = backup / ".ava/state/upgrade.json"
    if source_upgrade_backup.is_file():
        previous = read_json(source_upgrade_backup, "ROLLBACK_FAILED")
    else:
        previous = idle_journal()
    if terminal == "rolled-back":
        journal = plan["journal"]
        journal.update({
            "status": "rolled-back",
            "stage": "rolled-back",
            "updated_at": now(),
            "staging": None,
            "failure": None,
            "allowed_operations": ["normal"],
        })
        atomic_json(root / ".ava/state/upgrade.json", journal)
    else:
        atomic_json(root / ".ava/state/upgrade.json", previous)


