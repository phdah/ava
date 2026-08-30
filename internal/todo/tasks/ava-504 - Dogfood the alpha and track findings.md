---
id: ava-504
title: Dogfood the alpha and track findings
status: Won't Fix
assignee: []
created_date: ''
updated_date: '2026-08-30 18:15'
labels:
  - internal
  - roadmap
  - phase-05
  - release
  - dogfood
dependencies: []
ordinal: 504
---

## Description

Exercise published prereleases through realistic Ava and OpenCode usage, record bounded findings, and continue until the user explicitly closes alpha dogfooding. This umbrella is intentionally parked and is not the current work queue.

## Operating contract

Only the user may mark this umbrella complete. Passing tests, an empty blocker list, completed qualification infrastructure, or another prerelease never imply closure.

Dogfooding covers fresh and mature installation, repeated OpenCode sessions, role/workflow routing, conversational transitions, context maintenance, inbox ingestion, independent review, damaged managed state, semantic reconciliation, finalization, rollback, uninstall, reinstall, and supported published upgrade transitions.

For every release-relevant finding:

1. record observed behavior and evidence
2. classify it as `blocker`, `required-v1`, or approved `post-v1`
3. create one bounded native Backlog.md task
4. preserve the release gate it blocks
5. resolve actionable work in dependency/priority order

Repository implementation completion and immutable-release qualification are separate. Code, tests, documentation, task state, and resolution evidence can complete a finding while published-asset verification remains a release gate.

## Release authoring boundary

When release progression is explicitly resumed, each prerelease continues to use Ava's adjacent-edge release catalog model: inherit reviewed history unchanged, add exactly one previous-to-target edge, assess only that edge, preserve reviewed semantic-impact rationale, add only transition-local guidance/migrations, retain or explicitly retire supported sources, and qualify older supported sources through composition.

## Closure gate

Before asking the user to close dogfooding when this path is resumed, verify that the corrective-alpha obligations are complete, no blocker remains, no `required-v1` finding remains pending, and every new release-relevant defect has a recorded disposition.

A clear user statement that dogfooding is complete or that Ava should proceed to the release candidate is sufficient. Do not infer closure.

## State at Backlog.md migration

Findings 01 through 30 except post-v1 Finding 25 are implementation-complete. Finding 30 completed as a no-op after its proposed detached-process solution was rejected as solving an unproven root cause. Findings 33 and 34 are also implementation-complete. Historical Findings 31/32 and earlier 34-36 proposals were removed by explicit user decision and are not resurrected as active tasks.

Finding 25 remains post-v1 and non-blocking as AVA-5625. There are no pending blocker or `required-v1` dogfood findings at migration.

The synthetic qualification system reached a 305-file finalized corpus with eight qualification families and a maintained 17-scenario runner. Subsequent work fixed semantic-path reporting, OpenCode large-JSON capture, hardcoded semantic-path qualification, inbox disposition/fidelity controls, and the seven-source representative inbox qualification variant. The last recorded release action before parking was to assemble a fresh corrective-alpha candidate, rerun the complete matrix, obtain fresh signoff, and then request explicit dogfood closure before RC work.

That release action is historical parked state, not the current implementation queue.

## Finding creation contract

A new dogfood defect that requires repository work should become one bounded native Backlog.md task with:

- observed user-visible behavior
- exact reproduction/evidence
- `blocker`, `required-v1`, or `post-v1` classification and affected release gate
- root cause, or `unknown` when investigation is part of the task
- bounded repository scope
- observable completion criteria and regression coverage
- resolution evidence when implemented
- separate release-qualification follow-up when immutable assets must still be exercised

Do not complete this umbrella from an individual finding PR.
