---
type: Distribution Contract
title: Ava Project Task Board
description: Defines the default project-owned Backlog.md board, task-management role boundary, installation scaffold, and upgrade behavior.
tags: [ava, distribution, backlog, tasks, roles, ownership, upgrades]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-30T18:42:00+02:00
---

# Ava Project Task Board

Ava installs a local, repository-native project task board based on Backlog.md. The board is project content, not Ava runtime state.

# Role decision

Project task maintenance is a distinct durable responsibility and therefore belongs to the managed **Project Task Manager** role.

The split is justified because task lifecycle work owns a cross-cutting record of work: decomposition, priorities, dependencies, acceptance criteria, progress, completion, reopening, and history. Those responsibilities apply across implementation domains but do not grant authority to perform the work represented by a task.

Execution roles such as software engineering, technical writing, project management, or project-specific domain roles retain ownership of their deliverables and decisions. Project Steward retains project-wide trusted guidance and workflow ownership. Role Manager retains role lifecycle ownership. Ava Maintenance retains installed Ava lifecycle ownership.

# Installed scaffold

Fresh installation may create the following project-owned files when absent:

```text
./backlog.config.yml
./backlog/tasks/.gitkeep
./backlog/completed/.gitkeep
```

The default configuration uses `./backlog/`, `TASK-*` IDs, `To Do`, `In Progress`, and `Done` states, local-only browser defaults, no Backlog remote operations, and no automatic Git commits.

`project_name` is intentionally generic in the create-if-absent scaffold and may be renamed by the project owner. The entire configuration is project-owned and may be changed after installation.

# Operating model

Backlog.md is an interface over native repository files. It is not required as a persistent service.

When the CLI is available, task-management agents begin by loading its current workflow instructions:

```sh
backlog instructions overview
```

They should use the detailed workflow guidance and command help provided by the installed/current Backlog.md version rather than an Ava-maintained copy of the upstream CLI manual.

Humans may use the same state through `backlog task`, `backlog board`, or the local `backlog browser`. Direct valid Markdown edits are also authoritative project edits. The Project Task Manager preserves native Backlog.md structure and validates direct edits with the CLI when available.

# Ownership

`./backlog.config.yml` and everything under the configured project backlog directory are project-owned unless the project explicitly establishes a different project-local convention.

They are not listed in `/.ava/state/manifest.json`, do not receive Ava managed-file checksums, and must never be moved under `./.ava/` merely to make them discoverable to agents.

Ava-managed role instructions may define how task management is performed, but managed instructions do not own the task records themselves.

# Installation and upgrades

Release assembly marks the default backlog scaffold as `project-owned` with `create-if-absent` operations.

On fresh installation or explicit adoption, an absent scaffold file may be created. Existing project files are preserved byte-for-byte.

Deterministic upgrades never create, replace, delete, move, or merge project-owned task-board content. When a later Ava release introduces or changes a recommended project-owned task scaffold, upgrade guidance may describe that recommendation, but project-owned changes occur only through explicit semantic migration or normal project task management.

This preserves the core upgrade boundary: `./.ava/` is managed by Ava release tooling; the project backlog is maintained by the project and its authorized task-management role.

# Approval boundary

The Project Task Manager may perform routine task lifecycle operations that directly follow the user's request or an approved plan. Explicit user approval is required for destructive cleanup or deletion, materially ambiguous reprioritization, scope changes that alter the requested outcome, and new architectural/product/security decisions that are not already authorized.
