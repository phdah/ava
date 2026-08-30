---
id: ava-543
title: "Automate release qualification and evidence state"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "release", "qualification", "required-v1"]
ordinal: 543
---

## Description

Implement mandatory hands-off release qualification, independent audit, explicit user acceptance, and release-PR merge gating. This native Backlog.md task contains the complete pre-Backlog task record.

## Migrated task record

---
type: Internal Development Task
title: Automate Release Qualification and Evidence State
description: Implement mandatory hands-off release qualification, independent audit, explicit user acceptance, and release-PR merge gating.
tags: [internal, roadmap, release, qualification, automation, evidence, opencode]
status: complete
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 4.3
classification: required-v1
blocks: next-qualification-run
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T15:39:53+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-17T12:26:00+02:00
---

# Automate Release Qualification and Evidence State

## Purpose

Make full model-backed release qualification a mandatory pre-merge gate for every Ava release while keeping execution repository-only and non-interactive.

## Approved behavior

- `qualify-release.sh` qualifies the exact previous published release against exact locally assembled target assets from the release PR revision.
- The maintained 17-scenario matrix, complete top-level/nested OpenCode session inventory, and fresh independent audit run automatically.
- Mechanical or evidence failures produce `failed`; blocker/major audit findings produce `needs-review`; a clean result produces `awaiting-user-signoff`.
- Automation never accepts its own result.
- Explicit user approval is recorded through `accept-release-qualification.sh` as `basis: qualified-run`.
- Release PR policy blocks merge until the exact target has accepted qualification.
- Acceptance is bound to the qualified repository revision and local target asset identity. Any non-qualification content change after that revision requires requalification.
- Historical releases `v1.0.0-alpha.1` through `v1.0.0-alpha.14` are accepted with `basis: historical-backfill`, without claiming modern qualification evidence.
- Raw assets, workspaces, command output, and transcripts remain outside Git. Compact evidence and acceptance state live under `internal/release/qualification/`.
- The fixture oracle is evaluator-only and must not be exposed to qualification agents.
- No qualification or acceptance operation creates a Git commit or dogfood finding automatically.

## Implementation

The completed implementation is centered on:

- `internal/release/qualify-release.sh`
- `internal/release/qualification_automation.py`
- `internal/release/qualification-opencode.sh`
- `internal/release/qualification/audit-prompt.md`
- `internal/release/accept-release-qualification.sh`
- `internal/release/qualification_acceptance.py`
- `internal/release/qualification/current-state.json`
- `.github/workflows/release-pr-policy.yml`
- qualification and acceptance regression tests under `internal/release/tests/`

## Release sequence

For every new release:

1. prepare the release-please PR, semantic-impact decision, adjacent edge, and all intended release content
2. run deterministic validation/tests
3. assemble exact local target assets from a clean release PR revision
4. run `qualify-release.sh`
5. correct and rerun any `failed` or `needs-review` result
6. present `awaiting-user-signoff` evidence to the user
7. after explicit approval, record acceptance with `accept-release-qualification.sh`
8. commit only the qualification-state/evidence changes
9. require the Release PR policy check to pass
10. merge and publish

## Completion

Implementation is complete when the repository tests confirm execution identity, session coverage, audit severity, explicit signoff, historical backfill, release-PR gating, and post-qualification invalidation behavior.

Release-specific qualification now occurs inside each release PR before merge; it is no longer a separate optional or post-publication gate.
