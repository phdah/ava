---
type: Internal Development Task
title: Create the Change Reviewer Role
description: Define an independent semantic review role with read-only authority by default.
tags: [internal, roadmap, roles, review]
status: pending
phase: 2
order: 4
timestamp: 2026-07-25T00:00:00Z
---

# Create the Change Reviewer Role

## Why

Ava projects need an independent role that can evaluate changes without being the role that authored them. This provides a deliberate consistency and authority check before broad instruction changes are accepted.

## Intended responsibilities

- review proposed or completed changes to roles, shared instructions, policies, workflows, and knowledge
- detect contradictions between responsibilities, instructions, capabilities, and constraints
- identify accidental expansion of authority or destructive behavior
- check whether role and workflow routing remain clear and non-overlapping
- verify progressive disclosure and context boundaries
- report concrete findings and recommended corrections
- support workflows such as `review-change`, `review-role-change`, and `review-project-policy`

## Boundaries

- should be read-only by default
- must not automatically rewrite reviewed material unless the user explicitly requests remediation and its capabilities permit it
- must not act as a generic deterministic validator
- must not approve unresolved material policy or architectural decisions on the user's behalf
- must remain independent from the role that created the reviewed change where possible

## Independence options to define

- a fresh agent session
- isolated context containing only the change and applicable instructions
- a separate read-only review pass explicitly activated by workflow
- future multi-agent execution outside Ava's initial runtime scope

## Completion criteria

- create the complete role under `templates/base/roles/change-reviewer/`
- define default read-only authority and escalation paths
- define practical independence requirements
- add clear routing conditions for review requests
- distinguish semantic review from deterministic structural validation
