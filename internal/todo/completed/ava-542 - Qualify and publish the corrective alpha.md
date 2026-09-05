---
id: ava-542
title: Qualify and publish the corrective alpha
status: Done
assignee: []
created_date: ''
updated_date: '2026-09-01 19:54'
labels:
  - internal
  - roadmap
  - phase-05
  - release
  - qualification
  - dogfood
  - "Won't Fix"
dependencies: []
ordinal: 542
---

## Description

Publish the completed dogfood corrections through one new immutable alpha and collect the pinned published-release evidence required before alpha dogfooding can be closed and release-candidate work can begin. This task is intentionally parked.

Release-please determines the actual target prerelease and channel when this path is resumed. Do not hard-code a future alpha number and never move, replace, or reuse an immutable published tag.

## Entry dependencies

Do not complete or publish the corrective alpha until:

- every dogfood finding classified to block the next prerelease is implementation-complete
- AVA-541 has satisfied its qualification gate
- no new blocker prevents publication
- the exact target version and source revision receive approval through Ava's maintained release-PR process

## Release preparation contract

When explicitly resumed:

- let release-please derive the canonical target and channel
- review the exact previous-to-target managed delta
- complete the project-owned semantic-impact assessment and preserve reviewed rationale
- author exactly one immutable adjacent release record under `internal/release/catalogs/<target>.json`
- add only transition-local guidance, migrations, and retirement decisions
- keep historical catalog records immutable and do not reintroduce cumulative `upgrade-impact.json` authoring
- validate the release PR against its base revision
- run the complete repository release test suite
- qualify and reproducibly assemble the exact release revision before publication

## Published-asset qualification

Pinned immutable assets must then be exercised across empty and mature projects, every declared source upgrade, managed-state gating, recovery, semantic reconciliation, terminal finalization, transaction cleanup, realistic multi-turn routing, representative inbox ingestion, independent hierarchy/fidelity review, unresolved-routing behavior, and a fresh OpenCode session.

Qualification evidence must bind release identity, exact source revision, asset URLs/digests, transcripts, conformance results, project-owned before/after hashes, and scenario outcomes.

## Completion criteria

Completion requires one approved immutable corrective alpha, recorded terminal outcomes for every declared upgrade source, published-version/realistic-project evidence for applicable completed findings, clean maintained synthetic qualification across routing/ingestion/review/hierarchy/upgrade/recovery/finalization/maintenance, complete evidence manifests, and no pending next-prerelease blocker.

Completing this task never completes AVA-504 automatically. Explicit user-owned dogfood closure remains a separate gate before AVA-505.

This is historical parked release state, not the active queue.
