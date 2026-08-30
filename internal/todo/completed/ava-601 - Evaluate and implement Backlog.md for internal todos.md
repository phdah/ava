---
id: ava-601
title: "Evaluate and implement Backlog.md for internal todos"
status: "Done"
labels: ["internal", "roadmap", "phase-06", "backlog-md"]
ordinal: 601
---

## Description

Adopt Backlog.md as Ava's selected local Markdown-native task manager for repository-internal work, with native task files as the sole planning source of truth.

## Migrated task record

Historical metadata: Internal Development Task, phase 6 order 1, originally pending, generated 2026-08-05.

### Purpose and accepted boundaries

The selected tool is Backlog.md, not a generic compatibility layer or an evaluation of alternatives. Repository Markdown remains authoritative and board changes remain normal reviewable Git changes. No GitHub Pages site, hosted task service, external database, remote credentials, automatic commit/push behavior, or background service is required. Internal planning remains separate from distributed Ava project content.

The original scope required confirming the supported Backlog.md version and native layout/filenames/frontmatter/statuses/order/dependencies/labels/completed handling; comparing that model with Ava's phases/findings/status/navigation; defining and implementing migration without losing roadmap meaning or durable evidence; documenting local board operation; and adding validation for Backlog state.

The original constraints required native Backlog representation, no release-qualification redesign, preservation of umbrella/executable/finding distinctions and historical evidence, deterministic agent discovery, a single authoritative status source, and no automatic Git/remote behavior.

### Implemented operating model

Ava pins Backlog.md `1.50.1` for maintained validation and examples. Root `backlog.config.yml` points `backlog_directory` at `internal/todo`, uses task prefix `ava`, statuses `To Do`, `In Progress`, `Parked`, and `Done`, and disables remote operations and automatic commits.

Native task filenames use the configured prefix, for example `ava-602 - Evaluate and add a default Backlog.md project task role.md`, with matching frontmatter IDs such as `id: ava-602`. Active and parked work lives under `internal/todo/tasks/`; completed historical work lives under `internal/todo/completed/`.

The previous phase hierarchy, separate dogfood finding directory, phase indexes, operator todo file, finding template, and `/internal/todo.md` are fully migrated into native task bodies and removed. Seventy-two retained tasks/findings now carry their specification, rationale, decisions, completion evidence, relevant phase-level context, and historical release/dogfood context directly in the native task ledger. The Backlog frontmatter at the top of each file is the only mutable lifecycle source; historical pre-Backlog metadata preserved inside task bodies is documentary evidence only.

The current active dependency chain is AVA-601 -> AVA-602 -> AVA-701. AVA-601 completes this repository-internal adoption. AVA-602 is the next project-level Backlog.md adoption evaluation/implementation. AVA-701 follows it. Release-progression tasks AVA-504, AVA-505, AVA-506, AVA-541, AVA-542, AVA-551, and post-v1 AVA-5625 remain `Parked` by explicit user decision.

### Agent operating contract

Backlog.md's pinned README recommends CLI-based AI integrations bootstrap by running `backlog instructions overview`, with detailed versioned workflow guidance for task creation, task execution, and task finalization. Ava Internal Maintainer now packages that bootstrap into its required operating instructions rather than copying a stale full upstream manual. The maintainer loads the current Backlog workflow guidance for roadmap work, then applies Ava's stricter repository authority, approval, parked-task, dependency, validation and Git boundaries.

Backlog CLI/Web operations and direct valid Markdown edits operate on the same task files. Maintainers prefer the Backlog command surface for lifecycle/field changes where practical and validate direct edits before completion. `backlog board` and `backlog browser` expose the local task board; the browser remains loopback-only. Backlog itself does not commit or push Ava changes.

### Validation

`internal/todo/validate.py` validates the Backlog configuration, exact migrated task inventory, `ava-` filename/ID correspondence, allowed status/location rules, dependencies and cycles, current queue, explicitly parked release tasks, absence of legacy todo directories/files, and absence of transitional retained-spec wrappers.

The Python CI workflow validates the repository-native task ledger, requires Backlog's JSON view to discover the expected tasks rather than merely exit successfully, exercises a native lifecycle edit and restoration without losing migrated prose, and smoke-tests the local browser before running the existing release suite.

### Completion criteria

- supported version and native file assumptions are recorded
- Backlog can open Ava's internal board locally
- native tasks can be viewed and lifecycle-edited through Backlog without losing metadata/prose
- the complete internal hierarchy is migrated with ordering and durable completion evidence preserved
- direct valid Markdown remains supported
- statuses, dependencies and validation stay aligned after Backlog-driven changes
- setup and agent operating instructions are documented
- no internal todo content enters the distributed Ava base

## Migrated Phase 6 roadmap context

Phase 6 adopts Backlog.md first for Ava's internal roadmap and then for project-owned task management. The tool choice is fixed: native Markdown remains reviewable Git content and no hosted service/database is required.

The ordering is deliberate: prove the native model internally in AVA-601, then implement default installed-project support through AVA-602, deciding whether that capability belongs to a distinct role or the correct existing role/workflow. After AVA-602, continue with AVA-701 durable interaction evidence before reassessing release progression.