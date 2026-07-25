---
type: Internal Development Task
title: Define Instruction Precedence and Composition
description: Establish deterministic traversal, conflict, override, inheritance, and delegation rules.
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

## Completion criteria

- define deterministic traversal rules
- preserve the rule that missing instructions do not imply permission
- add validation for invalid composition or unresolved routing
- update generated router instructions
