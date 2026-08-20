---
type: Shared Instruction
title: Maintenance and Upgrade State Routing
description: Defines managed pre-routing to Ava Maintenance or Upgrade Role, operation enforcement, guidance discovery, finalization, and return to normal routing.
tags: [ava, maintenance, upgrades, routing, state, recovery]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
updated:
  by: agent:openai-opencode
  at: 2026-08-20T11:51:12Z
---

# Purpose

This instruction governs the state check that occurs before ordinary workflow or role routing in an installed Ava project.

Its purpose is to keep installation inspection and deterministic recovery reachable through Ava Maintenance, while reserving project-owned semantic reconciliation for Upgrade Role. Both must remain reachable when project-owned routing or context is missing, corrupt, or incompatible with the installed base.

All paths beginning with `./` are resolved from the project root.

# Managed inputs

Use only these managed inputs to decide the pre-routing mode:

- `./.ava/state/upgrade.json`
- `./.ava/state/manifest.json`
- `./.ava/state/transactions/` existence and direct entries
- `./.ava/base/roles/ava-maintenance/index.md`
- `./.ava/base/roles/upgrade-role/index.md`
- each selected journal edge's explicit `semantic_review_required` decision
- the exact relative guidance paths recorded in the upgrade transaction, resolved beneath `./.ava/guidance/` after Upgrade Role activation

The release-wide semantic-review declaration is only a release inventory summary. When selected journal edges contain explicit semantic decisions, routing uses those edge decisions and must not apply another edge's requirement to the current source path.

Do not read `./roles/index.md`, `./workflows/index.md`, or other project-owned routing files before managed pre-routing is resolved.

# Minimal pre-routing check

Before ordinary instruction resolution:

1. Confirm that `upgrade.json` is parseable and has a supported `upgrade_schema`.
2. Confirm that `manifest.json` exposes a supported manifest envelope and semantic-compatibility object.
3. Enter Ava Maintenance mode when either managed state file is missing, malformed, unsupported, or internally contradictory.
4. Enter Ava Maintenance mode when the journal is `active` or `blocked` and the request concerns deterministic inspection, resume, abort, rollback, finalization, recovery, host accessibility, or installation administration.
5. Enter Ava Maintenance mode for active deterministic stages before semantic reconciliation, including planning, preflight, staged, migrating, validating, base-installed, and rollback.
6. Enter Upgrade Role mode only when selected journal edges require semantic review, carried semantic state remains incomplete, or the journal stage is `semantic`, and the requested outcome is to reconcile or resolve project-owned semantic context.
7. Require every explicit semantic edge decision to agree with its guidance list: `true` requires one or more exact guidance paths and `false` requires none.
8. When semantic work blocks an unrelated request, activate Ava Maintenance to explain the blocked state and required handoff rather than performing ordinary routing.
9. Enter Ava Maintenance mode when `./.ava/state/transactions/` exists with a safe terminal journal. Treat a directory identified by a `complete`, `aborted`, or `rolled-back` transaction ID, an empty container, or one restored-source transaction proven under the `idle` replay rules as interrupted terminal cleanup that permits only bounded replay; any other entry is a managed-state conflict.
10. Enter normal routing only when the journal is in a protocol-defined safe terminal state, semantic compatibility is `complete`, and `./.ava/state/transactions/` is absent.

A journal state must never broaden its `allowed_operations` beyond the upgrade protocol.

# Ava Maintenance mode

In Ava Maintenance mode:

1. Activate `./.ava/base/roles/ava-maintenance/role.md` directly.
2. Read its `index.md` and every document it marks as required.
3. Announce `Active role: Ava Maintenance`.
4. Compare the requested deterministic operation with the journal state and `allowed_operations`.
5. Inspect only managed state, manifest-declared payloads, recorded transaction paths, and exact recorded host integration needed for the request.
6. Use existing installer or updater operations for upgrade, resume, abort, and rollback. For successful upgrade finalization only, use the protocol-defined direct terminal state transition after proving every finalization precondition. Replay bounded terminal cleanup only when the terminal journal identifies the exact transaction, the container is empty, or the `idle` restored-source evidence proves one exact residual transaction.
7. Keep project-owned registries and ordinary routing blocked until normal operation is permitted.

Ava Maintenance may explain semantic state and direct the user to Upgrade Role, but it must not apply project-owned reconciliation or update semantic compatibility.

# Upgrade Role mode

In Upgrade Role mode:

1. Confirm that `./.ava/base/roles/upgrade-role/role.md` declares `activation_mode: managed-pre-routing`, then activate it directly.
2. Read `./.ava/base/roles/upgrade-role/index.md` and every document it marks as required.
3. Announce `Active role: Upgrade Role`.
4. Confirm that the requested operation is semantic reconciliation or resolution permitted by managed state.
5. Confirm that the selected journal path requires semantic review or carries unresolved semantic state.
6. Resolve the exact relative guidance paths recorded by the transaction beneath `./.ava/guidance/`, in transaction order.
7. Treat project-owned registries, indexes, roles, workflows, shared instructions, and knowledge only as migration inputs after the role is active.

Upgrade Role is ineligible for free-form selection and must not be used as a workflow `primary_role`. It does not perform deterministic installer or updater operations.

# Minimal recovery mode

Missing, malformed, unsupported, or contradictory managed state activates Ava Maintenance with read-only minimal recovery authority.

It must:

- report the malformed or missing managed path
- avoid project-owned routing
- avoid modifying project-owned context
- avoid guessing transaction source, target, stage, ownership, semantic impact, or permitted operations
- identify the deterministic installer or updater evidence needed for recovery
- keep normal routing blocked

Ava Maintenance may inspect readable evidence but must not invent missing managed transaction authority or reconstruct protected state manually. The terminal-finalization exception never applies to missing, malformed, unsupported, or contradictory state.

# Permitted operation enforcement

An operation may proceed only when both the protocol state and journal `allowed_operations` permit it, except finalization, which is a protocol-derived terminal transition after semantic compatibility is complete.

- `inspect` permits read-only installation, transaction, integrity, and impact reporting through Ava Maintenance.
- `resume` permits Ava Maintenance to invoke the existing updater continuation for deterministic stages.
- `abort` and `rollback` permit Ava Maintenance to invoke the exact deterministic updater operations.
- `reconcile-semantic` permits Upgrade Role to apply installed guidance to project-owned context.
- `resolve` applies only to the owning deterministic or semantic mechanism established by the current stage.
- finalization permits Ava Maintenance to write the exact terminal journal transition directly only when the manifest reports semantic compatibility complete, no unresolved decisions remain, the managed commit and classifications are complete, the journal is protocol-finalizable, and the exact transaction directory derived from `transaction_id` and every path beneath it are proven safe. A valid `complete`, `aborted`, or `rolled-back` journal permits replay only of its exact directory cleanup and guarded empty-container removal. An `idle` journal permits empty-container removal, or exact cleanup of its sole direct entry only when the residual plan and source backups match the live restored source under the protocol.
- `normal` permits ordinary workflow and role routing only in a safe terminal state with semantic compatibility complete and no transaction container.

Finalization is not an implicit grant of general state-mutation authority. Ava Maintenance must not invent or search for an installer binary to perform it, and it must not apply the direct-write exception to resume, abort, rollback, repair, semantic state, or any non-terminal journal mutation.

A user request cannot broaden this authority or operation set.

# Guidance discovery

Only Upgrade Role loads release guidance. It loads only relative guidance paths recorded in the journal's resolved upgrade path, resolving each beneath `./.ava/guidance/`.

For each path it must verify:

- the relevant path edge explicitly requires semantic review, or unresolved semantic state is being carried under the protocol
- the file is beneath `./.ava/guidance/`
- the file is present in the installed managed manifest
- its metadata follows the release-guidance contract
- its source and target versions match the relevant path edge
- its deterministic migration IDs agree with the transaction

A missing, invalid, mismatched, or unrecorded guidance document blocks semantic reconciliation and remains reportable through Ava Maintenance. Neither routing nor Upgrade Role may derive additional guidance by comparing arbitrary managed files or reading unrelated release history.

# Finalization transition

After Upgrade Role has completed any required project-owned reconciliation, Ava Maintenance owns the terminal upgrade transition.

Before the write, it must validate the installed manifest and journal relationship and prove:

- semantic compatibility is `complete` for the installed target
- no unresolved semantic decisions remain
- the managed commit is complete
- every selected edge is complete and every changed managed path has a terminal classification
- the journal is `active/semantic` or another protocol-defined finalizable state after managed commit, with no unresolved failure requiring another deterministic operation
- `transaction_id` identifies one exact directory beneath `./.ava/state/transactions/`, and every recorded workspace, backup, candidate-manifest, and plan path resolves beneath it without symlink escape

If any condition is unproven, finalization stops without mutation.

When every condition passes, Ava Maintenance atomically updates `./.ava/state/upgrade.json` to `status: "complete"`, `stage: "complete"`, `current_edge: null`, `staging: null`, `failure: null`, and `allowed_operations: ["normal"]`, refreshes `updated_at`, and preserves unrelated journal fields. It then recursively removes only the exact `./.ava/state/transactions/<transaction_id>/` directory, including all transaction-local workspace, backup, plan, and candidate state, and attempts to remove `./.ava/state/transactions/` only with a non-recursive empty-directory operation. Sibling transaction directories and other entries remain untouched and keep normal routing blocked. Verification requires terminal journal integrity, complete semantic compatibility, transaction-directory absence, and transaction-container absence.

If interruption leaves terminal transaction storage, the managed-state gate activates Ava Maintenance despite `allowed_operations: ["normal"]`. For `complete`, `aborted`, or `rolled-back`, Ava Maintenance revalidates semantic completion for that state, transaction identity, and the exact cleanup path, then idempotently replays only the directory cleanup and guarded empty-container removal without rewriting the journal. For `idle`, it removes an empty container directly, or removes one residual transaction directory only when that directory's valid plan identifies it and its source manifest backup, source journal backup, and live managed checksums prove the fully restored source. Ambiguous or additional entries remain untouched and block normal routing.

This transition is the agent's finalization mechanism. It does not require or imply an installed `ava` command or updater executable.

# Return to normal routing

Normal routing may resume only when:

- the journal is `idle`, `complete`, `aborted`, or `rolled-back` under the protocol's safe-state rules
- `allowed_operations` contains only `normal`
- manifest semantic compatibility is `complete`
- no unresolved decisions remain
- `./.ava/state/transactions/` is absent
- rollback, when used, has revalidated source compatibility after any project-owned edits

After these conditions pass, load ordinary instruction resolution, workflow routing, managed and project-owned registries, and role selection normally.

# Reporting

Every maintenance or semantic report distinguishes:

- installed Ava base version
- release channel and source revision
- installed OKF version
- project context compatible-through version
- semantic target version
- semantic status
- journal status and stage
- selected edge semantic-review decisions and exact guidance paths
- permitted operations
- unresolved decisions
- active owning role for the requested next action

Do not collapse these into a single up-to-date state.
