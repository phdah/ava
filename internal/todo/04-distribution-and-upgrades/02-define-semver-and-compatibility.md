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

The accepted public contract is documented in [Ava Versioning and Compatibility](/distribution/versioning.md). The installed manifest shape is defined by [manifest.schema.json](/distribution/schemas/manifest.schema.json).

## Accepted decisions

- `/.ava/state/manifest.json` is the Ava-managed ownership and installed-state record.
- `ava_version` identifies only the installed Ava-managed base distribution.
- `okf_version` remains a separate knowledge-format compatibility value.
- Semantic compatibility of project-owned context is recorded separately through `compatible_through`, `target_version`, `status`, and `unresolved_decisions`.
- Valid semantic states are `complete`, `pending`, `partial`, and `blocked`, with explicit state invariants.
- Deterministic tooling exclusively controls manifest schema, installed release identity, `ava_version`, `okf_version`, timestamps, and the managed-file inventory.
- The explicit Upgrade Role is the sole agent role allowed to update semantic compatibility state and may never change release identity, managed paths, or checksums.
- Immutable managed payload files require SHA-256 checksums. Mutable managed state files are schema and transition validated and must not contain self-checksums.
- PATCH preserves supported structure and intended behavior.
- MINOR requires explicit opt-in reachability or repeatable evidence that existing routing, workflow, role-selection, authority, validation, and intended-behavior outcomes are unchanged.
- Behavior-changing additions, resolution ambiguity, and authority changes are MAJOR even when old files remain readable.
- The first supported stable distribution is `1.0.0`; pre-stable testing uses SemVer prereleases.
- Direct version skipping is allowed only when the target explicitly supports the source and includes all required deterministic migrations and semantic guidance.
- Ava-managed deprecations use `deprecated_since` and `removal_not_before`.

## Repository impact

The public contract and manifest schema are indexed under `/distribution/`. Installed behavior remains unchanged by the repository move.

## Validation

The schema was parsed with `python -m json.tool` and validated with `jsonschema` against valid complete and pending states and invalid mutable-state checksums.
