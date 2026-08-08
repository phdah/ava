---
type: Internal Development Task
title: Compose semantic upgrades from adjacent release edges
description: Replace duplicated source-to-target semantic guidance with deterministic composition of reviewed adjacent release edges.
tags: [internal, roadmap, dogfood, releases, upgrades, semantics]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 9
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.11
generated:
  by: agent:openai-chatgpt
  at: 2026-08-08T23:58:55+02:00
---

# Compose semantic upgrades from adjacent release edges

## Observed behavior

Completing the `1.0.0-alpha.11` release required the target release to restate complete source-to-target upgrade assessments for every supported prerelease. Earlier semantic obligations from alpha.10 were copied into new alpha.5-to-alpha.11 through alpha.9-to-alpha.11 edges even though the only new alpha.10-to-alpha.11 managed change was the root router and required no project-owned semantic work.

This makes each release responsible for recreating cumulative upgrade guidance from every supported source. The authoring and review cost grows with the number of releases, and duplicated obligations can drift or be omitted.

## Reproduction and evidence

Review release PR [#68](https://github.com/phdah/ava/pull/68) and compare:

- `internal/release/upgrade-impact.json` for `1.0.0-alpha.10`
- `internal/release/upgrade-impact.json` for `1.0.0-alpha.11`
- target-specific guidance directories under `internal/release/guidance/`

The alpha.11 impact file repeats cumulative semantic evidence and requires new target-specific guidance for older sources. The alpha.10-to-alpha.11 edge correctly has no guidance, but prior alpha.9-to-alpha.10 obligations are represented again as alpha.9-to-alpha.11 guidance rather than composed from immutable adjacent edges.

The public guidance contract already describes ordered multi-version composition and explicit supersession, while the release process still materializes complete direct source-to-target guidance for every target.

## Classification

This is `required-v1` and blocks the release candidate.

The current implementation is safe because every direct edge is reviewed and validated. It does not need to block the next corrective alpha. However, carrying the quadratic authoring model into stable support would make long-lived upgrade maintenance unnecessarily expensive and increase the probability of inconsistent or incomplete semantic obligations.

## Root cause

The release model treats each target release as the sole owner of a complete set of direct source-to-target edges. Release qualification derives cumulative managed deltas, semantic evidence, and target-specific guidance for every supported source instead of inheriting a previously reviewed immutable edge graph and appending only newly introduced adjacent edges.

## Scope

Design and implement a deterministic adjacent-edge upgrade model, subject to explicit approval of the resulting public contract change.

The intended direction is:

- each release authors and reviews only newly introduced adjacent edge definitions and guidance
- the target release remains self-contained by carrying forward the immutable reviewed edge catalog and referenced guidance needed for its supported source range
- the updater resolves a deterministic managed upgrade path from installed `ava_version` to the target
- semantic work is resolved separately from `semantic_compatibility.compatible_through` to the target
- guidance obligations are loaded in exact edge order and remain cumulative unless a later edge explicitly supersedes an earlier guidance ID
- unsupported gaps, cycles, altered inherited edges, ambiguous paths, or unprovable composition block preflight
- release qualification proves inherited edge identity and completeness without requiring release authors to rewrite cumulative source-to-target prose

Do not implement runtime inference from changelogs, arbitrary historical prose, repository history, or network access to mutable releases.

## Completion criteria

- public release, versioning, upgrade, and guidance contracts define adjacent-edge inheritance and deterministic path resolution consistently
- release schemas represent inherited immutable edges, newly authored edges, ordered semantic guidance, supersession, and supported-source retention without target-specific duplication
- release assembly produces a self-contained target release with every edge and guidance document required for its supported source range
- release PR validation reviews only new or explicitly retired edges while proving inherited edge definitions and checksums are unchanged
- the updater resolves managed and semantic paths separately, including when `ava_version` is ahead of `compatible_through`
- cumulative guidance is loaded exactly once per traversed edge in deterministic order
- no-guidance adjacent edges advance semantic compatibility mechanically only when all earlier obligations are already complete
- pending, partial, and blocked semantic state may be carried only when every traversed edge permits it and the composed path covers the last completed compatibility version
- gaps, cycles, conflicting supersession, missing guidance, altered inherited edges, and non-composable paths fail before managed mutation
- fixtures cover direct adjacent upgrades, multi-edge upgrades, semantically lagging projects, no-op semantic edges, explicit supersession, unsupported gaps, rollback, and resume
- release tooling, installer behavior, validators, tests, documentation, indexes, and conceptual logs remain aligned
- the user explicitly approves the final public contract before implementation records it as accepted
- concrete resolution and repository-validation evidence are added to this task in the resolving PR

## Resolution evidence

Pending.

## Release qualification follow-up

Publish and validate a release whose supported path spans at least three adjacent edges. Verify both:

1. a project fully compatible with its installed source traverses only newly applicable semantic edges
2. a project whose installed base is newer than `compatible_through` receives every outstanding semantic obligation exactly once before compatibility advances

Confirm that the release contains no separately authored cumulative source-to-target guidance documents for paths that can be proven by adjacent-edge composition.
