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
  at: 2026-08-10T15:58:00+02:00
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

Findings 01 through 15 are complete. There are currently no pending dogfood findings, but this umbrella remains active until the user explicitly closes dogfooding.

Finding 13 was exposed while completing the `1.0.0-alpha.14` release PR. The initial release-edge assessment incorrectly treated the absence of deterministic project-owned edits as evidence that semantic review was unnecessary. The implemented release procedure now separates managed delta, possible project-owned incompatibility, and required reconciliation. It requires reviewed rationale for both `true` and `false`, bounded guidance when review is required, and leaves the semantic decision with the maintainer rather than deterministic validation.

Finding 14 was exposed during realistic Inbox Ingester use. The managed role encoded project-root `./inbox/` and `./inbox/index.md` references as Markdown links from its nested role directory, and the host resolved them beneath `/.ava/base/roles/inbox-ingester/`. The implemented fix now names those project-owned paths explicitly as project-root paths in prose and adds assembled-payload regression coverage so required reading cannot silently return to the broken role-relative link shape.

Finding 15 was exposed during a realistic alpha.13 to alpha.14 upgrade in a dogfood project. After semantic reconciliation completed, Ava Maintenance could not finalize the journal because the instructions deferred finalization to an installer or updater binary that does not exist. The implemented fix makes Ava Maintenance itself the successful finalization mechanism: it validates the terminal preconditions, atomically writes only the protocol-defined terminal journal state, removes only the exact recorded transaction workspace, and verifies normal routing without broadening resume, abort, rollback, repair, or other state-mutation authority.

Finding 10 established that pull-request change types are selected from supported distribution impact rather than implementation novelty or source location. Repository-only qualification work remains non-releasable when it does not change produced assets or supported behavior, while internal release tooling remains releasable when its output or guarantees change.

Finding 12 refined finding 07's unconditional no-bypass guarantee into conversation-aware routing. Every request still performs the managed-state gate, but a pure clarification may be roleless and a same-objective scoped follow-up may retain the already-active role without repeated registry traversal or unchanged required-reading reload. New tasks, explicit workflows or roles, changed authority or domain, scoped work after roleless handling, uncertain role fit, and managed-state overrides force fresh routing.

The synthetic vault and corrective immutable alpha qualification are the next pending supporting work. New `blocker` or `required-v1` findings may still preempt that sequence. After those two supporting tasks pass, the next action is the explicit user-owned closure gate before RC publication.
