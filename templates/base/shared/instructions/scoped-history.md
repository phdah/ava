---
type: Shared Instruction
title: Scoped History
description: Rules for creating and updating the nearest log.md without duplicating routine Git history.
tags: [ava, history, logs, changes, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T21:52:00Z
---

# Purpose

Use scoped `log.md` files to preserve meaningful conceptual or structural history that future agents and users may need to understand the current project.

Git remains the complete history of file edits. A scoped log records durable changes in meaning, authority, ownership, routing, or structure. It must not become a duplicate commit log.

# General rule

Create or update the nearest relevant `log.md` only when both conditions are true:

- the change is conceptually or structurally significant within that scope
- understanding the change later requires more than reading the current file contents or a routine Git diff

Do not create logs speculatively. When the first qualifying change occurs in a scope without a log, create it then.

# Selecting the owning scope

Choose the nearest directory whose `index.md` owns discovery of the changed concept or structure.

Use these scope rules:

- **Project scope:** Use the bundle-root `log.md` for public format changes, global instruction semantics, top-level structure, project-wide routing, compatibility boundaries, or changes spanning several top-level scopes.
- **Role scope:** Use the role's nearest `log.md` for changes to its purpose, activation, responsibilities, authority, capabilities, constraints, required reading, or routing boundary.
- **Workflow scope:** Use the nearest workflow-owning `log.md` for changes to a workflow's primary role, procedural meaning, required inputs, expected output, operating mode, or trigger semantics.
- **Knowledge scope:** Use the nearest knowledge-owning `log.md` for classification changes, scope ownership, canonical identity, structural reorganization, splits, merges, moves, deprecations, or replacements.

If a workflow or concept owns a dedicated directory, that directory is normally the nearest scope. Otherwise use the directory whose index directly lists the document.

# Changes that require scoped history

Create or update the nearest log for changes such as:

- introducing or changing a public format or instruction-resolution rule
- adding, removing, renaming, relocating, or repurposing stable project structure
- changing role authority, activation, routing, capabilities, or constraints
- changing a workflow's primary role or procedural contract
- changing the meaning or ownership of a project, role, workflow, or knowledge scope
- splitting, consolidating, moving, replacing, or deprecating canonical knowledge
- introducing a compatibility or migration requirement
- reversing or materially revising a previously recorded conceptual decision

# Changes represented only by Git history

Do not create or update a scoped log for:

- spelling, grammar, formatting, or style corrections
- wording changes that preserve meaning and authority
- metadata timestamp or generation updates
- index synchronization that only reflects an already logged change
- routine additions or corrections to knowledge that do not change identity, ownership, or classification
- implementation details, test updates, or refactoring that do not change the documented contract or structure
- ordinary file edits whose purpose is clear from the resulting document and Git diff

# Placement and duplication

Record a qualifying change once at the nearest owning scope.

Do not repeat the same entry in every ancestor log. Use an ancestor log only when the change itself affects that ancestor's contract or spans several child scopes.

When a local change also establishes a project-wide rule, record the project-wide consequence in the root log and avoid repeating implementation details from the local scope.

# Log maintenance

A scoped `log.md`:

- is a reserved document and does not require normal frontmatter
- should be linked from its owning `index.md` when it exists
- should use dated sections in reverse chronological order
- should use concise entries that name the change and explain its durable consequence or rationale
- may link to the affected role, workflow, instruction, or knowledge documents
- must not include exhaustive file lists, commit hashes, or routine implementation details

Consult the nearest relevant log when change history, rationale, compatibility, or recency matters to the current task.

# Completion checks

After a qualifying change:

- the entry exists at the nearest owning scope
- no unnecessary duplicate entry exists at an ancestor or sibling scope
- the owning index links the log when one was created
- routine edits remain represented only by Git history
- the entry describes the durable conceptual or structural consequence rather than the mechanics of the edit
