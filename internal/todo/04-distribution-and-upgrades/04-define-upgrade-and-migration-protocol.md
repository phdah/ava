---
type: Internal Development Task
title: Define Upgrade and Migration Protocol
description: Define safe base reconciliation, deterministic migrations, conflicts, rollback, and separate semantic completion state.
tags: [internal, roadmap, upgrades, migrations]
status: pending
phase: 4
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T22:27:00+02:00
---

# Define Upgrade and Migration Protocol

## Define

- how the updater reads `ava_version` and resolves a target base version
- three-way comparison between the previously installed base, current local managed files, and target base
- automatic replacement when managed files are locally unchanged
- conflict handling when managed files and the target release both changed
- deterministic migration discovery, ordering, idempotency, and recording
- whether upgrades may skip versions or must traverse migration edges
- transactional staging, validation, rollback, and resume behavior
- separate state transitions for deterministic installation and project-owned semantic compatibility
- the complete upgrade operation as one bounded transaction with deterministic and semantic stages
- which operations remain permitted while an upgrade is in progress, pending, partial, or blocked
- how a user resumes, resolves, aborts, or rolls back an incomplete upgrade
- a pre-routing upgrade-state check performed by the Ava-managed root `AGENTS.md` before normal workflow, role, instruction, or project-registry resolution
- an Ava-managed upgrade-mode routing path that remains usable when project-owned routing contracts are incompatible with the newly installed base
- the exact point at which normal project-owned registries may be consulted after upgrade routing and authority have already been established

## Required state semantics

- `ava_version` advances only after deterministic base installation and migrations succeed.
- Advancing `ava_version` does not imply that project-owned context has completed semantic migration.
- Semantic compatibility must record its own completed, partial, blocked, or pending state and target version.
- Reports must show both installed base version and semantic compatibility state.
- The overall upgrade remains active until semantic migration completes, the user explicitly rolls back, or the protocol reaches another defined terminal state.
- Normal Ava operations must not begin while the upgrade remains active. Only upgrade inspection, conflict resolution, user-decision capture, resume, abort, and rollback operations are permitted.
- When the managed manifest indicates an active or incomplete upgrade, the managed router must enter upgrade mode before reading project-owned workflow or role registries.
- Upgrade-mode activation, required guidance discovery, role resolution, and permitted-operation checks must be available entirely from Ava-managed files.
- Project-owned registries may be inspected as migration targets only after the managed Upgrade Role and bounded upgrade authority are active.
- A blocked semantic migration is not treated as a completed upgrade merely because deterministic installation succeeded.

## Safety rules

- never silently overwrite locally modified managed files
- never rewrite project-owned context as part of deterministic base replacement
- do not advance `ava_version` after failed deterministic work
- do not mark semantic compatibility complete while unresolved decisions remain
- do not resume ordinary project operations while the upgrade transaction is incomplete
- do not depend on project-owned registries, indexes, or routing instructions to discover or activate the Upgrade Role
- do not allow an incompatible project-owned routing contract to prevent inspection, resume, abort, rollback, or semantic migration
- retain enough state to explain and resume an interrupted or blocked upgrade

## Completion criteria

- define local manifest and migration-state changes for every upgrade stage
- define the entry, permitted operations, and exit conditions for every incomplete upgrade state
- define conflict, abort, rollback, and resume semantics
- define direct and chained upgrade behavior
- provide worked examples for PATCH, MINOR, and MAJOR transitions
- demonstrate an installed-new-base but pending-semantic-migration state and show that ordinary operations remain blocked
- demonstrate a fresh agent invocation entering managed upgrade mode even when project-owned role and workflow registries are incompatible or unreadable under the target base
- define the pre-routing manifest check, managed upgrade activation path, and the point at which project-owned files become safe migration inputs
- align the protocol with installer implementation, Upgrade Role authority, validation, and release assets