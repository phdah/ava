---
type: Internal Development Task
title: Define Ava SemVer and Compatibility
description: Define installed-base versioning and separate semantic compatibility for project-owned context.
tags: [internal, roadmap, semver, compatibility]
status: complete
phase: 4
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T12:08:00+02:00
---

# Define Ava SemVer and Compatibility

The accepted public contract is documented in [Ava Versioning and Compatibility](/templates/versioning-and-compatibility.md). The installed manifest shape is defined by [manifest.schema.json](/templates/schemas/manifest.schema.json).

## Accepted decisions

- `/.ava/state/manifest.json` is the Ava-managed ownership and installed-state record.
- `ava_version` identifies only the installed Ava-managed base distribution.
- `okf_version` remains a separate knowledge-format compatibility value.
- Semantic compatibility of project-owned context is recorded separately through `compatible_through`, `target_version`, `status`, and `unresolved_decisions`.
- Valid semantic states are `complete`, `pending`, `partial`, and `blocked`, with explicit state invariants.
- Deterministic tooling exclusively controls manifest schema, installed release identity, `ava_version`, `okf_version`, timestamps, and the managed-file inventory.
- Deterministic tooling may mechanically retain semantic completion when a release declares no semantic review, or initialize a pending target when review is required.
- The explicit Upgrade Role is the sole agent role allowed to update semantic compatibility state and may never change release identity, managed paths, or checksums.
- Immutable managed payload files require SHA-256 checksums.
- Mutable managed state files are schema and transition validated and must not contain self-checksums.
- `manifest.json` and `upgrade.json` are recorded as managed state rather than immutable payload.
- PATCH preserves supported structure and intended behavior.
- MINOR requires explicit opt-in reachability or repeatable evidence that every existing routing, workflow, role-selection, authority, validation, and intended-behavior outcome is unchanged.
- Any addition that changes or makes an existing resolution or authority outcome ambiguous is MAJOR even when old files remain readable.
- MINOR review compares maintained fixtures across validation, ownership, routing, required reading, capabilities, constraints, workflow mode, mutation authority, and semantic migration requirements.
- The current unversioned repository has no release compatibility guarantee. Ava's first supported stable distribution is `1.0.0`; pre-stable testing uses `1.0.0-alpha.N`, `beta.N`, and `rc.N` prereleases.
- Stable installers do not select prereleases automatically.
- Direct version skipping is allowed only when the target explicitly supports the source and includes all required deterministic migrations and semantic guidance. Otherwise a declared chained path is required.
- Ava-managed deprecations use `deprecated_since` and `removal_not_before`; removal or behavior-changing replacement requires the applicable MAJOR release.
- Compatibility claims assume host conformance with complete instruction loading and unknown-field preservation. Host discovery status remains separate from Ava version and semantic completion.
- The latest MINOR of the current MAJOR receives PATCH maintenance. The immediately previous MAJOR remains a supported upgrade source for at least twelve months after the next MAJOR becomes stable.

## Repository impact

- Added the public versioning and compatibility contract.
- Added a Draft 2020-12 JSON Schema for the installed manifest.
- Added schema navigation under `/templates/schemas/`.
- Aligned the distribution contract with payload checksums and mutable state validation.
- Added versioned deprecation metadata and validation rules to the document metadata contract.
- Updated repository navigation and conceptual history.

## Validation

The schema was parsed with `python -m json.tool` and validated with `jsonschema` against:

- a valid pending semantic migration
- a valid complete semantic migration
- rejection of checksums on mutable state entries

The policy defines the repeatable MINOR compatibility proof that the later validation-fixtures task must implement.
