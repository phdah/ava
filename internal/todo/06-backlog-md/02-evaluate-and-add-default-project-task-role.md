---
type: Internal Development Task
title: Evaluate and Add a Default Backlog.md Project Task Role
description: Evaluate the correct role ownership and add managed base support for project-owned tasks using Backlog.md's native Markdown format.
tags: [internal, roadmap, roles, planning, markdown, backlog-md]
status: pending
phase: 6
order: 2
depends_on: 01-evaluate-and-implement-backlog-md-for-internal-todos
generated:
  by: agent:openai-chatgpt
  at: 2026-08-05T20:50:10+02:00
---

# Evaluate and Add a Default Backlog.md Project Task Role

## Purpose

Make Backlog.md task management available as a default capability in projects installed from Ava's managed base.

The project task format must be Backlog.md's native Markdown model. Backlog.md is the selected human board UI, while the active Ava role maintains the same files directly through the host agent's filesystem tools.

## Dependency

Complete [Evaluate and Implement Backlog.md for Internal Todos](01-evaluate-and-implement-backlog-md-for-internal-todos.md) first. The distributed project capability must build on the proven Backlog.md schema and operating model used internally.

## Evaluation scope

1. Decide whether Backlog.md task maintenance requires a distinct durable role or should be owned by an existing managed role with a bounded workflow.
2. Define routing conditions that distinguish task planning and board maintenance from implementation, project-context maintenance, and generic documentation work.
3. Define the project-owned Backlog.md task root, native schema, indexes, lifecycle states, dependencies, labels, priorities, and completed-task handling.
4. Define authority for creating, reprioritizing, splitting, completing, reopening, archiving, and deleting tasks.
5. Define when user approval is required, especially for reprioritization, scope changes, destructive operations, and architectural decisions.
6. Evaluate whether the capability belongs in the v1 managed base or a later compatible release.

## Implementation scope

When the evaluation supports a distinct default role:

- add the role under `templates/base/roles/`
- provide deterministic required reading, capabilities, constraints, and operating instructions
- register it with non-overlapping routing conditions
- add the shared Backlog.md task-format contract required by installed projects
- add create-if-absent project-owned scaffolding or setup guidance where appropriate
- add fixtures and validation for both Backlog.md UI changes and direct role-driven Markdown changes
- update affected role, template, distribution, and release-guidance indexes

When an existing role or workflow is the correct owner, record the rationale and implement the same default Backlog.md capability there rather than adding a redundant role.

## Constraints

- Project task files must remain project-owned content.
- The managed role and shared contracts may define the Backlog.md format but must not own or silently overwrite project tasks.
- Do not substitute a generic task-board format or alternative board tool for Backlog.md.
- The role must edit Backlog.md's native files directly rather than requiring browser automation.
- Do not require GitHub Pages, remote write APIs, automatic Git operations, or embedded credentials.
- Do not introduce ambiguous routing with Software Engineer, Technical Writer, Project Manager, or other maintained roles.

## Completion criteria

- the role-versus-existing-role decision and rationale are recorded
- the project task location, ownership, Backlog.md schema, lifecycle, and authority model are explicit
- routing conditions are deterministic and covered by validation
- an installed project can initialize and use a Backlog.md board for project-owned tasks
- the active Ava role can create and maintain the same Backlog.md task files directly
- moving or editing cards through Backlog.md preserves all Ava-required task semantics
- affected indexes, fixtures, contracts, scaffolding, and upgrade guidance are aligned
