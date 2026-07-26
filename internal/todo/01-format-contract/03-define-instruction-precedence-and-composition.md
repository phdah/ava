---
type: Internal Development Task
title: Define Instruction Precedence and Composition
description: Establish deterministic traversal, conflict, override, inheritance, delegation, and scoped history rules.
tags: [internal, roadmap, format, instructions]
status: pending
phase: 1
order: 3
timestamp: 2026-07-25T00:00:00Z
---

# Define Instruction Precedence and Composition

## Decide

- precedence between root, shared, role, workflow, and task-specific instructions
- whether roles can inherit from or compose other roles
- whether workflows may delegate to supporting roles
- how conflicts are surfaced
- whether narrower instructions may override broader constraints
- which conceptual or structural changes require creating or updating the nearest scoped `log.md`
- which routine edits must remain represented only by Git history

## Completion criteria

- define deterministic traversal rules
- preserve the rule that missing instructions do not imply permission
- define scoped `log.md` creation and update rules across project, role, workflow, and knowledge scopes
- add validation for invalid composition or unresolved routing
- update generated router instructions