---
id: ava-5639
title: Harden and recover release publication after partial failure
status: To Do
assignee: []
created_date: '2026-09-02 22:46'
updated_date: '2026-09-03 20:39'
labels:
  - internal
  - roadmap
  - release
  - publication
  - reliability
  - github-actions
milestone: m-0
dependencies: []
type: enhancement
ordinal: 6638
---

## Description

Harden Ava's post-merge publication workflow so the normal release path is not unnecessarily vulnerable to unrelated release-please failures, and make publication safely resumable when an unavoidable transient or external failure still leaves partial release state.

The alpha.17 release exposed both problems. In workflow run `33680822686`, release-please successfully identified PR #121, created the alpha.17 release/tag state, and marked the PR `autorelease: tagged`. It then continued into its separate next-release-PR bookkeeping. While backfilling the file list for commit `c91f1781b6a966444458e9f5ad1f3e68e06ae1a7`, the GitHub/API connection terminated with `other side closed`. The whole `googleapis/release-please-action` step was therefore marked failed even though release creation had already progressed, so every Ava validation, assembly, attestation, upload, and publication step was skipped.

The retry demonstrated the second weakness: release-please could now see `v1.0.0-alpha.17` and completed successfully, but reported no newly-created release in that attempt. Because Ava's publication steps are all gated only by `steps.release.outputs.release_created == 'true'`, the retry skipped the complete publication pipeline rather than resuming the already-established release identity.

The immediate network/API disconnect itself may be transient and outside Ava's control. The preventable design problem is that successful release creation and Ava publication are coupled to additional release-please bookkeeping that can fail afterward, and that publication eligibility is represented only by an ephemeral action output rather than durable repository/release state.

A correct implementation must therefore address both prevention and recovery. It should reduce or eliminate the failure window that caused alpha.17 where reasonably possible, and it must still recover safely if GitHub, release-please, attestation, upload, or another external dependency fails after any durable release mutation.

## Required behavior

1. Investigate the alpha.17 first-attempt failure and explicitly document which part was an external/transient transport failure versus which part was caused by Ava's workflow structure.
2. Decouple Ava's publication decision from unrelated post-release release-please PR-maintenance work where the release-please interface permits it. A successfully-established release identity must not be discarded merely because subsequent next-release-PR bookkeeping fails.
3. Do not use `release_created` from one action invocation as the sole durable source of truth for whether publication should run. Resolve and verify durable state such as the accepted version, exact tag, tagged revision, and GitHub Release state.
4. Detect a partially-created target release after the release PR has merged, including at least the state where the correct tag exists but the GitHub Release object or release assets are missing.
5. Before continuing or resuming publication, prove the target tag points to the exact accepted release merge revision and that the corresponding qualification acceptance is valid.
6. Run or resume the same validation, reproducible assembly, conformance, attestation, asset upload, and publish sequence from the exact tagged source even when the current release-please invocation did not emit `release_created == true`.
7. Make retry/recovery idempotent: rerunning after partial success must reuse compatible state or fail closed rather than duplicate, overwrite, retag, or silently publish mismatched assets.
8. A fully published matching release should be a safe no-op or explicit already-complete result.
9. `workflow_dispatch` or another explicit GitHub Actions recovery entry point must be capable of finishing a known partially published release without requiring local or user-hosted release tooling.
10. Consider bounded automatic retry only for operations that are demonstrably safe and idempotent. Do not mask persistent failures or retry release mutations blindly.
11. Document both the normal hardened publication path and the recovery procedure in the authoritative internal release flow.
12. Preserve release-please's required version/tag/release-PR behavior while avoiding unnecessary coupling between release creation, next-PR maintenance, and Ava asset publication.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The alpha.17 first-attempt failure is reproduced or modeled accurately in tests: release/tag creation succeeds, later release-please bookkeeping fails, and Ava still has a well-defined durable publication state instead of losing the release event
- [ ] #2 The implementation distinguishes the external `other side closed` transport failure from the preventable workflow coupling that allowed it to strand publication
- [ ] #3 Ava publication eligibility is derived from verified durable release identity/state and is not solely dependent on a fresh `release_created == true` action output
- [ ] #4 Tests cover interruption after tag/release creation and prove a subsequent normal retry or explicit recovery run reaches the publication steps even when release-please no longer reports a newly-created release
- [ ] #5 Recovery verifies tag, version, accepted qualification, exact source revision, and existing GitHub Release state before assembling or publishing
- [ ] #6 Recovery never deletes, moves, or recreates a correct existing tag merely to retrigger release-please
- [ ] #7 Release assembly is still performed reproducibly from the exact tagged source, conformance is checked, assets are attested, and only matching assets are uploaded
- [ ] #8 Repeated publication/recovery attempts are idempotent across missing-release, draft or partial-release, and already-published states, with mismatches failing closed
- [ ] #9 The design evaluates whether release creation/publication can be separated from next-release-PR maintenance, or otherwise prevents a later release-please bookkeeping failure from suppressing an already-valid publication path
- [ ] #10 The GitHub Actions manual recovery entry point is documented and can be operated from a repository-connected maintainer session
- [ ] #11 The authoritative release procedure documents diagnosis, prevention strategy, automatic retry boundaries, and manual recovery for partial post-merge publication
- [ ] #12 The alpha.17 partial publication incident is recovered through the maintained path and the resulting immutable release is verified; AVA-5638 records the successful end-to-end proof
<!-- AC:END -->
