# Ava release procedure

This is the authoritative release operator flow. Stable semantic versions are the maintained release channel. Release Please defines the candidate version. GitHub Actions performs mandatory deterministic qualification. Explicit user acceptance is required before a release PR may merge. Post-merge publication is derived from durable tag and GitHub Release state and is safely resumable.

Stable `1.0.0` is the root release. There is no supported source release before it and no upgrade edge into it. The checked-in release ledger therefore starts empty and the first immutable adjacent edge is created by `1.0.1` as `1.0.0 -> 1.0.1`.

## 1. Identify the release candidate

Use the current Release Please PR targeting `main`. Read the candidate version from its release changes and validate it with `internal.release.validate_release_pr`.

The candidate must be an exact repository revision. Do not qualify or publish mutable working state.

For the first supported release, the repository baseline before the Release Please PR uses the internal `0.0.0` version sentinel only so Release Please can propose `1.0.0`. The sentinel is not a release, tag, installable version, source release, or upgrade edge.

## 2. Bind qualification identity

`internal/release/qualification/config.json` selects the active qualification operation from `pair-catalog.json`.

For `1.0.0`:

- there is no source release,
- target is the exact local `1.0.0` candidate revision,
- target assembly contains no supported upgrade edges,
- qualification is target-only.

For `1.0.1` and later:

- source is the exact immediately previous published stable release with verified asset digests,
- target is the exact local candidate revision,
- qualification is bound to the adjacent source-to-target pair.

The target revision, release manifest, qualification matrix, driver, and source identity when one exists are part of execution identity.

## 3. Run pre-edge qualification

For ordinary releases after `1.0.0`, the release PR first runs deterministic `pre-edge` qualification before a new adjacent edge is authored. It covers target installation, mature-project preservation, and managed-damage behavior that does not depend on the new edge.

The first `1.0.0` release has no edge to author. Its target-only qualification therefore proceeds directly through the applicable deterministic release checks without pretending that a previous release exists.

A failing qualification is a release blocker. Correct the implementation and rerun the exact candidate.

## 4. Review semantic impact for an upgrade

This step applies only when a source release exists.

The Ava Internal Maintainer reviews the exact previous release against the target candidate and records whether project-owned semantic reconciliation is required. Tooling must not guess semantic migration need. A managed behavior change and the presence or absence of deterministic project-file migrations are evidence for the maintainer, not a substitute for reviewed judgment. The recorded result must include a rationale.

### Managed delta

Describe changes to Ava-managed files, installation behavior, schemas, routing, lifecycle behavior, or other managed contracts.

### Project-owned compatibility

Determine whether the managed delta can invalidate project-owned meaning or behavior, including roles, workflows, shared instructions, indexes, host entrypoints, or other project-owned extensions.

### Required reconciliation

When project-owned compatibility can be affected, define bounded discovery conditions, completion criteria, and reviewed guidance. Otherwise record why no project-owned reconciliation is required.

There is no source-to-target semantic review for `1.0.0` because there is no supported source release or upgrade transition.

## 5. Author the adjacent edge

This step applies only after `1.0.0`.

Create exactly one release-local catalog record for the immediately previous stable release to the candidate. Add only guidance, migrations, and retirement decisions introduced by that edge. Earlier stable release records remain immutable.

Run the maintained release suite:

```sh
internal/release/test.sh
```

For `1.0.0`, no catalog record is created and the assembled release manifest contains an empty supported-upgrade edge inventory.

## 6. Run final qualification

Push the completed Release Please PR.

For `1.0.0`, final qualification proves the exact target release through all applicable target-only deterministic checks. Upgrade resume, abort, rollback, semantic reconciliation, and source-to-target upgrade checks are inapplicable because no source release exists.

For later releases, final qualification repeats the deterministic mechanical checks, validates the reviewed adjacent edge, exercises lifecycle recovery paths, and performs a deterministic source-to-target upgrade.

A passing final run writes evidence with status `awaiting-user-signoff` and exposes the evidence through GitHub Actions.

## 7. Accept qualification

Review the exact final CI evidence. A clean deterministic run does not accept itself.

After the user explicitly accepts that run, apply acceptance through the maintained acceptance-request path or `internal/release/accept-release-qualification.sh`. Acceptance is bound to the run ID, repository revision, target identity, execution digest, and source identity when one exists.

Do not synthesize acceptance, reuse acceptance for another revision, or merge before the release policy observes accepted state.

## 8. Merge the Release Please PR

Once required CI checks pass and final qualification is accepted, merge the Release Please PR using **Create a merge commit**. Do not squash or rebase it. The accepted qualification is bound to an exact commit on the release branch, and the merge commit must preserve that qualified revision in the published revision's ancestry.

This differs from ordinary implementation PRs, which may be squash merged so their reviewed Conventional Commit title becomes one canonical release-classified commit on `main`.

Do not manually create, move, or recreate release tags.

## 9. Publish from durable release state

`.github/workflows/release-please.yml` owns post-merge publication. For the accepted target it:

1. resolves the expected version, tag, tagged revision, and GitHub Release candidates,
2. proves the tag matches the exact accepted release revision,
3. validates qualification acceptance,
4. runs `internal/release/test.sh`,
5. assembles twice from the exact tagged source and proves byte-for-byte reproducibility,
6. runs release conformance,
7. validates or creates one compatible draft release,
8. attests the release assets,
9. uploads only missing assets and fails closed on digest mismatches,
10. publishes the exact draft by release ID,
11. verifies the published release is immutable and complete,
12. runs Release Please maintenance for the next release separately.

A fully published matching release is an already-complete result.

## Recovery after partial publication

Use the `workflow_dispatch` entry point in `.github/workflows/release-please.yml` with the known release tag. The same durable-state planner and publication sequence are used for recovery.

Recovery may reuse a compatible draft and matching uploaded assets. It must never move a correct tag, overwrite mismatched assets, reuse an incompatible draft, or publish when release identity is ambiguous.

See [publication recovery](publication-recovery.md) for the recovery contract.

## Retry boundary

Automatic retry is appropriate only for read-only or demonstrably idempotent operations. Mutating tag, release, asset, and publication operations are guarded by durable identity and digest checks. Persistent or ambiguous failures stop the workflow for explicit diagnosis.
