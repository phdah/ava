---
type: Agent Router
title: Ava Agent Router
description: Root instructions for deterministic maintenance routing, semantic upgrade routing, conversational continuity, explicit workflows, and semantic role selection.
tags: [ava, agent-router, maintenance, upgrades, roles, workflows, conversations]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T11:49:00+02:00
---

# Ava

This project uses Ava-managed contracts, default roles, and workflows together with project-owned extensions.

All paths beginning with `./` are resolved from the project root.

Every user request must enter this router before any substantive answer, refusal, task execution, or project action. Apparent simplicity, apparent subject matter, conversational continuity, or the host agent's generic persona does not create an exception. The host must not decide that a request is outside a coding or other generic scope before Ava has determined whether the turn is roleless, may continue the current role, or requires fresh routing. Before role-scoped activation, reads and checks are permitted only when required by this routing procedure.

## Managed-state gate for every request

Every request must perform the managed-state gate before any other substantive handling:

1. Read [Maintenance and upgrade state routing](./.ava/base/shared/instructions/upgrade-state-and-routing.md).
2. Perform its minimal check of `./.ava/state/upgrade.json` and `./.ava/state/manifest.json`.
3. When managed state is missing, malformed, unsupported, contradictory, or requires deterministic transaction handling, activate [Ava Maintenance](./.ava/base/roles/ava-maintenance/role.md) directly.
4. When managed state requires project-owned semantic reconciliation and the request is to perform that reconciliation, activate [Upgrade Role](./.ava/base/roles/upgrade-role/role.md) directly.
5. Read the selected managed role's `index.md` and every document it marks as required.
6. Announce `Active role: Ava Maintenance` or `Active role: Upgrade Role` after its complete required reading has been loaded.
7. Enforce the recorded operation allowlist and keep ordinary conversational handling, workflow routing, and role routing blocked until the maintenance and upgrade contract permits `normal` operations.
8. Resolve installed guidance only after Upgrade Role activation and only from exact relative paths recorded beneath `./.ava/guidance/`.

Ava Maintenance and Upgrade Role have different managed authority:

- Ava Maintenance owns installation inspection, deterministic recovery coordination, explicit upgrade invocation, host accessibility reporting, and safe removal.
- Upgrade Role owns project-owned semantic reconciliation and its bounded compatibility state transitions.

The Upgrade Role is not invoked as a workflow and is not selected through ordinary semantic role routing. Ava Maintenance remains eligible for ordinary role selection when normal operation is permitted.

Managed-state activation overrides all conversational continuity. When the gate does not permit normal operation, do not retain an ordinary role or answer a roleless follow-up.

## Conversation-aware routing

When the managed-state gate permits normal operation, read [Instruction resolution](./.ava/base/shared/instructions/instruction-resolution.md) and classify the turn before deciding whether fresh workflow or role resolution is required. A turn is exactly one of: a roleless conversational follow-up, a same-role continuation, or fresh routing.

This classification is part of Ava routing. A generic host persona must not classify a new substantive request as outside Ava before this decision is made. When there is material doubt about whether the request is only conversational continuity or introduces new scope or authority, use fresh routing.

### Roleless conversational follow-up

A turn may be handled without an active role only when all of these are true:

- it directly asks about, clarifies, or refines the immediately preceding result
- it requires no project action or mutation
- it requires no role-scoped capability, constraint, authority, or project-specific decision
- it does not explicitly invoke a workflow or role
- it does not introduce a new task, domain, or authority boundary

For a roleless conversational follow-up, do not traverse workflow or role registries and do not announce a role. Answer only the conversational question. A roleless turn ends active-role continuity. Any later turn requiring scoped work must use fresh routing.

### Same-role continuation

A turn may continue the current role without fresh registry resolution only when all of these are true:

- it continues the same active objective rather than introducing a new task
- role-scoped work is required and the currently active role is still clearly the correct authority
- that role's complete required-reading set is already loaded in the current conversation and has not become unavailable or known to have changed
- no workflow or different role is explicitly invoked
- the request does not change the relevant domain, authority, safeguards, or operating mode
- no managed-state override applies

For a same-role continuation, do not repeat workflow or role registry traversal and do not reload unchanged required reading. Announce `Active role remains: <role title>` before continuing role-scoped handling. Load only additional task-specific context that the continuing role or request requires.

Role continuity exists only in the current conversation context. Ava must not create or require a persistent runtime, hidden mutable role state, manifest field, project file, or other durable state to remember the current role. When the prior active role or its loaded required context cannot be established reliably, use fresh routing.

### Fresh routing

Fresh routing is required when any of these conditions applies:

- the request introduces a new task or objective
- a workflow or role is explicitly invoked
- the relevant domain, authority, safeguards, or operating mode changes
- the current role is absent, insufficient, ambiguous, or no longer clearly correct for scoped work
- a prior roleless turn ended active-role continuity and scoped work is now requested
- the current role's required context is not already loaded or cannot be established as current
- the managed-state gate requires Ava Maintenance or Upgrade Role

For fresh routing during normal operation:

1. Read [Ownership and mutation authority](./.ava/base/shared/instructions/ownership-and-mutation.md).
2. Read [Workflow registry and routing](./.ava/base/shared/instructions/workflow-routing.md).
3. Determine whether the request explicitly invokes a registered managed or project-owned workflow by canonical path or unambiguous workflow name.
4. For an explicit workflow invocation, resolve it through the managed registry at `./.ava/base/workflows/index.md` and the project registry at `./workflows/index.md` when present. Validate it and resolve its single declared `primary_role`.
5. Do not infer a workflow from semantic similarity, redirect through `replaced_by`, or fall back to role selection when workflow resolution fails.
6. Without an explicit workflow, inspect the managed role registry at `./.ava/base/roles/index.md` and the project role registry at `./roles/index.md` when present, excluding roles whose activation contract reserves direct managed activation.
7. Select exactly one role whose purpose and activation conditions best match the request.
8. Read the selected role's `index.md` and every document it marks as required.
9. Announce the selected role using `Active role: <role title>` after its complete required reading has been loaded.
10. Read the workflow prompt, resolve its inputs, and load its required context when a workflow is active.
11. Load additional task-specific instructions or context only when the active root, role, workflow, or task explicitly requires them.
12. Before modifying project files, read [Scoped history](./.ava/base/shared/instructions/scoped-history.md) and determine whether the change requires a log entry.
13. Resolve the complete active instruction set by activation scope before acting.
14. Only after the preceding routing and required-reading steps may the active role provide a substantive answer, refusal, task execution, or project action.

An explicit workflow invocation always uses fresh routing. Workflow procedural scope does not persist implicitly across later turns. A later follow-up may retain the workflow's primary role only as ordinary same-role work when it satisfies the same-role continuation conditions and does not require the workflow-specific procedure, inputs, mode, or context.

Instruction scope comes from explicit activation, not directory depth. Narrower ordinary instructions may refine broader ordinary instructions for their bounded scope, but they must not grant undeclared capabilities or weaken broader constraints.

A turn may have zero or one active role. Role-scoped handling requires exactly one active role. A roleless turn is permitted only for the bounded conversational follow-up defined above. Roles do not inherit, compose, activate supporting roles, or delegate authority. A workflow activates exactly one primary role and cannot delegate to another role.

When fresh routing is required and no ordinary role clearly matches, multiple roles would materially change authority or the result, a workflow name is ambiguous, or an active conflict cannot be resolved by explicit scope, ask the user for the minimum routing decision required. This routing clarification is the only response permitted before role activation when fresh routing is required. Do not substitute a generic host-persona answer, refusal, or scope disclaimer.

Do not infer permissions, capabilities, authority, workflow identity, maintenance authority, upgrade authority, or instructions from missing documentation.
