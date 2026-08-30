---
id: ava-5625
title: "Offer optional todo tracking for qualification failures"
status: "Parked"
labels: ["internal", "roadmap", "phase-05", "release", "post-v1", "process"]
ordinal: 5625
---

## Description

When release qualification reports `failed` or `needs-review`, optionally offer to record the individual findings as bounded Backlog.md tasks on `main`. This is accepted post-v1 process convenience only and is intentionally parked with release progression.

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