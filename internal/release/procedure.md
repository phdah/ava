# Ava release procedure

This is the authoritative release operator flow. The release PR defines the candidate version. GitHub Actions performs mandatory deterministic qualification. The maintainer owns semantic review and explicit user acceptance. Post-merge publication is derived from durable tag and release state and is safely resumable.

## 1. Identify the release candidate

Use the current release-please PR targeting `main`. Read the candidate version from its release changes and validate it with `internal.release.validate_release_pr`.

The candidate must be an exact repository revision. Do not qualify or publish mutable working state.

## 2. Bind the qualification pair

`internal/release/qualification/config.json` selects one active adjacent source-to-target pair from `pair-catalog.json`.

- Source is the exact previous published release and its verified asset digests.
- Target is the exact local candidate revision.
- Only the immediately previous supported release is authored as the new edge. Earlier support is composed from immutable adjacent catalogs.

The pair, target revision, release manifest, and qualification matrix are part of execution identity.

## 3. Run pre-edge qualification

The release PR triggers `.github/workflows/release-qualification.yml`, which executes `python3 -m internal.release.qualification_ci` against the exact PR head. The CI driver prepares immutable source assets and a repository-external synthetic fixture, then runs the deterministic `pre-edge` stage.

Pre-edge qualification covers target installation and managed-damage behavior that does not depend on the new adjacent upgrade edge. It fails before edge authoring when the candidate is mechanically invalid. Pre-edge output is transient CI evidence and does not create release acceptance state.

A failing qualification is a release blocker. Correct the implementation in normal repository work and rerun CI.

## 4. Perform semantic impact review

The Ava Internal Maintainer reviews the exact previous release against the target candidate and records whether project-owned semantic reconciliation is required. Tooling must not guess semantic migration need.

The review records these sections:

### Managed delta

Describe changes to Ava-managed files, installation behavior, schemas, routing, lifecycle behavior, or other managed contracts. A managed behavior change is evidence to review, not a semantic decision by itself.

### Project-owned compatibility

Determine whether the managed delta can invalidate project-owned meaning or behavior, including roles, workflows, shared instructions, indexes, host entrypoints, or other project-owned extensions. The presence or absence of deterministic project-file migrations does not decide this question.

### Required reconciliation

When project-owned compatibility can be affected, define bounded discovery conditions, completion criteria, and reviewed guidance for reconciliation. When it cannot, state that no project-owned reconciliation is required and record the rationale.

The decision and rationale are maintainer-owned. Deterministic validation may verify that the reviewed decision is represented consistently, but it must not infer semantic impact from managed behavioral change or deterministic project-file changes.

## 5. Author the adjacent edge

After pre-edge qualification passes and semantic impact is reviewed, author exactly one adjacent upgrade edge from the previous release to the candidate using the maintained catalog model and reviewed guidance.

Run the maintained release suite:

```sh
internal/release/test.sh
```

The suite validates release policy, assembly, catalogs, conformance, qualification contracts, publication/recovery behavior, and repository boundaries.

## 6. Run final qualification

Push the completed release PR. GitHub Actions reruns qualification and selects the `final` stage when the target declares the required adjacent edge.

Final qualification repeats the deterministic mechanical scenarios, validates the adjacent edge, exercises lifecycle recovery paths, and runs a deterministic source-to-target upgrade. A passing final run writes a run record with status `awaiting-user-signoff` and exposes the evidence as a CI artifact.

## 7. Accept qualification

Review the final CI evidence. A clean deterministic run does not accept itself.

After the user explicitly accepts that exact final run, apply acceptance through `internal/release/accept-release-qualification.sh` or the validated acceptance-request path handled by `qualification_ci.py`. Acceptance is bound to the run ID, pair, repository revision, source/target identity, and execution digest.

Do not synthesize acceptance, reuse acceptance for another revision, or merge before the release policy validator observes the accepted state.

## 8. Merge the release PR

Once required CI checks pass and the final qualification is accepted, merge the current release-please PR using **Create a merge commit**. Do not squash or rebase the release PR. The accepted qualification is bound to a commit on the release-PR branch, and the merge commit must preserve that qualified revision in the published revision's ancestry.

This is intentionally different from ordinary implementation PRs, which may be squash merged so their Conventional Commit title becomes one canonical release-classified commit on `main`.

Do not manually create, move, or recreate release tags.

## 9. Publish from durable release state

`.github/workflows/release-please.yml` owns post-merge publication. It separates release identity creation from next-release-PR maintenance and does not use a fresh `release_created` action output as publication authority.

For the accepted target it:

1. resolves the expected version, tag, tagged revision, and GitHub Release candidates,
2. proves the tag matches the exact accepted release revision,
3. validates qualification acceptance from maintained tooling,
4. runs `internal/release/test.sh`,
5. assembles the release twice from the exact tagged source and proves byte-for-byte reproducibility,
6. runs release conformance,
7. validates or creates one compatible draft release,
8. attests the release assets,
9. uploads only assets that are missing and fails closed on digest mismatches,
10. publishes the exact draft by release ID,
11. verifies the published release is immutable and complete,
12. runs release-please PR maintenance for the next release separately.

A fully published matching release is an already-complete result.

## Recovery after partial publication

Use the `workflow_dispatch` entry point in `.github/workflows/release-please.yml` with the known release tag. The same durable-state planner and publication sequence are used for recovery; there is no separate publication implementation.

Recovery may reuse a compatible draft and matching uploaded assets. It may delete only redundant compatible drafts after validating all same-tag candidates. It must never move a correct tag, overwrite mismatched assets, reuse an incompatible draft, or publish when release identity is ambiguous.

### Temporary alpha.19 squash recovery

`v1.0.0-alpha.19` was accidentally squash merged after its exact final qualification had been accepted. Release Please created the tag and draft before the permanent ancestry validator correctly stopped publication. The tag must not be moved or recreated.

Manual recovery of that exact tag may use `internal.release.qualification_squash_recovery` from maintained `main` tooling. This exception is deliberately bounded to:

- target `1.0.0-alpha.19` from `1.0.0-alpha.18`,
- tagged revision `4aeb06b4292b9c768ea745ca5989e94c24d4be7c`,
- release PR base `3d45f49ade63604cadeff89d376f3fa36b8f007d`,
- the recorded accepted final tree,
- a clean explicitly accepted qualification run,
- and a direct tree comparison proving that the tagged revision differs from the qualified revision only under `internal/release/qualification/`.

The workflow fetches the qualified revision recorded in the acceptance ledger only for this exact recovery. Every other release continues through the normal ancestry-based `qualification_acceptance` validator. Remove this temporary alpha.19 recovery module and workflow branch after the final alpha has been published and its stable-bootstrap evidence has been captured.

See [publication recovery](publication-recovery.md) for the general recovery contract.

## Retry boundary

Automatic retry is appropriate only for read-only or demonstrably idempotent operations. Mutating tag, release, asset, and publication operations are guarded by durable identity and digest checks. Persistent or ambiguous failures stop the workflow for explicit diagnosis.
