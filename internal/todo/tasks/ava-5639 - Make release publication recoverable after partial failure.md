---
id: ava-5639
title: Harden and recover release publication after partial failure
status: Done
assignee: []
created_date: '2026-09-02 22:46'
updated_date: '2026-09-04 15:30'
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

The retry demonstrated the second weakness: release-please could now see `v1.0.0-alpha.17` and completed successfully, but reported no newly-created release in that attempt. Because Ava's publication steps were gated only by `steps.release.outputs.release_created == 'true'`, the retry skipped the complete publication pipeline rather than resuming the already-established release identity.

The immediate network/API disconnect itself may be transient and outside Ava's control. The preventable design problem was that successful release creation and Ava publication were coupled to additional release-please bookkeeping that could fail afterward, and that publication eligibility was represented only by an ephemeral action output rather than durable repository/release state.

A correct implementation therefore addresses both prevention and recovery. It reduces the failure window and recovers safely if GitHub, release-please, attestation, upload, or another external dependency fails after any durable release mutation.

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
- [x] #1 The alpha.17 first-attempt failure is reproduced or modeled accurately in tests: release/tag creation succeeds, later release-please bookkeeping fails, and Ava still has a well-defined durable publication state instead of losing the release event
- [x] #2 The implementation distinguishes the external `other side closed` transport failure from the preventable workflow coupling that allowed it to strand publication
- [x] #3 Ava publication eligibility is derived from verified durable release identity/state and is not solely dependent on a fresh `release_created == true` action output
- [x] #4 Tests cover interruption after tag/release creation and prove a subsequent normal retry or explicit recovery run reaches the publication steps even when release-please no longer reports a newly-created release
- [x] #5 Recovery verifies tag, version, accepted qualification, exact source revision, and existing GitHub Release state before assembling or publishing
- [x] #6 Recovery never deletes, moves, or recreates a correct existing tag merely to retrigger release-please
- [x] #7 Release assembly is still performed reproducibly from the exact tagged source, conformance is checked, assets are attested, and only matching assets are uploaded
- [x] #8 Repeated publication/recovery attempts are idempotent across missing-release, draft or partial-release, and already-published states, with mismatches failing closed
- [x] #9 The design evaluates whether release creation/publication can be separated from next-release-PR maintenance, or otherwise prevents a later release-please bookkeeping failure from suppressing an already-valid publication path
- [x] #10 The GitHub Actions manual recovery entry point is documented and can be operated through the repository's maintained Actions path
- [x] #11 The authoritative release procedure documents diagnosis, prevention strategy, automatic retry boundaries, and manual recovery for partial post-merge publication
- [x] #12 The alpha.17 partial publication incident is recovered through the maintained path and the resulting immutable release is verified; AVA-5638 records the successful end-to-end proof
<!-- AC:END -->

## Implementation evidence

- `.github/workflows/release-please.yml` splits release creation (`skip-github-pull-request`) from later next-release-PR maintenance (`skip-github-release`) and never gates publication on `release_created`.
- `internal/release/publication.py` resolves exact durable tag identity and plans compatible asset reuse by GitHub SHA-256 digest.
- Recovery checks out current maintained publication tooling separately from the exact immutable tagged source, then runs release identity validation, qualification acceptance, the maintained release suite, reproducible double assembly, conformance, attestation, missing-only upload, publication, and immutable release verification from that tag.
- `internal/release/tests/test_publication.py` models missing, partial draft, mismatched, already-published, non-release, and stale-tag states. `test_publication_workflow.py` freezes the split release-please and explicit recovery contract.
- `internal/release/publication-recovery.md` records the alpha.17 diagnosis, hardened normal path, retry boundaries, and manual recovery procedure.
- Live recovery run `33859391629` successfully resolved `v1.0.0-alpha.17` to `fa51a2b1578443115e076bfb54edd66eec4dbc1e`, validated its accepted qualification, passed all 309 maintained release tests, and reproduced/conformed the release twice. It then exposed that GitHub's release-by-tag endpoint does not expose drafts: the workflow mistook the existing draft as missing, created a second empty compatible draft, and failed before any asset upload or publication.
- Follow-up recovery hardening enumerates the Releases collection including drafts, validates every same-tag candidate before mutation, preserves the most complete compatible draft, deletes only redundant compatible drafts by release ID, fails closed on any mismatch or published-state ambiguity, and performs draft upload/publication mutations by exact release ID rather than tag lookup.
- The maintained recovery path subsequently completed alpha.17 publication. GitHub reports `v1.0.0-alpha.17` at revision `fa51a2b1578443115e076bfb54edd66eec4dbc1e` as published, immutable, and populated with the expected release assets.

## Resolution

The parked boundary is cleared. The follow-up recovery fix is merged and the live alpha.17 incident has been recovered through the maintained publication path. The task is complete and AVA-5640 is unblocked.