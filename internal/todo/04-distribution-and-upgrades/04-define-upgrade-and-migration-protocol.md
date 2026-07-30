---
type: Internal Development Task
title: Define Upgrade and Migration Protocol
description: Define safe base reconciliation, deterministic migrations, conflicts, rollback, and separate semantic completion state.
tags: [internal, roadmap, upgrades, migrations]
status: proposed
phase: 4
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Define Upgrade and Migration Protocol

This task becomes active only after explicit user approval of the distribution-first architecture.

## Define

- how the updater reads `ava_version` and resolves a target base version
- three-way comparison between the previously installed base, current local managed files, and target base
- automatic replacement when managed files are locally unchanged
- conflict handling when managed files and the target release both changed
- deterministic migration discovery, ordering, idempotency, and recording
- whether upgrades may skip versions or must traverse migration edges
- transactional staging, validation, rollback, and resume behavior
- separate state transitions for deterministic installation and project-owned semantic compatibility

## Required state semantics

- `ava_version` advances only after deterministic base installation and migrations succeed.
- Advancing `ava_version` does not imply that project-owned context has completed semantic migration.
- Semantic compatibility must record its own completed, partial, blocked, or pending state and target version.
- Reports must show both installed base version and semantic compatibility state.

## Safety rules

- never silently overwrite locally modified managed files
- never rewrite project-owned context as part of deterministic base replacement
- do not advance `ava_version` after failed deterministic work
- do not mark semantic compatibility complete while unresolved decisions remain
- retain enough state to explain and resume an interrupted upgrade

## Completion criteria

- define local manifest and migration-state changes for every upgrade stage
- define conflict and rollback semantics
- define direct and chained upgrade behavior
- provide worked examples for PATCH, MINOR, and MAJOR transitions
- demonstrate an installed-new-base but pending-semantic-migration state
- align the protocol with installer implementation and release assets