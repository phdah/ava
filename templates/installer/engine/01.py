    ownership: str
    reason: str
    source: pathlib.Path | None = None
    target_sha: str | None = None
    previous_sha: str | None = None
    role: str | None = None


try:
    release = load_json(ASSETS / 'ava-release.json', 'INVALID_RELEASE_MANIFEST')
    if release.get('release_schema') != 1:
        fail('UNSUPPORTED_RELEASE_SCHEMA', f'unsupported release schema: {release.get("release_schema")}')
    for key, expected in EXPECTED.items():
        if release.get(key) != expected:
            fail('RELEASE_IDENTITY_MISMATCH', f'release {key} is {release.get(key)!r}, expected {expected!r}')
    if release.get('installer_protocol', 0) > int(os.environ['AVA_INSTALLER_PROTOCOL']):
        fail('UNSUPPORTED_INSTALLER_PROTOCOL', 'release requires a newer installer protocol')

    asset_records = release.get('assets')
    if not isinstance(asset_records, list):
        fail('INVALID_RELEASE_MANIFEST', 'assets must be an array')
    by_name = {entry.get('name'): entry for entry in asset_records if isinstance(entry, dict)}
    for name in ('ava-base.tar.gz', 'ava-guidance.tar.gz', 'ava-migrations.tar.gz'):
        record = by_name.get(name)
        path = ASSETS / name
        if not record or record.get('sha256') != sha256(path) or record.get('size') != path.stat().st_size:
            fail('ASSET_MANIFEST_MISMATCH', f'{name} does not match ava-release.json')

    installed_files = release.get('installed_files')
    if not isinstance(installed_files, list) or not installed_files:
        fail('INVALID_RELEASE_MANIFEST', 'installed_files must be a non-empty array')

    if DRY_RUN:
        workspace_ctx = tempfile.TemporaryDirectory(prefix='ava-dry-run-')
        workspace = pathlib.Path(workspace_ctx.name)
    else:
        TARGET.mkdir(parents=True, exist_ok=True)
        if TARGET.is_symlink():
            fail('UNSAFE_TARGET', 'target root must not be a symlink')
        txid = f'{dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")}-{uuid.uuid4().hex[:12]}'
        transaction_root = TARGET / f'.ava-install-{txid}'
        if transaction_root.exists():
            fail('TRANSACTION_EXISTS', 'transaction workspace already exists')
        transaction_root.mkdir(parents=True)
        workspace = transaction_root / 'workspace'
        workspace.mkdir()
        workspace_ctx = None

    base_root = validate_archive(ASSETS / 'ava-base.tar.gz', 'ava-base.tar.gz', workspace)
    guidance_root = validate_archive(ASSETS / 'ava-guidance.tar.gz', 'ava-guidance.tar.gz', workspace)
    migration_root = validate_archive(ASSETS / 'ava-migrations.tar.gz', 'ava-migrations.tar.gz', workspace)

    current_manifest_path = TARGET / '.ava' / 'state' / 'manifest.json'
    current_upgrade_path = TARGET / '.ava' / 'state' / 'upgrade.json'
    current: dict[str, Any] | None = None
    if (TARGET / '.ava').exists():
        if not current_manifest_path.is_file():
            fail('UNRECOGNIZED_AVA', '/.ava exists without a supported manifest', path='/.ava')
        current = load_json(current_manifest_path, 'INVALID_INSTALLED_MANIFEST')
        if current.get('manifest_schema') != 1:
            fail('UNSUPPORTED_MANIFEST_SCHEMA', f'unsupported installed manifest schema: {current.get("manifest_schema")}')
    elif (TARGET / 'AGENTS.md').exists() and not ADOPT_AGENTS:
        fail('AGENTS_COLLISION', 'existing /AGENTS.md requires --adopt-agents after its project-specific meaning is preserved', path='/AGENTS.md')

    if current_upgrade_path.exists():
        old_upgrade = load_json(current_upgrade_path, 'INVALID_UPGRADE_STATE')
        if old_upgrade.get('status') in {'active', 'blocked'}:
            fail('UPGRADE_ALREADY_ACTIVE', 'an active or blocked Ava upgrade must be resolved before starting another', path='/.ava/state/upgrade.json')

    old_payload: dict[str, dict[str, Any]] = {}
    if current:
        for entry in current.get('managed_files', []):
            if isinstance(entry, dict) and entry.get('kind') == 'payload':
                old_payload[entry.get('path', '')] = entry
        for path, entry in old_payload.items():
            relative = destination(path)
            live = target_path(relative)
            expected_sha = entry.get('sha256')
            if not live.is_file():
                fail('MANAGED_FILE_MISSING', 'managed file is missing', path=path)
            actual = sha256(live)
            if actual != expected_sha:
                fail('MANAGED_FILE_CONFLICT', f'managed file checksum is {actual}, expected {expected_sha}', path=path)

    source_version = current.get('ava_version') if current else None
    target_version = release['ava_version']
    selected_edge: dict[str, Any] | None = None
    if source_version and source_version != target_version:
        edges = release.get('upgrade_paths', {}).get('edges', [])
        for edge in edges:
            if edge.get('from') == source_version and edge.get('to') == target_version:
                selected_edge = edge
                break
        if selected_edge is None:
            fail('UNSUPPORTED_UPGRADE_PATH', f'no declared upgrade path from {source_version} to {target_version}')
        if selected_edge.get('mode') == 'chained':
            intermediates = ', '.join(selected_edge.get('intermediates', []))
            fail('INTERMEDIATE_RELEASE_REQUIRED', f'install intermediate releases in order before {target_version}: {intermediates}')
        compatibility = current.get('semantic_compatibility', {})
        if compatibility.get('status') != 'complete' and not selected_edge.get('carry_unresolved_semantic_state'):
            fail('SEMANTIC_STATE_CONFLICT', 'target release does not permit carrying unresolved semantic compatibility state')

    changes: list[Change] = []
    target_payload: dict[str, dict[str, Any]] = {}
    selected_bootstraps = 0
    seen_destinations: set[str] = set()

    for record in installed_files:
        if not isinstance(record, dict):
            fail('INVALID_RELEASE_MANIFEST', 'installed_files entries must be objects')
        source_path = rel_path(record.get('source_path', ''), field='source path')
        dest_value = record.get('destination', '')
        dest = destination(dest_value)
        if dest_value in seen_destinations:
            fail('INVALID_RELEASE_MANIFEST', f'duplicate installed destination: {dest_value}')
        seen_destinations.add(dest_value)
        source = base_root.joinpath(*source_path.parts)
        if not source.is_file():
            fail('MISSING_PAYLOAD_ENTRY', f'base archive has no source entry {source_path}')
        actual_source_sha = sha256(source)
        if actual_source_sha != record.get('sha256'):
            fail('PAYLOAD_CHECKSUM_MISMATCH', f'payload entry checksum is {actual_source_sha}, expected {record.get("sha256")}', path=str(source_path))

        ownership = record.get('ownership')
        operation = record.get('operation')
        role = record.get('role')
        if ownership == 'ava-managed':
            if operation != 'replace-managed':
                fail('INVALID_RELEASE_MANIFEST', f'managed path has invalid operation: {dest_value}')
            allowed = dest_value == '/AGENTS.md' or dest_value.startswith('/.ava/') or role == 'bootstrap'
            if not allowed:
                fail('INVALID_MANAGED_PATH', 'managed path is outside the Ava namespace', path=dest_value)
            if role == 'bootstrap':
                if not BOOTSTRAP or BOOTSTRAP != dest_value.lstrip('/'):
                    continue
                selected_bootstraps += 1
            if role == 'state':
                continue
            target_payload[dest_value] = record
            live = target_path(dest)
            old = old_payload.get(dest_value)
            if old:
                if old.get('sha256') == record.get('sha256'):
                    changes.append(Change(dest_value, 'retain', ownership, 'managed payload already matches target', source, record['sha256'], old['sha256'], role))
                else:
                    changes.append(Change(dest_value, 'replace', ownership, 'verified managed payload changes in target release', source, record['sha256'], old['sha256'], role))
            elif live.exists():
                if dest_value == '/AGENTS.md' and ADOPT_AGENTS:
                    changes.append(Change(dest_value, 'replace', ownership, 'explicit /AGENTS.md adoption', source, record['sha256'], sha256(live) if live.is_file() else None, role))
                elif role == 'bootstrap' and live.is_file() and sha256(live) == record['sha256']:
                    changes.append(Change(dest_value, 'retain', ownership, 'existing bootstrap exactly matches target release', source, record['sha256'], record['sha256'], role))
                else:
                    fail('MANAGED_PATH_COLLISION', 'unclassified path collides with managed release content', path=dest_value)
            else:
                changes.append(Change(dest_value, 'create', ownership, 'new managed payload', source, record['sha256'], None, role))
