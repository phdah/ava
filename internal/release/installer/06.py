def apply_transaction(
    root: Path,
    installed: dict[str, Any] | None,
    prior_upgrade: dict[str, Any] | None,
    target: Bundle,
    bundles: list[Bundle],
    edges: list[dict[str, Any]],
    target_payload: dict[str, dict[str, Any]],
    operations: list[dict[str, Any]],
    scaffolds: list[dict[str, Any]],
    semantic: dict[str, Any],
    migration_steps: list[dict[str, Any]],
) -> None:
    fresh = installed is None
    transaction_id = uuid.uuid4().hex
    if fresh:
        transaction_root = root / ".ava-install" / transaction_id
        transaction_relative = f".ava-install/{transaction_id}"
    else:
        transaction_root = root / ".ava/state/transactions" / transaction_id
        transaction_relative = f".ava/state/transactions/{transaction_id}"
    workspace = transaction_root / "workspace"
    backup = transaction_root / "backup"
    workspace.mkdir(parents=True, exist_ok=False)
    backup.mkdir(parents=True, exist_ok=False)

    for path, item in target_payload.items():
        copy_candidate(Path(item["source"]), workspace, path, item["sha256"])
    completed_migrations = execute_migrations(workspace, migration_steps, target_payload)
    manifest = target_manifest(target, target_payload, semantic)
    validate_installed_manifest(manifest)
    candidate_manifest = workspace / "manifest.json"
    atomic_json(candidate_manifest, manifest)

    for operation in operations:
        if operation["current_sha256"] is not None:
            backup_live_file(root, backup, operation["path"])
    if installed:
        backup_live_file(root, backup, "/.ava/state/manifest.json")
        backup_live_file(root, backup, "/.ava/state/upgrade.json")

    path_edges = [{**edge, "completed": False} for edge in edges]
    journal = {
        "upgrade_schema": 1,
        "transaction_id": transaction_id,
        "status": "active",
        "stage": "staged",
        "source": source_release_state(installed) if installed else release_state(target),
        "target": release_state(target),
        "path": path_edges,
        "current_edge": 0 if path_edges else None,
        "created_at": now(),
        "updated_at": now(),
        "staging": {
            "workspace": f"/{transaction_relative}/workspace",
            "backup": f"/{transaction_relative}/backup",
            "candidate_manifest": f"/{transaction_relative}/workspace/manifest.json",
            "live_mutation_started": False,
            "managed_commit_complete": False,
        },
        "migrations": {
            "resolved_order": [step["id"] for step in topological_migrations(migration_steps)],
            "active_id": None,
            "completed": completed_migrations,
        },
        "managed_changes": operations,
        "project_changes": [],
        "failure": None,
        "allowed_operations": ["inspect", "resume", "abort"],
    }
    plan = {
        "backup_relative": f"{transaction_relative}/backup",
        "workspace_relative": f"{transaction_relative}/workspace",
        "source_payload": list(installed_payload(installed).values()) if installed else [],
        "target_payload": sorted(target_payload),
        "operations": operations,
        "scaffolds": scaffolds,
        "semantic": semantic,
        "journal": journal,
    }
    atomic_json(transaction_root / "plan.json", plan)
    if installed:
        atomic_json(root / ".ava/state/upgrade.json", journal)

    created_scaffolds: list[str] = []
    try:
        journal["staging"]["live_mutation_started"] = True
        journal["stage"] = "validating"
        journal["allowed_operations"] = ["inspect", "resume", "rollback"]
        journal["updated_at"] = now()
        if installed:
            atomic_json(root / ".ava/state/upgrade.json", journal)

        for operation in operations:
            path = operation["path"]
            live = safe_live_path(root, path)
            if operation["operation"] == "retain":
                continue
            if operation["operation"] == "delete":
                live.unlink()
                remove_empty_parents(live, root)
            else:
                candidate = candidate_path(workspace, path)
                live.parent.mkdir(parents=True, exist_ok=True)
                atomic_write(live, candidate.read_bytes())
        for scaffold in scaffolds:
            if scaffold["operation"] != "create":
                continue
            live = safe_live_path(root, scaffold["path"])
            live.parent.mkdir(parents=True, exist_ok=True)
            source = Path(scaffold["source"])
            atomic_write(live, source.read_bytes())
            created_scaffolds.append(scaffold["path"])

        for path, item in target_payload.items():
            live = safe_live_path(root, path, permit_missing=False)
            if not live.is_file() or sha256_file(live) != item["sha256"]:
                raise AvaError("POST_VALIDATION_FAILED", f"installed payload validation failed: {path}")
        for scaffold in scaffolds:
            if scaffold["operation"] == "create":
                live = safe_live_path(root, scaffold["path"], permit_missing=False)
                if not live.is_file() or sha256_file(live) != scaffold["sha256"]:
                    raise AvaError("POST_VALIDATION_FAILED", f"scaffold validation failed: {scaffold['path']}")

        atomic_json(root / ".ava/state/manifest.json", manifest)
        for edge in journal["path"]:
            edge["completed"] = True
        for change in journal["managed_changes"]:
            if change["operation"] != "retain":
                change["classification"] = "applied"
        journal["current_edge"] = None
        journal["staging"]["managed_commit_complete"] = True
        journal["updated_at"] = now()
        if semantic["status"] == "complete":
            journal.update({"status": "complete", "stage": "complete", "staging": None, "allowed_operations": ["normal"]})
        else:
            journal.update({"status": "active", "stage": "semantic", "allowed_operations": ["inspect", "reconcile-semantic", "rollback"]})
        atomic_json(root / ".ava/state/upgrade.json", journal if installed or semantic["status"] != "complete" else idle_journal())
        if semantic["status"] == "complete":
            shutil.rmtree(transaction_root, ignore_errors=True)
            if fresh:
                try:
                    transaction_root.parent.rmdir()
                except OSError:
                    pass
        print(f"Installed Ava {target.version} in {root}")
        if semantic["status"] != "complete":
            print("Deterministic upgrade complete. Normal routing remains blocked.")
            print("Activate the Ava Upgrade Role through the managed root AGENTS.md and apply the installed guidance.")
    except Exception:
        for path in reversed(created_scaffolds):
            live = safe_live_path(root, path)
            if live.is_file():
                live.unlink()
                remove_empty_parents(live, root)
        try:
            if installed:
                restore_transaction(root, plan, terminal="source")
            else:
                for operation in reversed(operations):
                    live = safe_live_path(root, operation["path"])
                    saved = backup_path(backup, operation["path"])
                    if saved.is_file():
                        live.parent.mkdir(parents=True, exist_ok=True)
                        atomic_write(live, saved.read_bytes())
                    elif live.is_file():
                        live.unlink()
                shutil.rmtree(root / ".ava", ignore_errors=True)
        finally:
            shutil.rmtree(transaction_root, ignore_errors=True)
        raise


def discovery_outcome(selected_bootstraps: set[str]) -> str:
    return "host-bootstrap" if selected_bootstraps else "explicit-only"


def perform_install(args: argparse.Namespace) -> None:
    root = args.target.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    if not root.is_dir() or root.is_symlink():
        raise AvaError("INVALID_TARGET", "target must resolve to a normal directory")
    probe = root / f".ava-write-test-{uuid.uuid4().hex}"
    try:
        probe.write_text("test")
    except OSError as exc:
        raise AvaError("TARGET_NOT_WRITABLE", f"target is not writable: {root}") from exc
    finally:
        probe.unlink(missing_ok=True)

    installed, upgrade = load_installed_state(root)
    if installed and upgrade and upgrade.get("status") in {"active", "blocked"}:
        raise AvaError("ACTIVE_TRANSACTION", "an upgrade transaction is active; use --rollback or complete semantic reconciliation")
    if installed and installed["semantic_compatibility"]["status"] != "complete":
        raise AvaError("SEMANTIC_STATE_BLOCKED", "semantic compatibility is incomplete; reconcile or rollback before another upgrade")

    embedded = os.environ.get("AVA_VERSION", "")
    if args.version:
        target_version = canonical_version(args.version)
    elif VERSION_RE.fullmatch(embedded):
        target_version = embedded
    else:
        raise AvaError("VERSION_REQUIRED", "development installer requires --version")
    source_version = installed["ava_version"] if installed else None
    if source_version == target_version:
        for path, item in installed_payload(installed).items():
            live = safe_live_path(root, path, permit_missing=False)
            if not live.is_file() or sha256_file(live) != item["sha256"]:
                raise AvaError("MANAGED_CONFLICT", f"installed file is not intact: {path}")
        print(f"Ava {target_version} is already installed and valid.")
        return

    work_root = root / f".ava-download-{uuid.uuid4().hex}"
    work_root.mkdir()
    try:
        bundles, edges = resolve_bundles(source_version, target_version, args, work_root)
        target = bundles[-1]
        selected_bootstraps = select_bootstraps(target, installed, args.host_bootstrap)
        target_payload, _, migration_steps = construct_target_payload(bundles, edges, selected_bootstraps)
        operations = plan_operations(root, installed, target_payload, args.adopt_existing_agents)
        scaffolds = plan_scaffolds(root, target, installed is None)
        semantic = build_semantic_state(installed, target, edges)
        discovery = discovery_outcome(selected_bootstraps)
        print_plan(operations, scaffolds, semantic, discovery, args.json)
        if args.dry_run:
            return
        apply_transaction(root, installed, upgrade, target, bundles, edges, target_payload, operations, scaffolds, semantic, migration_steps)
        print(f"Bootstrap discovery: {discovery}")
    finally:
        shutil.rmtree(work_root, ignore_errors=True)


def load_active_plan(root: Path, journal: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    staging = journal.get("staging")
    if not isinstance(staging, dict):
        raise AvaError("NO_ROLLBACK", "upgrade journal has no durable staging state")
    backup_destination = staging.get("backup")
    if not isinstance(backup_destination, str):
        raise AvaError("NO_ROLLBACK", "upgrade journal has no backup path")
    backup = safe_live_path(root, backup_destination, permit_missing=False)
    transaction_root = backup.parent
    plan_path = transaction_root / "plan.json"
    plan = read_json(plan_path, "NO_ROLLBACK")
    return transaction_root, plan


