---
type: Internal Release Procedure
title: Ava Release Automation
description: Defines stable Release Please proposals, first-release qualification, adjacent stable upgrades, and immutable publication.
tags: [internal, releases, automation, release-please, conventional-commits]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-05T13:20:00+02:00
---

# Ava Release Automation

Ava uses Release Please as a single-package coordinator. Stable semantic versions are the maintained release channel. Release Please proposes versions, updates `CHANGELOG.md`, `version.txt`, and the release manifest, creates immutable tags and draft releases, and publishes only after every maintained gate succeeds.

Stable `1.0.0` is the root release. No supported release precedes it. The repository uses `0.0.0` only as an internal pre-release sentinel so Release Please can propose the first `1.0.0`; that sentinel is never published or installed.

## Merge-boundary contract

Ordinary pull request titles use:

```text
<type>(<optional-scope>)!: <subject>
```

Releasable types are `feat`, `fix`, `perf`, and `revert`. Other supported types are internal-only unless marked breaking.

Ordinary implementation PRs may be squash merged so the reviewed Conventional Commit PR title becomes one canonical release-classified commit on `main`.

Release Please PRs are the exception. After final qualification and explicit acceptance, merge the Release Please PR with **Create a merge commit**. Do not squash or rebase it. Qualification is bound to an exact commit on the release branch and the merge commit must preserve that commit in the published revision's ancestry.

## Select change types from supported distribution impact

A pull request title is a release-impact claim. Select the Conventional Commit type from what merging the pull request changes in the supported Ava distribution, not from implementation novelty or repository location.

Implementation novelty alone never justifies `feat`. Repository location is not the classification boundary. Internal release tooling can still be a `feat` or `fix` when it changes the produced distribution or supported release behavior, while repository-only tests, documentation, CI, and bookkeeping remain non-releasable.

Maintained examples:

- `feat(host): add opt-in managed host support` is a distribution capability and therefore a minor release.
- `fix(installer): preserve project-owned host configuration` is a supported distribution fix even though its implementation lives under internal release tooling.
- `test(release): add synthetic qualification vault` is repository-only and does not create a release.
- `docs(release): clarify internal qualification procedure` is repository-only and does not create a release.
- `chore(internal): reorganize roadmap bookkeeping` is repository-only and does not create a release.
- `feat!: replace the public manifest contract` is a breaking supported distribution change and therefore a major release.

The public [Ava Versioning and Compatibility](../../distribution/versioning.md) contract is authoritative for PATCH, MINOR, and MAJOR compatibility meaning.

## First Release Please PR: `1.0.0`

The first stable Release Please PR is a root-release bootstrap, not an upgrade.

It must satisfy all of these conditions:

- base repository version is the internal `0.0.0` sentinel,
- target version is exactly `1.0.0`,
- stable Release Please configuration is active,
- no `internal/release/catalogs/1.0.0.json` exists,
- no previous-release source is supplied to qualification,
- assembled `ava-release.json` contains an empty `upgrade_paths.edges` array,
- final qualification is target-only and reaches explicit user acceptance.

There is no semantic transition review and no upgrade guidance for `1.0.0` because no supported source release exists.

## Later Release Please PRs

Starting with `1.0.1`, a newly created release PR is intentionally incomplete until the maintainer adds exactly one release-local record:

```text
internal/release/catalogs/<target>.json
```

That record contains exactly one `<previous> -> <target>` edge and only the guidance, migrations, and source-retirement decisions introduced by that transition. Earlier stable release records remain immutable.

The release gate validates:

- target and stable channel identity,
- the edge starts at the immediately previous supported release,
- exactly the target release record changes relative to the Release Please PR base,
- transition-local guidance and migration references,
- recursive stable-line continuity,
- unique composed paths for every retained supported source.

## Semantic-impact assessment

Semantic-impact assessment applies only when a source release exists. Before authoring a later adjacent edge, the maintainer reviews the exact previous-to-target delta and records a rationale. A managed behavior change is evidence to inspect, not an automatic semantic result. The presence or absence of deterministic project-file migrations is also evidence, not the decision itself.

### Managed delta

Describe the exact change to Ava-managed files, installer behavior, schemas, routing, lifecycle behavior, or other managed contracts.

### Project-owned compatibility

Determine whether that managed delta can invalidate project-owned meaning or behavior, including roles, workflows, shared instructions, indexes, host entrypoints, or other project-owned extensions.

### Required reconciliation

If project-owned compatibility can be affected, define bounded discovery conditions, completion criteria, and reviewed guidance. Otherwise record the reviewed rationale for why compatibility advances mechanically without guidance.

`1.0.0` has no source release, so this transition-specific assessment is not applicable to the root release.

## Assembly

For `1.0.0`, assembly runs without an upgrade catalog and emits zero supported upgrade edges.

For every later release, the workflow supplies the target release-local catalog record. The reviewed assembler follows stable adjacent records recursively and generates installer-compatible direct projections for retained supported sources.

## Publication

After a Release Please PR is merge-committed, automation verifies the exact tag and source SHA, revalidates accepted qualification, runs the maintained suite, assembles twice, compares digests, validates conformance, attests assets, uploads without clobbering, publishes the exact draft, and verifies immutability.

The supported release history therefore begins at `v1.0.0`. All future immutable compatibility history is derived from stable adjacent records beginning with `1.0.0 -> 1.0.1`.
