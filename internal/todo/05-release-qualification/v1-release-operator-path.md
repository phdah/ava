---
type: Internal Release Qualification Procedure
title: V1 Release Operator Path
description: Canonical ordered path from the current alpha state to Ava 1.0.0.
tags: [internal, roadmap, release, qualification, operator]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T15:58:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-29T13:20:00+02:00
---

# V1 Release Operator Path

## Ordered path to `1.0.0`

1. Finish the [synthetic v1 qualification system](04a-build-synthetic-qualification-vault.md).
2. [Prepare, qualify, accept, and publish the corrective alpha](04b-qualify-and-publish-corrective-alpha.md).
3. Obtain explicit user closure of [alpha dogfooding](04-dogfood-alpha-and-track-findings.md).
4. [Prepare, qualify, accept, and publish the `1.0.0` release candidate](05-publish-release-candidate.md).
5. [Stabilize the published release candidate](05a-stabilize-release-candidate.md).
6. [Prepare, qualify, accept, and publish `1.0.0`](06-qualify-and-publish-v1.md).

A new blocker preempts the next prerelease. A `required-v1` dogfood finding preempts the release gate named by its `blocks` field.

Current ordering: Findings 22 through 30, 33, and 34 are implementation-complete, with Finding 30 complete as a no-op. Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local` ended `needs-review` on independent-audit findings in inbox ingestion. Findings 27 through 29 record the execution-scope, rendered disposition-reconciliation, and runner semantic-claim issues from that audit. Finding 34 supersedes Finding 27's mechanism-level restriction while preserving Findings 28 and 29. The original Findings 34, 35, and 36 are removed, and Findings 31 and 32 are also removed after reassessment because they primarily mitigated the old multi-hour ingestion workload that Finding 33 substantially reduced. There are no pending next-prerelease blockers. Finding 25 is post-v1 and does not preempt this path.

## Step 1: finish the qualification system

The synthetic fixture, pinned images, maintained 17-scenario runner, recovery checkpoints, session inventory, independent audit, compact evidence, explicit user acceptance, historical acceptance ledger, and release-PR merge gate are the qualification system.

The core qualification-system implementation is complete, including Finding 34's removal of Finding 27's mechanism-level ingestion restriction without replacement execution guidance. The complete pending-inbox scenario still applies bounded structural checks and reports `structural-pass` with semantic status pending audit, so the independent audit remains the semantic gate rather than the runner overstating its evidence.

Step 1 remains open until a fresh complete matrix run against the updated corrective-alpha candidate reaches accepted qualification evidence. After this implementation reaches `main`, let release-please update the corrective-alpha release PR, assemble the exact candidate from that clean release PR revision, and run the complete qualification operation through the existing `qualify-release.sh` flow. The run must not use the former external OpenCode large-JSON shim; Finding 24's repository-owned buffering is part of the qualification implementation being exercised. If the real run exposes a concrete reliability or semantic problem, record a new bounded finding from observed behavior. A `failed` or `needs-review` result must be corrected and rerun. A clean result must receive explicit user signoff before Step 1 advances.

## Step 2: corrective alpha

Follow [Ava Release Publication Procedure](../../release/procedure.md):

1. let release-please create/determine the corrective-alpha PR and version
2. complete the semantic-impact assessment and adjacent release record
3. run deterministic validation/tests
4. assemble the local candidate from the clean release PR revision
5. configure published alpha.14 -> local corrective-alpha as the active qualification pair
6. run `qualify-release.sh`
7. fix and rerun any `failed` or `needs-review` result
8. obtain explicit user approval when the result is `awaiting-user-signoff`
9. record acceptance with `accept-release-qualification.sh` and commit the qualification state
10. require the Release PR policy check to pass
11. merge and let publication automation publish/verify the immutable release

Step 2 completes only when the corrective alpha is published and its pre-merge qualification acceptance is preserved in the release-quality ledger.

## Step 3: close alpha dogfooding

After Step 2, verify no blocker or `required-v1` finding remains. Then obtain an explicit user statement that alpha dogfooding is complete or Ava should proceed to the release candidate.

Do not infer closure from passing tests or an empty findings backlog.

## Step 4: release candidate

Follow the same mandatory release procedure. The RC release PR cannot merge until its exact local candidate has passed full qualification and received explicit user acceptance.

## Step 5: stabilize the RC

Exercise the published RC through the maintained stabilization matrix. Record any release-relevant defect as a bounded finding. If a fix changes release content, produce another RC through the same mandatory pre-merge qualification flow.

## Step 6: stable `1.0.0`

Follow the same mandatory release procedure from the accepted RC to `1.0.0`. The stable release PR cannot merge until its candidate has passed full qualification and explicit user acceptance. After merge, verify the immutable published tag, assets, checksums, attestations, and stable convenience URL.

## Historical acceptance

Existing releases through `v1.0.0-alpha.14` are accepted in the release-quality ledger with `basis: historical-backfill`. New releases require `basis: qualified-run`.

## Answering "what is next?"

Read `/internal/todo.md` first, then use this file for the current numbered step and its immediate operator action.
