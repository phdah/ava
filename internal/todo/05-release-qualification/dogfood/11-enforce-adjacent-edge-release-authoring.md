---
type: Internal Development Task
title: Normalize and enforce adjacent-edge release authoring
description: Store one immutable previous-to-target edge per release and recursively compose the records required for an upgrade.
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
  at: 2026-08-09T17:50:00+02:00
---

# Normalize and Enforce Adjacent-Edge Release Authoring

## Resolution

The active repository now stores upgrade history as an immutable linked ledger. Each target release file owns exactly one edge from the immediately previous release:

1. `1.0.0-alpha.6.json` owns `1.0.0-alpha.5 -> 1.0.0-alpha.6`
2. `1.0.0-alpha.7.json` owns `1.0.0-alpha.6 -> 1.0.0-alpha.7`
3. `1.0.0-alpha.8.json` owns `1.0.0-alpha.7 -> 1.0.0-alpha.8`
4. `1.0.0-alpha.9.json` owns `1.0.0-alpha.8 -> 1.0.0-alpha.9`
5. `1.0.0-alpha.10.json` owns `1.0.0-alpha.9 -> 1.0.0-alpha.10`
6. `1.0.0-alpha.11.json` owns `1.0.0-alpha.10 -> 1.0.0-alpha.11`
7. `1.0.0-alpha.12.json` owns `1.0.0-alpha.11 -> 1.0.0-alpha.12`

The alpha.9 to alpha.10 record owns the existing knowledge-hierarchy and inbox-fidelity guidance. Later records explicitly declare no new project-owned semantic impact. No target file repeats historical edges or guidance.

Active `internal/release/upgrade-impact.json` authoring is removed. Historical target-specific guidance remains read-only repository evidence, and release assembly stages only paths referenced by their owning edge records.

## Implemented release contract

Every future prerelease and stable release must:

1. leave all existing release records unchanged
2. create only `internal/release/catalogs/<target>.json`
3. author exactly one `previous_release -> target` edge
4. assess only that managed delta
5. add only transition-local migrations, semantic guidance, and retirement decisions
6. resolve older sources by recursively loading every release record between source and target

The release PR validator rejects a missing target record, a skipped or wrong predecessor, cumulative guidance, invalid retirement decisions, guidance artifact digest changes, historical catalog-file changes, and legacy `upgrade-impact.json` authoring.

The reviewed assembler composes the selected release records in memory and derives installer-compatible source-to-target projections mechanically. Those projections are generated output and do not reintroduce cumulative authored state.

## Regression evidence

Required release policy and repository tests cover:

- one edge per release file
- recursive chain composition
- a missing intermediate record
- a skipped or wrong predecessor
- transition-local guidance only
- guidance artifact digest mutation
- explicit, unknown, and invalid source retirement
- explicit no-impact edges
- three retained historical sources
- semantic lag with exact-once guidance
- prerelease and stable SemVer transitions

The release PR workflow and `internal/release/test.sh` both execute the strict record and chain tests.

## Completion criteria

- [x] active historical history is normalized into one immutable record per adjacent edge
- [x] no release file contains a cumulative graph snapshot
- [x] cumulative repository-local preparation state is non-selectable archival evidence
- [x] immutable published release assets remain untouched
- [x] release instructions require exactly one new target record
- [x] legacy direct source-to-target data is read-only
- [x] release tooling adds only the previous-to-target record
- [x] validation recursively composes the records between source and target
- [x] missing, skipped, cyclic, or non-adjacent chains are rejected
- [x] cumulative guidance and assessments are rejected
- [x] historical edge, guidance, digest, artifact, and migration identity is immutable
- [x] retained sources qualify through unique recursive composition
- [x] source retirement is stored with the release that makes the decision
- [x] no-impact edges carry an explicit false semantic decision
- [x] the alpha.12 failure mode has regression coverage
- [x] at least three historical sources pass through composition
- [x] semantic lag receives guidance exactly once
- [x] release PR and complete repository workflows require the tests
- [x] the rule is channel-neutral
- [x] release documentation, indexes, tooling, fixtures, and conceptual history are aligned
- [x] repository validation evidence is recorded

## Release qualification follow-up

The next immutable release must prove against its exact tagged revision that every older record remained unchanged, only the target record was added, at least three retained sources resolve recursively, and outstanding semantic guidance is applied exactly once.
