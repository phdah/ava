---
id: ava-5641
title: Graduate Ava from alpha releases to stable 1.0.0
status: In Progress
assignee: []
created_date: '2026-09-05 00:23'
updated_date: '2026-09-05 17:19'
labels:
  - internal
  - roadmap
  - release
  - stable
  - v1
  - migration
  - release-please
milestone: m-0
dependencies:
  - ava-5640
references:
  - ava-5640
type: enhancement
ordinal: 6640
---

## Description

Graduate Ava from the prerelease development line to the real stable `1.0.0` release line, then prove that the ordinary stable release workflow works by producing `1.0.1` through Release Please and the maintained release gates.

The public prerelease Releases and tags were intentionally removed after their final publication and evidence capture. The stable-line design was subsequently tightened: `1.0.0` is a fresh root release, not an upgrade from the final prerelease. No prerelease edge, source release, semantic-transition state, catalog history, qualification history, or bootstrap reconstruction is retained in the operational stable repository state. Development history remains only in task records and Git history.

Stable `1.0.0` therefore has zero supported upgrade sources. The first permanent immutable adjacent edge is `1.0.0 -> 1.0.1`.

Publishing `v1.0.0` also closes the pre-1.0 roadmap era. Once `v1.0.0` is fully qualified, explicitly accepted, published, immutable, and verified, every roadmap task already `Done` must move from `internal/todo/tasks/` into Backlog.md's `internal/todo/completed/` directory using the native completed-task workflow. Unfinished work must not move.

The migration remains active through the `1.0.1` proof. AVA-5641 is not complete merely because `1.0.0` exists.

## Required behavior

1. Start from merged AVA-5640/PR #126 and the single maintained release implementation.
2. Complete the final prerelease publication and capture sufficient evidence before destructive cleanup.
3. Inventory the complete prerelease GitHub Release/tag deletion set and fail closed on unexpected objects.
4. Delete every prerelease Release object and tag in the frozen target set and independently verify none remain publicly.
5. Switch Release Please to stable semantics with `1.0.0` as the first supported release.
6. Purge prerelease operational lineage from the repository working tree outside task history: release catalogs, transition guidance, qualification runs/acceptance history, semantic-transition evidence, reconstruction/reset tooling, release-history evidence, changelog history, and maintained documentation references.
7. Treat repository `0.0.0` only as an internal Release Please sentinel before the first stable PR. It must never be a published release, tag, installed version, or upgrade edge.
8. Bootstrap `v1.0.0` as a source-less root release. It must have no release-local catalog record and an empty `upgrade_paths.edges` inventory.
9. Qualify `v1.0.0` through all applicable deterministic target-only checks, including fresh install, mature-project preservation, managed-damage handling, conformance, reproducible assembly, attestation, publication, and immutable verification. Upgrade resume/abort/rollback and semantic-transition checks are inapplicable because no supported source exists.
10. Require explicit user acceptance of the exact final `1.0.0` qualification run before merging the Release Please PR.
11. Merge Release Please PRs with a merge commit so accepted qualification ancestry is preserved. Ordinary implementation PRs may continue to squash merge.
12. After verified `v1.0.0` publication, migrate every roadmap task already `Done` to `internal/todo/completed/` while preserving task history. Leave `To Do`, `In Progress`, and `Parked` tasks active.
13. Update the roadmap validator and guidance so `completed/` is the canonical finished-task location.
14. Remove the temporary first-release seeding state after `1.0.0` is established unless it has an independently justified permanent purpose.
15. Produce `1.0.1` from ordinary post-`1.0.0` work using normal stable Release Please behavior.
16. Qualify `1.0.0 -> 1.0.1` through the ordinary adjacent-edge workflow, including semantic-impact assessment where applicable, deterministic upgrade qualification, explicit user acceptance, merge-commit publication, attestation, and immutable verification.

## Hard constraints

- The public release history begins at `v1.0.0`.
- The stable operational repository state must not depend on or describe the removed prerelease release lineage outside task history.
- Do not create an upgrade edge into `1.0.0`.
- Do not synthesize a fake previous release merely to reuse the ordinary upgrade gate.
- Do not bypass deterministic qualification, reproducible assembly, conformance, attestation, explicit acceptance, or immutable publication.
- Do not move completed roadmap tasks until `v1.0.0` itself is published and verified.
- `1.0.1` must use the ordinary stable adjacent-release workflow.
- Stable Release Please PRs must preserve the exact accepted release-branch revision in merge ancestry.

## Implementation notes

- PR #126 merged AVA-5640 and established the single maintained release implementation.
- The final prerelease was fully qualified, explicitly accepted, published, and verified immutable before cleanup.
- Release PR #129 was accidentally squash merged; PR #130 repaired that publication with a bounded recovery and permanently documented the merge-commit requirement for Release Please PRs.
- Final prerelease publication evidence and the destructive deletion inventory were captured before cleanup.
- PR #133 switched Release Please to stable semantics and installed a fail-closed deletion workflow.
- The destructive reset deleted all 19 recorded prerelease GitHub Release objects and all 19 recorded prerelease tag refs. Independent checks then showed zero public Releases and zero matching prerelease refs.
- The original transition design reconstructed the final prerelease as a source for `1.0.0`. That design was rejected in favor of a clean stable root.
- PR #134 removed the old operational lineage, reset checked-in qualification state to `bootstrap-to-1.0.0`, made root qualification target-only, refreshed the README and changelog, and added regression coverage preventing old release-line identifiers outside task history.
- `v1.0.0` was finally qualified, explicitly accepted, merge-committed at `88ee933c8e008b464562b07ffbf04a18e59c4d32`, published on 2026-09-05, verified immutable, and populated with all seven expected assets.
- A stale post-publication Release Please PR #140 proposed `1.0.0` again because the one-time package `release-as` override remained configured. PR #140 was closed without merge.
- The post-bootstrap cleanup removes `bootstrap-sha`, `initial-version`, and package `release-as`. `force-tag-creation` remains because Ava intentionally uses draft Releases and needs the durable tag to exist immediately for subsequent Release Please discovery.
- AVA-5641 remains `In Progress` until `v1.0.1` proves the ordinary stable workflow.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The final prerelease is fully qualified, explicitly accepted, published, immutable, and populated with the expected assets before migration proceeds
- [x] #2 Exact evidence and a fail-closed deletion inventory are captured before destructive public cleanup
- [x] #3 Release Please is configured for ordinary stable semantic versioning with `1.0.0` as the initial stable release
- [x] #4 Every inventoried prerelease GitHub Release object is deleted and independent verification finds no public prerelease Release remaining
- [x] #5 Every inventoried prerelease Git tag/ref is deleted and independent verification finds no matching prerelease tag remaining
- [ ] #6 No prerelease operational lineage remains in live release configuration, catalogs, guidance, qualification state/history, documentation, tests, runtime state, or changelog outside task history
- [x] #7 A clean source-less stable `v1.0.0` root release passes applicable qualification, reproducible assembly, conformance, attestation, publication, and immutable verification
- [x] #8 Any first-release-only seeding mechanism is removed or reduced to a justified permanent root-release contract after `v1.0.0` exists
- [ ] #9 After verified `v1.0.0` publication, every roadmap task already in `Done` state is moved to `internal/todo/completed/` with complete history preserved
- [ ] #10 Roadmap documentation, validator, and tests recognize `completed/` as canonical finished work and leave unfinished statuses active
- [ ] #11 Release Please subsequently proposes `1.0.1` using ordinary stable version semantics
- [ ] #12 The `1.0.0 -> 1.0.1` transition passes the normal adjacent-edge qualification flow with explicit user acceptance
- [ ] #13 `v1.0.1` is published through the ordinary stable workflow, immutable, points to the exact accepted revision, and contains the expected assets
- [ ] #14 The final maintained repository state has stable `1.0.x` release behavior as the sole current release path and regression coverage against reintroducing the removed pre-stable operational lineage
<!-- AC:END -->
