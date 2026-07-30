---
type: Internal Development Task
title: Define Ava SemVer and Compatibility
description: Define how Ava release versions communicate behavioral, structural, and migration compatibility.
tags: [internal, roadmap, semver, compatibility]
status: pending
phase: 4
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T11:26:00Z
---

# Define Ava SemVer and Compatibility

## Define

- the project-level `ava_version` contract and its relationship to `okf_version`
- PATCH changes that preserve supported structure and intended behavior
- MINOR changes that remain backward-compatible for installed projects
- MAJOR changes that require an incompatible format, routing, ownership, or behavioral migration
- compatibility guarantees before and after Ava 1.0.0
- supported direct and chained upgrade paths
- how deprecated files, metadata, roles, and workflows communicate removal timelines
- how a project records completed and pending migrations

## Required decisions

- whether an installer may skip intermediate releases when migrations exist
- how release candidates and prerelease channels are represented
- how older host agents or incomplete instruction-loading behavior affect compatibility claims
- when an upgrade is installed but not semantically complete

## Completion criteria

- publish a precise SemVer policy with examples
- define the installed version and migration-state metadata
- define compatibility and support windows
- align release notes, validation, and upgrade behavior with the policy
