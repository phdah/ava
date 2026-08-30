---
type: Shared Instruction
title: Project Task Board
description: Defines the project-owned Backlog.md task model, storage boundary, direct-edit compatibility, and lifecycle safeguards.
tags: [ava, instructions, backlog, tasks, ownership]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-30T18:42:00+02:00
---

# Purpose

This instruction defines the task-board contract used by roles that read or maintain project tasks.

Backlog.md is the default interface and native Markdown format for project task state. Ava does not introduce a parallel task schema or a managed task database.

# Project-owned storage

When `./backlog.config.yml` exists, read its `backlog_directory` setting and treat that configured directory as the project task root. The default Ava scaffold uses:

```text
./backlog.config.yml
./backlog/tasks/
./backlog/completed/
```

The configuration and task tree are project-owned content. They must not be added to the Ava managed-file manifest or moved below `./.ava/`.

Existing task-board files always win over create-if-absent installation scaffolds. Deterministic upgrades do not rewrite project task state.

# Native task model

Use Backlog.md's native task representation. Preserve native frontmatter and sections that are outside the active change, including task identity, status, dependencies, labels, priority, assignee, acceptance criteria, implementation plan, notes, and final summary when present.

Task identity and relationships are explicit data. Do not infer dependencies or ordering from filenames alone, and do not renumber an existing task merely to change its priority.

Direct valid Markdown edits are authoritative project changes. They must remain readable by a compatible Backlog.md CLI and browser. Do not translate tasks into an Ava-specific compatibility format.

# Current CLI instructions

Before performing Backlog.md lifecycle operations, load the instructions supplied by the currently available Backlog CLI:

```sh
backlog instructions overview
```

Load the detailed task-creation, task-execution, or task-finalization instruction identified by the overview when relevant. Before using an unfamiliar command, inspect `backlog <command> --help`.

Ava intentionally does not embed a frozen copy of the Backlog.md CLI manual. If the CLI is unavailable, use the native Markdown contract and the active role's direct-edit safeguards instead.

# Lifecycle semantics

Task state tracks the work record; it does not grant authority to perform the work described by the task.

A task may be completed only when its requested outcome and applicable completion conditions are satisfied. Reopening preserves task identity and relevant history. Splitting a task must preserve the intended outcome and make new dependency relationships explicit.

Deletion, purging history, destructive archival, materially ambiguous reprioritization, material scope changes, and new architectural, security, product, or compatibility decisions require the approval defined by the active role and project instructions.

# Validation

After task-board mutation, when a compatible Backlog.md CLI is available:

- run a non-destructive read or list operation to confirm parsing
- verify changed task identity and intended status
- verify changed dependencies or relationships when applicable
- preserve unrelated native fields and sections

A CLI validation failure is evidence that the native task edit is incomplete or incompatible and must not be hidden by creating a second representation.
