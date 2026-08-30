---
id: ava-5609
title: "Compose semantic upgrades from adjacent release edges"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5609
---

## Description

Redesign the general release and upgrade process to replace duplicated source-to-target semantic guidance with deterministic composition of reviewed adjacent release edges.

## Migrated task record

Historical metadata: phase 5 finding 9, `required-v1`, blocking release candidate, exposed during `1.0.0-alpha.11`, completed after user-approved public-contract implementation.

### Problem and accepted architecture

Alpha.11 exposed a general release-process problem: every target release restated complete source-to-target assessments for all supported prereleases and copied earlier semantic obligations into new target-specific guidance. This was safe but quadratic and created drift/omission risk.

The approved model applies to prerelease and stable releases: each release reviews only one new adjacent edge; the target catalog is self-contained for retained sources; inherited edge identity is protected by canonical SHA-256; managed paths resolve from installed `ava_version`; semantic paths resolve separately from `semantic_compatibility.compatible_through`; guidance composes in edge order exactly once; supersession applies only to already-active guidance IDs; and gaps, cycles, ambiguity, tampering, unsupported sources, invalid carry state, or missing artifacts fail before mutation. Previously published direct source-to-target releases remain readable during compatibility transition.

### Repository implementation and evidence

The user explicitly approved this public contract on 2026-08-09. Implementation added `distribution/adjacent-upgrade-edges.md`, `distribution/schemas/upgrade-catalog.schema.json`, `internal/release/adjacent_edges.py`, `compose_adjacent_catalog.py`, `validate_adjacent_catalog.py`, a semantically lagging catalog fixture, and `test_adjacent_edges.py`. These cover immutable edge digests, inheritance, unique managed/semantic paths, carry rules, ordered guidance/supersession, source retirement, direct/multi-edge paths, gaps, ambiguity, tampering, semantic lag, no-op advancement, duplicate guidance, and channel-independent composition.

PR #76 passed conventional-title, release policy, full Python workflow, 13 focused adjacent-edge regressions, and canonical one-edge managed/two-edge lagging-semantic fixture validation. Documentation, schema, tooling, fixtures, indexes and conceptual history were aligned.

### Release qualification follow-up

A later catalog-based immutable release was still required to prove a supported path spanning at least three adjacent edges for both a fully compatible source and an installed base ahead of `compatible_through`, with each outstanding semantic obligation applied exactly once and no separately authored cumulative guidance. This is release evidence, not grounds to reopen the completed implementation task.