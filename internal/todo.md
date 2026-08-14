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
  at: 2026-08-14T12:11:00+02:00
---

# Ava Internal To-Do List

This file is the authoritative entry point for answering what Ava development work comes next. It is internal repository context and must never be copied into distributed projects.

Use the [ordered roadmap](todo/index.md) for broad phase navigation. Use the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md) for the exact ordered path from the current alpha state to `1.0.0`.

## Current phase

[V1 release qualification](todo/05-release-qualification/) is active.

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains open while the remaining alpha qualification work is performed. There is currently 1 pending dogfood finding, 0 pending blockers, and 1 pending `required-v1` finding.

## Official next action

**Implement Finding 19: add one-command synthetic qualification runner.**

[Finding 18](todo/05-release-qualification/dogfood/18-verify-relative-calendar-dates.md) is implementation-complete. The managed base now conditionally requires deterministic calendar verification before relevant persistence converts relative calendar language into an absolute fact, with source-versus-host reference semantics, ambiguity preservation, boundary fixtures, Change Reviewer coverage, and assembled-payload regression coverage.

[Finding 19](todo/05-release-qualification/dogfood/19-add-one-command-qualification-runner.md) now preempts execution of the remaining Step 1 qualification scenarios. It composes the complete maintained matrix, including Finding 17's authentic resume/abort checkpoints and Finding 18's calendar regression, behind one internal shell entry point. After Finding 19 is complete, execute the runner and return to the remaining Step 1 signoff gate. Do not regenerate the already finalized corpus or images unless qualification exposes a fixture defect.

Use these user-owned local paths for the current qualification run:

```text
qualification vault: ~/stuff/ava-qualification-vault/
test project:        ~/stuff/project-vault
```

## Official path to `1.0.0`

1. finish the synthetic v1 qualification vault
2. qualify and publish the corrective alpha
3. obtain explicit user closure of alpha dogfooding
4. publish the `1.0.0` release candidate
5. stabilize the published release candidate
6. qualify and publish `1.0.0`

The exact procedure, commands, evidence, and advancement gates are defined in the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md).

## Dogfood signoff

The user does **not** need to close dogfooding before steps 1 or 2. Dogfooding intentionally remains open while the synthetic qualification work and corrective-alpha qualification are performed.

Explicit user closure is required before step 4, release-candidate publication, may begin. After step 2 is complete and no blocker or `required-v1` finding remains, a clear user statement that dogfooding is complete or that Ava should proceed to the release candidate is sufficient. Do not infer closure from an empty findings backlog or passing qualification.

## Preemption rule

A newly recorded dogfood finding classified as `blocker` or `required-v1` preempts the current release path until it is resolved. An approved `post-v1` finding does not preempt the path.

## Answering "what is next?"

For a status-only question such as "what am I doing next?":

1. read this file
2. report the **Official next action** exactly as the current step
3. read the linked section of the V1 release operator path only when the user wants the practical steps or verification commands
4. do not reconstruct ordering from historical findings, pending checkboxes, or unrelated roadmap phases

Only read deeper task, release, or fixture context when executing the work, validating a gate, or when this entry point reports a newly preempting finding.

A finding is complete when its bounded repository change, regression coverage, documentation, indexes, and resolution evidence are committed. Published-asset or realistic-project evidence may remain a later release gate without returning that finding to pending implementation status.
