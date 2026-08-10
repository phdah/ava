---
type: Shared Instruction
title: Maintenance and Upgrade State Routing
description: Defines managed pre-routing to Ava Maintenance or Upgrade Role, operation enforcement, guidance discovery, finalization, and return to normal routing.
tags: [ava, maintenance, upgrades, routing, state, recovery]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T14:51:00+02:00
---

# Purpose

This instruction governs the state check that occurs before ordinary workflow or role routing in an installed Ava project.

Its purpose is to keep installation inspection and deterministic recovery reachable through Ava Maintenance, while reserving project-owned semantic reconciliation for Upgrade Role. Both must remain reachable when project-owned routing or context is missing, corrupt, or incompatible with the installed base.

All paths beginning with `./` are resolved from the project root.

# Managed inputs

Use only these managed inputs to decide the pre-routing mode:

- `./.ava/state/upgrade.json`
- `./.ava/state/manifest.json`
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
9. Enter normal routing only when the journal is in a protocol-defined safe terminal state and semantic compatibility is `complete`.

A journal state must never broaden its `allowed_operations` beyond the upgrade protocol.

# Ava Maintenance mode

In Ava Maintenance mode:

1. Activate `./.ava/base/roles/ava-maintenance/role.md` directly.
2. Read its `index.md` and every document it marks as required.
3. Announce `Active role: Ava Maintenance`.
4. Compare the requested deterministic operation with the journal state and `allowed_operations`.
5. Inspect only managed state, manifest-declared payloads, recorded transaction paths, and exact recorded host integration needed for the request.
6. Use existing installer or updater operations for upgrade, resume, abort, and rollback. For successful upgrade finalization only, use the protocol-defined direct terminal state transition after proving every finalization precondition.
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
- finalization permits Ava Maintenance to write the exact terminal journal transition directly only when the manifest reports semantic compatibility complete, no unresolved decisions remain, the managed commit and classifications are complete, the journal is protocol-finalizable, and any transaction workspace selected for cleanup is exact and safe.
- `normal` permits ordinary workflow and role routing only in a safe terminal state with semantic compatibility complete.

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
- any recorded transaction workspace resolves safely to the exact transaction owned by the journal

If any condition is unproven, finalization stops without mutation.

When every condition passes, Ava Maintenance atomically updates `./.ava/state/upgrade.json` to `status: "complete"`, `stage: "complete"`, `current_edge: null`, `staging: null`, `failure: null`, and `allowed_operations: ["normal"]`, refreshes `updated_at`, and preserves unrelated journal fields. It then removes only the exact recorded transaction workspace and verifies the terminal journal, complete semantic compatibility, and workspace absence.

This transition is the agent's finalization mechanism. It does not require or imply an installed `ava` command or updater executable.

# Return to normal routing

Normal routing may resume only when:

- the journal is `idle`, `complete`, `aborted`, or `rolled-back` under the protocol's safe-state rules
- `allowed_operations` contains only `normal`
- manifest semantic compatibility is `complete`
- no unresolved decisions remain
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
