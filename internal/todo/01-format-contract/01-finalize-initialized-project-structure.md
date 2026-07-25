---
type: Internal Development Task
title: Finalize the Initialized Project Structure
description: Decide and document the stable and extensible structure created by ava init.
tags: [internal, roadmap, format, structure]
status: in-progress
phase: 1
order: 1
timestamp: 2026-07-25T00:00:00Z
---

# Finalize the Initialized Project Structure

## Decide

- exact directories and reserved files created by `ava init`
- required root files and registries
- role directory requirements
- workflow directory and registry requirements
- shared instruction and context locations
- inbox convention
- index and log placement
- whether templates are part of generated projects or only repository sources

## Approved knowledge structure

- `ava init` creates a top-level `knowledge/` directory.
- `knowledge/` initially contains only its required `index.md`; no scope, domain, collection, or concept subdirectories are pre-created.
- durable growth and classification rules live in `shared/instructions/knowledge-organization.md`.
- future knowledge structure grows as a decision tree from real information.
- every created knowledge directory contains an `index.md` that acts as a local classification and navigation node.
- canonical concept documents have one primary location and use links for secondary relationships.
- scoped `log.md` files are created only when meaningful conceptual or structural history needs to be preserved.

## Completion criteria

- document the stable and user-extensible portions of the tree
- update the README example tree
- update `templates/base/`
- add validation rules for every mandatory path
- document which future structural changes require migration support
