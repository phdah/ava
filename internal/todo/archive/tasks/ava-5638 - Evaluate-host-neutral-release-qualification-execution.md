---
id: ava-5638
title: Evaluate host-neutral release qualification execution
status: Parked
assignee: []
created_date: '2026-09-01 20:20'
updated_date: '2026-09-03 20:39'
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

<!-- SECTION:DESCRIPTION:BEGIN -->
Evaluate and implement a release-qualification path that does not require OpenCode, ChatGPT Work, or another specific agent host as the mandatory runtime.

The release gate should protect deterministic release safety without coupling publication to one stochastic consumer-agent runtime or one ChatGPT mode. Agent-behavior simulations may remain useful QA, but normal release qualification should be executable regardless of whether the maintainer is operating from ordinary ChatGPT chat, Work, or another repository-capable session.

## Implemented direction

PR [#122](https://github.com/phdah/ava/pull/122) now implements the approved minimal release qualification:

- `qualify-release.sh pre-edge` runs an ephemeral deterministic fail-fast preflight before semantic review and edge authoring.
- The active maintainer session reviews the exact managed delta, records the semantic-impact decision and rationale, and authors the adjacent edge and any required transition-local guidance/migrations.
- `qualify-release.sh final` is the single authoritative qualification run after the edge exists.
- The final run repeats the pre-edge checks and adds authentic deterministic previous-to-target upgrade, resume, abort, and rollback checks.
- Only the final deterministic run is committed as qualification evidence and may enter `awaiting-user-signoff`.
- Mandatory deterministic qualification executes in GitHub Actions, so the active maintainer session does not need shell access or a particular ChatGPT execution mode.
- GitHub Actions returns generated evidence/acceptance state as exact artifacts; the active repository-connected session applies those artifact bytes to the release PR, ensuring the resulting commits trigger the normal PR workflow cycle.
- The normal repository Python/unit suite remains in GitHub Actions and is not duplicated by the maintainer session.
- No synthetic routing, calendar, clarification, inbox-ingestion, semantic-reconciliation/finalization, role-led uninstall, or independent LLM-audit turn is required by the normal release gate.
- Those scenarios remain optional behavioral QA for targeted changes, milestone testing, or future host evaluation.

This redesign followed the first real Work validation attempt for alpha.17. Fresh same-workspace agent execution worked, but the run consumed substantial Work credits and then produced a false negative when a correct clarification question did not contain one of the validator's expected lexical tokens. That demonstrated that general consumer-agent simulation was too expensive and brittle to be mandatory release evidence.

A subsequent simplification removed the remaining Work requirement entirely: because the mandatory gate is deterministic, GitHub Actions is now the canonical executor and the active chat only orchestrates repository changes, exact artifact handoff, and approval.

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

## Session-neutral release flow

The maintained flow must not require the user to switch ChatGPT modes.

From whichever repository-capable maintainer session is active:

1. resolve the release PR and exact previous release
2. configure the exact qualification pair
3. let the release-qualification GitHub Actions workflow run the deterministic pre-edge checks automatically
4. perform the maintainer semantic-impact assessment and author the adjacent edge after pre-edge is green
5. let GitHub Actions run the authoritative deterministic final qualification and upload the exact evidence state transition as an artifact
6. download and apply that evidence artifact exactly to the release PR through the connected GitHub capability
7. inspect the committed final evidence and required checks
8. stop for explicit user approval
9. after approval, either run the acceptance helper directly when shell access exists or create the transient `internal/release/qualification/acceptance-request.json` through the connected GitHub capability
10. let GitHub Actions validate the request and upload the accepted-state transition as an artifact
11. download and apply that acceptance artifact exactly, including removal of the transient request
12. merge only after Release PR policy and all required checks pass

A normal ChatGPT chat with repository read/write access should therefore be sufficient. ChatGPT Work remains usable but is not privileged or required.

## Live validation gate

The implementation remains **Parked**, not `Done`, until the simplified session-neutral flow is exercised against the alpha.17 release context.

A successful proof should show that an ordinary repository-connected ChatGPT session can drive the release workflow without switching to Work and without using OpenCode or user-hosted compute for mandatory qualification.

The proof should reach at least `awaiting-user-signoff` with deterministic qualification evidence created by GitHub Actions and applied from its exact artifact. If the user chooses to complete the real release, the same session should also be able to record the explicit acceptance request, apply the validated acceptance artifact, merge, and verify publication.

After one complete session-neutral alpha.17 proof succeeds under those conditions, move AVA-5638 to `Done` and record the release/run as completion evidence.

## Future generic behavioral execution follow-up

The normal release gate is now host-neutral because it no longer needs an agent runtime at all. Optional behavioral QA is a separate concern.

A future task may expose one generic behavioral protocol with interchangeable adapters. ChatGPT Work could be one adapter; OpenCode or another capable runtime could be reintroduced without changing the deterministic release gate.

PR [#122](https://github.com/phdah/ava/pull/122) is the primary recovery reference because its history contains the OpenCode-specific pieces that were removed and the successive Work-specific designs that were later simplified away.

Do not restore OpenCode merely for normal release qualification. If an OpenCode behavioral adapter is later reintroduced, AVA-5637 should apply only to those optional OpenCode-owned sessions and should hard-disable MCPs there.

## Completion criteria

- normal release qualification requires neither OpenCode nor ChatGPT Work nor delegated consumer-agent turns
- deterministic pre-edge and final checks cover the maintained release-safety invariants
- the adjacent edge and semantic-impact rationale are still reviewed before final qualification
- only one authoritative final qualification run is required for acceptance
- final evidence remains bound to the exact source, target, repository revision, and deterministic executor provenance
- GitHub Actions and explicit user acceptance remain mandatory
- qualification/acceptance artifacts can be applied exactly from an ordinary repository-connected ChatGPT session
- an ordinary repository-connected ChatGPT session can drive the simplified flow end-to-end in the alpha.17 proof
- optional behavioral QA is clearly separated from release acceptance
- future generic host-adapter work has an explicit recovery reference to PR #122
<!-- SECTION:DESCRIPTION:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Re-evaluated 2026-09-03: closing as superseded rather than proceeding with the ChatGPT-specific live-validation gate. The substantive goal is achieved and verified: release qualification runs deterministically in GitHub Actions (qualification_host: github-actions on the alpha16->17 run), pre-edge + final checks both ran, the adjacent edge/semantic review was authored (PR #122), exactly one final run was produced, and acceptance was recorded and PR #121 merged. What is NOT satisfied is the narrow 'ordinary repository-connected ChatGPT session (not OpenCode/Work) drives the flow end-to-end' proof this task specifically asked for -- but that proof is now moot: the team no longer uses ChatGPT Work sessions at all, so validating plain-ChatGPT-chat portability serves no practical purpose. Archiving rather than marking Done, since the specific completion criterion as written was never literally exercised, but the underlying architecture it was chasing (host-neutral, GH-Actions-driven qualification) is real and in place. Unrelated finding surfaced during this review, tracked separately: v1.0.0-alpha.17 is stuck as a GitHub Draft release with zero uploaded assets (unlike alpha.16, which published normally with all assets); the release-please publish steps (assemble/attest/upload/publish) show as skipped on the runs right after the PR #121 merge. Needs investigation independent of this task.
<!-- SECTION:NOTES:END -->
