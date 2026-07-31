---
type: Internal Development Task
title: Implement Validation and Upgrade Fixtures
description: Validate installed base state, semantic compatibility, trust modes, conflicts, rollback, and supported transitions.
tags: [internal, roadmap, validation, testing, upgrades]
status: pending
phase: 4
order: 7
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Implement Validation and Upgrade Fixtures

This task begins after completion of the preceding design and installer tasks.

## Implement

- validation for installed `ava_version`, release source, managed-file checksums, deterministic migration state, and separate semantic compatibility
- validation that the manifest remains at its Ava-managed path and is updated only by permitted upgrade mechanisms
- fixtures for a minimal fresh installation and a project with project-owned context
- fixtures for eligible adoption, an existing unversioned Ava structure, pre-existing root files, path collisions, explicit resolution, and safe refusal
- unchanged, locally modified, missing, and corrupt managed-file cases
- PATCH, MINOR, MAJOR, direct, and chained upgrade transitions
- deterministic migration success, failure, interruption, retry, and rollback cases
- semantic migration pending, partial, blocked, and completed states
- an installed-new-base state whose project-owned context remains compatible only through an earlier version
- checks that ordinary Ava routing remains blocked while the overall upgrade is incomplete
- Upgrade Role fixtures covering roles, workflows, shared instructions, knowledge, registries, `index.md`, `log.md`, metadata, links, filenames, and directory-layout migrations
- checks that semantic completion fails when any required affected project-owned file or relationship remains inconsistent
- checks that project-owned content and internal Ava files never leak into managed replacement
- release-asset consistency and integrity tests
- convenience bootstrap trust assumptions and verified bootstrap authenticity tests
- release-publication checks that detect when immutable releases are not enabled or a published release is not immutable

## Completion criteria

- every supported installation, adoption, and upgrade path has an integration fixture
- unsupported or unsafe states fail with actionable diagnostics
- rollback and resume behavior are tested
- validation distinguishes deterministic failure from pending semantic work
- validation never equates `ava_version` with semantic completion
- validation proves that normal operation cannot resume before semantic migration reaches a permitted terminal state
- Upgrade Role validation proves exhaustive affected-file discovery and bounded authority
- verified installation fails when provenance or attestation verification fails
- release publication fails when immutability requirements are not satisfied
- CI verifies release artifacts using the same paths used by users
