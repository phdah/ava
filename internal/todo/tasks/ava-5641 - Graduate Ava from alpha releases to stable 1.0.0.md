---
id: ava-5641
title: Graduate Ava from alpha releases to stable 1.0.0
status: To Do
assignee: []
created_date: '2026-09-05 00:23'
updated_date: '2026-09-05 00:23'
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

Graduate Ava from the alpha prerelease line to the real stable `1.0.0` release line, then prove that the ordinary stable release workflow works by producing `1.0.1` through Release Please and the maintained release gates.

Ava is currently at `1.0.0-alpha.18`. After AVA-5640/PR #126 is merged, the existing alpha release process should first produce one final fully-qualified prerelease, expected to be `v1.0.0-alpha.19`. That successful release is a hard gate for this migration. If Release Please proposes a different next prerelease version, stop and resolve the version-state discrepancy rather than silently proceeding.

After the final alpha release is proven, intentionally reset the public prerelease release history: remove every alpha GitHub Release and every corresponding alpha tag, including stale or duplicate draft releases. Then bootstrap a clean stable `v1.0.0` release from the verified repository state. The stable bootstrap may require a one-time manual publication path because the normal release-to-release qualification assumes a previous release exists.

The migration is not complete when `1.0.0` exists. It must also switch Ava's maintained Release Please configuration and release gates to stable semantic versions and exercise the resulting normal path end-to-end by producing and publishing `1.0.1` from `1.0.0`.

## Required behavior

1. Treat merged AVA-5640/PR #126 as a prerequisite so the stable cutover starts from the cleaned, single maintained release implementation.
2. Produce one final release through the current prerelease flow, expected to be `v1.0.0-alpha.19`, and require normal qualification, explicit acceptance, publication, immutable release verification, and complete assets before any alpha cleanup begins.
3. Before destructive cleanup, record the exact final-alpha source revision and any checksums, qualification evidence, catalog/guidance state, or other deterministic inputs needed to bootstrap the stable baseline safely.
4. Change maintained release configuration from alpha prerelease versioning to ordinary stable semantic versioning. Remove live assumptions that every release is `1.0.0-alpha.N` or that `prerelease`/`alpha` settings remain enabled.
5. Delete every GitHub Release belonging to the alpha line, including published releases and any stale, duplicate, or draft alpha release objects.
6. Delete every corresponding alpha Git tag/ref, including `v1.0.0-alpha.*`, and verify that no alpha release object or alpha tag remains in GitHub after cleanup.
7. Audit repository release state after the deletion. Alpha-specific material may remain only when it is required immutable historical evidence; it must not remain as live release configuration, an active release dependency, or an alternative release path.
8. Bootstrap a clean `v1.0.0` stable release from the exact intended stable baseline. If the normal workflow cannot create the first stable release because it requires a previous release, implement or use an explicitly bounded one-time bootstrap/manual path rather than weakening the permanent release gates.
9. The `v1.0.0` release must use the normal reproducible assembly, conformance, attestation, asset publication, and immutable release verification guarantees that are applicable without a previous stable release.
10. After `v1.0.0` is established, ensure Release Please operates in stable mode and creates the next patch release as `1.0.1` from ordinary post-`1.0.0` changes.
11. Qualify `1.0.0 -> 1.0.1` through the normal release-to-release workflow, including the maintained upgrade edge where required, deterministic qualification, explicit user acceptance, merge, publication, and post-publication verification.
12. Remove any temporary bootstrap exception or one-off stable-seeding mechanism after `1.0.0` is established unless it has an independently justified permanent purpose. The normal maintained state after this task must be the ordinary stable Release Please + release qualification flow.
13. Update authoritative release documentation, tests, schemas, policies, examples, and boundary checks so stable releases are the canonical current behavior and alpha-specific operational assumptions cannot silently return.

## Hard constraints

- Do not delete alpha releases or tags until the final alpha release has completed successfully and the exact stable-bootstrap inputs have been captured.
- Treat deletion of alpha releases and tags as an intentional destructive reset. Inventory the complete target set first and fail closed if unexpected non-alpha releases/tags would be affected.
- Do not preserve an alpha GitHub Release or alpha tag merely for convenience. The intended public release history after the reset begins at `v1.0.0`.
- Do not permanently bypass qualification, reproducible assembly, attestation, or publication verification to create `1.0.0`. Any bootstrap exception must be one-time, narrow, explicit, and removed or disabled after use.
- `1.0.1` must be produced by the ordinary stable workflow, not by repeating the manual/bootstrap mechanism used for `1.0.0`.
- Stable release tags must resolve to the exact accepted revisions and published assets must come from those exact tagged sources.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 AVA-5640 is merged and the final alpha release, expected `v1.0.0-alpha.19`, is fully qualified, explicitly accepted, published, immutable, and populated with the expected assets before migration proceeds
- [ ] #2 The exact final-alpha revision and deterministic inputs needed for the stable bootstrap are recorded before any destructive release/tag deletion
- [ ] #3 Release Please and maintained release configuration are converted from alpha prerelease semantics to ordinary stable semantic versioning
- [ ] #4 Every alpha GitHub Release, including drafts/duplicates, is deleted and GitHub contains no remaining `1.0.0-alpha.*` release object
- [ ] #5 Every alpha Git tag/ref is deleted and GitHub contains no remaining `v1.0.0-alpha.*` tag
- [ ] #6 No alpha-only assumption remains in live release configuration, gates, documentation, tests, or runtime state; any retained alpha material is clearly non-operational historical evidence
- [ ] #7 A clean stable `v1.0.0` release is bootstrapped from the intended exact source revision with applicable reproducible assembly, conformance, attestation, asset publication, and immutable verification guarantees
- [ ] #8 Any one-time bootstrap/manual exception needed for `v1.0.0` is narrowly scoped and removed or disabled after the stable baseline exists
- [ ] #9 Release Please subsequently proposes `1.0.1` using stable version semantics without alpha/prerelease configuration
- [ ] #10 The `1.0.0 -> 1.0.1` transition passes the normal maintained release qualification and release-to-release/upgrade workflow with explicit user acceptance
- [ ] #11 `v1.0.1` is published through the ordinary stable workflow, immutable, points to the exact accepted revision, and contains the expected release assets
- [ ] #12 The final maintained repository state has stable `1.0.x` release behavior as the sole current release path, with regression coverage preventing accidental return to alpha release semantics
<!-- AC:END -->
