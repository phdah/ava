---
type: Internal Development Task
title: Enforce adjacent-edge release authoring
description: Make every future release author exactly one new adjacent upgrade edge and prevent legacy cumulative source-to-target authoring from passing release preparation.
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
---

# Enforce adjacent-edge release authoring

## Architectural scope

This is a general release-process correction, not a repair limited to `1.0.0-alpha.12`.

The accepted adjacent-edge contract already defines the intended model for future prerelease and stable releases. Every release proposal created after this finding is resolved must inherit the reviewed catalog unchanged and author exactly one new edge from the immediately previous released version to the proposed target. Older supported source versions reach the target through deterministic composition of retained adjacent edges.

Legacy direct source-to-target manifests may remain readable for already published releases and explicitly grandfathered historical inputs. That compatibility is consumption-only. It must never be treated as permission to author a new release through the legacy cumulative model.

## Observed behavior

The `1.0.0-alpha.12` release proposal contained the implementation that introduced adjacent-edge composition, but release completion still recreated target-specific guidance and source-to-target assessments for multiple earlier prereleases.

The release added cumulative guidance from alpha.5 through alpha.9 directly to alpha.12 instead of inheriting earlier reviewed edges and adding only alpha.11 to alpha.12. The release checks passed because the compatibility transition still accepted the older representation for an in-progress proposal.

This proved that the repository currently distinguishes neither clearly nor mechanically between:

- reading historical direct source-to-target release data for compatibility
- authoring a new release under the accepted adjacent-edge process

A passing release policy check can therefore endorse a representation that the authoritative architecture says maintainers must no longer create.

## Reproduction and evidence

- PR #76 completed the accepted adjacent-edge model and states that each release appends and reviews only its new adjacent edge while inherited edges retain immutable identity.
- PR #74 prepared `1.0.0-alpha.12` with newly authored cumulative guidance directories from multiple older sources directly to alpha.12.
- The release policy and Python checks passed even though the proposal used the superseded cumulative authoring path.
- The release was merged, demonstrating that documentation, procedure, and validation did not make the intended authoring mode operationally unambiguous.

## Classification

This finding is a `blocker` for the next prerelease.

Without a correction, every future release can repeat the same mistake, grow cumulative guidance quadratically, rewrite previously reviewed semantic obligations, and pass qualification through a compatibility path that exists only to read historical releases. The next release must not be prepared until the authoring contract and release gate agree.

## Root cause

The adjacent-edge implementation preserved backward read compatibility but did not establish a hard authoring boundary.

Release instructions still contain legacy source-to-target language, release completion can still select the old `upgrade-impact.json` workflow, and validation accepts the legacy representation without proving that the proposal is a historical grandfathered release rather than a newly authored catalog-based release.

The process relied on the maintainer to infer that backward compatibility was not an authoring option. That inference is unsafe and contradicted by the accepted goal of making release preparation deterministic.

## Required process

The resolving implementation must make the following process authoritative for every future Ava prerelease and stable release:

1. Load the latest published self-contained adjacent-edge catalog.
2. Preserve every inherited edge, digest, guidance record, and referenced guidance artifact exactly.
3. Author exactly one new edge from the immediately previous released Ava version to the proposed target.
4. Assess only the managed delta introduced by that new adjacent edge for project-owned semantic impact.
5. Add semantic guidance only when that new adjacent edge requires project-owned reconciliation.
6. Do not recreate cumulative source-to-target assessments, migrations, or guidance for older supported sources.
7. Retain or explicitly retire supported entry points without rewriting the inherited path that serves them.
8. Resolve older source versions through the unique composed adjacent-edge path.
9. Qualify every retained supported source against the composed path, including semantic compatibility lag, without producing target-specific duplicate guidance.
10. Treat legacy direct source-to-target data as read-only historical compatibility input, never as a valid authoring mode for a new release.

For avoidance of doubt, a release with no project-owned semantic impact still authors its one adjacent edge with an explicit reviewed no-impact decision. It does not omit the edge, and it does not restate older no-impact or impact decisions against the new target.

## Scope

The resolving PR must update and align the general release process, not patch one version-specific fixture. It must include:

- release-maintainer instructions and release PR procedure that prescribe the exact adjacent-edge workflow above
- removal or correction of conflicting instructions that require cumulative source-to-target assessment for new releases
- an explicit transition rule identifying historical representations that remain readable and the point after which catalog authoring is mandatory
- release preparation tooling that starts from inherited catalog state and accepts only one newly authored adjacent edge
- release policy validation that rejects cumulative target-specific guidance or assessments in a new catalog-based release
- validation that rejects modified inherited edges, digests, guidance metadata, or guidance artifacts
- validation that rejects a missing or non-adjacent previous-release-to-target edge
- validation that permits supported-source retirement only through the explicit catalog contract
- validation of unique composed managed and semantic paths for every retained supported source
- clear failure messages that tell a maintainer to author the adjacent edge rather than fall back to the legacy workflow
- migration or cleanup rules for repository-local release preparation state left by the alpha.12 incident, without changing immutable published release assets

The implementation must apply to alpha, beta, release-candidate, stable, patch, minor, and major releases. Channel labels and SemVer magnitude must not change the adjacent authoring rule.

## Completion criteria

- [ ] all authoritative release instructions say that new releases author exactly one adjacent edge
- [ ] legacy direct source-to-target support is explicitly read-only and cannot be selected for new release authoring
- [ ] release tooling inherits immutable catalog history and adds only the previous-release-to-target edge
- [ ] release validation rejects more than one newly authored edge
- [ ] release validation rejects new cumulative source-to-target guidance, migrations, or semantic assessments
- [ ] release validation rejects any mutation of inherited edge or guidance identity
- [ ] release validation rejects a missing, skipped, ambiguous, or non-adjacent new edge
- [ ] retained supported sources are qualified through deterministic path composition
- [ ] explicit source retirement remains possible only through the accepted catalog rules
- [ ] no-impact adjacent edges require a reviewed explicit no-impact decision without duplicated historical prose
- [ ] focused regression tests reproduce the alpha.12 failure mode and prove that it is rejected
- [ ] regression tests prove that a correct one-edge release with at least three retained historical source versions passes
- [ ] regression tests cover semantic compatibility lag and exact-once guidance composition
- [ ] the process is channel-neutral across prerelease and stable SemVer forms
- [ ] affected release documentation, schemas, procedures, fixtures, indexes, and conceptual history are aligned
- [ ] concrete repository-validation evidence is recorded in this task

## Resolution evidence

Complete this section in the resolving implementation PR. Record the implementing PR, exact changed release contracts and tooling, focused regression tests, and complete repository validation.

## Release qualification follow-up

The first release prepared after this finding is resolved must provide immutable evidence that:

1. its release branch inherited prior edge and guidance identities unchanged
2. it authored only the one adjacent edge from the immediately previous release to the target
3. no cumulative target-specific guidance was added for older supported sources
4. at least three retained historical source versions resolved uniquely through composition
5. a semantically lagging installation received each outstanding guidance obligation exactly once

This is release-gate evidence after the repository implementation is complete. It does not keep or return the finding to `pending` once the process, enforcement, tests, documentation, and resolution evidence are merged.
