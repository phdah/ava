---
type: Internal Development Task
title: Isolate Qualification Session Inventory
description: Ensure each qualification run inventories only OpenCode sessions created for that exact run and cannot absorb historical qualification sessions.
tags: [internal, roadmap, release, qualification, opencode, sessions, evidence, reliability]
status: complete
phase: 5
parent: 04c-automate-release-qualification-evidence
order: 4.5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-30T14:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-30T16:00:00+02:00
---

# Isolate Qualification Session Inventory

## Purpose

Fix the session-inventory contamination observed during `v1.0.0-alpha.15` qualification, where sessions from an earlier qualification run were attributed to the current run and caused the independent audit to report a major evidence-integrity finding.

Historical OpenCode sessions must be allowed to remain on the host. Correct qualification must not depend on deleting or cleaning up old sessions first.

## Current failure mode

The qualification automation already snapshots OpenCode sessions before and after execution and computes newly created session IDs. However, session IDs recovered from runner command output could previously enter the relevant-session set without being constrained to the current run's newly created session boundary. A historical session referenced in output could therefore be incorrectly included and later bound to a current scenario.

## Approved direction

Make the exact qualification operation the authoritative inventory boundary:

- a top-level session may enter the inventory only when it was created after the run's before-snapshot and belongs to the current qualification execution
- nested sessions may enter only as descendants of sessions already proven to belong to the current run
- session IDs discovered from runner stdout, stderr, prompts, exports, or other evidence are hints for binding, not authority to cross the before/after boundary
- every inventoried session must resolve to the current execution root and one maintained scenario
- historical sessions must never become current-run evidence merely because their IDs or content appear in current command output
- do not require global OpenCode session deletion, pre-run cleanup, or destructive database maintenance

## Implementation

The completed implementation makes the before/after session delta authoritative:

- `build_session_inventory()` derives the owned candidate set exclusively from session IDs absent from the before-snapshot and present after the run
- only newly created top-level sessions can seed the inventory, using current runner output or execution-root membership as binding evidence
- nested sessions are added only through descendant closure over the same newly created ID set
- historical IDs parsed from `runner-commands.jsonl` remain useful scenario/prompt hints but cannot enter the inventory unless they are also new for the current operation
- every inventoried session must resolve its project root inside the exact current execution root before evidence is accepted
- every inventoried session must bind to a maintained scenario, directly, through a current-run ancestor, or through its execution-root path
- a child whose current-run parent is absent from the final inventory is rejected rather than silently producing incomplete evidence

No OpenCode session cleanup or deletion is introduced.

## Regression coverage

Regression tests now deliberately preserve historical OpenCode sessions and stale session IDs while executing consecutive synthetic runs. They verify that:

- historical sessions are never exported or included even when their IDs appear in current runner output
- current top-level sessions and nested child sessions are present
- current sessions bind to the maintained scenario
- consecutive runs on the same host produce disjoint inventories without cleanup
- a newly created session whose project root lies outside the current execution is rejected

## Completion criteria

- session inventory is exact-run isolated by construction
- historical OpenCode sessions cannot contaminate new qualification evidence
- nested current-run sessions remain fully captured
- no cleanup step is required before qualification
- regression tests prove consecutive runs produce independent inventories
- the independent audit receives only evidence belonging to the run it is evaluating

## Completion

Complete. Qualification session evidence is now derived from a closed set of sessions created by the current operation, with descendant and execution-root checks preventing historical-session contamination.
