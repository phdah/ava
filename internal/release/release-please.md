---
type: Internal Release Procedure
title: Ava Release Automation
description: Defines release-please version proposals, release-local edge completion, semantic-impact assessment, recursive qualification, and immutable publication.
tags: [internal, releases, automation, release-please, conventional-commits]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-05T09:30:00+02:00
---

# Ava Release Automation

Ava uses release-please as a single-package coordinator. It proposes versions, updates `CHANGELOG.md`, `version.txt`, and the release manifest, creates immutable tags and draft releases, and publishes only after every maintained gate succeeds.

## Merge-boundary contract

Ordinary pull request titles use:

```text
<type>(<optional-scope>)!: <subject>
```

Releasable types are `feat`, `fix`, `perf`, and `revert`. Other supported types are internal-only unless marked breaking.

Ordinary implementation PRs do not predeclare a release version or upgrade edge. They may be squash merged so the reviewed Conventional Commit PR title becomes one canonical release-classified commit on `main`.

Release Please PRs are the exception. After final qualification and explicit acceptance, merge the Release Please PR with **Create a merge commit**. Do not squash or rebase it. Qualification is bound to an exact commit on the release-PR branch, and the merge commit must retain that qualified commit in the published revision's ancestry. The generated release PR footer repeats this requirement at the merge boundary.

## Select change types from supported distribution impact

A pull request title is a release-impact claim. Select the Conventional Commit type from what merging the pull request changes in the supported Ava distribution, not from how new, substantial, or technically interesting the repository implementation is.

Assess observable impact on:

- installed Ava-managed content
- public distribution, versioning, ownership, routing, workflow, role, guidance, or state contracts
- release assets and the information they expose
- installer or updater behavior and guarantees
- supported agent routing, authority, validation, migration, or other intended behavior

Repository location is not the classification boundary. A change under `internal/` is non-releasable only when its effect remains repository-only. An internal assembler, validator, or release-tooling change still uses `feat`, `fix`, `perf`, or a breaking marker when it changes the resulting distribution, accepted behavior, or supported guarantee.

Implementation novelty alone never justifies `feat`. Use `feat` only for backward-compatible capability exposed through the Ava distribution or its supported behavior. Use `fix` when the supported distribution previously behaved incorrectly, `perf` when a supported behavior becomes materially more efficient without changing its contract, and `revert` when reverting a releasable change restores supported distribution behavior.

Use non-releasable types such as `test`, `docs`, `ci`, `build`, `refactor`, or `chore` when the change only affects repository maintenance, qualification, fixtures, CI, internal documentation, or development structure and does not alter produced release assets or supported Ava behavior. Mark any incompatible supported distribution change as breaking regardless of source location or ordinary type.

The public [Ava Versioning and Compatibility](../../distribution/versioning.md) contract remains authoritative for whether an observable distribution change is PATCH, MINOR, or MAJOR. This release procedure maps Conventional Commit claims to release-please; it does not redefine compatibility.

Representative classifications:

| Pull request title | Resulting impact | Release level |
|---|---|---|
| `feat(host): add opt-in managed host support` | Backward-compatible capability exposed by the distribution | minor |
| `fix(installer): preserve project-owned host configuration` | Corrects supported installer behavior, even though the implementation is internal | patch |
| `test(release): add synthetic qualification vault` | Adds repository-only qualification fixtures and tests | none |
| `docs(release): clarify internal qualification procedure` | Changes maintainer-only documentation without changing supported behavior | none |
| `chore(internal): reorganize roadmap bookkeeping` | Changes repository maintenance state only | none |
| `feat!: replace the public manifest contract` | Changes a supported public contract incompatibly | major |

The synthetic qualification vault case is intentionally `test(release)`, not `feat`, even though the fixture is a substantial new repository capability. Conversely, an implementation under `internal/release/` is not automatically internal-only when it changes the release users install or the guarantees Ava makes about it.

## Release PR contract

A newly created release PR is intentionally incomplete. Its policy check remains red until one target release record exists and passes recursive chain validation.

The maintainer completes it by creating only:

```text
internal/release/catalogs/<target>.json
```

That file contains exactly one `<previous> -> <target>` edge, only guidance and migrations introduced by that edge, and any source-retirement decisions made by the target release. Earlier release records remain untouched.

This also applies to the first published release. `1.0.0-alpha.1.json` owns `0.0.0 -> 1.0.0-alpha.1`; there is no release-without-an-edge bootstrap exception.

The gate validates:

- target and channel identity
- exactly one target release record changed relative to the release PR base
- the edge starts at the immediately previous release
- the first release starts at the `0.0.0` bootstrap sentinel
- the record contains only transition-local guidance and migration references
- guidance metadata, digest, and artifact integrity
- explicit, valid source-retirement decisions
- recursive continuity through every intermediate release record
- unique composed paths for every retained source

`upgrade-impact.json`, `upgrade-sources.txt`, cumulative catalog snapshots, and published direct edges are not current authoring inputs.

## Semantic-impact assessment

Before authoring the adjacent edge, the release author reviews the exact previous-to-target managed delta and answers three separate questions:

1. **Managed delta:** What Ava-managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed?
2. **Project-owned compatibility:** Could valid active project-owned context remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible because of that managed delta?
3. **Required reconciliation:** If project-owned compatibility can be affected, what bounded project-owned concepts must the Upgrade Role inspect or reconcile before semantic compatibility may advance?

Set `semantic_review_required: true` when project-owned context may require semantic inspection or reconciliation because of the managed delta. The absence of a deterministic project-file migration does not justify `false`. Project-owned roles, workflows, shared instructions, indexes, host entrypoints, metadata, links, and other active instruction relationships can encode assumptions that remain structurally valid while becoming incompatible.

Set `semantic_review_required: false` when the reviewed managed delta cannot make supported project-owned context require semantic reconciliation. A managed behavior change alone does not automatically require semantic review. The author must be able to explain why existing valid project-owned context remains compatible and, when the previous semantic state is complete, why compatibility may advance mechanically.

Assessment starts from the changed managed contracts and follows only plausible active project-owned dependencies. Do not replace bounded discovery with a blanket scan of unrelated project content.

The release PR body or review record must contain an explicit semantic-impact rationale for both `true` and `false` decisions. The release author owns the initial classification and evidence. The reviewer or approver confirms that the rationale follows the project-owned compatibility test before accepting the edge.

For `true`, transition-local upgrade guidance must identify:

- the affected project-owned concepts
- bounded discovery conditions for finding potentially incompatible active context
- completion criteria that prove reconciliation is complete

For `false`, no semantic guidance is authored for that edge. Existing deterministic validation enforces representation consistency between the boolean and guidance references. It does not infer whether semantic review is needed and must not replace maintainer judgment.

## Assembly and publication

The release workflow sets:

```text
AVA_UPGRADE_CATALOG=internal/release/catalogs/<target>.json
```

The reviewed assembler follows `edge.from` recursively through earlier release records, stages the guidance referenced by those edges, and derives installer-compatible projections for each retained source. The cumulative graph exists only during validation and assembly.

After merge, automation verifies the exact tag and source SHA, proves that only the target record was added, reruns the complete `0.0.0`-to-target chain validation and repository suite, assembles twice, compares digests, validates conformance, attests assets, uploads without clobbering, and publishes the existing draft.

The same release-local record rule applies to alpha, beta, release candidate, stable, patch, minor, and major releases.
