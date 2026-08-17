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
  at: 2026-08-17T12:26:00+02:00
---

# Ava Internal To-Do List

This file is the authoritative entry point for answering what Ava development work comes next. It is internal repository context and must never be copied into distributed projects.

Use the [ordered roadmap](todo/index.md) for broad phase navigation. Use the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md) for the exact path to `1.0.0`.

## Current phase

[V1 release qualification](todo/05-release-qualification/) is active.

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains open until the user explicitly closes it. Any new blocker or `required-v1` finding preempts release progression until resolved.

## Official next action

**Prepare the corrective-alpha release PR and qualify its exact candidate before merge.**

The hands-off qualification system is implementation-complete. Release-specific qualification now belongs inside the mandatory [release publication procedure](release/procedure.md):

1. let release-please establish the target version/PR
2. complete semantic-impact assessment and adjacent release record
3. run deterministic validation/tests
4. assemble the exact local target assets from the clean release PR revision
5. run `internal/release/qualify-release.sh`
6. obtain explicit user signoff on `awaiting-user-signoff`
7. record acceptance with `internal/release/accept-release-qualification.sh`
8. require the Release PR policy check to pass before merge

Do not publish or merge a new release without accepted qualification state.

## Official path to `1.0.0`

1. finish the synthetic v1 qualification system
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
