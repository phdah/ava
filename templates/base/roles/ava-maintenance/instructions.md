---
type: Role Instructions
title: Ava Maintenance Instructions
description: Procedure for reporting installed state, coordinating deterministic recovery, finalizing successful upgrades, checking host access, initiating upgrades, and safely removing Ava.
tags: [ava, role, maintenance, installation, recovery, uninstall, instructions]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T21:47:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T14:51:00+02:00
---

# Entry procedure

Before reporting or mutating installation state:

1. Resolve the project root used by the active host.
2. Read `./.ava/state/manifest.json` and `./.ava/state/upgrade.json` when present.
3. Validate their supported envelopes and internal relationship before trusting version, ownership, stage, or operation fields.
4. Classify the request as read-only inspection, deterministic operation coordination, explicit upgrade, semantic handoff, finalization, or removal.
5. Stop before mutation when managed state cannot prove the requested authority or exact target paths.

Do not read project-owned registries to establish maintenance authority.

# Installation report

Report these fields separately:

- installed Ava base version from `ava_version`
- release tag and channel
- source revision
- installed OKF version
- manifest schema and journal schema support
- semantic compatible-through version
- semantic target version
- semantic status and unresolved decisions
- journal status, stage, failure, and allowed operations
- host integration and managed-context accessibility
- managed-file integrity summary

Never collapse installed version and semantic compatibility into one up-to-date value.

# Managed integrity inspection

Use the manifest as the ownership and checksum inventory.

For every managed payload entry:

1. resolve its logical path beneath the project root
2. reject traversal, symlink ambiguity, and non-regular files
3. classify the current state as unchanged, missing, modified, or invalid
4. compare bytes using the recorded SHA-256 value

Validate managed state files through their schemas and allowed transitions rather than expecting self-checksums.

Report unrecorded content beneath `./.ava/` as unexpected unless the journal identifies it as the current transaction workspace, backup, or candidate state. Do not delete or adopt unexpected content automatically.

A modified, missing, or corrupt managed path remains Ava-managed conflict evidence. Do not overwrite, merge, reclassify, or manually reconstruct it.

# Host accessibility

Report host discovery as one of the states supported by the installed contract, such as project-provided or explicit-only. Do not claim native host support without maintained conformance evidence.

For a recorded project-owned host entrypoint:

- verify that the exact path exists as a normal file
- report that Ava does not own or modify it
- report a stale or inaccessible entrypoint without repairing it automatically

For OpenCode, inspect `./opencode.json` or `./opencode.jsonc` only when present. Report managed context as readable when project configuration permits reading `.ava/**`. Report whether editing `.ava/**` is denied, asks for confirmation, or is broader than the default recommendation. When the required read permission is absent, provide the minimal merge instruction and preserve the project-owned file unchanged unless the user separately authorizes project configuration work.

# Deterministic transaction recovery

Use journal status, stage, staging state, failure, and `allowed_operations` to explain the safe next action.

- Invoke resume only when `resume` is allowed and recorded source, current, or target checksums prove safe continuation.
- Invoke abort only when `abort` is allowed. Before live mutation it discards the staged transaction; after live mutation the existing installer may convert abort into rollback.
- Invoke rollback only when `rollback` is allowed and project-owned semantic changes have the explicit resolutions required by the protocol.
- Use the exact existing installer or updater operation for resume, abort, and rollback. Do not reproduce those state transitions manually.

When the journal requires `reconcile-semantic`, hand the project-owned reconciliation task to the Upgrade Role. Ava Maintenance may continue to explain the deterministic state, but it must not mark semantic compatibility pending, partial, blocked, or complete.

If the host cannot execute a required installer-backed operation, report the exact command or action the user must run. Do not claim that the operation completed.

# Successful upgrade finalization

Finalization is the only deterministic journal transition Ava Maintenance performs directly. It is not an installer invocation and must not trigger a search for an `ava` binary, updater executable, or transaction-local installer path.

Before changing any journal field, verify all of these preconditions from managed state:

1. `manifest.json` is valid and reports `semantic_compatibility.status: "complete"` for the installed target.
2. The semantic compatibility object has no unresolved decisions.
3. `upgrade.json` is valid and represents the same installed target and transaction.
4. The managed commit is complete, every selected path edge is completed, and every managed change that required action has a terminal classification.
5. The journal is `active/semantic` or another protocol-defined finalizable state reached after the managed commit; it is not an earlier deterministic stage and has no unresolved failure requiring resume, resolve, abort, or rollback.
6. Any recorded transaction workspace selected for cleanup resolves safely beneath `./.ava/state/transactions/` and belongs to this exact journal.

If any precondition is missing, contradictory, or cannot be proven, stop without changing the journal. Explain the exact failed precondition and keep normal routing blocked.

After every precondition passes, atomically write the protocol-defined terminal journal transition directly to `./.ava/state/upgrade.json`:

```json
{
  "status": "complete",
  "stage": "complete",
  "current_edge": null,
  "staging": null,
  "failure": null,
  "allowed_operations": ["normal"]
}
```

Also refresh the journal's `updated_at` using the established state timestamp format. Preserve all other journal fields unchanged unless the installed protocol explicitly defines them as part of this terminal transition.

After the atomic terminal write succeeds, remove only the exact recorded transaction workspace for this journal. Do not remove backups or any other state unless the protocol identifies them as part of that workspace. Verify that the journal now reads as `complete/complete`, `allowed_operations` is exactly `["normal"]`, semantic compatibility remains complete, and the recorded transaction workspace is absent.

This direct write is a bounded finalization exception to the general rule against manual journal mutation. It does not authorize manual resume, repair, rollback, semantic-state changes, or arbitrary managed-state editing.

# Explicit upgrade

An explicit upgrade remains a deterministic installer or updater operation.

Before invocation:

1. report the current installed identity and semantic status
2. confirm that no incompatible active transaction owns the installation
3. resolve the requested release or channel through the installer contract
4. prefer dry-run inspection when the target or project collision outcome is not yet established
5. invoke the verified existing mechanism only with user authorization

Do not add or require standalone status, version, repair, finalization, or uninstall command modes. User requests interpreted by this role are the interface.

# Removal procedure

Removal is a bounded role-led filesystem operation, not a release transaction.

Proceed only after explicit user intent and all of these checks pass:

1. `manifest.json` proves this is a supported Ava installation.
2. The journal is in a safe terminal or idle state.
3. Semantic compatibility has no active pending, partial, or blocked work.
4. Every path selected for deletion is recorded as Ava-managed.
5. `./AGENTS.md` still matches its recorded managed checksum.
6. No unrecorded content exists beneath `./.ava/`.
7. No modified, missing, corrupt, or non-regular managed path would cause uncertain or project-specific content to be discarded.

When a recorded managed file is modified, missing, corrupt, or unexpected content exists, report it and require an explicit conflict resolution before removal. Do not treat a general uninstall request as permission to discard uncertain content.

After the checks pass:

1. record the exact project-owned paths that must be preserved
2. remove the complete managed `./.ava/` directory
3. remove `./AGENTS.md`
4. leave project-owned roles, workflows, shared instructions, knowledge, inbox content, root indexes, logs, OpenCode configuration, and host entrypoints unchanged
5. verify that removed managed paths are absent and preserved project-owned paths are unchanged
6. report every removed and preserved path
7. report any project-owned host entrypoint that may now contain a stale reference to `./AGENTS.md`

A modified root router blocks automatic removal because deleting it could discard project-specific meaning. A stale project-owned host entrypoint is reported, never edited automatically.

# Completion report

State:

- active role and operation
- installed and semantic state before the operation
- managed integrity findings
- deterministic mechanism invoked, or direct terminal finalization performed, when any
- exact removed, preserved, or conflicted paths
- host accessibility or stale-reference findings
- validation performed
- unresolved decisions and required user action
