---
type: Internal Development Task
title: Implement Validation and Upgrade Fixtures
description: Validate installed base state, semantic compatibility, trust modes, conflicts, rollback, and supported transitions.
tags: [internal, roadmap, validation, testing, upgrades]
status: proposed
phase: 4
order: 7
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Implement Validation and Upgrade Fixtures

This task becomes active only after explicit user approval of the distribution-first architecture and completion of the preceding design tasks.

## Implement

- validation for installed `ava_version`, release source, managed-file checksums, deterministic migration state, and separate semantic compatibility
- fixtures for a minimal fresh installation and a project with project-owned context
- unchanged, locally modified, missing, and corrupt managed-file cases
- PATCH, MINOR, MAJOR, direct, and chained upgrade transitions
- deterministic migration success, failure, interruption, retry, and rollback cases
- semantic migration pending, partial, blocked, and completed states
- an installed-new-base state whose project-owned context remains compatible only through an earlier version
- checks that project-owned content and internal Ava files never leak into managed replacement
- release-asset consistency and integrity tests
- convenience bootstrap trust assumptions and verified bootstrap authenticity tests

## Completion criteria

- every supported installation and upgrade path has an integration fixture
- unsupported or unsafe states fail with actionable diagnostics
- rollback and resume behavior are tested
- validation distinguishes deterministic failure from pending semantic work
- validation never equates `ava_version` with semantic completion
- verified installation fails when provenance or attestation verification fails
- CI verifies release artifacts using the same paths used by users