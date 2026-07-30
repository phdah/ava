---
type: Internal Development Task
title: Implement Validation and Upgrade Fixtures
description: Validate installed state and test fresh installs, conflicts, rollback, and supported upgrade transitions.
tags: [internal, roadmap, validation, testing, upgrades]
status: pending
phase: 4
order: 7
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T11:26:00Z
---

# Implement Validation and Upgrade Fixtures

## Implement

- validation for installed version, release source, managed-file checksums, migration state, and pending semantic guidance
- fixtures for a minimal fresh installation and a project with user-owned context
- unchanged, locally modified, missing, and corrupt managed-file cases
- PATCH, MINOR, MAJOR, direct, and chained upgrade transitions
- deterministic migration success, failure, interruption, retry, and rollback cases
- semantic migration pending and completed states
- checks that project-owned content and internal Ava files never leak into managed replacement
- release-asset consistency and checksum tests

## Completion criteria

- every supported installation and upgrade path has an integration fixture
- unsupported or unsafe states fail with actionable diagnostics
- rollback and resume behavior are tested
- validation can distinguish deterministic failure from pending semantic work
- CI verifies release artifacts using the same paths used by users
