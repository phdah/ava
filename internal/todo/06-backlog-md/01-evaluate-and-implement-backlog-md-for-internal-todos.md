---
type: Internal Development Task
title: Evaluate and Implement Backlog.md for Internal Todos
description: Evaluate Backlog.md's native Markdown model and implement it as Ava's selected internal task-board system.
tags: [internal, roadmap, planning, markdown, backlog-md]
status: pending
phase: 6
order: 1
generated:
  by: agent:openai-chatgpt
  at: 2026-08-05T20:50:10+02:00
---

# Evaluate and Implement Backlog.md for Internal Todos

## Purpose

Adopt Backlog.md as the selected local agile-board tool for Ava's internal todos while preserving Markdown files in Git as the authoritative planning state.

This is not an evaluation of alternative board products or a generic task-board compatibility exercise. The tool choice is Backlog.md. The evaluation concerns the exact native integration, migration, and operating model before implementation.

## Accepted boundaries

- Backlog.md is the selected board tool when this task is implemented.
- Ava's internal task files must use Backlog.md's native supported Markdown representation rather than a separate generic board schema.
- The Markdown files in the repository remain the source of truth and the changes produced by the board remain normal reviewable Git changes.
- No GitHub Pages site, hosted task service, or external database is required.
- Internal planning remains separate from files distributed to Ava projects.

## Scope

1. Confirm the supported Backlog.md version and its native directory layout, filenames, frontmatter, status model, ordering, dependencies, labels, and completed-task handling.
2. Compare that model with Ava's existing phase indexes, task frontmatter, dogfood findings, status rules, and progressive-discovery requirements.
3. Define the migration from the current internal todo hierarchy to Backlog.md's native model without losing roadmap meaning, durable completion evidence, or agent navigation.
4. Install and configure Backlog.md for the Ava repository's internal todos.
5. Migrate the internal todo hierarchy and status metadata to the selected representation.
6. Document how a maintainer starts and uses the local Backlog.md board and how resulting Markdown changes are reviewed and committed.
7. Add validation that keeps Backlog.md task state, Ava indexes, and roadmap state aligned.

## Constraints

- Do not replace Backlog.md with a custom or generic compatibility layer.
- Do not redesign release qualification or discard historical completed-task evidence merely to simplify the board.
- Preserve the distinction between umbrella tasks, executable tasks, and dogfood findings, representing them through Backlog.md where possible and documenting any necessary retained supporting indexes.
- Preserve deterministic links and progressive discovery for agents working directly with the repository files.
- Avoid duplicate status sources. Backlog.md state and Ava roadmap state must have one authoritative mapping.
- Do not introduce automatic commits, pushes, remote credentials, or background services as part of the integration.

## Completion criteria

- the supported Backlog.md version and native file-format assumptions are recorded
- Backlog.md can open Ava's internal todo board through its local web UI
- an existing Ava task can be displayed, edited, moved, reopened, and completed through Backlog.md without losing Ava metadata or prose
- the current internal todo hierarchy has been migrated without losing active ordering or durable completion evidence
- direct agent or human Markdown edits remain valid Backlog.md task changes
- task status, dependencies, indexes, and validation remain aligned after board-driven changes
- setup and operating instructions are documented
- no internal todo content is added to the distributed Ava base
