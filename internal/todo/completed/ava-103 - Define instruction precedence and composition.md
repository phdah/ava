---
id: ava-103
title: "Define instruction precedence and composition"
status: "Done"
labels: ["internal", "roadmap", "phase-01"]
ordinal: 103
---

## Description

Define deterministic instruction precedence and composition. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Define Instruction Precedence and Composition
description: Establish deterministic traversal, conflict, override, inheritance, delegation, and scoped history rules.
tags: [internal, roadmap, format, instructions]
status: complete
phase: 1
order: 3
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T21:52:00Z
---

# Define Instruction Precedence and Composition

## Approved decisions

- Instruction scope is established through explicit activation and references, not filesystem depth.
- The resolution chain is root router, applicable shared instructions, active role, active workflow, task-specific instructions and context, and the current user request.
- Narrower ordinary behavioural instructions may refine broader ordinary instructions only within their explicitly activated scope.
- The active role remains the semantic authority boundary for the task.
- Capabilities and constraints are cumulative. Narrower scopes may reduce authority but cannot grant missing capabilities or weaken broader constraints.
- Missing instructions never imply permission, capability, authority, or precedence.
- Ava initially supports exactly one active role. Roles do not inherit, compose, activate supporting roles, or delegate authority.
- A workflow activates exactly one primary role and cannot declare supporting or delegated roles.
- Role transitions replace the active role after the new role's complete required reading has been loaded and announced.
- Same-scope conflicts, authority conflicts, constraint conflicts, and materially ambiguous routing must be surfaced rather than silently resolved.
- Scoped logs record major conceptual or structural history at the nearest owning scope. Routine edits remain represented only by Git history.

## Authoritative contracts

- [Instruction resolution](/templates/base/shared/instructions/instruction-resolution.md) defines activation, scope, precedence, authority, role and workflow composition, conflict handling, and validation requirements.
- [Scoped history](/templates/base/shared/instructions/scoped-history.md) defines project, role, workflow, and knowledge log ownership and the boundary between scoped history and routine Git history.

## Applied integration

- updated the generated root router to load and apply the instruction-resolution contract
- required the router to consult the scoped-history contract before project mutation
- documented explicit activation scope and single-role composition in the repository README
- added both contracts to the initialized project structure and shared instruction index
- recorded invalid composition, unresolved routing, capability expansion, and constraint weakening as blocking validation findings
- recorded the public format decision in the repository log

## Validation boundary

This phase defines the invalid states and required findings. Executable validator implementation remains in the deterministic validation phase.

## Completion

- defined deterministic traversal and instruction resolution
- preserved the rule that missing instructions do not imply permission
- prohibited initial role inheritance, composition, supporting-role activation, and delegation
- defined workflow-to-role authority boundaries
- defined conflict and routing escalation
- defined scoped `log.md` creation and update rules across project, role, workflow, and knowledge scopes
- updated and indexed the generated router instructions
- documented future validation requirements for invalid composition and unresolved routing