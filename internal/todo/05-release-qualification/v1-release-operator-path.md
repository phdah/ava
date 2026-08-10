---
type: Internal Release Qualification Procedure
title: V1 Release Operator Path
description: Canonical ordered procedure for answering what comes next and advancing Ava from the current alpha state to the first stable 1.0.0 release.
tags: [internal, roadmap, release, qualification, operator]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T15:58:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T16:23:00+02:00
---

# V1 Release Operator Path

## Purpose

This file is the canonical ordered execution path from the current alpha qualification state to Ava `1.0.0`.

When the user asks what to do next, do not reconstruct the answer from pending checkboxes or historical findings. Read `/internal/todo.md`, follow its single current-next-action link to this procedure, and report the first incomplete step below together with its immediate operator action.

Detailed task files remain authoritative for acceptance criteria and background. This procedure is authoritative for ordering, advancement gates, current execution status, and the practical operator sequence.

## Ordered path to `1.0.0`

1. Finish the [synthetic v1 qualification vault](04a-build-synthetic-qualification-vault.md).
2. [Qualify and publish the corrective alpha](04b-qualify-and-publish-corrective-alpha.md).
3. Obtain explicit user closure of [alpha dogfooding](04-dogfood-alpha-and-track-findings.md).
4. [Publish the `1.0.0` release candidate](05-publish-release-candidate.md).
5. [Stabilize the published release candidate](05a-stabilize-release-candidate.md).
6. [Qualify and publish `1.0.0`](06-qualify-and-publish-v1.md).

A newly discovered blocker or `required-v1` dogfood finding preempts this sequence until that finding is resolved. A `post-v1` finding does not preempt the sequence.

## Dogfood closure

Dogfooding remains intentionally open while steps 1 and 2 are performed. The user does not need to close dogfooding before the synthetic-vault work or the corrective-alpha qualification.

Explicit user closure is required only before step 4 may begin. After step 2 is complete, no blocker or `required-v1` finding is open, and the user states that alpha dogfooding is complete or that Ava should proceed to the release candidate, mark the dogfood umbrella complete and advance to step 4.

Do not infer closure from an empty findings backlog, passing tests, or publication of another alpha.

## Step 1: finish synthetic-vault qualification

### Current status

The deterministic fixture implementation is complete.

The user confirmed on 2026-08-10 that the synthetic corpus and all five specified images have already been generated in a repository-external local directory and look correct. Treat that confirmation as completion of the **content-generation subphase**. The repository cannot inspect those local bytes, so do not claim independent hash, file-type, or oracle verification until the local fixture commands are run.

Current subphase status:

- [x] deterministic corpus generated locally
- [x] five specified images generated locally and visually accepted by the user
- [ ] image finalization and finalized-corpus verification recorded
- [ ] qualification variants materialized
- [ ] clean OpenCode ingestion and routing evidence completed
- [ ] independent semantic review and expected-outcome checks completed
- [ ] upgrade, recovery, finalization, and lifecycle scenarios completed
- [ ] run manifests validated and qualification evidence accepted

The immediate goal is therefore **validation of the generated corpus through real ingestion and qualification**, not generation of another corpus.

### Operator procedure

Point `QUALIFICATION_ROOT` at the user's existing generated directory outside the Ava repository:

```sh
QUALIFICATION_ROOT=/absolute/path/to/existing/qualification-vault
```

1. Finalize and hash the five already-generated image files. This verifies that they exist at the exact declared destinations and records their actual bytes in the finalized inventory:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py finalize-images "$QUALIFICATION_ROOT"
```

2. Verify the complete finalized corpus before ingestion:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py verify "$QUALIFICATION_ROOT"
```

If either command fails, fix the reported local fixture problem before continuing. Do not regenerate content merely because these commands have not previously been run.

3. Materialize all eight isolated qualification variants:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py materialize-variants "$QUALIFICATION_ROOT"
```

4. Use the execution plans recorded in the generated variants as the scenario-specific source of truth. Exercise them against the exact assembled Ava revision under qualification. At minimum, complete the fresh-install, mature-project, registered-role, pending-inbox, damaged-managed-content, interrupted-upgrade, pending-semantic-reconciliation, and uninstall/reinstall scenarios required by the task.

5. For inbox-ingestion qualification, process the corpus in chronological batches where the execution plan calls for staged ingestion. Copy the direct files from each batch into the project inbox rather than copying the batch directory itself:

```text
01-pre-move
02-move-transition
03-renovation
04-settled
```

For each batch, start from the scenario state defined by the execution plan, run the managed inbox-ingestion flow in a clean OpenCode session, and record the transcript, loaded paths, selected role, role announcement point, source dispositions, and resulting project-owned changes.

6. After ingestion, run an independent semantic review against the expected outcomes in the fixture oracle. Check at minimum:

- durable versus non-durable disposition
- private/work routing separation
- hierarchy and progressive discovery
- source fidelity and attribution
- temporal state and supersession, especially around the February move
- repeated and duplicate facts
- role routing and conversational follow-up behavior
- image-derived facts against their declared expected outcomes

7. Exercise the remaining lifecycle variants and record deterministic state evidence for damaged managed content, interrupted upgrades, semantic reconciliation, successful agent-driven finalization, uninstall, and reinstall. Preserve before-and-after project-owned hashes so the evidence can prove which files changed.

8. Populate the run manifest for every accepted scenario with the exact Ava version, source revision, asset identity, host/model/session identity, project-owned hashes, installer and conformance output, transcript, expected outcome, actual outcome, reviewer, and linked finding.

9. Validate every populated run manifest before accepting its result:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py verify-run-manifest /absolute/path/outside/ava/run-manifest.json
```

10. Run repository qualification after any repository-side evidence or task-link updates:

```sh
internal/release/test.sh
internal/release/validate-boundaries.sh
```

### Step 1 completion gate

Advance only when the synthetic-vault task's completion criteria are satisfied, including finalized five-image inventory, all required qualification variants exercised, clean OpenCode ingestion and review evidence recorded, run manifests valid, and repository boundary validation passing.

User confirmation of corpus and image quality completes generation, but does not by itself complete Step 1 because the purpose of this step is qualification of actual Ava behavior against that corpus.

## Step 2: qualify and publish the corrective alpha

Use the maintained [release publication procedure](../../release/procedure.md). Do not author `upgrade-impact.json` or cumulative target-specific guidance.

1. Let release-please determine the actual next prerelease version and release PR.
2. Review the exact previous-to-target managed delta and make the project-owned semantic-impact decision.
3. Author exactly one adjacent previous-to-target release record under `internal/release/catalogs/<target>.json` using the maintained adjacent-edge tooling. A representative command shape is:

```sh
python3 internal/release/compose_adjacent_catalog.py \
  --previous-version <previous-version> \
  --new-edge <edge-json> \
  [--new-guidance <guidance-json>] \
  --guidance-root internal/release/guidance \
  --output internal/release/catalogs/<target-version>.json
```

4. Validate the release PR against its base revision:

```sh
python3 internal/release/validate_release_pr.py \
  --root . \
  --previous-version <previous-version> \
  --base-revision <release-pr-base-sha>
```

5. Run the complete release suite:

```sh
internal/release/test.sh
```

6. Merge only after the adjacent edge, semantic-impact rationale, and release PR are reviewed and accepted.
7. After immutable publication, exercise the published pinned assets against the synthetic-vault scenarios and the realistic dogfood checks required by the corrective-alpha task. Include the realistic multi-turn routing evidence from finding 12 and fresh-agent terminal-finalization evidence from finding 15.
8. Record exact tag, revision, asset digests, source-to-target outcomes, transcripts, conformance results, and linked findings in qualification evidence.

### Step 2 completion gate

Advance only when the corrective alpha is immutable and every required published-asset qualification result passes or has produced a newly tracked blocker or `required-v1` finding.

## Step 3: close alpha dogfooding

This is a user-owned gate, not another technical verification task.

Before asking for closure, verify:

- step 2 is complete
- there are no pending blockers
- there are no pending `required-v1` findings
- every newly discovered release-relevant defect has a disposition

Then ask the user whether alpha dogfooding is complete and Ava should proceed to RC qualification. A clear affirmative statement is sufficient. Record that closure in the dogfood umbrella task and Phase 5 indexes.

## Step 4: publish the `1.0.0` release candidate

Follow [Publish the `1.0.0` Release Candidate](05-publish-release-candidate.md) and the maintained release procedure.

1. Confirm dogfooding is explicitly closed and the public v1 contracts are frozen.
2. Let release-please determine the canonical RC version, normally `1.0.0-rc.1` unless the approved sequence requires otherwise.
3. Author exactly one adjacent latest-alpha-to-RC edge and complete the semantic-impact assessment.
4. Run release-PR validation and `internal/release/test.sh` using the same commands as step 2.
5. Run the complete conformance, OpenCode, synthetic-vault, upgrade, maintenance, semantic-reconciliation, finalization, and uninstall matrix against the exact assembled revision.
6. Publish the immutable RC only after explicit approval of the exact version and revision.
7. Re-run the required qualification against the published pinned RC assets and bind the evidence to the immutable tag and digests.

## Step 5: stabilize the published RC

Follow [Stabilize the Published Release Candidate](05a-stabilize-release-candidate.md).

1. Regenerate and verify the fixed synthetic-vault baseline.
2. Exercise the full published-RC matrix: fresh install, mature install, repeated OpenCode sessions, routing classes, workflows, ingestion, project-context maintenance, role creation, semantic review, damaged managed state, recovery, finalization, upgrade paths, uninstall, and reinstall.
3. Validate all run manifests and retained project-owned hashes.
4. Record every defect requiring repository work as a bounded finding.
5. If an incompatible public contract or behavior change is required, publish another RC and repeat this step completely.
6. Accept the RC as the stable input only when no blocker or `required-v1` finding remains and every known limitation has a stable-safe disposition.

## Step 6: qualify and publish `1.0.0`

Follow [Qualify and Publish `1.0.0`](06-qualify-and-publish-v1.md).

1. Confirm RC stabilization is complete and the stable acceptance gate is satisfied.
2. Build the exact stable asset set twice from one clean source revision and require identical digests.
3. Verify fresh installation and the declared RC-to-stable upgrade from assembled assets.
4. Verify the complete OpenCode, recovery, finalization, semantic compatibility, uninstall, trust, and documentation requirements.
5. Run the complete repository and release qualification suite.
6. Obtain explicit approval for version `1.0.0` and the exact source revision.
7. Publish the immutable `v1.0.0` release as stable and set it as `latest` only after every maintained gate succeeds.
8. Install fresh and upgrade from the latest RC using the published assets, then verify tag target, asset inventory, checksums, attestation, immutable state, and stable convenience URL.
9. Update public repository status documentation to identify `1.0.0` as the first supported stable Ava distribution.

## Answering "what is next?"

For a status-only question, answer from `/internal/todo.md` and this file. State:

1. the current numbered step
2. the immediate next operator action
3. the completion gate for that step
4. the following step

Do not scan historical findings or infer a different sequence unless the current entry point reports a new preempting blocker or `required-v1` finding.
