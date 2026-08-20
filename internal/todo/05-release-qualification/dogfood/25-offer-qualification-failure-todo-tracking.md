---
type: Internal Development Task
title: Offer Optional Todo Tracking for Qualification Failures
description: When release qualification reports a failed or needs-review result, ask whether its findings should be recorded as todos on main, and record them there only on explicit yes.
tags: [internal, roadmap, dogfood, release, process]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 25
classification: post-v1
blocks: none
affected_version: n/a
generated:
  by: agent:openai-opencode
  at: 2026-08-20T00:00:00Z
---

# Offer Optional Todo Tracking for Qualification Failures

## Observed behavior

Qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local` failed. Findings 22, 23, and 24 above were created manually, on request, on `main`. There is currently no defined step in `internal/release/procedure.md` for offering to do this automatically.

## Classification

This is `post-v1`: a process convenience, not a release-blocking defect. It does not block the next prerelease or the release candidate.

## Scope

Add a small, explicit step to `internal/release/procedure.md`'s failure-handling section:

1. After reporting a `failed` or `needs-review` qualification result, ask the user whether its individual findings should be recorded as todos.
2. If the user answers yes, create the bounded dogfood-finding-style todo entries on `main` (never on the release branch) as ordinary repository work, following the existing finding template and backlog index conventions.
3. If the user answers no, or does not respond, do not create any todo entries.

## Hard constraints (must not be weakened by the implementation)

- This step must never mark a qualification run accepted, satisfy the merge gate, or otherwise unblock the release PR. Creating a todo is a repository record only.
- This step must require an explicit answer for each qualification failure it applies to. It must not be pre-authorized, defaulted to yes, or triggered without the user being asked.
- Todo entries created this way must be committed to `main`, not to the release branch under qualification.
- This step must not replace or shortcut the existing requirement that a fixed defect requires a new candidate and a full fresh qualification run.

## Completion criteria

- `internal/release/procedure.md` documents the ask-then-record step with the constraints above
- the step is exercised at least once in an actual release qualification failure and confirmed to behave as described

## Resolution evidence

_Complete in the resolving implementation PR._
