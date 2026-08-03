---
type: Internal Development Task
title: Implement Validation, Conformance, and Upgrade Fixtures
description: Validate the public format, installed base state, semantic compatibility, filesystem safety, trust modes, conflicts, rollback, and supported transitions.
tags: [internal, roadmap, validation, testing, conformance, upgrades]
status: pending
phase: 4
order: 10
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T14:09:00+02:00
---

# Implement Validation, Conformance, and Upgrade Fixtures

This task begins after completion of the preceding design, repository-boundary, installer, path, and managed-directory discoverability tasks.

## Validation contract

Define and implement stable machine-readable findings with at least:

- rule identifier
- severity with stable `error`, `warning`, and `recommendation` semantics
- affected path
- actionable message
- deterministic fix availability
- whether a semantic or user decision is required
- related role, workflow, version, migration, or release asset when applicable

Required structure and references must produce blocking findings. Optional context may produce non-blocking findings when its absence does not invalidate routing, authority, installation, or upgrade behavior.

Automatic repair is permitted only when the correct result is unambiguous and deterministic. Validation and repair must never silently resolve contradictory instructions, choose between competing canonical documents, grant authority, delete uncertain project knowledge, or change role or workflow purpose.

## Implement

- validation for required files and directories, reserved filenames, frontmatter presence and schema, internal links, indexes, registry membership, required-reading paths, workflow-to-role references, duplicate identifiers, orphaned documents, deprecated references, and internal-content leakage
- validation that role, workflow, and instruction discovery follows explicit indexes and registries and reports missing or ambiguous required paths
- validation of the repository boundary between public distribution contracts, release payload sources, and internal release procedures
- separation of structural and deterministic findings from semantic compatibility findings and unresolved project decisions
- validation for installed `ava_version`, release source, managed-file checksums, deterministic migration state, and separate semantic compatibility
- validation that the manifest remains at its Ava-managed path and is updated only by permitted upgrade mechanisms
- fixtures for a minimal fresh installation, a complete base installation, and a project with project-owned context
- invalid-format fixtures covering role structures, workflow routing, required and optional references, metadata, duplicate identifiers, orphaned documents, deprecated references, and internal-content leakage
- fixtures for eligible adoption, an existing unversioned Ava structure, pre-existing root files, path collisions, explicit resolution, and safe refusal
- unchanged, locally modified, missing, and corrupt managed-file cases
- path-normalization, parent-traversal, symlink-escape, unsafe-archive-entry, and out-of-root write cases
- staged grouped-change, expected-version, dry-run, pre-validation, post-validation, partial-apply prevention, and rollback cases
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

- the current public Ava format has a complete structural conformance validator
- validation severity and finding fields remain stable and machine-readable
- required and optional failures are distinguished consistently
- deterministic fixes never make semantic or authority decisions
- every supported installation, adoption, and upgrade path has an integration fixture
- unsupported or unsafe states fail with actionable diagnostics
- filesystem safety fixtures prove that no operation can escape the selected target root
- grouped changes cannot leave a partially applied project after validation or apply failure
- rollback and resume behavior are tested
- validation distinguishes deterministic failure from pending semantic work
- validation never equates `ava_version` with semantic completion
- validation proves that normal operation cannot resume before semantic migration reaches a permitted terminal state
- Upgrade Role validation proves exhaustive affected-file discovery and bounded authority
- verified installation fails when provenance or attestation verification fails
- release publication fails when immutability requirements are not satisfied
- CI verifies release artifacts using the same paths used by users
