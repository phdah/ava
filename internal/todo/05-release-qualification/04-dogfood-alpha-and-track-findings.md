---
type: Internal Development Task
title: Dogfood the Alpha and Track Findings
description: Exercise published prereleases through real Ava and OpenCode usage, manage findings durably, and continue until the user explicitly closes dogfooding.
tags: [internal, roadmap, alpha, dogfooding, defects, opencode]
status: pending
phase: 5
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-14T11:40:00+02:00
---

# Dogfood the Alpha and Track Findings

## Purpose and authority

The alpha exists to expose failures not found by fixtures or design review. Findings are managed through the [Alpha Dogfood Findings](dogfood/) backlog.

Only the user may mark this umbrella task complete. A passing suite, empty backlog, or another prerelease does not complete dogfooding automatically.

Use the [V1 Release Operator Path](v1-release-operator-path.md) for the canonical ordering between remaining dogfood qualification, explicit closure, release-candidate publication, and stable qualification.

## Required scenario coverage

Dogfooding covers installation into empty and mature projects, repeated OpenCode sessions, role and workflow routing, conversational follow-ups and routing transitions, context maintenance, inbox ingestion, independent review, damaged-state diagnosis, transaction recovery, semantic upgrades, uninstall, reinstall, and every supported published transition.

The synthetic qualification vault supplies a reproducible baseline, but realistic projects remain required.

## Backlog operation

For each finding:

1. record behavior and evidence
2. classify it as `blocker`, `required-v1`, or approved `post-v1`
3. create one bounded task
4. add it to the findings index
5. resolve the first actionable item in dependency order

Implementation completion and immutable-release qualification are separate. Repository code, tests, documentation, indexes, and resolution evidence complete a finding. Published-asset checks remain release gates.

## Release authoring during dogfooding

Every new prerelease uses the canonical adjacent catalog:

1. inherit all previous edges and guidance unchanged
2. author exactly one previous-to-target edge
3. assess only that edge
4. apply the project-owned semantic-impact assessment and preserve reviewed rationale for `semantic_review_required`
5. add only transition-local guidance and migrations
6. retain or explicitly retire supported sources
7. qualify older sources through composition

`upgrade-impact.json` and cumulative target-specific guidance are historical compatibility evidence, not active authoring inputs.

## Closure gate

Dogfooding stays open while the synthetic qualification vault and corrective-alpha qualification are completed. The user does not need to close this task before those two supporting tasks run.

Ask for explicit user closure after the corrective alpha has passed its published-asset qualification and before release-candidate publication begins. Before asking, verify:

- the corrective-alpha task is complete
- there are no pending blockers
- there are no pending `required-v1` findings
- every newly discovered release-relevant defect has a recorded disposition

A clear user statement that dogfooding is complete or that Ava should proceed to the release candidate is sufficient. Record that decision by marking this umbrella complete and synchronizing the Phase 5 indexes. Do not infer closure from an empty backlog or passing qualification.

## Current state

Findings 01 through 17 are implementation-complete. Finding 18 requires deterministic verification before relevant relative calendar language is persisted as an absolute fact. This umbrella remains active until the user explicitly closes dogfooding.

The synthetic corpus and all five specified images are finalized and verified in a repository-external local directory. The user materialized all eight qualification families and exercised ingestion, routing, managed-content damage, semantic reconciliation, finalization, rollback, uninstall, and reinstall behavior.

Finding 17 now provides deterministic repository-only checkpoints that execute the exact assembled target installer transaction machinery and stop at authentic abortable and resumable boundaries. The remaining interrupted-upgrade work is qualification execution: run the maintained checkpoint commands against the selected assets, exercise the real `--abort` and `--resume` operations, and record their terminal evidence and user signoff.

Finding 13 was exposed while completing the `1.0.0-alpha.14` release PR. The implemented release procedure now separates managed delta, possible project-owned incompatibility, and required reconciliation and requires reviewed rationale for both semantic-review outcomes.

Finding 14 repaired Inbox Ingester project-root inbox references and added assembled-payload regression coverage. Finding 15 made Ava Maintenance the successful terminal finalization mechanism after proving protocol preconditions. Finding 16 bounded ingestion-time scoped-history authority to additive-only changes while preserving prior history.

Finding 10 established that pull-request change types are selected from supported distribution impact rather than implementation novelty or source location. Repository-only qualification work remains non-releasable when it does not change produced assets or supported behavior, while internal release tooling remains releasable when its output or guarantees change.

Finding 12 refined finding 07's unconditional no-bypass guarantee into conversation-aware routing while preserving the managed-state gate and fresh-routing transition rules.

Finding 18 currently preempts completion of synthetic-vault qualification. Complete the calendar-verification work, repeat its affected scenario, execute resume and abort with finding 17's maintained harness, finish the synthetic-vault signoff gate, and continue to corrective immutable alpha qualification. New `blocker` or `required-v1` findings may still preempt that sequence. After those supporting tasks pass, the next action is the explicit user-owned closure gate before RC publication.
