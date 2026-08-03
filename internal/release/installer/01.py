def validate_release_manifest(manifest: Any, expected_version: str) -> None:
    if not isinstance(manifest, dict):
        raise AvaError("INVALID_MANIFEST", "release manifest must be an object")
    top_keys = {
        "release_schema", "ava_version", "tag", "channel", "source_repository", "source_revision",
        "published_at", "installer_protocol", "okf_version", "manifest_schema", "semantic_review_required",
        "assets", "installed_files", "upgrade_paths", "guidance", "migrations",
    }
    require_exact_keys(manifest, top_keys, "release manifest")
    if manifest["release_schema"] != 1 or manifest["manifest_schema"] != 1:
        raise AvaError("UNSUPPORTED_SCHEMA", "unsupported release or installed manifest schema")
    if manifest["installer_protocol"] > PROTOCOL:
        raise AvaError("UNSUPPORTED_INSTALLER", f"release requires installer protocol {manifest['installer_protocol']}")
    if manifest["ava_version"] != expected_version or manifest["tag"] != f"v{expected_version}":
        raise AvaError("IDENTITY_MISMATCH", "release version and selected tag disagree")
    if manifest["channel"] != derive_channel(expected_version):
        raise AvaError("IDENTITY_MISMATCH", "release channel and version disagree")
    if manifest["source_repository"] != REPOSITORY or not SHA1_RE.fullmatch(manifest["source_revision"]):
        raise AvaError("IDENTITY_MISMATCH", "invalid release source identity")
    if not isinstance(manifest["semantic_review_required"], bool):
        raise AvaError("INVALID_MANIFEST", "semantic_review_required must be boolean")

    assets = manifest["assets"]
    if not isinstance(assets, list) or [item.get("name") for item in assets if isinstance(item, dict)] != list(ASSETS):
        raise AvaError("INVALID_MANIFEST", "release asset inventory must use the canonical ordered asset set")
    roles = ("installer", "base", "guidance", "migrations", "release-manifest", "release-notes", "checksums")
    for index, item in enumerate(assets):
        if not isinstance(item, dict) or item.get("role") != roles[index]:
            raise AvaError("INVALID_MANIFEST", f"invalid asset record: {ASSETS[index]}")
        if item["name"] not in ("ava-release.json", "SHA256SUMS"):
            if not SHA256_RE.fullmatch(str(item.get("sha256", ""))) or not isinstance(item.get("size"), int) or item["size"] < 1:
                raise AvaError("INVALID_MANIFEST", f"invalid hashed asset record: {item['name']}")

    installed = manifest["installed_files"]
    if not isinstance(installed, list) or not installed:
        raise AvaError("INVALID_MANIFEST", "installed_files must be non-empty")
    destinations: set[str] = set()
    source_paths: set[str] = set()
    for item in installed:
        keys = {"source_asset", "source_path", "destination", "ownership", "operation", "role", "sha256"}
        if not isinstance(item, dict):
            raise AvaError("INVALID_MANIFEST", "installed file record must be an object")
        require_exact_keys(item, keys, "installed file")
        if item["source_asset"] != "ava-base.tar.gz":
            raise AvaError("INVALID_MANIFEST", "installed file source asset must be ava-base.tar.gz")
        safe_relative(item["source_path"])
        destination_relative(item["destination"])
        if item["destination"] in destinations or item["source_path"] in source_paths:
            raise AvaError("INVALID_MANIFEST", "duplicate installed destination or source path")
        destinations.add(item["destination"])
        source_paths.add(item["source_path"])
        if not SHA256_RE.fullmatch(item["sha256"]):
            raise AvaError("INVALID_MANIFEST", f"invalid installed checksum: {item['destination']}")
        if item["ownership"] == "ava-managed":
            if item["operation"] != "replace-managed" or item["role"] not in {"router", "base", "bootstrap", "state"}:
                raise AvaError("INVALID_MANIFEST", f"invalid managed mapping: {item['destination']}")
        elif item["ownership"] == "project-owned":
            if item["operation"] != "create-if-absent" or item["role"] != "scaffold":
                raise AvaError("INVALID_MANIFEST", f"invalid scaffold mapping: {item['destination']}")
            allowed_roots = ("/index.md", "/log.md", "/roles/", "/workflows/", "/shared/", "/knowledge/", "/inbox/")
            if item["destination"] not in {"/index.md", "/log.md"} and not item["destination"].startswith(allowed_roots[2:]):
                raise AvaError("INVALID_MANIFEST", f"scaffold is outside project-owned extension paths: {item['destination']}")
        else:
            raise AvaError("INVALID_MANIFEST", f"invalid ownership: {item['destination']}")
    ordered_destinations = sorted(destinations)
    for index, destination in enumerate(ordered_destinations):
        prefix = destination.rstrip("/") + "/"
        if any(other.startswith(prefix) for other in ordered_destinations[index + 1:]):
            raise AvaError("INVALID_MANIFEST", f"installed file paths have a file-directory collision: {destination}")
    if "/AGENTS.md" not in destinations:
        raise AvaError("INVALID_MANIFEST", "release does not install /AGENTS.md")

    upgrade_paths = manifest["upgrade_paths"]
    if not isinstance(upgrade_paths, dict) or set(upgrade_paths) != {"edges"} or not isinstance(upgrade_paths["edges"], list):
        raise AvaError("INVALID_MANIFEST", "invalid upgrade path inventory")
    edge_sources: set[str] = set()
    for edge in upgrade_paths["edges"]:
        keys = {"from", "to", "mode", "intermediates", "carry_unresolved_semantic_state", "migration_ids", "guidance_paths"}
        if not isinstance(edge, dict):
            raise AvaError("INVALID_MANIFEST", "upgrade edge must be an object")
        require_exact_keys(edge, keys, "upgrade edge")
        source = canonical_version(edge["from"])
        if source in edge_sources or edge["to"] != expected_version:
            raise AvaError("INVALID_MANIFEST", "duplicate upgrade source or wrong target")
        edge_sources.add(source)
        intermediates = edge["intermediates"]
        if not isinstance(intermediates, list) or any(canonical_version(item) != item for item in intermediates):
            raise AvaError("INVALID_MANIFEST", "invalid intermediate version")
        if edge["mode"] == "direct" and intermediates:
            raise AvaError("INVALID_MANIFEST", "direct edge cannot declare intermediates")
        if edge["mode"] == "chained" and not intermediates:
            raise AvaError("INVALID_MANIFEST", "chained edge requires intermediates")
        if edge["mode"] not in {"direct", "chained"} or not isinstance(edge["carry_unresolved_semantic_state"], bool):
            raise AvaError("INVALID_MANIFEST", "invalid upgrade edge mode")
        if not isinstance(edge["migration_ids"], list) or len(edge["migration_ids"]) != len(set(edge["migration_ids"])):
            raise AvaError("INVALID_MANIFEST", "invalid migration id list")
        if not isinstance(edge["guidance_paths"], list) or len(edge["guidance_paths"]) != len(set(edge["guidance_paths"])):
            raise AvaError("INVALID_MANIFEST", "invalid guidance path list")
        for path in edge["guidance_paths"]:
            safe_relative(path)

    guidance = manifest["guidance"]
    if not isinstance(guidance, dict) or set(guidance) != {"entries"} or not isinstance(guidance["entries"], list):
        raise AvaError("INVALID_MANIFEST", "invalid guidance inventory")
    guidance_paths: set[str] = set()
    for item in guidance["entries"]:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise AvaError("INVALID_MANIFEST", "invalid guidance entry")
        safe_relative(item["path"])
        if item["path"] in guidance_paths or not SHA256_RE.fullmatch(item["sha256"]):
            raise AvaError("INVALID_MANIFEST", "duplicate or invalid guidance entry")
        guidance_paths.add(item["path"])

    migrations = manifest["migrations"]
    if not isinstance(migrations, dict) or set(migrations) != {"files", "steps"}:
        raise AvaError("INVALID_MANIFEST", "invalid migration inventory")
    migration_files: set[str] = set()
    for item in migrations["files"]:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise AvaError("INVALID_MANIFEST", "invalid migration file")
        safe_relative(item["path"])
        if item["path"] in migration_files or not SHA256_RE.fullmatch(item["sha256"]):
            raise AvaError("INVALID_MANIFEST", "duplicate or invalid migration file")
        migration_files.add(item["path"])
    migration_ids: set[str] = set()
    for step in migrations["steps"]:
        keys = {"id", "from", "to", "order", "depends_on", "apply_path", "verify_path", "descriptor_sha256", "idempotent"}
        if not isinstance(step, dict):
            raise AvaError("INVALID_MANIFEST", "migration step must be an object")
        require_exact_keys(step, keys, "migration step")
        if step["id"] in migration_ids or step["idempotent"] is not True or step["to"] != expected_version:
            raise AvaError("INVALID_MANIFEST", "invalid migration identity or target")
        migration_ids.add(step["id"])
        canonical_version(step["from"])
        safe_relative(step["apply_path"])
        safe_relative(step["verify_path"])
        if step["apply_path"] not in migration_files or step["verify_path"] not in migration_files:
            raise AvaError("INVALID_MANIFEST", "migration entry point missing from inventory")
        if not SHA256_RE.fullmatch(step["descriptor_sha256"]):
            raise AvaError("INVALID_MANIFEST", "invalid migration descriptor checksum")


