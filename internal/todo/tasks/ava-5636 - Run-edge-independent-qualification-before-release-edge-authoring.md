---
id: ava-5636
title: Run edge-independent qualification before release-edge authoring
status: To Do
assignee: []
created_date: '2026-09-01 20:04'
labels:
  - internal
  - roadmap
  - release
  - qualification
  - fail-fast
milestone: m-0
dependencies: []
type: enhancement
ordinal: 6635
---

## Description

Reorder Ava's release process so qualification work that does not semantically depend on the adjacent release edge runs before edge authoring. The purpose is to fail fast on candidate defects before spending time on semantic-impact review, catalog authoring, guidance, migrations, or other edge-specific work.

The existing release procedure performs edge authoring before the full qualification run. Full qualification is also revision-bound and currently depends on candidate assembly that requires the adjacent catalog, so this change must split qualification deliberately rather than simply moving the existing command earlier unchanged.

## Required behavior

1. Inventory the current release qualification checks and classify each check as either:
   - **edge-independent**: valid against the target release behavior without the adjacent release record, semantic guidance, migrations, or source-retirement decisions
   - **edge-dependent**: semantically or mechanically requires the completed adjacent edge or resulting release metadata
2. Run all edge-independent qualification as the first substantive release validation after release-please has identified the target release.
3. Stop immediately when the early qualification phase fails or needs review. Do not author the adjacent edge, semantic guidance, migrations, or related release-specific state after such a failure.
4. Only after the edge-independent phase succeeds, perform managed-delta review, semantic-impact assessment, and adjacent-edge authoring.
5. Run the edge-dependent qualification checks after the edge is complete.
6. Preserve a final release gate whose evidence proves that both phases apply to the same intended target release and that no relevant change invalidated the earlier phase.
7. Do not rerun expensive edge-independent checks after edge authoring unless the authored edge or another intervening change can affect what those checks validated.

## Design constraints

- Early qualification is a fail-fast gate, not automatic release acceptance.
- The split must not weaken the existing requirement that every release receives complete qualification and explicit user signoff before merge.
- Revision and invalidation rules must remain sound. If edge authoring can alter an input observed by an early check, that check must either be classified as edge-dependent or rerun after the change.
- The implementation must make the phase boundary explicit in scripts, evidence, and the release procedure rather than relying on operators to remember which checks can be skipped.
- Qualification failures must continue to produce actionable evidence and must not mutate release content automatically.

## Implementation scope

- update the authoritative release procedure and release-flow ordering
- split or parameterize qualification tooling so the two phases are mechanically enforced
- make candidate preparation possible for the edge-independent phase without requiring the adjacent catalog where appropriate
- classify the maintained qualification matrix and independent audit checks by phase
- update qualification evidence/state so final acceptance can verify both phases and their revision/content relationship
- update release-PR policy validation and invalidation rules as required
- add regression coverage proving fail-fast behavior and proving that edge-dependent checks still run before acceptance

## Completion criteria

- a release with an edge-independent qualification failure stops before adjacent-edge authoring
- every maintained qualification check has one explicit phase or a documented reason it must run in both phases
- successful early qualification is reused safely rather than blindly rerun after edge authoring
- any change that could invalidate early evidence is detected and forces the necessary requalification
- edge-dependent checks execute after edge authoring and remain mandatory
- final user signoff and release-PR merge policy require complete valid evidence from both phases
- the documented release procedure reflects the implemented order and can be followed without manual interpretation
