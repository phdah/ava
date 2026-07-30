---
type: Internal Development Task
title: Define Upgrade and Migration Protocol
description: Define safe managed-file reconciliation, deterministic migrations, conflicts, rollback, and completion state.
tags: [internal, roadmap, upgrades, migrations]
status: pending
phase: 4
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T11:26:00Z
---

# Define Upgrade and Migration Protocol

## Define

- how the updater reads the installed version and resolves a target version
- three-way comparison between the previously installed base, current local managed files, and target base
- automatic replacement when managed files are locally unchanged
- conflict handling when managed files and the target release both changed
- deterministic migration discovery, ordering, idempotency, and recording
- whether upgrades may skip versions or must traverse migration edges
- transactional staging, validation, rollback, and resume behavior
- the distinction between deterministic completion and pending semantic migration

## Safety rules

- never silently overwrite locally modified managed files
- never rewrite project-owned context as part of deterministic base replacement
- do not advance the installed version after failed deterministic work
- retain enough state to explain and resume an interrupted upgrade

## Completion criteria

- define the local manifest and migration-state changes for every upgrade stage
- define conflict and rollback semantics
- define direct and chained upgrade behavior
- provide worked examples for PATCH, MINOR, and MAJOR transitions
- align the protocol with installer implementation and release assets
