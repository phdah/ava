---
id: ava-602
title: "Evaluate and add a default Backlog.md project task role"
status: "In Progress"
dependencies: [ava-601]
labels: ["internal", "roadmap", "phase-06", "backlog-md", "roles"]
ordinal: 602
---

## Description

Evaluate and add a default project task-management capability built around Backlog.md, using the lessons from AVA-601. Decide whether that capability belongs in a distinct durable role or in an existing managed role/workflow, then implement the justified default shape in Ava's managed base and installation flow.

## Scope

- Compare the responsibility, routing, approval, and ownership boundaries of project task management with the existing role catalog.
- Decide explicitly whether a distinct first-class role is justified.
- If a distinct role is justified, add a complete maintained role definition, register it, and define composition boundaries with adjacent roles such as Software Engineer, Technical Writer, Project Manager, and other execution roles.
- If a distinct role is not justified, integrate the capability into the best existing managed home and document why a split was rejected.
- Scaffold `backlog.config.yml` and a minimal native task structure in a newly installed project rather than hiding project task state under `.ava/`.
- Keep Backlog state repository-native, project-owned, Git-reviewable, and usable through both direct Markdown editing and the Backlog CLI/browser.
- Avoid copying a frozen Backlog CLI manual into Ava; agents performing task management should load the currently available Backlog instructions instead.
- Reflect the scaffold in ownership and upgrade contracts so `.ava/*` remains tool-managed while the project backlog remains user-owned project content.
- Add validation/conformance coverage proving installation, Backlog CLI lifecycle operations after install, direct valid task edits, and compatibility with the existing release/test pipeline.
- Update setup/operator documentation so users and installed agents can discover and operate the local task board.
- If the behavior ships in the v1 managed base or a later compatible release, align release-guidance indexes without weakening unsupported upgrade boundaries.

## Completion criteria

- The role-vs-existing-role decision is documented with explicit routing and ownership rationale.
- The default project backlog scaffold and operating model are defined.
- New installs receive a usable native Backlog task board without manual schema reconstruction.
- The responsible role can read, create, update, and complete tasks within project-local authorization boundaries while deferring destructive cleanup to explicit user approval.
- Direct valid Markdown edits remain authoritative-compatible with Backlog.md.
- Backlog storage and ownership are explicit, project-owned, and upgrade-safe relative to `.ava/*`.
- Installation/conformance coverage exercises both the role instructions and a working Backlog CLI task lifecycle.
- User-facing setup/operator docs explain how to use the board locally.
- Existing roles compose with the task-management capability without overlapping execution ownership.
