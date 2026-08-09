---
type: Internal Development Task
title: Normalize and enforce adjacent-edge release authoring
description: Convert the active historical upgrade graph to one canonical adjacent-edge catalog and require every future release to append exactly one new adjacent edge.
tags: [internal, roadmap, dogfood, releases, upgrades, validation]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 11
classification: blocker
blocks: next-prerelease
affected_version: general release process, exposed by 1.0.0-alpha.12
generated:
  by: agent:openai-chatgpt
  at: 2026-08-09T16:25:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T16:42:00+02:00
---

# Normalize and Enforce Adjacent-Edge Release Authoring

## Architectural scope

This is a general release-process correction, not a repair limited to `1.0.0-alpha.12`.

The accepted adjacent-edge contract applies to every future Ava prerelease and stable release. The active repository must contain one canonical upgrade history made entirely from immutable adjacent edges. A release inherits that history unchanged and authors exactly one new edge from the immediately previous released version to the proposed target. Older supported source versions reach the target only through deterministic composition of retained adjacent edges.

The existing active historical upgrade graph must also be normalized. Every retained supported transition up to the current release must be represented by its consecutive adjacent edge, with semantic obligations attached to the transition where the managed contract actually introduced them. Active release preparation must not retain a parallel cumulative source-to-target representation.

Already published tags, GitHub Release assets, checksums, attestations, and manifests are immutable and must not be rewritten. Legacy direct source-to-target data may remain readable when consuming those historical releases. Repository-local legacy material may remain only as clearly archival evidence that cannot be selected by release authoring or qualification.

## Observed behavior

The `1.0.0-alpha.12` release proposal contained the implementation that introduced adjacent-edge composition, but release completion still recreated target-specific guidance and source-to-target assessments for multiple earlier prereleases.

The release added cumulative guidance from alpha.5 through alpha.9 directly to alpha.12 instead of inheriting earlier reviewed obligations and adding only alpha.11 to alpha.12. The release checks passed because the compatibility transition still accepted the older representation for an in-progress proposal.

This proved that the repository currently distinguishes neither clearly nor mechanically between:

- importing historical direct source-to-target data so an already published release remains readable
- maintaining the canonical historical graph used by future releases
- authoring the one new adjacent edge for a proposed release

A passing release policy check can therefore endorse a representation that the authoritative architecture says maintainers must no longer create.

## Reproduction and evidence

- PR #76 completed the accepted adjacent-edge model and states that each release appends and reviews only its new adjacent edge while inherited edges retain immutable identity.
- PR #74 prepared `1.0.0-alpha.12` with newly authored cumulative guidance directories from multiple older sources directly to alpha.12.
- The release policy and Python checks passed even though the proposal used the superseded cumulative authoring path.
- The active repository did not contain a fully normalized canonical adjacent-edge history for the retained supported release range, so the maintainer could still fall back to cumulative `upgrade-impact.json` authoring.
- The release was merged, demonstrating that documentation, repository state, procedure, tests, and validation did not make the intended authoring mode operationally unambiguous.

## Classification

This finding is a `blocker` for the next prerelease.

Without a correction, every future release can repeat the same mistake, grow cumulative guidance quadratically, rewrite previously reviewed semantic obligations, or choose between two active representations of the same upgrade history. The next release must not be prepared until historical state has one canonical adjacent representation and the release gate enforces exactly one new adjacent edge.

## Root cause

The adjacent-edge implementation preserved backward read compatibility and supplied generic catalog tooling, but it did not complete the transition of real release history or establish a hard authoring boundary.

Release instructions still contain legacy source-to-target language, release completion can still select the old `upgrade-impact.json` workflow, active repository state still contains cumulative target-specific material, and validation accepts the legacy representation without proving that it is immutable historical input rather than newly authored release state.

The test suite proves graph composition and inherited identity, but it does not make the release delta itself strict enough. It can accept a valid final graph without proving that the proposal inherited all prior edges unchanged and added exactly one new adjacent edge.

The process therefore relied on the maintainer to infer both that backward compatibility was not an authoring option and that historical obligations should be reconstructed through adjacent composition. Those inferences are unsafe and contradict deterministic release preparation.

## Required historical normalization

The resolving implementation must perform a one-time transition of active repository state:

1. Inventory every retained supported historical Ava release and every published direct source-to-target edge, migration, semantic decision, and guidance artifact.
2. Build one canonical adjacent edge for every retained transition between consecutive releases.
3. Derive each adjacent edge from the exact managed delta and reviewed semantic impact introduced by that transition.
4. Attach an existing semantic obligation to the earliest adjacent edge whose managed contract introduced it. Do not copy it onto later no-impact edges merely because a cumulative release repeated it.
5. Preserve semantic meaning for every retained supported source by proving that adjacent composition yields the intended effective migrations and guidance obligations.
6. Assign canonical edge and guidance digests and freeze them as inherited history for later releases.
7. Replace active repository-local cumulative source-to-target preparation state with the normalized catalog.
8. Remove, relocate, or clearly mark legacy repository-local cumulative guidance and assessments as archival compatibility evidence so release tooling cannot discover or select them as active inputs.
9. Leave immutable published releases untouched and retain read compatibility only where required to consume their original assets.
10. Document any historical case that cannot be converted without a semantic decision and block completion until that decision is explicit.

Normalization must not invent new project-owned obligations. It must preserve reviewed meaning while assigning each obligation to its correct adjacent transition.

## Required future release process

After normalization, every Ava prerelease and stable release must follow this process:

1. Load the latest canonical self-contained adjacent-edge catalog.
2. Preserve every inherited edge, digest, guidance record, and referenced guidance artifact exactly.
3. Author exactly one new edge from the immediately previous released Ava version to the proposed target.
4. Assess only the managed delta introduced by that new adjacent edge for project-owned semantic impact.
5. Add semantic guidance only when that new adjacent edge requires project-owned reconciliation.
6. Do not recreate cumulative source-to-target assessments, migrations, or guidance for older supported sources.
7. Retain or explicitly retire supported entry points without rewriting the inherited path that serves them.
8. Resolve older source versions through the unique composed adjacent-edge path.
9. Qualify every retained supported source against the composed path, including semantic compatibility lag, without producing target-specific duplicate guidance.
10. Treat legacy direct source-to-target data as read-only historical compatibility input, never as a valid authoring mode for a new release.

A release with no project-owned semantic impact still authors its one adjacent edge with an explicit reviewed no-impact decision. It does not omit the edge, and it does not restate older no-impact or impact decisions against the new target.

## Strict release-delta validation

Release validation and tests must reason about the difference between the inherited catalog and the proposed catalog, not only whether the proposed final graph is valid.

For every normal release proposal, the release policy must require all of the following:

- the proposed catalog has exactly one edge that is not present in the inherited catalog
- that edge is exactly `previous_release -> proposed_target`
- no inherited edge was added, removed, reordered semantically, or modified
- no inherited edge digest, guidance record, guidance digest, migration reference, or guidance artifact changed
- no second target-reaching shortcut or cumulative source-to-target edge was introduced
- no new cumulative guidance or semantic assessment was added for an older source
- supported-source changes are limited to retaining existing entries, adding the immediately previous release when appropriate, or explicitly retiring entries under the accepted policy

The gate must fail when the release authors zero new edges, more than one new edge, a skipped edge, a non-adjacent edge, a shortcut edge, or a graph that is compositionally valid but was produced through an invalid release delta.

## Scope

The resolving PR must update and align the general release process, not patch one version-specific fixture. It must include:

- normalization of the active historical upgrade graph into canonical adjacent edges
- release-maintainer instructions and release PR procedure that prescribe the exact adjacent-edge workflow
- removal or correction of conflicting instructions that require cumulative source-to-target assessment for new releases
- an explicit transition rule identifying immutable published representations that remain readable while making catalog authoring mandatory
- release preparation tooling that starts from inherited catalog state and accepts only one newly authored adjacent edge
- release policy validation based on an inherited-versus-proposed catalog diff
- validation that rejects cumulative target-specific guidance or assessments in a new release
- validation that rejects modified inherited edges, digests, guidance metadata, guidance artifacts, or migration references
- validation that rejects a missing or non-adjacent previous-release-to-target edge
- validation that rejects target-reaching shortcuts even when unique path resolution would otherwise succeed
- validation that permits supported-source retirement only through the explicit catalog contract
- validation of unique composed managed and semantic paths for every retained supported source
- clear failure messages that tell a maintainer to author one adjacent edge rather than fall back to the legacy workflow
- cleanup or archival rules for repository-local release preparation state left by the alpha.12 incident, without changing immutable published release assets

The implementation must apply to alpha, beta, release-candidate, stable, patch, minor, and major releases. Channel labels and SemVer magnitude must not change the adjacent authoring rule.

## Required regression coverage

The resolving implementation must add focused tests that prove the release-delta rule, including:

- zero newly authored edges fails
- exactly one `previous -> target` edge passes
- two newly authored edges fail
- one adjacent edge plus one cumulative shortcut edge fails
- one skipped `older -> target` edge fails
- an edge from a version other than the immediately previous release fails
- mutation of any inherited edge field or digest fails
- mutation of inherited guidance metadata, content digest, or referenced artifact fails
- deletion of an inherited edge fails unless it is part of an explicit supported-source retirement allowed by policy
- cumulative guidance copied from an older obligation to the new target fails
- a no-impact edge without an explicit reviewed no-impact decision fails
- a correct one-edge release retaining at least three historical source versions passes through composition
- a semantically lagging installation receives outstanding guidance exactly once
- prerelease and stable SemVer forms use the same single-edge rule

Tests must be wired into the required release PR policy and complete repository test workflow. A generic adjacent-edge unit test suite that is not exercised by the release gate is insufficient.

## Completion criteria

- [ ] the active historical upgrade graph is normalized into canonical adjacent edges
- [ ] active cumulative repository-local source-to-target preparation state is removed or made non-selectable archival evidence
- [ ] immutable published release assets remain untouched and readable where required
- [ ] all authoritative release instructions say that new releases author exactly one adjacent edge
- [ ] legacy direct source-to-target support is explicitly read-only and cannot be selected for new release authoring
- [ ] release tooling inherits immutable catalog history and adds only the previous-release-to-target edge
- [ ] release validation compares inherited and proposed catalogs rather than validating only the final graph
- [ ] release validation rejects zero, more than one, skipped, shortcut, or non-adjacent newly authored edges
- [ ] release validation rejects new cumulative source-to-target guidance, migrations, or semantic assessments
- [ ] release validation rejects any mutation or omission of inherited edge or guidance identity
- [ ] retained supported sources are qualified through deterministic path composition
- [ ] explicit source retirement remains possible only through the accepted catalog rules
- [ ] no-impact adjacent edges require a reviewed explicit no-impact decision without duplicated historical prose
- [ ] focused regression tests reproduce the alpha.12 failure mode and prove that it is rejected
- [ ] regression tests prove that a correct one-edge release with at least three retained historical source versions passes
- [ ] regression tests cover semantic compatibility lag and exact-once guidance composition
- [ ] tests are required by both release PR policy and the complete repository workflow
- [ ] the process is channel-neutral across prerelease and stable SemVer forms
- [ ] affected release documentation, schemas, procedures, fixtures, indexes, and conceptual history are aligned
- [ ] concrete repository-validation evidence is recorded in this task

## Resolution evidence

Complete this section in the resolving implementation PR. Record the implementing PR, exact normalized historical edges, archived or removed legacy state, changed release contracts and tooling, focused regression tests, and complete repository validation.

## Release qualification follow-up

The first release prepared after this finding is resolved must provide immutable evidence that:

1. its release branch inherited every normalized historical edge and guidance identity unchanged
2. it authored only the one adjacent edge from the immediately previous release to the target
3. no cumulative target-specific guidance was added for older supported sources
4. at least three retained historical source versions resolved uniquely through composition
5. a semantically lagging installation received each outstanding guidance obligation exactly once
6. the strict release-delta tests and release policy gate passed against the exact tagged revision

This is release-gate evidence after the repository implementation is complete. It does not keep or return the finding to `pending` once normalization, process enforcement, tests, documentation, and resolution evidence are merged.
