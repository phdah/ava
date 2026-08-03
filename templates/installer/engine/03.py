                    except OSError:
                        pass
            else:
                atomic_json(current_upgrade_path, upgrade)
        except Exception:
            pass

    try:
        current_upgrade_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_json(current_upgrade_path, upgrade)
        staging_state['live_mutation_started'] = True
        upgrade['updated_at'] = now()
        atomic_json(current_upgrade_path, upgrade)

        for change in changes:
            if change.operation in {'retain', 'skip'}:
                continue
            live = target_path(destination(change.path))
            if change.operation in {'replace', 'delete'}:
                backup(change)
            if change.operation == 'delete':
                live.unlink()
                applied.append(change)
                continue
            assert change.source is not None
            live.parent.mkdir(parents=True, exist_ok=True)
            temp = live.with_name(f'.{live.name}.ava-new-{os.getpid()}')
            shutil.copyfile(change.source, temp)
            os.chmod(temp, stat.S_IMODE(change.source.stat().st_mode) or 0o644)
            os.replace(temp, live)
            applied.append(change)

        migration_steps = {step['id']: step for step in release.get('migrations', {}).get('steps', [])}
        migration_ids = selected_edge.get('migration_ids', []) if selected_edge else []
        upgrade['stage'] = 'migrating'
        upgrade['migrations']['resolved_order'] = migration_ids
        atomic_json(current_upgrade_path, upgrade)
        for migration_id in migration_ids:
            step = migration_steps.get(migration_id)
            if step is None:
                fail('MISSING_MIGRATION', f'upgrade edge references unknown migration: {migration_id}', stage='migrating')
            apply_script = migration_root.joinpath(*rel_path(step['apply_path'], field='migration apply path').parts)
            verify_script = migration_root.joinpath(*rel_path(step['verify_path'], field='migration verify path').parts)
            upgrade['migrations']['active_id'] = migration_id
            atomic_json(current_upgrade_path, upgrade)
            env = dict(os.environ, AVA_TARGET_ROOT=str(TARGET), AVA_SOURCE_VERSION=source_version or '', AVA_TARGET_VERSION=target_version)
            subprocess.run(['/bin/sh', str(apply_script)], check=True, env=env)
            subprocess.run(['/bin/sh', str(verify_script)], check=True, env=env)
            upgrade['migrations']['completed'].append({
                'id': migration_id,
                'descriptor_sha256': step['descriptor_sha256'],
                'edge_index': 0,
                'completed_at': now(),
                'postcondition_verified': True,
            })
            upgrade['migrations']['active_id'] = None

        upgrade['stage'] = 'validating'
        atomic_json(current_upgrade_path, upgrade)
        for change in changes:
            if change.ownership != 'ava-managed' or change.operation in {'delete', 'skip'}:
                continue
            live = target_path(destination(change.path))
            if not live.is_file() or sha256(live) != change.target_sha:
                fail('POST_APPLY_VALIDATION_FAILED', 'managed payload did not match target checksum', stage='validating', path=change.path)

        semantic_required = bool(release.get('semantic_review_required')) and current is not None
        if semantic_required:
            previous_compat = current.get('semantic_compatibility', {})
            semantic = {
                'compatible_through': previous_compat.get('compatible_through', source_version),
                'target_version': target_version,
                'status': 'pending',
                'unresolved_decisions': [],
            }
        else:
            semantic = {
                'compatible_through': target_version,
                'target_version': None,
                'status': 'complete',
                'unresolved_decisions': [],
            }

        manifest_files = []
        for path, record in sorted(target_payload.items()):
            manifest_files.append({'path': path, 'role': record.get('role', 'base'), 'kind': 'payload', 'sha256': record['sha256']})
        manifest_files.extend([
            {'path': '/.ava/state/manifest.json', 'role': 'state', 'kind': 'state'},
            {'path': '/.ava/state/upgrade.json', 'role': 'state', 'kind': 'state'},
        ])
        candidate_manifest = {
            'manifest_schema': release['manifest_schema'],
            'ava_version': target_version,
            'okf_version': release['okf_version'],
            'installed_at': now(),
            'release': {
                'tag': release['tag'],
                'channel': release['channel'],
                'source_revision': release['source_revision'],
                'release_manifest_sha256': RELEASE_SHA,
            },
            'managed_files': manifest_files,
            'semantic_compatibility': semantic,
        }
        atomic_json(transaction_root / 'candidate-manifest.json', candidate_manifest)

        upgrade['stage'] = 'base-installed'
        staging_state['managed_commit_complete'] = True
        for edge in upgrade['path']:
            edge['completed'] = True
        for item in upgrade['managed_changes']:
            if item['classification'] == 'staged':
                item['classification'] = 'applied'
            item['current_sha256'] = item['target_sha256']
        atomic_json(current_upgrade_path, upgrade)

        atomic_json(current_manifest_path, candidate_manifest)

        if semantic_required:
            upgrade['status'] = 'active'
            upgrade['stage'] = 'semantic'
            upgrade['allowed_operations'] = ['inspect', 'reconcile-semantic', 'abort', 'rollback']
        else:
            upgrade['status'] = 'complete'
            upgrade['stage'] = 'complete'
            upgrade['allowed_operations'] = ['normal']
        upgrade['updated_at'] = now()
        atomic_json(current_upgrade_path, upgrade)

        discovery = 'host-bootstrap' if BOOTSTRAP else 'explicit-only'
        print(f'AVA_RESULT mode=applied source={source_version or "none"} target={target_version} discovery={discovery} semantic={semantic["status"]}')
        if semantic_required:
            print('AVA_HANDOFF Read ./.ava/guidance and activate the managed Upgrade Role to reconcile project-owned context.')
        else:
            shutil.rmtree(transaction_root)
    except BaseException:
        rollback()
        raise

except AvaError as exc:
    parts = [f'AVA_ERROR code={exc.code}', f'stage={exc.stage}']
    if exc.path:
        parts.append(f'path={exc.path}')
    parts.append(f'message={json.dumps(exc.message)}')
    print(' '.join(parts), file=sys.stderr)
    raise SystemExit(1)
except subprocess.CalledProcessError as exc:
    print(f'AVA_ERROR code=MIGRATION_FAILED stage=migrating message={json.dumps(str(exc))}', file=sys.stderr)
    raise SystemExit(1)
