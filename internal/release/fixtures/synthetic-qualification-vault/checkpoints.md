# Interrupted Upgrade Qualification Checkpoints

`checkpoint.py` is repository-only qualification tooling for the synthetic v1 vault. It deliberately stops the exact assembled target installer at durable transaction boundaries so `--abort` and `--resume` can be exercised against authentic installer-created state.

It is not an installer mode, is not included in release assets, and must not be copied into an installed project.

## Preconditions

Start from an isolated project with a healthy source Ava release already installed. Semantic compatibility must be complete and no upgrade transaction may be active. Use the exact assembled target asset directory under qualification.

```sh
PROJECT=/absolute/path/to/project
TARGET_ASSETS=/absolute/path/to/target/assets
```

## Abort checkpoint

Create the checkpoint:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/checkpoint.py \
  abort \
  --target "$PROJECT" \
  --asset-dir "$TARGET_ASSETS"
```

The command succeeds only when the real installer has created its plan, backup, candidate workspace, and active journal while `stage` is `staged`, `live_mutation_started` is `false`, `managed_commit_complete` is `false`, and `abort` is allowed. The live installed manifest and managed payload remain at the source release.

Exercise the public recovery operation with the same assembled installer:

```sh
sh "$TARGET_ASSETS/ava-install.sh" \
  --target "$PROJECT" \
  --asset-dir "$TARGET_ASSETS" \
  --abort
```

Accept the scenario only when the source manifest and managed checksums are restored, the exact transaction workspace is removed, project-owned hashes are unchanged, and normal routing is enabled again.

## Resume checkpoint

Create the checkpoint:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/checkpoint.py \
  resume \
  --target "$PROJECT" \
  --asset-dir "$TARGET_ASSETS"
```

The command lets the real installer perform the managed writes and deliberately interrupts immediately before the live target manifest commit. The resulting transaction must remain `active/validating` with `live_mutation_started` true, `managed_commit_complete` false, the source manifest still live, the target candidate manifest durable, and `resume` allowed.

Exercise the public recovery operation:

```sh
sh "$TARGET_ASSETS/ava-install.sh" \
  --target "$PROJECT" \
  --asset-dir "$TARGET_ASSETS" \
  --resume
```

For a target that does not require semantic reconciliation, accept only the complete target state with `allowed_operations: ["normal"]` and no remaining transaction workspace. For a semantic target, accept the authentic post-resume semantic stage defined by the installer instead. In either case, project-owned hashes must remain unchanged.

## Safety and evidence boundary

The harness extracts and executes the Python payload from the exact assembled `ava-install.sh`. It removes only the script's top-level command dispatcher in memory, then intercepts existing atomic transaction writes to stop at the selected boundary. It does not write or edit `manifest.json`, `upgrade.json`, `plan.json`, backups, candidate files, or managed payload itself.

Before reporting a checkpoint, it verifies the installer-created transaction structure, candidate target identity, permitted source/current/target managed checksums, and project-owned inventory. A checkpoint JSON record proves only that the setup state is authentic. It is not accepted qualification evidence until the real assembled installer operation has run and the resulting terminal state is recorded in the scenario run manifest.
