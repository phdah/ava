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
  at: 2026-07-30T15:26:00Z
---

# Define Ava SemVer and Compatibility

## Fixed version distinction

- `ava_version` identifies only the installed Ava-managed base distribution.
- `ava_version` advances when the deterministic base upgrade succeeds.
- Semantic compatibility of project-owned context is tracked separately.
- A project may therefore have `ava_version: 2.0.0` while semantic compatibility remains completed only through an earlier version.
- Validation and reporting must make that state explicit rather than presenting the project as fully migrated.

## Define

- the project-level `ava_version` contract and its relationship to `okf_version`
- the separate semantic-compatibility metadata and allowed states
- PATCH changes that preserve supported structure and intended behavior
- MINOR changes that remain backward-compatible for installed projects
- MAJOR changes that require an incompatible format, routing, ownership, or behavioral migration
- compatibility guarantees before and after Ava 1.0.0
- supported direct and chained upgrade paths
- how deprecated files, metadata, roles, and workflows communicate removal timelines
- how completed, partial, blocked, and pending semantic migrations are recorded

## Required decisions

- the exact semantic-compatibility field names and schema
- whether an installer may skip intermediate releases when migrations exist
- how release candidates and prerelease channels are represented
- how older host agents or incomplete instruction-loading behavior affect compatibility claims
- how commands and reports distinguish installed base state from semantic completion

## Completion criteria

- publish a precise SemVer policy with examples
- define `ava_version` strictly as installed-base state
- define separate semantic-compatibility metadata and transitions
- define compatibility and support windows
- align release notes, validation, and upgrade behavior with the policy