        elif ownership == 'project-owned':
            if operation != 'create-if-absent' or role != 'scaffold':
                fail('INVALID_RELEASE_MANIFEST', f'project-owned entry is not create-if-absent scaffold: {dest_value}')
            if dest_value.startswith('/.ava/') or dest_value == '/AGENTS.md':
                fail('INVALID_SCAFFOLD_PATH', 'project scaffold targets a managed path', path=dest_value)
            live = target_path(dest)
            if live.exists():
                changes.append(Change(dest_value, 'skip', ownership, 'project-owned path already exists', source, record['sha256'], None, role))
            else:
                changes.append(Change(dest_value, 'create', ownership, 'create-if-absent project scaffold', source, record['sha256'], None, role))
        else:
            fail('INVALID_RELEASE_MANIFEST', f'unknown ownership class: {ownership!r}')

    if BOOTSTRAP and selected_bootstraps != 1:
        fail('UNKNOWN_BOOTSTRAP', f'no optional bootstrap has destination /{BOOTSTRAP}')

    def add_archive_payload(root: pathlib.Path, inventory: Any, prefix: str, role: str) -> None:
        if not isinstance(inventory, list):
            fail('INVALID_RELEASE_MANIFEST', f'{role} inventory must be an array')
        for entry in inventory:
            source_rel = rel_path(entry.get('path', ''), field=f'{role} path')
            source = root.joinpath(*source_rel.parts)
            if not source.is_file() or sha256(source) != entry.get('sha256'):
                fail('PAYLOAD_CHECKSUM_MISMATCH', f'{role} inventory does not match archive', path=str(source_rel))
            dest_value = f'/{prefix}/{source_rel}'
            target_payload[dest_value] = {'sha256': entry['sha256'], 'role': role}
            live = target_path(destination(dest_value))
            old = old_payload.get(dest_value)
            if old and old.get('sha256') == entry['sha256']:
                changes.append(Change(dest_value, 'retain', 'ava-managed', f'{role} payload already matches target', source, entry['sha256'], old['sha256'], role))
            elif old:
                changes.append(Change(dest_value, 'replace', 'ava-managed', f'{role} payload changes in target release', source, entry['sha256'], old['sha256'], role))
            elif live.exists():
                fail('MANAGED_PATH_COLLISION', f'unclassified path collides with {role} payload', path=dest_value)
            else:
                changes.append(Change(dest_value, 'create', 'ava-managed', f'new {role} payload', source, entry['sha256'], None, role))

    add_archive_payload(guidance_root, release.get('guidance', {}).get('entries', []), '.ava/guidance', 'guidance')
    add_archive_payload(migration_root, release.get('migrations', {}).get('files', []), '.ava/migrations', 'migration')

    for old_path, entry in old_payload.items():
        if old_path not in target_payload and not any(c.path == old_path and c.operation == 'delete' for c in changes):
            changes.append(Change(old_path, 'delete', 'ava-managed', 'managed payload removed by target release', None, None, entry['sha256'], entry.get('role')))

    for change in sorted(changes, key=lambda item: item.path):
        print(f'AVA_PLAN operation={change.operation} ownership={change.ownership} path={change.path} reason={json.dumps(change.reason)}')

    if DRY_RUN:
        print(f'AVA_RESULT mode=dry-run source={source_version or "none"} target={target_version} discovery={"host-bootstrap" if BOOTSTRAP else "explicit-only"}')
        if workspace_ctx:
            workspace_ctx.cleanup()
        raise SystemExit(0)

    transaction_id = transaction_root.name
    created_at = now()
    source_state = None
    if current:
        source_state = {
            'ava_version': current['ava_version'],
            'okf_version': current['okf_version'],
            'tag': current['release']['tag'],
            'source_revision': current['release']['source_revision'],
            'release_manifest_sha256': current['release']['release_manifest_sha256'],
        }
    target_state = {
        'ava_version': release['ava_version'],
        'okf_version': release['okf_version'],
        'tag': release['tag'],
        'source_revision': release['source_revision'],
        'release_manifest_sha256': RELEASE_SHA,
    }
    edge_journal = []
    if selected_edge:
        edge_journal = [{**selected_edge, 'completed': False}]

    managed_journal = []
    for change in changes:
        if change.ownership == 'ava-managed':
            managed_journal.append({
                'path': change.path,
                'operation': 'retain' if change.operation == 'retain' else change.operation,
                'previous_sha256': change.previous_sha,
                'current_sha256': change.previous_sha,
                'target_sha256': change.target_sha,
                'classification': 'unchanged' if change.operation == 'retain' else 'staged',
            })

    staging_state = {
        'workspace': f'/.ava-install-{transaction_id}/workspace',
        'backup': f'/.ava-install-{transaction_id}/backup',
        'candidate_manifest': f'/.ava-install-{transaction_id}/candidate-manifest.json',
        'live_mutation_started': False,
        'managed_commit_complete': False,
    }
    upgrade = {
        'upgrade_schema': 1,
        'transaction_id': transaction_id,
        'status': 'active',
        'stage': 'staged',
        'source': source_state or target_state,
        'target': target_state,
        'path': edge_journal or [{
            'from': target_version,
            'to': target_version,
            'mode': 'direct',
            'intermediates': [],
            'carry_unresolved_semantic_state': False,
            'migration_ids': [],
            'guidance_paths': [],
            'completed': False,
        }],
        'current_edge': 0,
        'created_at': created_at,
        'updated_at': created_at,
        'staging': staging_state,
        'migrations': {'resolved_order': [], 'active_id': None, 'completed': []},
        'managed_changes': managed_journal,
        'project_changes': [],
        'failure': None,
        'allowed_operations': ['inspect', 'abort', 'rollback'],
    }

    backup_root = transaction_root / 'backup'
    backup_root.mkdir()
    applied: list[Change] = []

    def backup(change: Change) -> None:
        live = target_path(destination(change.path))
        if not live.exists():
            return
        relative = destination(change.path)
        backup_path = backup_root.joinpath(*relative.parts)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(live, backup_path)

    def rollback() -> None:
        for change in reversed(applied):
            live = target_path(destination(change.path))
            backup_path = backup_root.joinpath(*destination(change.path).parts)
            if backup_path.exists():
                live.parent.mkdir(parents=True, exist_ok=True)
                os.replace(backup_path, live)
            elif live.exists():
                live.unlink()
        upgrade['status'] = 'rolled-back'
        upgrade['stage'] = 'rolled-back'
        upgrade['updated_at'] = now()
        upgrade['allowed_operations'] = ['normal']
        upgrade['failure'] = None
        try:
            if current is None:
                current_upgrade_path.unlink(missing_ok=True)
                for directory in (current_upgrade_path.parent, current_upgrade_path.parent.parent):
                    try:
                        directory.rmdir()
