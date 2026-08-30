---
id: ava-602
title: "Evaluate and add a default Backlog.md project task role"
status: "Done"
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Evaluate whether task lifecycle ownership is durable enough to justify a first-class role and define non-overlapping routing with execution and project-maintenance roles.
2. Add the selected role and a shared native Backlog.md task-board contract to the managed base.
3. Add project-owned create-if-absent Backlog.md scaffolding for fresh installations and preserve the `.ava/` ownership boundary.
4. Align installer validation, distribution contracts, routing indexes, and operator guidance.
5. Validate repository parsing, Backlog.md lifecycle behavior, browser operation, clean-project installation, direct native Markdown compatibility, and the existing release qualification suite.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
A distinct Project Task Manager role was selected because task records, prioritization, dependencies, and lifecycle state are durable cross-cutting responsibilities, while implementation and domain decisions remain with the roles that own those deliverables.

Backlog.md's current CLI workflow remains the preferred mutation surface. Direct native Markdown editing is retained as a compatibility/fallback path and must preserve native fields and validate with Backlog.md when available.

Published alpha.15 release guidance was intentionally left unchanged because it is immutable release evidence and this PR does not create a new release edge. Upgrade behavior for the project-owned task scaffold is defined in the distribution contract: deterministic upgrades preserve project-owned state, while future release authoring can add semantic guidance only if the next release edge actually requires project-owned reconciliation.

Validation passed on PR #115: internal Backlog validation, native Backlog parsing and lifecycle checks, local browser smoke test, clean-project install with task lifecycle and direct-edit compatibility, and the full release qualification suite.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented a first-class Project Task Manager in Ava's managed base and a project-owned Backlog.md task board for fresh installs. Added deterministic routing and authority boundaries, a shared native task-board contract, create-if-absent `backlog.config.yml` and `backlog/` scaffolding, installer ownership support, distribution and upgrade guidance, and end-to-end validation.

Execution ownership remains with the relevant domain role. Project Task Manager owns only task records and cross-task lifecycle. The implementation was verified by all PR checks, including a clean installation, Backlog.md lifecycle operations, compatible direct Markdown edits, browser parsing, and the full release qualification suite.
<!-- SECTION:FINAL_SUMMARY:END -->
