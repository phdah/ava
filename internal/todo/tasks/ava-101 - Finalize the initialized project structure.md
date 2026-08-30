---
id: ava-101
title: "Finalize the initialized project structure"
status: "Done"
labels: ["internal", "roadmap", "phase-01"]
ordinal: 101
---

## Description

Finalize the stable initialized project structure. This native Backlog.md task contains the complete pre-Backlog task record and the phase-level roadmap context that previously lived in separate files.

## Migrated task record

---
type: Internal Development Task
title: Finalize the Initialized Project Structure
description: Decide and document the stable and extensible structure created by ava init.
tags: [internal, roadmap, format, structure]
status: complete
phase: 1
order: 1
timestamp: 2026-07-26T00:00:00Z
---

# Finalize the Initialized Project Structure

## Decided structure

`ava init` creates the minimal project tree documented in the repository README and represented exactly by `templates/base/`.

The stable top-level project locations are:

- `AGENTS.md` as the agent entry point and role router
- `index.md` as the root project index
- `inbox/` for untrusted or unclassified source material
- `knowledge/` for trusted, durable project knowledge
- `roles/` for role definitions and the role registry
- `workflows/` for workflow definitions and the workflow registry
- `shared/` for project-wide instructions and context

These locations are intentionally broad. Knowledge grows beneath `knowledge/`, roles beneath `roles/`, and workflows beneath `workflows/`. Ava does not pre-create speculative taxonomies or other empty structures.

## Approved structure rules

- `knowledge/` initially contains only its required `index.md`; no scope, domain, collection, or concept subdirectories are pre-created.
- durable growth and classification rules live in `shared/instructions/knowledge-organization.md`.
- future knowledge structure grows as a decision tree from real information.
- every created knowledge directory contains an `index.md` that acts as a local classification and navigation node.
- canonical concept documents have one primary location and use links for secondary relationships.
- scoped `log.md` files are created only when meaningful conceptual or structural history needs to be preserved.
- the Inbox Ingester and Project Steward require the knowledge organization instruction before acting.
- every future role permitted to mutate `knowledge/` must list the knowledge organization instruction in its required-reading manifest.
- every `index.md` enumerates and explains only direct child files and directories; each child directory owns discovery of its own descendants.
- ancestor indexes must not duplicate descendant navigation entries. Cross-scope relationships use contextual Markdown links instead.
- repository source templates remain under `templates/base/` and are not copied into initialized projects as a `templates/` directory.

## Validation boundary

A structurally valid initialized project must contain every path and reserved file created by `ava init`. Missing mandatory paths are validation errors. Additional user-defined content beneath the stable project locations is allowed unless a narrower format rule prohibits it.

Detailed validation implementation belongs to the deterministic validation phase.

## Migration boundary

Migration support is required when a future Ava version removes, renames, relocates, or repurposes a stable path or reserved file created by `ava init`.

Adding optional files, directories, roles, workflows, knowledge structures, or other user-extensible content does not by itself require migration support.

## Completion

- documented the stable and user-extensible portions of the tree
- updated the README project tree
- aligned `templates/base/` with the documented structure
- defined validation expectations for mandatory paths
- defined which future structural changes require migration support

## Migrated phase roadmap context

# Phase 01: Format Contract and Base Structure

Finalize the stable format boundaries before implementation establishes public behavior.

## Tasks

1. [x] Finalize the initialized project structure
2. [x] Finalize metadata and document-type rules
3. [x] Define instruction precedence and composition
4. [x] Define document update metadata

Phase 01 is complete. The format now distinguishes creation provenance from latest meaningful-update provenance, preserves reserved-document behavior, and freezes validation examples for the first alpha.

The next phase was Core roles for initialized projects.