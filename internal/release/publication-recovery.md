---
type: Internal Release Procedure
title: Ava Release Publication Recovery
description: Defines durable, idempotent post-merge publication and recovery from partial GitHub release state.
tags: [internal, releases, publication, recovery, github-actions]
generated:
  by: agent:openai-chatgpt
  at: 2026-09-03T20:31:00+02:00
---

# Ava Release Publication Recovery

Ava publication must be recoverable from durable repository and GitHub state. A successful release identity must not depend on one `release-please` action invocation still reporting `release_created`.

## Alpha.17 incident and failure boundary

The first `v1.0.0-alpha.17` publication attempt in workflow run `33680822686` established release/tag state and then failed inside release-please while it was doing subsequent next-release-PR bookkeeping. The reported `other side closed` failure while fetching commit history is an external transient failure.

The preventable Ava failure was structural: release creation, next-release-PR maintenance, and every publication step were coupled to one action invocation, and the publication pipeline was gated only by `steps.release.outputs.release_created == 'true'`. On retry, release-please correctly saw that the tag had already been created and therefore did not emit a new release-created result, leaving Ava unable to resume publication.

The hardened workflow treats those as separate concerns.

## Durable publication identity

Publication identity is resolved from immutable state, not from release-please outputs:

- the canonical version in the tagged source `version.txt`
- the exact `v<version>` tag
- the exact commit targeted by that tag
- the previous release revision and version
- the accepted qualification ledger and accepted run bound to the target release
- the exact GitHub Release state for that tag

For an automatic `main` run, publication is eligible only when `v$(cat version.txt)` exists and points to the exact triggering revision. An ordinary later commit that still contains the same version is therefore not mistaken for a release.

For explicit recovery, `workflow_dispatch` accepts `release_tag`. The workflow checks out maintained publication tooling separately from the immutable tagged source. This allows current recovery code to validate and publish an older already-tagged release while all release validation, tests, assembly, notes, and assets still come from the exact tag being recovered.

The tag is never rewritten as part of recovery.

## Normal hardened publication path

The normal post-merge workflow is:

1. Run release-please in release-only mode with `skip-github-pull-request: true`. The action is allowed to fail without immediately discarding any release identity it may already have established.
2. Resolve the durable tag identity from the exact source revision. If release-please failed before establishing a matching tag, fail the workflow.
3. Validate the release PR identity and the explicit accepted qualification state from the tagged source.
4. Run the maintained repository/release suite, assemble the release twice, compare digests, and run release conformance.
5. Derive the GitHub Release body from the exact target section in the tagged `CHANGELOG.md`.
6. Inspect the GitHub Release by tag. If the exact tag exists but the Release object is missing, recreate the expected draft Release without changing the tag.
7. Compare every existing Release asset against the freshly assembled asset with GitHub's SHA-256 digest. Reject unexpected assets, duplicate names, metadata differences, or digest mismatches.
8. Reuse matching assets and stage only missing assets for upload. Never use `--clobber`.
9. Attest the verified draft assets, upload only missing assets, and publish the draft.
10. Verify that the resulting Release is non-draft, immutable, has the exact expected assets and digests, and passes `gh release verify`.
11. Only after publication has completed or been proven already complete, invoke release-please a second time with `skip-github-release: true` to create or update the next release PR.

A failure in the final next-release-PR maintenance step may make the workflow red, but it cannot undo or prevent a publication that has already completed. Rerunning the workflow revalidates the published release as an exact no-op before retrying PR maintenance.

## Recovery states

The same path handles these states without a second release PR and without tag rewriting:

- **Tag exists, Release missing:** recreate the exact draft Release from tagged source metadata and changelog notes, then continue the full validation, assembly, attestation, upload, publish, and verification path.
- **Draft Release has some matching assets:** verify every existing digest, reuse matching assets, attest the verified draft set, and upload only missing files.
- **Draft Release has all expected assets:** verify all digests, attest the verified draft set, and publish it.
- **Published Release exactly matches:** treat publication as already complete and perform final verification without uploading or publishing again.
- **Any incompatible durable state:** fail rather than overwrite it. This includes a tag/revision mismatch, qualification mismatch, Release metadata mismatch, unexpected asset, or asset digest mismatch.

The workflow does not blindly retry mutation loops. Recovery occurs through an explicit rerun or `workflow_dispatch`, and each mutation is preceded by durable-state verification. Operations are repeated only where the already-correct state can be proven reusable.

## Manual recovery

Use the `release-please` workflow's `workflow_dispatch` entry point with an exact existing tag, for example:

```text
release_tag = v1.0.0-alpha.17
```

An explicit recovery run skips release-please release creation and next-release-PR maintenance. It resolves the supplied tag, validates accepted qualification, assembles from that immutable source, reconciles only compatible draft/missing publication state, and verifies the final immutable release.

If the requested tag is missing, points to a different revision than the checked-out source, or does not match `version.txt`, recovery fails without mutation.

## Retry and immutability rules

- Never rewrite a release tag during recovery.
- Never use asset clobbering as a retry mechanism.
- Never replace a mismatched existing asset.
- Never mutate an already-published incompatible Release.
- Reassemble and revalidate from the exact tagged source on every recovery run.
- Reuse matching existing draft assets only after exact SHA-256 verification.
- Treat an exactly matching immutable published Release as success.
