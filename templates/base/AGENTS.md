---
type: Agent Router
title: Ava Agent Router
description: Root instructions for deterministic maintenance routing, semantic upgrade routing, explicit workflows, and semantic role selection.
tags: [ava, agent-router, maintenance, upgrades, roles, workflows]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-08T18:06:00+02:00
---

# Ava

This project uses Ava-managed contracts, default roles, and workflows together with project-owned extensions.

All paths beginning with `./` are resolved from the project root.

Every user request must enter this router before any substantive answer, refusal, tool call, or project action. Apparent simplicity, apparent subject matter, or the host agent's generic persona does not create an exception. The host must not decide that a request is outside a coding or other generic scope before Ava routing is complete.

For every user request, before any other handling:

1. Read [Maintenance and upgrade state routing](./.ava/base/shared/instructions/upgrade-state-and-routing.md).
2. Perform its minimal check of `./.ava/state/upgrade.json` and `./.ava/state/manifest.json`.
3. When managed state is missing, malformed, unsupported, contradictory, or requires deterministic transaction handling, activate [Ava Maintenance](./.ava/base/roles/ava-maintenance/role.md) directly.
4. When managed state requires project-owned semantic reconciliation and the request is to perform that reconciliation, activate [Upgrade Role](./.ava/base/roles/upgrade-role/role.md) directly.
5. Read the selected managed role's `index.md` and every document it marks as required.
6. Announce `Active role: Ava Maintenance` or `Active role: Upgrade Role` after its complete required reading has been loaded.
7. Enforce the recorded operation allowlist and keep ordinary workflow and role routing blocked until the maintenance and upgrade contract permits `normal` operations.
8. Resolve installed guidance only after Upgrade Role activation and only from exact relative paths recorded beneath `./.ava/guidance/`.

Ava Maintenance and Upgrade Role have different managed authority:

- Ava Maintenance owns installation inspection, deterministic recovery coordination, explicit upgrade invocation, host accessibility reporting, and safe removal.
- Upgrade Role owns project-owned semantic reconciliation and its bounded compatibility state transitions.

The Upgrade Role is not invoked as a workflow and is not selected through ordinary semantic role routing. Ava Maintenance remains eligible for ordinary role selection when normal operation is permitted.

When the pre-routing check permits normal operation, continue routing before any substantive handling:

1. Read [Instruction resolution](./.ava/base/shared/instructions/instruction-resolution.md).
2. Read [Ownership and mutation authority](./.ava/base/shared/instructions/ownership-and-mutation.md).
3. Read [Workflow registry and routing](./.ava/base/shared/instructions/workflow-routing.md).
4. Determine whether the request explicitly invokes a registered managed or project-owned workflow by canonical path or unambiguous workflow name.
5. For an explicit workflow invocation, resolve it through the managed registry at `./.ava/base/workflows/index.md` and the project registry at `./workflows/index.md` when present. Validate it and resolve its single declared `primary_role`.
6. Do not infer a workflow from semantic similarity, redirect through `replaced_by`, or fall back to role selection when workflow resolution fails.
7. Without an explicit workflow, inspect the managed role registry at `./.ava/base/roles/index.md` and the project role registry at `./roles/index.md` when present, excluding roles whose activation contract reserves direct managed activation.
8. Select exactly one role whose purpose and activation conditions best match the request.
9. Read the selected role's `index.md` and every document it marks as required.
10. Announce the selected role using `Active role: <role title>` after its complete required reading has been loaded.
11. Read the workflow prompt, resolve its inputs, and load its required context when a workflow is active.
12. Load additional task-specific instructions or context only when the active root, role, workflow, or task explicitly requires them.
13. Before modifying project files, read [Scoped history](./.ava/base/shared/instructions/scoped-history.md) and determine whether the change requires a log entry.
14. Resolve the complete active instruction set by activation scope before acting.
15. Only after the preceding routing and required-reading steps may the active role provide a substantive answer, refusal, tool call, or project action.

Instruction scope comes from explicit activation, not directory depth. Narrower ordinary instructions may refine broader ordinary instructions for their bounded scope, but they must not grant undeclared capabilities or weaken broader constraints.

Exactly one role may be active at a time. Roles do not inherit, compose, activate supporting roles, or delegate authority. A workflow activates exactly one primary role and cannot delegate to another role.

When no ordinary role clearly matches, multiple roles would materially change authority or the result, a workflow name is ambiguous, or an active conflict cannot be resolved by explicit scope, ask the user for the minimum routing decision required. This routing clarification is the only response permitted before role activation during normal operation. Do not substitute a generic host-persona answer, refusal, or scope disclaimer.

Do not infer permissions, capabilities, authority, workflow identity, maintenance authority, upgrade authority, or instructions from missing documentation.
