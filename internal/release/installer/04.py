def construct_target_payload(
    bundles: list[Bundle], edges: list[dict[str, Any]]
) -> tuple[dict[str, dict[str, Any]], list[tuple[Bundle, dict[str, Any]]], list[dict[str, Any]]]:
    target = bundles[-1]
    payload: dict[str, dict[str, Any]] = {}
    for item in target.manifest["installed_files"]:
        if item["ownership"] != "ava-managed":
            continue
        allowed_managed_destination(item)
        payload[item["destination"]] = {
            "path": item["destination"],
            "role": item["role"],
            "sha256": item["sha256"],
            "source": str(target.base / item["source_path"]),
        }

    guidance_sources: list[tuple[Bundle, dict[str, Any]]] = []
    seen_guidance: dict[str, str] = {}
    for bundle, edge in zip(bundles, edges):
        inventory = {item["path"]: item for item in bundle.manifest["guidance"]["entries"]}
        for relative in edge["guidance_paths"]:
            item = inventory.get(relative)
            if item is None:
                raise AvaError("INVALID_UPGRADE_GRAPH", f"edge guidance is absent from archive: {relative}")
            destination = f"/.ava/guidance/{relative}"
            prior = seen_guidance.get(destination)
            if prior and prior != item["sha256"]:
                raise AvaError("GUIDANCE_COLLISION", f"composed guidance path differs across releases: {destination}")
            seen_guidance[destination] = item["sha256"]
            payload[destination] = {
                "path": destination,
                "role": "guidance",
                "sha256": item["sha256"],
                "source": str(bundle.guidance / relative),
            }
            guidance_sources.append((bundle, item))

    migration_steps: list[dict[str, Any]] = []
    seen_migrations: set[str] = set()
    for edge_index, (bundle, edge) in enumerate(zip(bundles, edges)):
        inventory = {item["id"]: item for item in bundle.manifest["migrations"]["steps"]}
        for migration_id in edge["migration_ids"]:
            if migration_id in seen_migrations:
                raise AvaError("INVALID_MIGRATION_GRAPH", f"duplicate migration id across path: {migration_id}")
            step = inventory.get(migration_id)
            if step is None:
                raise AvaError("INVALID_MIGRATION_GRAPH", f"edge migration is absent from release: {migration_id}")
            if step["from"] != edge["from"] or step["to"] != edge["to"]:
                raise AvaError("INVALID_MIGRATION_GRAPH", f"migration transition mismatch: {migration_id}")
            migration_steps.append({**step, "bundle": bundle, "edge_index": edge_index})
            seen_migrations.add(migration_id)
    return payload, guidance_sources, migration_steps


def topological_migrations(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {step["id"]: step for step in steps}
    for step in steps:
        for dependency in step["depends_on"]:
            if dependency not in by_id:
                raise AvaError("INVALID_MIGRATION_GRAPH", f"missing migration dependency: {dependency}")
    ordered: list[dict[str, Any]] = []
    remaining = set(by_id)
    while remaining:
        ready = [by_id[item] for item in remaining if set(by_id[item]["depends_on"]).issubset({entry["id"] for entry in ordered})]
        if not ready:
            raise AvaError("INVALID_MIGRATION_GRAPH", "migration dependency cycle")
        ready.sort(key=lambda item: (item["order"], item["id"]))
        for item in ready:
            ordered.append(item)
            remaining.remove(item["id"])
    return ordered


def candidate_path(workspace: Path, destination: str) -> Path:
    return workspace / "files" / destination_relative(destination)


def copy_candidate(source: Path, workspace: Path, destination: str, expected_sha: str) -> None:
    if not source.is_file() or source.is_symlink():
        raise AvaError("MISSING_ASSETS", f"candidate source missing or unsafe: {source}")
    target = candidate_path(workspace, destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if sha256_file(target) != expected_sha:
        raise AvaError("CHECKSUM_MISMATCH", f"candidate checksum mismatch: {destination}")


def execute_migrations(workspace: Path, steps: list[dict[str, Any]], target_payload: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    completed: list[dict[str, Any]] = []
    for step in topological_migrations(steps):
        bundle: Bundle = step["bundle"]
        apply_spec = read_json(bundle.migrations / step["apply_path"], "INVALID_MIGRATION")
        verify_spec = read_json(bundle.migrations / step["verify_path"], "INVALID_MIGRATION")
        if not isinstance(apply_spec, dict) or set(apply_spec) != {"operations"} or not isinstance(apply_spec["operations"], list):
            raise AvaError("INVALID_MIGRATION", f"invalid apply spec: {step['id']}")
        for operation in apply_spec["operations"]:
            if not isinstance(operation, dict) or operation.get("operation") not in {"write", "delete"}:
                raise AvaError("INVALID_MIGRATION", f"invalid operation in migration: {step['id']}")
            destination = operation.get("path", "")
            destination_relative(destination)
            if destination not in target_payload and not destination.startswith("/.ava/state/"):
                raise AvaError("MIGRATION_SCOPE", f"migration targets undeclared managed path: {destination}")
            target = candidate_path(workspace, destination)
            if operation["operation"] == "delete":
                if set(operation) != {"operation", "path"}:
                    raise AvaError("INVALID_MIGRATION", f"invalid delete operation: {step['id']}")
                target.unlink(missing_ok=True)
            else:
                if set(operation) != {"operation", "path", "source"}:
                    raise AvaError("INVALID_MIGRATION", f"invalid write operation: {step['id']}")
                source_relative = safe_relative(operation["source"])
                source = bundle.migrations / source_relative
                if not source.is_file() or source.is_symlink():
                    raise AvaError("INVALID_MIGRATION", f"migration source missing: {source_relative}")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
        if not isinstance(verify_spec, dict) or set(verify_spec) != {"checks"} or not isinstance(verify_spec["checks"], list):
            raise AvaError("INVALID_MIGRATION", f"invalid verify spec: {step['id']}")
        for check in verify_spec["checks"]:
            if not isinstance(check, dict) or set(check) not in ({"path", "exists"}, {"path", "exists", "sha256"}):
                raise AvaError("INVALID_MIGRATION", f"invalid verification check: {step['id']}")
            destination = check["path"]
            destination_relative(destination)
            target = candidate_path(workspace, destination)
            if bool(target.exists()) != bool(check["exists"]):
                raise AvaError("MIGRATION_VERIFICATION", f"existence check failed: {destination}")
            if check.get("sha256") and (not target.is_file() or sha256_file(target) != check["sha256"]):
                raise AvaError("MIGRATION_VERIFICATION", f"checksum check failed: {destination}")
        completed.append({
            "id": step["id"],
            "descriptor_sha256": step["descriptor_sha256"],
            "edge_index": step["edge_index"],
            "completed_at": now(),
            "postcondition_verified": True,
        })
    for destination, item in target_payload.items():
        path = candidate_path(workspace, destination)
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            raise AvaError("MIGRATION_VERIFICATION", f"candidate differs from target release after migrations: {destination}")
    return completed


def source_release_state(manifest: dict[str, Any]) -> dict[str, str]:
    return {
        "ava_version": manifest["ava_version"],
        "okf_version": manifest["okf_version"],
        "tag": manifest["release"]["tag"],
        "source_revision": manifest["release"]["source_revision"],
        "release_manifest_sha256": manifest["release"]["release_manifest_sha256"],
    }


def build_semantic_state(installed: dict[str, Any] | None, target: Bundle, edges: list[dict[str, Any]]) -> dict[str, Any]:
    if installed is None:
        return {
            "compatible_through": target.version,
            "target_version": None,
            "status": "complete",
            "unresolved_decisions": [],
        }
    previous = installed["semantic_compatibility"]
    carry = previous["status"] != "complete"
    if carry and not all(edge["carry_unresolved_semantic_state"] for edge in edges):
        raise AvaError("SEMANTIC_STATE_BLOCKED", "upgrade path does not permit carrying unresolved semantic state")

    explicit_edge_decision = False
    selected_edge_requires_review = False
    for edge in edges:
        guidance_present = bool(edge["guidance_paths"])
        if "semantic_review_required" in edge:
            explicit_edge_decision = True
            required = edge["semantic_review_required"]
            if not isinstance(required, bool):
                raise AvaError("INVALID_UPGRADE_GRAPH", "edge semantic review decision is not boolean")
            if required and not guidance_present:
                raise AvaError("MISSING_GUIDANCE", "semantic review is required but the selected upgrade edge declares no guidance")
            if not required and guidance_present:
                raise AvaError("INVALID_UPGRADE_GRAPH", "selected non-semantic upgrade edge declares guidance")
            selected_edge_requires_review = selected_edge_requires_review or required
        else:
            selected_edge_requires_review = selected_edge_requires_review or guidance_present

    if not explicit_edge_decision:
        selected_edge_requires_review = (
            target.manifest["semantic_review_required"]
            or selected_edge_requires_review
        )
        if target.manifest["semantic_review_required"] and not any(edge["guidance_paths"] for edge in edges):
            raise AvaError("MISSING_GUIDANCE", "semantic review is required but the selected legacy upgrade path declares no guidance")

    if selected_edge_requires_review or carry:
        return {
            "compatible_through": previous["compatible_through"],
            "target_version": target.version,
            "status": "pending",
            "unresolved_decisions": [],
        }
    return {
        "compatible_through": target.version,
        "target_version": None,
        "status": "complete",
        "unresolved_decisions": [],
    }


def target_manifest(
    target: Bundle,
    target_payload: dict[str, dict[str, Any]],
    semantic: dict[str, Any],
    host_integration: dict[str, str] | None,
) -> dict[str, Any]:
    files = [
        {"path": path, "role": item["role"], "kind": "payload", "sha256": item["sha256"]}
        for path, item in sorted(target_payload.items())
    ]
    files.extend((
        {"path": "/.ava/state/manifest.json", "role": "state", "kind": "state"},
        {"path": "/.ava/state/upgrade.json", "role": "state", "kind": "state"},
    ))
    return {
        "manifest_schema": 1,
        "ava_version": target.version,
        "okf_version": target.manifest["okf_version"],
        "installed_at": now(),
        "release": {
            "tag": target.tag,
            "channel": target.manifest["channel"],
            "source_revision": target.manifest["source_revision"],
            "release_manifest_sha256": target.manifest_sha256,
        },
        "managed_files": files,
        "host_integration": host_integration,
        "semantic_compatibility": semantic,
    }


def idle_journal() -> dict[str, Any]:
    return {
        "upgrade_schema": 1,
        "transaction_id": None,
        "status": "idle",
        "stage": "idle",
        "source": None,
        "target": None,
        "path": [],
        "current_edge": None,
        "created_at": None,
        "updated_at": now(),
        "staging": None,
        "migrations": {"resolved_order": [], "active_id": None, "completed": []},
        "managed_changes": [],
        "project_changes": [],
        "failure": None,
        "allowed_operations": ["normal"],
    }
