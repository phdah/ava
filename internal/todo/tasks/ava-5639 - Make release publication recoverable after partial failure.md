---
id: ava-5639
title: Make release publication recoverable after partial failure
status: To Do
assignee: []
created_date: '2026-09-02 22:46'
labels:
  - internal
  - roadmap
  - release
  - publication
  - reliability
  - github-actions
milestone: m-0
dependencies: []
references:
  - ava-5638
type: enhancement
ordinal: 6638
---

## Description

Make Ava's post-merge publication workflow safely resumable when release-please creates only part of the release state before failing.

The alpha.17 release exposed the failure mode: release-please created tag `v1.0.0-alpha.17` at merge commit `fa51a2b1578443115e076bfb54edd66eec4dbc1e`, then workflow run `33680822686` failed with `other side closed` before Ava's validation, assembly, attestation, asset upload, and publication steps ran. Retrying the job succeeded superficially, but release-please returned `release_created == false`, causing every publication step guarded by that output to skip. No GitHub Release object was present afterward.

A correct recovery path must preserve the accepted immutable release identity and resume publication without deleting or moving a correct tag merely to make release-please emit a fresh release event.

## Required behavior

1. Detect a partially-created target release after the release PR has merged, including at least the state where the correct tag exists but the GitHub Release object or release assets are missing.
2. Before resuming, prove the target tag points to the exact accepted release merge revision and that the corresponding qualification acceptance is valid.
3. Resume the same validation, reproducible assembly, conformance, attestation, asset upload, and publish sequence from the exact tagged source even when `release_created` is false.
4. Make retry/recovery idempotent: rerunning after partial success must reuse compatible state or fail closed rather than duplicate, overwrite, retag, or silently publish mismatched assets.
5. A fully published matching release should be a safe no-op or explicit already-complete result.
6. `workflow_dispatch` or another explicit GitHub Actions recovery entry point must be capable of finishing a known partially published release without requiring local or user-hosted release tooling.
7. Document the recovery procedure in the authoritative internal release flow.
8. Preserve normal release-please creation behavior for the first successful post-merge run.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Tests cover an interruption after tag creation but before publication and prove a subsequent recovery run reaches the normal publication steps even when release-please no longer reports `release_created == true`
- [ ] #2 Recovery verifies tag, version, accepted qualification, and exact source revision before assembling or publishing
- [ ] #3 Recovery never deletes, moves, or recreates a correct existing tag merely to retrigger release-please
- [ ] #4 Release assembly is still performed reproducibly from the exact tagged source, conformance is checked, assets are attested, and only matching assets are uploaded
- [ ] #5 Repeated recovery attempts are idempotent across missing-release, draft or partial-release, and already-published states, with mismatches failing closed
- [ ] #6 The GitHub Actions manual recovery entry point is documented and can be operated from a repository-connected maintainer session
- [ ] #7 The authoritative release procedure documents how to diagnose and recover partial post-merge publication
- [ ] #8 The alpha.17 partial publication incident is recovered through the maintained path and the resulting immutable release is verified; AVA-5638 records the successful end-to-end proof
<!-- AC:END -->
