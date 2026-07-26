---
type: Agent Router
title: Ava Agent Router
description: Root instructions for selecting and loading the Ava role that best matches a user request.
tags: [ava, agent-router, roles]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T21:52:00Z
---

# Ava

This project uses Ava roles to provide task-specific instructions to agents.

Ava uses an OKF-inspired hierarchy: `index.md` files describe each directory and link to relevant documents; role files separate purpose, instructions, capabilities, constraints, and optional context; `log.md` files record major scoped changes. Follow links progressively instead of scanning the whole project.

Before acting on a user request:

1. Read [Instruction resolution](shared/instructions/instruction-resolution.md).
2. Determine whether the request invokes a registered workflow or is a free-form request.
3. For a workflow, resolve its single declared `primary_role`.
4. Otherwise, read [`roles/index.md`](roles/index.md) and select the role whose purpose and activation conditions best match the request.
5. Read the selected role's `index.md` and every document it marks as required.
6. Announce the selected role using `Active role: <role title>` after its complete required reading has been loaded and before acting under it.
7. Read the workflow prompt and workflow-specific context when a workflow is active.
8. Load additional task-specific instructions or context only when the active root, role, workflow, or task explicitly requires them.
9. Before modifying project files, read [Scoped history](shared/instructions/scoped-history.md) and determine whether the change requires a log entry.
10. Resolve the complete active instruction set by activation scope before acting.

Instruction scope comes from explicit activation, not directory depth. Narrower ordinary instructions may refine broader ordinary instructions for their bounded scope, but they must not grant undeclared capabilities or weaken broader constraints.

Exactly one role may be active at a time. Roles do not inherit, compose, activate supporting roles, or delegate authority. A workflow activates exactly one primary role and cannot delegate to another role.

Select roles automatically. Ask the user when no role clearly matches, when multiple roles would materially change authority or the result, or when an active conflict cannot be resolved by explicit scope.

When an explicitly invoked workflow or a new request changes the active role, complete the new role's required reading and announce it before acting under its instructions.

Do not infer permissions, capabilities, authority, or instructions from missing documentation.
