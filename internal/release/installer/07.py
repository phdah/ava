def perform_rollback(args: argparse.Namespace) -> None:
    root = args.target.expanduser().resolve()
    installed, journal = load_installed_state(root)
    if installed is None or journal is None or journal.get("status") not in {"active", "blocked"}:
        raise AvaError("NO_ROLLBACK", "there is no active upgrade transaction")
    project_changes = journal.get("project_changes", [])
    if any(item.get("resolution") != "reverted" for item in project_changes):
        raise AvaError("PROJECT_CHANGES_BLOCK_ROLLBACK", "project-owned upgrade changes must be explicitly reverted before managed rollback")
    transaction_root, plan = load_active_plan(root, journal)
    target_payload = {item["path"]: item for item in installed["managed_files"] if item["kind"] == "payload"}
    for path, item in target_payload.items():
        live = safe_live_path(root, path)
        if not live.is_file() or sha256_file(live) != item["sha256"]:
            raise AvaError("ROLLBACK_CONFLICT", f"target managed file changed after upgrade: {path}")
    restore_transaction(root, plan)
    shutil.rmtree(transaction_root, ignore_errors=True)
    print(f"Rolled back Ava managed content in {root}")


def current_sha(path: Path) -> str | None:
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise AvaError("RESUME_CONFLICT", f"managed path is not a normal file: {path}")
    return sha256_file(path)


def perform_resume(args: argparse.Namespace) -> None:
    root = args.target.expanduser().resolve()
    installed, journal = load_installed_state(root)
    if installed is None or journal is None or journal.get("status") not in {"active", "blocked"}:
        raise AvaError("NO_TRANSACTION", "there is no resumable upgrade transaction")
    staging = journal.get("staging")
    if not isinstance(staging, dict):
        raise AvaError("NO_TRANSACTION", "upgrade transaction has no staging state")
    if staging.get("managed_commit_complete"):
        if installed["semantic_compatibility"]["status"] == "complete":
            perform_finalize(args)
            return
        raise AvaError("SEMANTIC_STATE_BLOCKED", "deterministic work is complete; resume through the managed Upgrade Role")
    transaction_root, plan = load_active_plan(root, journal)
    workspace = root / plan["workspace_relative"]
    candidate_manifest_path = workspace / "manifest.json"
    candidate_manifest = read_json(candidate_manifest_path, "NO_TRANSACTION")
    validate_installed_manifest(candidate_manifest)
    target_payload = {
        item["path"]: item for item in candidate_manifest["managed_files"] if item["kind"] == "payload"
    }
    operations = plan["operations"]
    for operation in operations:
        live = safe_live_path(root, operation["path"])
        actual = current_sha(live)
        allowed = {operation["target_sha256"]}
        if operation["previous_sha256"] is not None:
            allowed.add(operation["previous_sha256"])
        if operation["current_sha256"] is not None:
            allowed.add(operation["current_sha256"])
        if operation["operation"] == "delete":
            allowed.add(None)
        if actual not in allowed:
            raise AvaError("RESUME_CONFLICT", f"managed path changed outside the transaction: {operation['path']}")

    journal.update({
        "status": "active",
        "stage": "validating",
        "updated_at": now(),
        "failure": None,
        "allowed_operations": ["inspect", "resume", "rollback"],
    })
    journal["staging"]["live_mutation_started"] = True
    atomic_json(root / ".ava/state/upgrade.json", journal)

    for operation in operations:
        live = safe_live_path(root, operation["path"])
        if operation["operation"] == "retain":
            continue
        if operation["operation"] == "delete":
            if live.is_file():
                live.unlink()
                remove_empty_parents(live, root)
        else:
            candidate = candidate_path(workspace, operation["path"])
            if not candidate.is_file() or sha256_file(candidate) != operation["target_sha256"]:
                raise AvaError("RESUME_CONFLICT", f"candidate payload is missing or corrupt: {operation['path']}")
            live.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(live, candidate.read_bytes())

    for path, item in target_payload.items():
        live = safe_live_path(root, path, permit_missing=False)
        if current_sha(live) != item["sha256"]:
            raise AvaError("POST_VALIDATION_FAILED", f"resumed payload validation failed: {path}")
    atomic_write(root / ".ava/state/manifest.json", candidate_manifest_path.read_bytes())
    for edge in journal["path"]:
        edge["completed"] = True
    for change in journal["managed_changes"]:
        if change["operation"] != "retain":
            change["classification"] = "applied"
    journal["current_edge"] = None
    journal["staging"]["managed_commit_complete"] = True
    journal["updated_at"] = now()
    semantic = candidate_manifest["semantic_compatibility"]
    if semantic["status"] == "complete":
        journal.update({"status": "complete", "stage": "complete", "staging": None, "allowed_operations": ["normal"]})
        atomic_json(root / ".ava/state/upgrade.json", journal)
        shutil.rmtree(transaction_root, ignore_errors=True)
    else:
        journal.update({"status": "active", "stage": "semantic", "allowed_operations": ["inspect", "reconcile-semantic", "rollback"]})
        atomic_json(root / ".ava/state/upgrade.json", journal)
    print("Ava deterministic upgrade resumed successfully.")


def perform_abort(args: argparse.Namespace) -> None:
    root = args.target.expanduser().resolve()
    installed, journal = load_installed_state(root)
    if installed is None or journal is None or journal.get("status") not in {"active", "blocked"}:
        raise AvaError("NO_TRANSACTION", "there is no active upgrade transaction")
    staging = journal.get("staging")
    if not isinstance(staging, dict):
        raise AvaError("NO_TRANSACTION", "upgrade transaction has no staging state")
    if staging.get("live_mutation_started"):
        perform_rollback(args)
        return
    transaction_root, plan = load_active_plan(root, journal)
    restore_transaction(root, plan, terminal="source")
    shutil.rmtree(transaction_root, ignore_errors=True)
    print("Ava upgrade aborted before live managed mutation.")


def perform_finalize(args: argparse.Namespace) -> None:
    root = args.target.expanduser().resolve()
    installed, journal = load_installed_state(root)
    if installed is None or journal is None:
        raise AvaError("NO_TRANSACTION", "Ava is not installed")
    if installed["semantic_compatibility"]["status"] != "complete":
        raise AvaError("SEMANTIC_STATE_BLOCKED", "semantic compatibility is not complete")
    if journal.get("status") not in {"active", "blocked", "complete"}:
        raise AvaError("NO_TRANSACTION", "upgrade journal is not finalizable")
    transaction_root = None
    if journal.get("staging"):
        transaction_root, _ = load_active_plan(root, journal)
    journal.update({
        "status": "complete",
        "stage": "complete",
        "current_edge": None,
        "updated_at": now(),
        "staging": None,
        "failure": None,
        "allowed_operations": ["normal"],
    })
    atomic_json(root / ".ava/state/upgrade.json", journal)
    if transaction_root:
        shutil.rmtree(transaction_root, ignore_errors=True)
    print("Ava upgrade finalized; normal routing is enabled.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install or upgrade Ava from immutable GitHub Release assets.")
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--version")
    parser.add_argument("--asset-dir", type=Path, help="Use a verified local release asset directory, primarily for development and offline installation.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit normalized JSON Lines plan output.")
    parser.add_argument("--verified", action="store_true", help="Require GitHub immutable release and asset attestation verification.")
    parser.add_argument("--adopt-existing-agents", action="store_true", help="Explicitly authorize replacement of an existing ./AGENTS.md after its project meaning has been preserved or discarded.")
    parser.add_argument(
        "--host-entrypoint",
        metavar="PATH",
        help="Record an existing project-owned host instruction file, relative to the project root. The installer validates but never modifies it.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--resume", action="store_true")
    mode.add_argument("--abort", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    mode.add_argument("--finalize", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.verified and args.asset_dir:
        raise AvaError("INVALID_ARGUMENT", "--verified cannot authenticate an arbitrary local asset directory")
    if args.resume:
        perform_resume(args)
    elif args.abort:
        perform_abort(args)
    elif args.rollback:
        perform_rollback(args)
    elif args.finalize:
        perform_finalize(args)
    else:
        perform_install(args)
    return 0


try:
    raise SystemExit(main())
except AvaError as exc:
    if "--json" in sys.argv:
        print(json.dumps({"type": "error", "code": exc.code, "message": exc.message}, sort_keys=True), file=sys.stderr)
    else:
        print(f"ERROR [{exc.code}]: {exc.message}", file=sys.stderr)
    raise SystemExit(1)
except (OSError, json.JSONDecodeError, tarfile.TarError) as exc:
    print(f"ERROR [INTERNAL_FAILURE]: {exc}", file=sys.stderr)
    raise SystemExit(1)
