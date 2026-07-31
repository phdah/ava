---
type: Shared Instruction
title: Upgrade State and Routing
description: Defines the managed pre-routing check, Upgrade Role activation, permitted operations, guidance discovery, and return to normal routing.
tags: [ava, upgrades, routing, state, recovery]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
---

# Purpose

This instruction governs the state check that occurs before ordinary workflow or role routing in an installed Ava project.

Its purpose is to keep upgrade inspection, semantic reconciliation, resume, abort, and rollback reachable even when project-owned routing or context is missing, corrupt, or incompatible with the installed base.

# Managed inputs

Use only these managed inputs to decide the routing mode:

- `/.ava/state/upgrade.json`
- `/.ava/state/manifest.json`
- `/.ava/base/roles/upgrade-role/index.md`
- the exact relative guidance paths recorded in the upgrade transaction, resolved beneath `/.ava/guidance/`

Do not read `/roles/index.md`, `/workflows/index.md`, or other project-owned routing files before upgrade-mode activation is resolved.

# Minimal pre-routing check

Before ordinary instruction resolution:

1. Confirm that `upgrade.json` is parseable and has a supported `upgrade_schema`.
2. Confirm that `manifest.json` exposes a supported manifest envelope and semantic-compatibility object.
3. Enter upgrade mode when either condition is true:
   - journal `status` is `active` or `blocked`
   - `semantic_compatibility.status` is not `complete`
4. Enter minimal recovery mode when either managed state file is missing, malformed, unsupported, or internally contradictory.
5. Enter normal routing only when the journal is in a protocol-defined safe terminal state and semantic compatibility is `complete`.

A journal state must never broaden its `allowed_operations` beyond the upgrade protocol.

# Upgrade mode

In upgrade mode:

1. Confirm that `/.ava/base/roles/upgrade-role/role.md` declares `activation_mode: managed-pre-routing`, then activate it directly.
2. Read `/.ava/base/roles/upgrade-role/index.md` and every document it marks as required.
3. Announce `Active role: Upgrade Role`.
4. Compare the requested operation with `allowed_operations`.
5. Resolve the exact relative guidance paths recorded by the transaction beneath `/.ava/guidance/`, in transaction order.
6. Treat project-owned registries, indexes, roles, workflows, shared instructions, and knowledge only as migration inputs after the role is active.

A role declaring `activation_mode: managed-pre-routing` is ineligible for free-form selection and must not be used as a workflow `primary_role`. Do not resolve a workflow, perform free-form role selection, or use ownership precedence to select another role while upgrade mode remains active.

# Minimal recovery mode

Minimal recovery mode permits only inspection and the recovery actions that can be proven safe from the readable managed state.

It must:

- report the malformed or missing managed path
- avoid project-owned routing
- avoid modifying project-owned context
- avoid guessing transaction source, target, stage, or permitted operations
- direct deterministic state repair to the installer or updater
- keep normal routing blocked

The Upgrade Role may inspect readable evidence but must not invent missing managed transaction authority.

# Permitted operation enforcement

An operation may proceed only when both the protocol state and journal `allowed_operations` permit it.

- `inspect` permits read-only state and impact reporting.
- `resolve` permits capturing an explicit decision or resolving a recorded blocking condition.
- `resume` permits continuing the current deterministic or semantic stage through its owning authority.
- `abort` and `rollback` remain deterministic updater operations except for project-context reconciliation required to make rollback safe.
- `reconcile-semantic` permits the Upgrade Role to apply installed guidance to project-owned context.
- `normal` permits ordinary workflow and role routing only in a safe terminal state with semantic compatibility complete.

A user request cannot broaden this allowlist.

# Guidance discovery

The Upgrade Role loads only relative guidance paths recorded in the journal's resolved upgrade path, resolving each beneath `/.ava/guidance/`.

For each path it must verify:

- the file is beneath `/.ava/guidance/`
- the file is present in the installed managed manifest
- its metadata follows the release-guidance contract
- its source and target versions match the relevant path edge
- its deterministic migration IDs agree with the transaction

A missing, invalid, or mismatched guidance document blocks semantic reconciliation.

# Return to normal routing

Normal routing may resume only when:

- the journal is `complete`, `aborted`, or `rolled-back` under the protocol's terminal-state rules
- `allowed_operations` contains only `normal`
- manifest semantic compatibility is `complete`
- no unresolved decisions remain
- rollback, when used, has revalidated source compatibility after any project-owned edits

After these conditions pass, load ordinary instruction resolution, workflow routing, managed and project-owned registries, and role selection normally.

# Reporting

Every upgrade-mode report distinguishes:

- installed Ava base version
- project context compatible-through version
- semantic target version
- semantic status
- journal status and stage
- permitted operations
- unresolved decisions

Do not collapse these into a single up-to-date state.
