---
type: Internal Development Task
title: Normalize and enforce adjacent-edge release authoring
description: Convert active upgrade history to one canonical adjacent-edge catalog and require every future release to append exactly one adjacent edge.
tags: [internal, roadmap, dogfood, releases, upgrades, validation]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 11
classification: blocker
blocks: next-prerelease
affected_version: general release process, exposed by 1.0.0-alpha.12
generated:
  by: agent:openai-chatgpt
  at: 2026-08-09T16:25:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T17:30:00+02:00
---

# Normalize and Enforce Adjacent-Edge Release Authoring

## Resolution

The active repository now has one canonical adjacent-edge history and one valid release-authoring path.

`internal/release/catalogs/1.0.0-alpha.12.json` normalizes retained support as:

1. `1.0.0-alpha.5 -> 1.0.0-alpha.6`
2. `1.0.0-alpha.6 -> 1.0.0-alpha.7`
3. `1.0.0-alpha.7 -> 1.0.0-alpha.8`
4. `1.0.0-alpha.8 -> 1.0.0-alpha.9`
5. `1.0.0-alpha.9 -> 1.0.0-alpha.10`
6. `1.0.0-alpha.10 -> 1.0.0-alpha.11`
7. `1.0.0-alpha.11 -> 1.0.0-alpha.12`

The alpha.9 to alpha.10 edge owns the existing knowledge-hierarchy and inbox-fidelity guidance. Later edges explicitly declare no new project-owned semantic impact. The catalog freezes every edge and guidance digest.

Active `internal/release/upgrade-impact.json` authoring is removed. Historical target-specific guidance remains read-only repository evidence, but release assembly stages only exact paths referenced by the canonical catalog.

## Implemented release contract

Every future prerelease and stable release must:

1. inherit the previous target catalog unchanged
2. author exactly one new `previous_release -> proposed_target` edge
3. assess only that managed delta
4. add only transition-local migrations and semantic guidance
5. retain supported entry points or record explicit retirement reasons
6. qualify older sources through deterministic adjacent path composition

The release PR validator compares inherited and proposed catalogs. It rejects zero or multiple new edges, skipped or non-adjacent edges, target shortcuts, cumulative guidance, inherited edge or guidance mutation, guidance artifact digest changes, silent retirement, and legacy `upgrade-impact.json` authoring.

The reviewed assembler derives installer-compatible source-to-target projections mechanically. Those projections are generated output and do not reintroduce cumulative authored state.

## Regression evidence

Required release policy and repository tests cover:

- zero new edges
- exactly one adjacent edge
- two new edges
- an adjacent edge plus a cumulative shortcut
- a skipped or wrong-source edge
- inherited edge and digest mutation
- inherited guidance metadata and artifact mutation
- copied cumulative guidance
- explicit and silent source retirement
- explicit no-impact edges
- three retained historical sources
- semantic lag with exact-once guidance
- prerelease and stable SemVer transitions

The release PR workflow and `internal/release/test.sh` both execute the strict catalog tests.

## Completion criteria

- [x] active historical history is normalized into canonical adjacent edges
- [x] cumulative repository-local preparation state is non-selectable archival evidence
- [x] immutable published release assets remain untouched
- [x] release instructions require exactly one new adjacent edge
- [x] legacy direct source-to-target data is read-only
- [x] release tooling inherits history and adds only the previous-to-target edge
- [x] validation compares inherited and proposed catalogs
- [x] zero, multiple, skipped, shortcut, and non-adjacent edges are rejected
- [x] cumulative guidance and assessments are rejected
- [x] inherited edge, guidance, digest, artifact, and migration identity is immutable
- [x] retained sources qualify through unique composition
- [x] source retirement requires the explicit retirement contract
- [x] no-impact edges carry an explicit false semantic decision
- [x] the alpha.12 failure mode has regression coverage
- [x] at least three historical sources pass through composition
- [x] semantic lag receives guidance exactly once
- [x] release PR and complete repository workflows require the tests
- [x] the rule is channel-neutral
- [x] release documentation, indexes, tooling, fixtures, and conceptual history are aligned
- [x] repository validation evidence is recorded

## Release qualification follow-up

The next immutable release must prove against its exact tagged revision that it inherited this catalog unchanged, authored only one new adjacent edge, added no cumulative target guidance, resolved at least three retained sources, and applied outstanding semantic guidance exactly once.
