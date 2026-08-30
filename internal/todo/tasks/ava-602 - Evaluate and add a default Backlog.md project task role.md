---
id: ava-602
title: "Evaluate and add a default Backlog.md project task role"
status: "In Progress"
labels: ["internal", "roadmap", "phase-06", "roles", "planning", "backlog-md"]
ordinal: 602
dependencies: ["ava-601"]
---

## Description

Make Backlog.md task management available as a default capability in projects installed from Ava's managed base, using the native Backlog.md Markdown model proven by AVA-601.

## Evaluation scope

1. Decide whether project task maintenance requires a distinct durable role or belongs to an existing managed role with a bounded workflow.
2. Define routing conditions that distinguish task planning/board maintenance from implementation, project-context maintenance, and generic documentation work.
3. Define the project-owned Backlog.md task root, native task model, lifecycle states, dependencies, labels, priorities, and completed-task handling.
4. Define authority for creating, reprioritizing, splitting, completing, reopening, archiving, and deleting tasks.
5. Define when user approval is required, especially for reprioritization, scope changes, destructive operations, and architectural decisions.
6. Decide whether the capability belongs in the v1 managed base or a later compatible release.

## Implementation scope

If a distinct default role is justified:

- add it under `templates/base/roles/`
- provide deterministic required reading, capabilities, constraints, and operating instructions
- register non-overlapping routing conditions
- add the shared Backlog.md task-format contract needed by installed projects
- add create-if-absent project-owned scaffolding or setup guidance as appropriate
- add fixtures and validation for both Backlog.md UI changes and direct role-driven Markdown changes
- align affected role, template, distribution, and release-guidance indexes

If an existing role/workflow is the correct owner, record the rationale and implement the same default Backlog.md capability there instead of adding a redundant role.

## Constraints

- project task files remain project-owned content
- managed roles/contracts may define the format but must not own or silently overwrite project tasks
- use Backlog.md's native task representation rather than a generic compatibility schema
- roles edit native task files directly and do not require browser automation
- do not require GitHub Pages, remote write APIs, automatic Git operations, or embedded credentials
- avoid ambiguous routing with Software Engineer, Technical Writer, Project Manager, or other maintained roles

## Completion criteria

- the role-versus-existing-role decision and rationale are recorded
- task location, ownership, native Backlog.md lifecycle, and authority model are explicit
- routing conditions are deterministic and validated
- an installed project can initialize and use a Backlog.md board for project-owned tasks
- the active Ava role can create and maintain the same native task files directly
- board-driven edits preserve all Ava-required task semantics
- affected indexes, fixtures, contracts, scaffolding, and upgrade guidance are aligned

This is the next active Ava internal task after AVA-601.
