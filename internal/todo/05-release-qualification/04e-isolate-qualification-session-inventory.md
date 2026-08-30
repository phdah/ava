---
type: Internal Development Task
title: Isolate Qualification Session Inventory
description: Ensure each qualification run inventories only OpenCode sessions created for that exact run and cannot absorb historical qualification sessions.
tags: [internal, roadmap, release, qualification, opencode, sessions, evidence, reliability]
status: pending
phase: 5
parent: 04c-automate-release-qualification-evidence
order: 4.5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-30T14:00:00+02:00
---

# Isolate Qualification Session Inventory

## Purpose

Fix the session-inventory contamination observed during `v1.0.0-alpha.15` qualification, where sessions from an earlier qualification run were attributed to the current run and caused the independent audit to report a major evidence-integrity finding.

Historical OpenCode sessions must be allowed to remain on the host. Correct qualification must not depend on deleting or cleaning up old sessions first.

## Current failure mode

The qualification automation already snapshots OpenCode sessions before and after execution and computes newly created session IDs. However, session IDs recovered from runner command output can currently enter the relevant-session set without being constrained to the current run's newly created session boundary. A historical session referenced in output can therefore be incorrectly included and later bound to a current scenario.

## Approved direction

Make the exact qualification operation the authoritative inventory boundary:

- a top-level session may enter the inventory only when it was created after the run's before-snapshot and belongs to the current qualification execution
- nested sessions may enter only as descendants of sessions already proven to belong to the current run
- session IDs discovered from runner stdout, stderr, prompts, exports, or other evidence are hints for binding, not authority to cross the before/after boundary
- every inventoried session must resolve to the current execution root and one maintained scenario
- historical sessions must never become current-run evidence merely because their IDs or content appear in current command output
- do not require global OpenCode session deletion, pre-run cleanup, or destructive database maintenance

## Implementation considerations

Review `build_session_inventory()` and `runner_prompt_map()` in `internal/release/qualification_automation.py`. Preserve the useful before/after snapshot model, but make the relationship between `new_ids`, direct runner-discovered sessions, descendants, scenario binding, and execution-root membership explicit and testable.

Prefer a simple invariant over cleanup logic: the current run owns a closed set of newly created sessions, and all evidence capture is derived from that set.

## Regression coverage

Add a regression fixture that deliberately includes historical OpenCode sessions before qualification starts, including sessions that resemble qualification sessions or whose IDs appear in preserved command output. Verify that:

- none of those historical sessions appear in the new run inventory
- all current top-level scenario sessions are present
- all current nested child sessions are present
- every inventory entry binds to the correct current scenario
- repeated qualification runs can execute on the same host without cleanup and still produce disjoint inventories

## Completion criteria

- session inventory is exact-run isolated by construction
- historical OpenCode sessions cannot contaminate new qualification evidence
- nested current-run sessions remain fully captured
- no cleanup step is required before qualification
- regression tests prove consecutive runs produce independent inventories
- the independent audit receives only evidence belonging to the run it is evaluating
