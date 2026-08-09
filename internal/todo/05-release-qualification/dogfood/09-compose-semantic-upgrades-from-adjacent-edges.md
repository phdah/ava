---
type: Internal Development Task
title: Compose semantic upgrades from adjacent release edges
description: Redesign the general release and upgrade process to replace duplicated source-to-target semantic guidance with deterministic composition of reviewed adjacent release edges.
tags: [internal, roadmap, dogfood, releases, upgrades, semantics]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 9
classification: required-v1
blocks: release-candidate
affected_version: release process, observed in 1.0.0-alpha.11
generated:
  by: agent:openai-chatgpt
  at: 2026-08-08T23:58:55+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T12:48:00+02:00
---

# Compose semantic upgrades from adjacent release edges

## Architectural scope

This is not a correction limited to `1.0.0-alpha.11` or prerelease handling. Alpha.11 exposed a general release-process problem.

The accepted model applies to future Ava prerelease and stable releases. Each release authors one new adjacent edge, carries forward immutable reviewed edge history, and resolves cumulative managed and semantic work through deterministic composition.

## Observed behavior

Completing the `1.0.0-alpha.11` release required the target release to restate complete source-to-target upgrade assessments for every supported prerelease. Earlier semantic obligations were copied into new target-specific guidance even when the newest edge added no project-owned semantic work.

That model was safe but quadratic. It increased authoring cost and created unnecessary opportunities for duplicated guidance to drift or be omitted.

## Resolution

Ava now defines an accepted adjacent-edge catalog contract:

- each release appends and reviews only its new adjacent edge
- the target catalog remains self-contained for every retained supported source
- inherited edges are protected by canonical SHA-256 identity
- managed paths resolve from installed `ava_version`
- semantic paths resolve separately from `semantic_compatibility.compatible_through`
- guidance is composed in edge order and applied exactly once
- later guidance may supersede only already active guidance IDs
- gaps, cycles, ambiguity, tampering, unsupported sources, invalid carry state, and missing artifacts fail before mutation
- already published direct source-to-target releases remain readable during the compatibility transition

The user explicitly approved this public contract on 2026-08-09 and directed that the resolving pull request represent a completed to-do on `main`.

## Repository implementation

The resolving implementation provides:

- [`distribution/adjacent-upgrade-edges.md`](../../../../distribution/adjacent-upgrade-edges.md), the accepted public contract
- [`distribution/schemas/upgrade-catalog.schema.json`](../../../../distribution/schemas/upgrade-catalog.schema.json), the catalog schema
- `internal/release/adjacent_edges.py`, implementing immutable edge digests, catalog validation, unique path resolution, separate managed and semantic paths, semantic carry rules, and ordered guidance supersession
- `internal/release/compose_adjacent_catalog.py`, appending one reviewed adjacent edge to inherited immutable history
- `internal/release/validate_adjacent_catalog.py`, proving inherited identity, supported-source retention, explicit retirement, and representative path behavior
- `internal/release/fixtures/adjacent-upgrade-catalog.json`, freezing a semantically lagging multi-edge example
- `internal/release/tests/test_adjacent_edges.py`, covering direct and multi-edge paths, gaps, ambiguity, digest tampering, inheritance, retirement, semantic lag, no-op semantic advancement, carry blocking, supersession, duplicate guidance, and channel-independent composition
- normal release test-runner integration for compilation, fixture validation, and regression execution

## Repository validation

Pull request #76 passed:

- Conventional PR title validation
- release PR policy validation
- the complete Python test workflow
- 13 focused adjacent-edge regression tests
- canonical fixture validation for a one-edge managed path and a two-edge semantic path from lagging compatibility state

## Completion criteria

- [x] the public contract defines adjacent-edge inheritance and deterministic path resolution
- [x] the schema represents immutable edges, supported sources, semantic guidance, and supersession
- [x] release tooling composes a self-contained target catalog from inherited history plus one new edge
- [x] validation proves inherited edge identity and explicit supported-source retirement
- [x] managed and semantic paths resolve separately
- [x] guidance is ordered, exact-once, and explicitly supersedable
- [x] no-guidance edges support mechanical semantic advancement only after earlier obligations are complete
- [x] unresolved semantic state crosses only explicitly permitted edges
- [x] invalid or non-composable graphs fail before mutation
- [x] generic fixtures cover successive releases and semantically lagging projects
- [x] documentation, schema, tooling, fixtures, tests, indexes, and conceptual history are aligned
- [x] the user approved the public contract
- [x] concrete repository-validation evidence is recorded

## Release qualification follow-up

Publish and validate a catalog-based release whose supported path spans at least three adjacent edges. Verify both:

1. a project fully compatible with its installed source traverses only newly applicable semantic edges
2. a project whose installed base is newer than `compatible_through` receives every outstanding semantic obligation exactly once before compatibility advances

Confirm that the release contains no separately authored cumulative source-to-target guidance for paths proven by adjacent-edge composition. This is immutable-release qualification evidence and does not keep this repository implementation task pending.
