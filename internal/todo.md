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
  at: 2026-08-10T16:33:00+02:00
---

# Ava Internal To-Do List

This file is the authoritative entry point for answering what Ava development work comes next. It is internal repository context and must never be copied into distributed projects.

Use the [ordered roadmap](todo/index.md) for broad phase navigation. Use the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md) for the exact ordered path from the current alpha state to `1.0.0`.

## Current phase

[V1 release qualification](todo/05-release-qualification/) is active.

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains open while the remaining alpha qualification work is performed. There are currently 0 pending dogfood findings, 0 pending blockers, and 0 pending `required-v1` findings.

## Official next action

**Step 1 of 6: exercise the finalized synthetic v1 qualification vault through ingestion and qualification.**

The synthetic corpus and all five specified images have been generated in a repository-external local directory and were visually accepted by the user on 2026-08-10. Image finalization and finalized-corpus verification have also been completed and recorded locally. The repository records that user-confirmed external progress without claiming direct access to the local artifacts.

The immediate operator action is now the execution sequence defined in the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md#step-1-finish-synthetic-vault-qualification):

1. materialize the eight qualification variants
2. exercise the variants against the exact Ava revision under qualification
3. complete clean OpenCode inbox ingestion in the required chronological batches
4. perform independent semantic review and the routing, hierarchy, fidelity, recovery, upgrade, and finalization checks required by the fixture
5. populate and validate the resulting run manifests
6. validate repository boundaries after any repository-side evidence updates

Do not regenerate or re-finalize the corpus or images unless later validation exposes a fixture defect or invalid local evidence. Advance when the [synthetic qualification task](todo/05-release-qualification/04a-build-synthetic-qualification-vault.md) meets its external ingestion, review, execution-evidence, and completion criteria.

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
