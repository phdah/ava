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
  at: 2026-08-14T12:48:00+02:00
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

The user confirmed on 2026-08-10 that the synthetic corpus and all five specified images have been generated in a repository-external local directory and look correct. The user also confirmed that image finalization and finalized-corpus verification have been completed and recorded. Treat those confirmations as completion of corpus generation and finalization for this qualification run. The repository cannot inspect the local bytes directly, so this is recorded as user-confirmed external evidence rather than repository-generated evidence.

Current subphase status:

- [x] deterministic corpus generated locally
- [x] five specified images generated locally and visually accepted by the user
- [x] image finalization and finalized-corpus verification recorded
- [x] qualification variants materialized
- [x] clean OpenCode ingestion and routing evidence completed
- [x] independent semantic review and expected-outcome checks completed
- [ ] complete one-command upgrade, recovery, finalization, lifecycle, and regression matrix accepted
- [ ] run manifests validated and qualification evidence accepted

Use these user-owned local paths for the current qualification run:

```text
qualification vault: ~/stuff/ava-qualification-vault/
test project:        ~/stuff/project-vault
```

The user has already exercised managed-content damage, semantic reconciliation, finalization, rollback, uninstall, and reinstall manually. [Finding 17](dogfood/17-add-resume-abort-qualification-checkpoints.md) is implementation-complete and provides authentic assembled-installer resume and abort checkpoints. [Finding 18](dogfood/18-verify-relative-calendar-dates.md) is implementation-complete and defines the corrected Thursday 2026-08-13 to Friday 2026-08-14 regression.

[Finding 19](dogfood/19-add-one-command-qualification-runner.md) is implementation-complete. The complete maintained matrix is now composed behind [one internal manual shell entry point](../../release/qualification-runner.md). There is no preempting repository finding.

The immediate goal is therefore **execute one complete runner matrix against exact selected pinned corrective-alpha source and target assets, validate its evidence, and finish the Step 1 run-manifest/signoff gate**.

### Operator procedure

Use the completed runner rather than reconstructing the previous manual command sequence.

1. Resolve the exact pinned source and target release asset directories. Do not use a mutable `latest` selection. The target must expose the semantic upgrade state required by the maintained rollback, reconciliation, and finalization scenarios.

2. Run the mutation-free preflight first:

```sh
internal/release/qualify-synthetic.sh \
  --qualification-root ~/stuff/ava-qualification-vault \
  --execution-root ~/stuff/ava-qualification-run \
  --source-assets /absolute/path/to/pinned/source-assets \
  --target-assets /absolute/path/to/pinned/target-assets \
  --test-project ~/stuff/project-vault \
  --opencode opencode \
  --model <provider/model> \
  --preflight-only
```

Require exact source and target identity, valid checksums, clean repository state, finalized corpus verification, all eight materialized families, safe repository-external output boundaries, and the deterministic 17-scenario plan.

3. Run the same command without `--preflight-only`:

```sh
internal/release/qualify-synthetic.sh \
  --qualification-root ~/stuff/ava-qualification-vault \
  --execution-root ~/stuff/ava-qualification-run \
  --source-assets /absolute/path/to/pinned/source-assets \
  --target-assets /absolute/path/to/pinned/target-assets \
  --test-project ~/stuff/project-vault \
  --opencode opencode \
  --model <provider/model>
```

Use `--transcript-dir /absolute/repository-external/path` only when a separate OpenCode transcript copy is needed. The runner-owned execution root already retains per-scenario command output, state, and the final summary for diagnosis.

4. Accept the runner result only when every maintained scenario reports `pass`. A `fail`, `skipped`, or `user-decision-required` result is non-terminal qualification evidence and keeps Step 1 open. Preserve the failed runner-owned workspace until the cause is understood. On rerun, passing scenarios remain retained while a non-passing scenario is recreated only from its materialized source variant.

5. Confirm the runner's terminal evidence proves, at minimum:

- finalized corpus and the supplied original test project remain byte-identical
- fresh and mature installs reach healthy installed conformance and normal routing
- private/work registered-role mutations stay within their owned boundaries
- the calendar regression persists `Friday` and `2026-08-14`, never `2026-08-15`
- complete inbox ingestion leaves no direct pending source
- managed-content damage reports only the exact expected stable conformance rule while preserving injected evidence
- resume and abort use Finding 17's authentic checkpoint plus real installer operation
- rollback is invoked exactly once and restores source managed and semantic state with transaction cleanup and normal routing
- semantic reconciliation and finalization reach a complete target state without inventing unresolved decisions
- role-led uninstall and pinned reinstall preserve project-owned bytes and finish with healthy installed conformance

6. Populate or complete the required run manifests from the accepted runner evidence with exact Ava version, source revision, asset identity, host/model/session identity, project-owned hashes, installer and conformance output, transcript, expected outcome, actual outcome, reviewer, and linked finding.

7. Validate every populated run manifest before accepting its result:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py verify-run-manifest /absolute/path/outside/ava/run-manifest.json
```

8. Run repository qualification after any repository-side evidence or task-link updates:

```sh
internal/release/test.sh
internal/release/validate-boundaries.sh
```

Do not regenerate, re-finalize, or re-verify the corpus or images unless later qualification exposes a fixture defect or invalidates the recorded local evidence.

### Step 1 completion gate

Advance only when the synthetic-vault task's completion criteria are satisfied, the complete runner matrix passes against the exact selected assets, required run manifests are valid, qualification evidence is accepted, and repository boundary validation passes.

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
