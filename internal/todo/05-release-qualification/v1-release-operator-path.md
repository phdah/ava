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
  at: 2026-08-14T16:27:00+02:00
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

The deterministic fixture, pinned image inputs, materialized variants, lower-level synthetic runner, authentic recovery checkpoints, calendar regression, and hands-off release qualification automation are implementation-complete.

Current subphase status:

- [x] deterministic corpus generated locally
- [x] five specified images generated locally, visually accepted by the user, and pinned under the internal fixture
- [x] image finalization and finalized-corpus verification recorded
- [x] qualification variants materialized
- [x] clean OpenCode ingestion and routing evidence completed
- [x] independent semantic review and expected-outcome checks completed
- [x] hands-off exact release acquisition, matrix execution, session inventory, independent audit, and compact evidence state implemented
- [ ] complete automated upgrade, recovery, finalization, lifecycle, and regression matrix accepted
- [ ] generated compact evidence accepted and Step 1 signed off

[Finding 17](dogfood/17-add-resume-abort-qualification-checkpoints.md), [Finding 18](dogfood/18-verify-relative-calendar-dates.md), and [Finding 19](dogfood/19-add-one-command-qualification-runner.md) are implementation-complete and are composed by [Hands-Off Release Qualification and Evidence State](../../release/qualification-automation.md).

The checked-in qualification catalog keeps the historical `v1.0.0-alpha.13 -> v1.0.0-alpha.14` pair separate from the active corrective pair. The active pair is exact immutable published `v1.0.0-alpha.14 -> exact local v1.0.0-alpha.15`. Historical evidence cannot be reused to qualify the corrective release.

The immediate goal is therefore **execute the hands-off operation against the exact local alpha.15 target assets, inspect the generated compact evidence, and explicitly accept it before Step 1 advances**.

### Operator procedure

1. Assemble or otherwise obtain one exact local `v1.0.0-alpha.15` release asset directory containing the complete seven-file release inventory. Do not use a mutable alias or a directory whose release manifest identifies another version or revision.

2. From a clean Ava checkout, run:

```sh
internal/release/qualify-release.sh \
  --target-assets /absolute/path/to/v1.0.0-alpha.15/assets
```

The operation itself must:

- acquire the exact immutable published alpha.14 source assets from the checked-in catalog
- verify published release immutability, attestations, checksums, manifest identity, and exact asset digests
- verify the exact local alpha.15 target asset set and its declared alpha.14-to-alpha.15 upgrade edge
- verify all five committed qualification images and regenerate a clean repository-external synthetic vault through the maintained fixture wrapper
- create a deterministic repository-external test-project integrity boundary
- run the synthetic runner preflight and complete maintained 17-scenario matrix with the checked-in qualification model
- preserve raw workspaces, release assets, command evidence, and transcripts outside the repository
- inventory every relevant top-level and nested OpenCode session and bind it to scenario, prompt digest, model, project root, transcript digest, parent, and terminal state
- run the maintained audit in a fresh OpenCode session with the checked-in audit model
- reject invalid audit output, incomplete evidence, unresolved required decisions, or any blocking or major audit finding
- write only compact run evidence and pair state under `internal/release/qualification/`, without creating a Git commit

3. Treat `failed` as a mechanical or incomplete qualification failure and `needs-review` as an audit-blocked result. Preserve the external workspace and correct the underlying cause before rerunning. A corrected rerun receives a new run id and cannot reuse passing work unless the complete execution identity is unchanged.

4. A mechanically and semantically clean operation must record `awaiting-user-signoff`. That state is intentionally not acceptance. Review the generated run record, session inventory, audit report, issue inventory, source/target identities, and raw-evidence digest before accepting the qualification result.

5. After accepting the generated evidence, run repository qualification for the resulting checked-in evidence or state changes before merging them:

```sh
internal/release/test.sh
internal/release/validate-boundaries.sh
```

Do not manually reconstruct the lower-level `qualify-synthetic.sh` sequence unless diagnosing the hands-off operation. The lower-level runner remains an implementation component, not the normal Step 1 operator entry point.

### Step 1 completion gate

Advance only when:

- the hands-off operation ran against the exact selected alpha.14-to-alpha.15 identities
- every maintained scenario passed
- the complete session inventory and independent audit are valid
- no blocking or major audit finding remains
- the automated pair state is `awaiting-user-signoff`
- the generated compact evidence has been explicitly reviewed and accepted
- repository qualification and boundary validation pass for any evidence-state commit

Step 1 completion is an evidence gate. It does not publish alpha.15 and does not close alpha dogfooding.

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
7. After immutable publication, update the qualification pair catalog to the exact published corrective release identity and use the hands-off qualification operation for the required published-asset evidence. Include any additional realistic checks required by the corrective-alpha task, including finding 12's multi-turn routing evidence and finding 15's fresh-agent terminal-finalization evidence.
8. Record exact tag, revision, asset digests, source-to-target outcomes, session inventory, audit, conformance results, and linked findings in qualification evidence.

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
5. Run the complete conformance, OpenCode, synthetic-vault, upgrade, maintenance, semantic-reconciliation, finalization, and uninstall matrix against the exact assembled revision through the hands-off qualification path.
6. Publish the immutable RC only after explicit approval of the exact version and revision.
7. Re-run the required qualification against the published pinned RC assets and bind the evidence to the immutable tag and digests.

## Step 5: stabilize the published RC

Follow [Stabilize the Published Release Candidate](05a-stabilize-release-candidate.md).

1. Generate and verify the fixed synthetic-vault baseline through the maintained automated path.
2. Exercise the full published-RC matrix: fresh install, mature install, repeated OpenCode sessions, routing classes, workflows, ingestion, project-context maintenance, role creation, semantic review, damaged managed state, recovery, finalization, upgrade paths, uninstall, and reinstall.
3. Validate the generated compact evidence, complete session inventories, audits, and retained project-owned hashes.
4. Record every defect requiring repository work as a bounded finding after reviewing the audit evidence.
5. If an incompatible public contract or behavior change is required, publish another RC and repeat this step completely.
6. Accept the RC as the stable input only when no blocker or `required-v1` finding remains and every known limitation has a stable-safe disposition.

## Step 6: qualify and publish `1.0.0`

Follow [Qualify and Publish `1.0.0`](06-qualify-and-publish-v1.md).

1. Confirm RC stabilization is complete and the stable acceptance gate is satisfied.
2. Build the exact stable asset set twice from one clean source revision and require identical digests.
3. Verify fresh installation and the declared RC-to-stable upgrade from assembled assets.
4. Verify the complete OpenCode, recovery, finalization, semantic compatibility, uninstall, trust, and documentation requirements through the maintained hands-off evidence path.
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
