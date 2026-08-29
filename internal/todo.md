---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-29T12:20:00+02:00
---

# Ava Internal To-Do List

This file is the authoritative entry point for answering what Ava development work comes next. It is internal repository context and must never be copied into distributed projects.

Use the [ordered roadmap](todo/index.md) for broad phase navigation. Use the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md) for the exact path to `1.0.0`.

## Current phase

[V1 release qualification](todo/05-release-qualification/) is active.

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains open until the user explicitly closes it. A blocker preempts the next prerelease; a `required-v1` finding preempts the release gate named by its `blocks` field.

## Official next action

**Resolve dogfood findings 31, 32, and 34 (blockers), before rerunning full qualification.**

Findings 22 through 29 are implementation-complete. Finding 30 is also complete, but intentionally as a no-op: its detached-session root-cause diagnosis was not established, so no qualification or release tooling was changed. Finding 33 is complete: the multi-hour `complete-pending-inbox` scenario is retained but its live qualification fixture is deterministically shrunk from 305 sources to the exact seven-source format lower bound while preserving `mapped`, `non-durable`, and `pending` section dispositions. The immutable 305-file corpus remains unchanged.

The 2026-08-24/25 operational-reliability investigation originally recorded findings 30 through 36. By explicit user decision, the original findings 34, 35, and 36 are removed from the backlog. Finding 34 is replaced with a blocker that restores normal agent tool freedom during Inbox Ingester work by reverting Finding 27's mechanism-level ban on scripts, code execution, temporary helpers, and other available tools. Findings 31, 32, and the replacement 34 are the remaining next-prerelease blockers. The next sequence is:

1. resolve dogfood findings 31, 32, and 34 (see [Alpha Dogfood Findings](todo/05-release-qualification/dogfood/))
2. assemble a new exact candidate from the updated corrective-alpha release PR revision
3. rerun the complete qualification matrix through the normal repository-owned OpenCode adapter and obtain explicit user signoff
4. continue to the [corrective-alpha release task](todo/05-release-qualification/04b-qualify-and-publish-corrective-alpha.md)

[Finding 25](todo/05-release-qualification/dogfood/25-offer-qualification-failure-todo-tracking.md) is post-v1 and does not block release progression. Findings 31, 32, and 34 currently block the corrective alpha. There are no remaining pending `required-v1` dogfood findings from the removed 35/36 work.

Do not publish or merge a new release without accepted qualification state. Do not begin release-candidate publication before the user explicitly closes alpha dogfooding.

## Official path to `1.0.0`

1. finish the synthetic v1 qualification gate through a fresh full run against the updated corrective-alpha candidate
2. prepare, qualify, accept, and publish the corrective alpha
3. obtain explicit user closure of alpha dogfooding
4. prepare, qualify, accept, and publish the `1.0.0` release candidate
5. stabilize the published release candidate
6. prepare, qualify, accept, and publish `1.0.0`

The exact ordering and gates are defined in the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md).

## Dogfood signoff

The user does not need to close dogfooding before the corrective alpha. Explicit closure is required before release-candidate publication begins.

## Answering "what is next?"

For a status-only question:

1. read this file
2. report the **Official next action**
3. read the linked V1 operator-path section only when practical steps or gates are requested

Do not reconstruct ordering from historical findings or unrelated roadmap phases.
