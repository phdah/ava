---
id: ava-410
title: "Implement validation, conformance, and upgrade fixtures"
status: "Done"
labels: ["internal", "roadmap", "phase-04"]
ordinal: 410
---

## Description

Implement complete structural and installed-state conformance validation plus upgrade fixtures. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Implement Validation, Conformance, and Upgrade Fixtures
description: Validate the public format, installed base state, agent-first maintenance, OpenCode support, semantic compatibility, filesystem safety, trust modes, conflicts, rollback, and supported transitions.
tags: [internal, roadmap, validation, testing, conformance, upgrades, maintenance, opencode]
status: completed
phase: 4
order: 10
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T14:09:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-03T22:30:00+02:00
---

# Implement Validation, Conformance, and Upgrade Fixtures

This task begins after completion of the distribution contracts, installer, path normalization, OpenCode support, document update metadata, and Ava Maintenance role.

## Validation contract

Define and implement stable machine-readable findings with at least:

- rule identifier
- severity with stable `error`, `warning`, and `recommendation` semantics
- affected path
- actionable message
- deterministic fix availability
- whether a semantic or user decision is required
- related role, workflow, version, migration, host, or release asset when applicable

Required structure and references must produce blocking findings. Optional context may produce non-blocking findings when its absence does not invalidate routing, authority, installation, upgrade behavior, or the claimed host support level.

Automatic repair is permitted only when the correct result is unambiguous and deterministic. Validation and repair must never silently resolve contradictory instructions, choose between competing canonical documents, grant authority, delete uncertain project knowledge, change role or workflow purpose, or bypass the Ava Maintenance or Upgrade Role authority boundaries.

## Implement

- validation for required files and directories, reserved filenames, frontmatter presence and schema, update metadata, internal links, indexes, registry membership, required-reading paths, workflow-to-role references, duplicate identifiers, orphaned documents, deprecated references, and internal-content leakage
- validation that role, workflow, and instruction discovery follows explicit indexes and registries and reports missing or ambiguous required paths
- validation of the repository boundary between public distribution contracts, release payload sources, and internal release procedures
- separation of structural and deterministic findings from semantic compatibility findings and unresolved project decisions
- validation for installed `ava_version`, release source, managed-file checksums, deterministic migration state, and separate semantic compatibility
- validation that the manifest remains at its Ava-managed path and is updated only by permitted upgrade mechanisms and role-authorized transitions
- validation of deterministic pre-routing to Ava Maintenance and semantic pre-routing to the Upgrade Role
- fixtures for a minimal fresh installation, a complete base installation, and a non-empty project with project-owned context
- invalid-format fixtures covering role structures, workflow routing, required and optional references, metadata, duplicate identifiers, orphaned documents, deprecated references, and internal-content leakage
- fixtures for eligible installation into an existing non-Ava project, pre-existing root files, path collisions, explicit resolution, and safe refusal
- explicit refusal of unknown or historical `.ava/` layouts without implementing an unversioned Ava migration path
- unchanged, locally modified, missing, corrupt, and unexpected managed-file cases
- path-normalization, parent-traversal, symlink-escape, unsafe-archive-entry, and out-of-root write cases
- staged grouped-change, expected-version, dry-run, pre-validation, post-validation, partial-apply prevention, and rollback cases
- deterministic migration success, failure, interruption, retry, resume, abort, rollback, and finalization cases
- Ava Maintenance reporting for installed identity, channel, source revision, OKF version, host state, managed integrity, and available recovery actions
- role-led uninstall cases that remove `.ava/` and an unchanged managed root router while preserving every project-owned path and host entrypoint
- uninstall refusal during active work or when managed ownership cannot be proven safely
- semantic migration pending, partial, blocked, and completed states
- an installed-new-base state whose project-owned context remains compatible only through an earlier version
- checks that ordinary Ava routing remains blocked while deterministic or semantic work is incomplete
- Upgrade Role fixtures covering roles, workflows, shared instructions, knowledge, registries, `index.md`, `log.md`, metadata, links, filenames, and directory-layout migrations
- checks that semantic completion fails when any required affected project-owned file or relationship remains inconsistent
- checks that project-owned content and internal Ava files never leak into managed replacement
- OpenCode conformance fixtures using the documented installation and project configuration path
- host-neutral discovery fixtures without unsupported named-host claims
- release-asset consistency and integrity tests
- convenience bootstrap trust assumptions and verified bootstrap authenticity tests
- prerelease channel, exact-tag selection, and explicitly declared alpha-to-alpha, alpha-to-RC, and RC-to-stable upgrade cases
- release-publication checks that detect when immutable releases are not enabled or a published release is not immutable

## No additional operational command surface

The validator may expose machine-readable findings to deterministic release tooling and tests. User-facing interpretation of installation health belongs to Ava Maintenance.

Do not introduce standalone status, version, repair, or uninstall commands as a substitute for the role. Existing deterministic installer operations remain available for the role to invoke when recovery requires them.

## Implementation result

- Added `internal/release/conformance.py` with repository, installed-project, release-asset, and automatic validation modes.
- Stabilized machine-readable finding fields, severity semantics, deterministic-fix and decision flags, related context, JSON, JSON Lines, and text output.
- Added explicit installed-state routing qualification that remains blocked by deterministic, semantic, or routing errors.
- Added release asset checksum, manifest metadata, version-channel, and immutable-publication evidence validation.
- Added an 86-case machine-readable conformance matrix with explicit prerelease transitions, semantic completion scope, host claims, trust modes, and executable evidence references.
- Added validator, matrix, and installer conformance tests for metadata, discovery, managed integrity, unknown historical layouts, dry-run behavior, grouped rollback, migration failure, exact version selection, OpenCode diagnostics, and publication failures.
- Wired the same validator and tests into the release test runner and repository boundary validation.

## Completion criteria

- the current public Ava format has a complete structural conformance validator
- validation severity and finding fields remain stable and machine-readable
- required and optional failures are distinguished consistently
- deterministic fixes never make semantic, authority, or ownership decisions
- every supported installation and upgrade path has an integration fixture
- historical unversioned Ava migration is not claimed or implemented
- unsupported or unsafe states fail with actionable diagnostics
- filesystem safety fixtures prove that no operation can escape the selected target root
- grouped changes cannot leave a partially applied project after validation or apply failure
- rollback, resume, abort, and finalization behavior are tested
- Ava Maintenance and Upgrade Role routing and authority are tested independently
- role-led uninstall removes Ava-managed state and routing without modifying project-owned content
- validation distinguishes deterministic failure from pending semantic work
- validation never equates `ava_version` with semantic completion
- validation proves that normal operation cannot resume before required deterministic or semantic work reaches a permitted terminal state
- OpenCode passes its maintained host-conformance fixture using the same installed assets and paths used by users
- verified installation fails when provenance or attestation verification fails
- release publication fails when immutability requirements are not satisfied
- CI verifies release artifacts using the same paths used by users