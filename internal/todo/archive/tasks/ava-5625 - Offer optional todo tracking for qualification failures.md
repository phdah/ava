---
id: ava-5625
title: Offer optional todo tracking for qualification failures
status: Parked
assignee: []
created_date: ''
updated_date: '2026-09-03 13:19'
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

<!-- SECTION:DESCRIPTION:BEGIN -->
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
<!-- SECTION:DESCRIPTION:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
The release procedure now requires a `failed` or `needs-review` result to be reported with its individual findings before the operator asks whether those findings should be recorded as bounded Backlog.md tasks on `main`. No tasks may be created without explicit user agreement, and task creation is explicitly non-progressing release bookkeeping.

The hands-off qualification procedure now separates automated qualification from conversational operator behavior. `qualify-release.sh` remains non-mutating and does not create Backlog.md tasks or infer consent. Any user-directed correction remains ordinary repository work followed by a new candidate, a fresh complete qualification run, and fresh user acceptance.

The implementation criteria are complete. The task is parked until a real future qualification produces `failed` or `needs-review`, at which point the documented ask-then-record behavior can be exercised and this task can be moved directly to `Done` with that run as completion evidence.

Re-evaluated 2026-09-03: completion criteria not met. (1) The ask-then-record wording added to internal/release/procedure.md by PR #117 (99c158d) was silently dropped by the later #122 rewrite (2988d6b, 'decouple qualification from agent host'); current procedure.md failure-handling section no longer documents the ask-then-record behavior or its constraints. (2) No real qualification run since parking has returned failed/needs-review (all of alpha14->15-corrective, alpha15->16, alpha16->17 are awaiting-user-signoff), so the behavior has never been exercised. Separately, the release process is now being simplified/shrunk (e.g. semantic review is being removed per ongoing release-process-cleanup work), so this task's premise is stale. Closing (archiving) rather than completing; owner will evaluate ask-then-record behavior manually going forward and open a fresh, right-sized task if a real failure shows it's still needed.
<!-- SECTION:NOTES:END -->
