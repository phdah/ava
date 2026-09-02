---
id: ava-5638
title: Evaluate host-neutral release qualification execution
status: Parked
assignee: []
created_date: '2026-09-01 20:20'
labels:
  - internal
  - roadmap
  - release
  - qualification
  - portability
  - host-neutral
milestone: m-0
dependencies: []
references:
  - ava-5636
  - ava-5637
type: enhancement
ordinal: 6636
---

## Description

Evaluate and implement a release-qualification path that does not require OpenCode as the mandatory runtime and can be executed from ChatGPT Work Cloud.

The release gate should protect deterministic release safety without coupling publication to one stochastic consumer-agent runtime. Agent-behavior simulations may remain useful QA, but they should only be mandatory when they provide release-safety evidence that cannot be checked mechanically.

## Implemented direction

PR [#122](https://github.com/phdah/ava/pull/122) now implements the approved minimal release qualification:

- `qualify-release.sh pre-edge` runs an ephemeral deterministic fail-fast preflight before semantic review and edge authoring.
- The release-maintainer Work session reviews the exact managed delta, records the semantic-impact decision and rationale, and authors the adjacent edge and any required transition-local guidance/migrations.
- `qualify-release.sh final` is the single authoritative qualification run after the edge exists.
- The final run repeats the pre-edge checks and adds authentic deterministic previous-to-target upgrade, resume, abort, and rollback checks.
- Only the final deterministic run is committed as qualification evidence and may enter `awaiting-user-signoff`.
- GitHub Actions owns the normal repository Python/unit suite; Work does not duplicate it merely for qualification.
- No synthetic routing, calendar, clarification, inbox-ingestion, semantic-reconciliation/finalization, role-led uninstall, or independent LLM-audit turn is required by the normal release gate.
- Those scenarios remain optional behavioral QA for targeted changes, milestone testing, or future host evaluation.

This redesign followed the first real Work validation attempt for alpha.17. Fresh same-workspace agent execution worked, but the run consumed substantial Work credits and then produced a false negative when a correct clarification question did not contain one of the validator's expected lexical tokens. That demonstrated that general consumer-agent simulation was too expensive and brittle to be mandatory release evidence.

## Deterministic release-safety checks

The normal release path must retain at least:

- exact immutable previous-release asset verification
- exact local target/repository revision binding
- candidate assembly and checksum validation
- fresh empty installation
- mature-project installation with project-owned byte preservation
- rejection of modified managed content
- rejection of missing managed content
- rejection of corrupt upgrade state
- rejection of unexpected managed content
- exactly one authentic previous-to-target edge in the final candidate
- deterministic previous-to-target upgrade preserving project-owned bytes
- interrupted upgrade resume
- interrupted upgrade abort
- rollback to the previous release
- synthetic corpus and external test-boundary integrity
- required GitHub Actions checks
- explicit user acceptance before merge
- post-merge immutable release verification

## Live validation gate

The implementation remains **Parked**, not `Done`, until the simplified flow is exercised from ChatGPT Work Cloud.

The intended proof target remains the alpha.17 release context. A successful proof should show that a Work session can:

1. resolve the release PR and exact previous release
2. run the deterministic pre-edge preflight without delegated qualification agents
3. perform the maintainer semantic-impact assessment and author the adjacent edge
4. run the authoritative deterministic final qualification on the exact reviewed revision
5. verify the required GitHub Actions results
6. reach `awaiting-user-signoff`
7. stop for explicit user approval before acceptance/merge when operating as a validation exercise, or complete acceptance/merge/publication when the user explicitly authorizes the real release

No OpenCode, Work Local, Codex Local, developer shell, or user-hosted qualification fallback may be silently introduced to make this Work proof pass.

After one complete Work proof succeeds under those conditions, move AVA-5638 to `Done` and record the release/run as completion evidence.

## Future generic execution follow-up

The current implementation intentionally proves ChatGPT Work first. It should not be interpreted as a permanent requirement that optional behavioral qualification be tied to Work.

After the deterministic Work release path is proven, reconsider whether optional behavioral QA should expose one generic host protocol with interchangeable adapters. ChatGPT Work could be one adapter; OpenCode or another capable runtime could be reintroduced without changing the deterministic release gate.

PR [#122](https://github.com/phdah/ava/pull/122) is the primary recovery reference because its history contains the OpenCode-specific pieces that were removed and the successive Work designs that replaced them.

Do not restore OpenCode merely for normal release qualification. If an OpenCode behavioral adapter is later reintroduced, AVA-5637 should apply only to those optional OpenCode-owned sessions and should hard-disable MCPs there.

## Completion criteria

- normal release qualification does not require OpenCode or delegated consumer-agent turns
- deterministic pre-edge and final checks cover the maintained release-safety invariants
- the adjacent edge and semantic-impact rationale are still reviewed before final qualification
- only one authoritative final qualification run is required for acceptance
- final evidence remains bound to the exact source, target, and repository revision
- GitHub Actions and explicit user acceptance remain mandatory
- ChatGPT Work can execute the simplified non-CI flow end-to-end in a live proof
- optional behavioral QA is clearly separated from release acceptance
- future generic host-adapter work has an explicit recovery reference to PR #122
