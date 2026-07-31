---
type: Agent Router
title: Ava Agent Router
description: Root instructions for resolving explicit workflows or selecting the Ava role that best matches a free-form request.
tags: [ava, agent-router, roles, workflows]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T10:32:00Z
---

# Ava

This project uses Ava roles to provide task-specific instructions to agents and workflows to activate one role for a predefined procedure.

Ava uses an OKF-inspired hierarchy: `index.md` files describe each directory and link to relevant documents; role files separate purpose, instructions, capabilities, constraints, and optional context; workflow files define bounded procedures; `log.md` files record major scoped changes. Follow links progressively instead of scanning the whole project.

Before acting on a user request:

1. Read [Instruction resolution](shared/instructions/instruction-resolution.md).
2. Read [Ownership and mutation authority](shared/instructions/ownership-and-mutation.md).
3. Read [Workflow registry and routing](shared/instructions/workflow-routing.md).
4. Determine whether the request explicitly invokes a registered workflow by canonical path or unambiguous workflow name.
5. For an explicit workflow invocation, resolve it through [`workflows/index.md`](workflows/index.md), validate it, and resolve its single declared `primary_role`. Do not infer a workflow from semantic similarity, redirect through `replaced_by`, or fall back to role selection when workflow resolution fails.
6. Otherwise, read [`roles/index.md`](roles/index.md) and select the role whose purpose and activation conditions best match the free-form request.
7. Read the selected role's `index.md` and every document it marks as required.
8. Announce the selected role using `Active role: <role title>` after its complete required reading has been loaded and before acting under it.
9. Read the workflow prompt, resolve its inputs, and load its required context when a workflow is active.
10. Load additional task-specific instructions or context only when the active root, role, workflow, or task explicitly requires them.
11. Before modifying project files, read [Scoped history](shared/instructions/scoped-history.md) and determine whether the change requires a log entry.
12. Resolve the complete active instruction set by activation scope before acting.

Instruction scope comes from explicit activation, not directory depth. Narrower ordinary instructions may refine broader ordinary instructions for their bounded scope, but they must not grant undeclared capabilities or weaken broader constraints.

Exactly one role may be active at a time. Roles do not inherit, compose, activate supporting roles, or delegate authority. A workflow activates exactly one primary role and cannot delegate to another role.

An explicitly invoked workflow takes precedence over free-form role selection. Without an explicit workflow invocation, select roles automatically and do not guess a workflow.

Ask the user when no role clearly matches, when multiple roles would materially change authority or the result, when a workflow name is ambiguous, or when an active conflict cannot be resolved by explicit scope.

When an explicitly invoked workflow or a new request changes the active role, complete the new role's required reading and announce it before acting under its instructions.

Do not infer permissions, capabilities, authority, workflow identity, or instructions from missing documentation.
