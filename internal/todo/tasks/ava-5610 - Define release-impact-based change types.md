---
id: ava-5610
title: "Define release-impact-based change types"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5610
---

## Description

Clarify that Conventional Commit types and SemVer release impact are determined by changes to the supported Ava distribution rather than implementation novelty or repository location.

## Migrated task record

Historical metadata: phase 5 finding 10, `required-v1`, blocking release candidate, affected revision `c2c1d84e05f7be16fbbb4442e44c594a7007ce01`, completed after implementation.

### Observed behavior and root cause

PR #75 added a repository-only synthetic qualification fixture but was initially titled `feat: add synthetic qualification vault`, which would imply a releasable minor feature even though no installed content, public contract, release asset, or supported behavior changed. The title was corrected to `test(release): add synthetic qualification vault`.

Release instructions listed releasable and non-releasable Conventional Commit types but did not clearly say classification must follow supported distribution impact rather than implementation novelty, size, or source path. Since pull-request titles become canonical squash commits, this could create unintended releases and false changelog/SemVer claims.

### Approved scope and completion criteria

The policy had to classify observable impact on installed content, public contracts, release assets, installer/updater behavior and supported agent behavior; reserve `feat` for backward-compatible distributed capability; keep repository-only tests/fixtures/qualification/CI/docs/maintenance non-releasable when they do not change output/guarantees; preserve the converse that `internal/` changes can still be releasable when they affect distribution; align with public SemVer; provide positive/negative examples across feat/fix/test/docs/chore/breaking; and freeze the distinction in validation/tests.

### Resolution evidence

`internal/release/release-please.md` now treats PR titles as release-impact claims based on observable supported-distribution impact. It reserves `feat` for distributed capability, keeps repository-only qualification/maintenance non-releasable when output is unchanged, and explicitly allows internal implementation to remain releasable when it changes produced assets, behavior or guarantees. The release procedure points to `distribution/versioning.md` for PATCH/MINOR/MAJOR semantics.

`internal/release/fixtures/release-please-policy.json` contains maintained cases across `feat`, `fix`, `test`, `docs`, `chore`, and breaking changes, including the synthetic-vault example. `internal/release/tests/test_release_please.py` verifies expected type/release level, includes internal-source releasable and repository-only non-releasable cases, and freezes documented policy language. The test is part of `internal/release/test.sh`; release logs and roadmap state recorded completion.

Release follow-up required a maintained release-please dry run or equivalent fixture proving a non-releasable repository-only PR does not advance a release proposal while a distribution-facing `feat` does.