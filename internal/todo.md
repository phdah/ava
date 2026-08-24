---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
updated:
  by: agent:opencode
  at: 2026-08-24T00:00:00Z
---

# Ava Internal To-Do List

This file is the authoritative entry point for answering what Ava development work comes next. It is internal repository context and must never be copied into distributed projects.

Use the [ordered roadmap](todo/index.md) for broad phase navigation. Use the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md) for the exact path to `1.0.0`.

## Current phase

[V1 release qualification](todo/05-release-qualification/) is active.

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains open until the user explicitly closes it. A blocker preempts the next prerelease; a `required-v1` finding preempts the release gate named by its `blocks` field.

## Official next action

**Resolve dogfood findings 27, 28, and 29, then assemble a new exact corrective-alpha candidate and run fresh full qualification.**

Findings 22 through 26 are implementation-complete. Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local` (candidate `77977f8`) passed all 17 runner scenarios and all repository tests but ended `needs-review`: the independent audit found two major issues and one minor issue in inbox ingestion. The next sequence is:

1. resolve [finding 27](todo/05-release-qualification/dogfood/27-prohibit-ad-hoc-code-during-inbox-ingestion.md) (bounded scope: prohibit ad hoc code execution during inbox ingestion)
2. resolve [finding 28](todo/05-release-qualification/dogfood/28-require-reconciled-inbox-disposition-evidence.md) (bounded scope: require reconciled per-passage disposition evidence)
3. decide an approach for and resolve [finding 29](todo/05-release-qualification/dogfood/29-decide-runner-inbox-semantic-detection-approach.md) (no bounded scope yet; needs an explicit approach decision first)
4. assemble a new exact candidate from the updated corrective-alpha release PR revision
5. rerun the complete 17-scenario qualification matrix through the normal repository-owned OpenCode adapter and obtain explicit user signoff
6. continue to the [corrective-alpha release task](todo/05-release-qualification/04b-qualify-and-publish-corrective-alpha.md)

[Finding 25](todo/05-release-qualification/dogfood/25-offer-qualification-failure-todo-tracking.md) is post-v1 and does not block release progression. Findings 27, 28, and 29 are the only pending dogfood findings blocking the corrective alpha.

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
