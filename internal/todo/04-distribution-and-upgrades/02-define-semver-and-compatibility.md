---
type: Internal Development Task
title: Define Ava SemVer and Compatibility
description: Define installed-base versioning and separate semantic compatibility for project-owned context.
tags: [internal, roadmap, semver, compatibility]
status: pending
phase: 4
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T22:30:00+02:00
---

# Define Ava SemVer and Compatibility

## Fixed version distinction

- `ava_version` identifies only the installed Ava-managed base distribution.
- `ava_version` and semantic migration state live in an Ava-managed manifest under the Ava-managed directory.
- The upgrade process is the only authority that may update the Ava-managed manifest. The explicit Upgrade Role is the sole agent role with authority to update it, while deterministic tooling may perform mechanical state transitions defined by the upgrade protocol.
- `ava_version` advances when the deterministic base upgrade succeeds.
- Semantic compatibility of project-owned context is tracked separately.
- A project may therefore have `ava_version: 2.0.0` while semantic compatibility remains completed only through an earlier version.
- Validation and reporting must make that state explicit rather than presenting the project as fully migrated.
- A new role, workflow, instruction, metadata field, default, or registry entry qualifies as MINOR only when it is opt-in or demonstrably preserves every existing routing, workflow-resolution, role-selection, authority, and intended-behavior outcome for already supported projects.
- Any addition that can change an existing resolution or authority outcome is behaviorally incompatible and requires MAJOR classification, even when the filesystem format remains readable.

## Define

- the Ava-managed manifest path, schema, ownership, and allowed writers
- the `ava_version` contract and its relationship to `okf_version`
- the separate semantic-compatibility metadata and allowed states
- which state transitions are mechanical updater actions and which require the Upgrade Role's semantic authority
- PATCH changes that preserve supported structure and intended behavior
- MINOR changes that are opt-in or provably preserve existing routing, resolution, authority, and behavior for installed projects
- MAJOR changes that require an incompatible format, routing, ownership, authority, resolution, or behavioral migration
- compatibility guarantees before and after Ava 1.0.0
- supported direct and chained upgrade paths
- how deprecated files, metadata, roles, and workflows communicate removal timelines
- how completed, partial, blocked, and pending semantic migrations are recorded

## Required decisions

- the exact manifest location, field names, schema, and field-level update rules
- whether an installer may skip intermediate releases when migrations exist
- how release candidates and prerelease channels are represented
- how older host agents or incomplete instruction-loading behavior affect compatibility claims
- how commands and reports distinguish installed base state from semantic completion
- how release review proves that a proposed MINOR role, workflow, instruction, metadata, default, or registry addition cannot alter existing selection or authority outcomes
- which additions are explicitly opt-in and how that opt-in is represented without changing default routing

## Completion criteria

- publish a precise SemVer policy with examples
- define `ava_version` strictly as installed-base state
- define the manifest as Ava-managed and identify the deterministic and agent authorities allowed to update it
- define separate semantic-compatibility metadata and transitions
- define a repeatable compatibility test for distinguishing safe opt-in MINOR additions from behavior-changing MAJOR additions
- include examples where a structurally readable role, workflow, or registry addition is nevertheless MAJOR because it changes resolution or authority
- define compatibility and support windows
- align release notes, validation, upgrade-role authority, and upgrade behavior with the policy
