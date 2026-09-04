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

Once required CI checks pass and the final qualification is accepted, merge the current release-please PR. Do not manually create, move, or recreate release tags.

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

Use the `workflow_dispatch` entry point in `.github/workflows/release-please.yml` with the known release tag. The same durable-state planner and publication sequence are used for recovery; there is no separate recovery implementation.

Recovery may reuse a compatible draft and matching uploaded assets. It may delete only redundant compatible drafts after validating all same-tag candidates. It must never move a correct tag, overwrite mismatched assets, reuse an incompatible draft, or publish when release identity is ambiguous.

See [publication recovery](publication-recovery.md) for diagnosis and operator commands.

## Retry boundary

Automatic retry is appropriate only for read-only or demonstrably idempotent operations. Mutating tag, release, asset, and publication operations are guarded by durable identity and digest checks. Persistent or ambiguous failures stop the workflow for explicit diagnosis.
