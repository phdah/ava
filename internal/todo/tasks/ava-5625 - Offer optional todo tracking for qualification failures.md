---
id: ava-5625
title: Offer optional todo tracking for qualification failures
status: In Progress
assignee: []
created_date: ''
updated_date: '2026-09-01 18:29'
labels:
  - internal
  - roadmap
  - phase-05
  - release
  - post-v1
  - process
milestone: m-0
dependencies: []
ordinal: 350.5
---

## Description

When release qualification reports `failed` or `needs-review`, optionally offer to record the individual findings as bounded Backlog.md tasks on `main`. This is accepted process convenience and is tracked toward the `v1.0.0` milestone as next-up roadmap work.

## Origin

Qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local` failed and Findings 22, 23, and 24 were subsequently created manually on request. The release procedure did not define an explicit ask-then-record step.

## Required behavior

After a future qualification failure:

1. report the qualification result and findings
2. ask the user whether those findings should be recorded as tasks
3. only after an explicit yes, create bounded native Backlog.md tasks on `main`
4. if the answer is no or absent, create nothing

## Hard constraints

- task creation never accepts qualification, satisfies a merge gate, or otherwise advances the release
- explicit user direction is required for each applicable failed qualification
- resulting tasks belong on `main`, not the release branch under qualification
- recording tasks never replaces the requirement for a corrected candidate and a completely fresh qualification run
- active release instructions must not silently self-correct repository/release content after qualification failure without user direction

## Completion criteria

- the release procedure documents the ask-then-record behavior and constraints
- release operator/qualification summaries use explicit user direction rather than automatic self-correction after failure
- the behavior is exercised in an actual future qualification failure

This remains non-blocking post-v1 work.

## Implementation notes

The release procedure now requires a `failed` or `needs-review` result to be reported with its individual findings before the operator asks whether those findings should be recorded as bounded Backlog.md tasks on `main`. No tasks may be created without explicit user agreement, and task creation is explicitly non-progressing release bookkeeping.

The hands-off qualification procedure now separates automated qualification from conversational operator behavior. `qualify-release.sh` remains non-mutating and does not create Backlog.md tasks or infer consent. Any user-directed correction remains ordinary repository work followed by a new candidate, a fresh complete qualification run, and fresh user acceptance.

The implementation criteria are complete. The final operational criterion intentionally remains pending until a real future qualification produces `failed` or `needs-review`, at which point the documented ask-then-record behavior can be exercised and this task can be moved to `Done` with that run as completion evidence.
