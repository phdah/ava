---
type: Internal Development Task
title: Define Release-Impact-Based Change Types
description: Clarify that Conventional Commit types and SemVer release impact are determined by changes to the supported Ava distribution rather than by implementation novelty or repository location.
tags: [internal, roadmap, dogfood, releases, semver, conventional-commits]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 10
classification: required-v1
blocks: release-candidate
affected_version: source revision c2c1d84e05f7be16fbbb4442e44c594a7007ce01
generated:
  by: agent:openai-chatgpt
  at: 2026-08-09T11:52:10+02:00
---

# Define Release-Impact-Based Change Types

## Observed behavior

PR #75 introduced a new repository-only synthetic qualification fixture and was initially titled `feat: add synthetic qualification vault`. Under the current release automation, that title classified the change as a releasable feature and therefore implied a minor Ava release even though the PR did not change installed Ava content, public contracts, release assets, or supported project behavior.

The distinction between a new internal implementation capability and a new user-facing or distribution-facing Ava capability is not explicit enough in the maintained Conventional Commit and release instructions.

## Reproduction and evidence

- PR: <https://github.com/phdah/ava/pull/75>
- Initial title: `feat: add synthetic qualification vault`
- Corrected title: `test(release): add synthetic qualification vault`
- The changed files are confined to repository-only release fixtures, qualification tests, internal roadmap documents, and boundary validation.
- `internal/release/validate_pr_title.py` maps every non-breaking `feat` title to a minor release while supported non-releasable types such as `test` produce no release level.
- `internal/release/release-please.md` identifies releasable and internal-only types but does not define the classification boundary in terms of resulting supported distribution behavior.

## Classification

This is `required-v1` and blocks the release candidate. Incorrect change-type selection can create unintended releases, misleading changelog entries, and false SemVer claims. The policy must be explicit before Ava relies on pull-request titles as the canonical squash commits consumed by release automation.

## Root cause

The release instructions define which Conventional Commit types are releasable, but they do not state clearly that authors must select the type from the effect on the supported Ava distribution rather than from whether the repository implementation is new, substantial, or located under `internal/`.

## Scope

The resolving PR must:

- define change-type selection by observable impact on installed Ava content, public contracts, release assets, installer or updater behavior, and supported agent behavior
- state that implementation novelty alone does not justify `feat`
- state that repository-only tests, fixtures, qualification tooling, CI, documentation, and maintenance changes use non-releasable types when they do not alter produced assets or supported behavior
- preserve the converse rule that a change implemented under `internal/` may still require `feat`, `fix`, `perf`, or a breaking marker when it changes the resulting distribution or guarantees
- align the Conventional Commit instructions with the public SemVer contract without redefining Ava version compatibility
- add representative positive and negative examples, including the synthetic qualification vault case
- add regression coverage that freezes the maintained policy and its examples

## Completion criteria

- the release instructions define the classification boundary using supported distribution impact
- `feat` is reserved for backward-compatible capability exposed through the Ava distribution or its supported behavior
- repository-only implementation categories are not automatically treated as releasable
- internal source location is not treated as proof that a change is non-releasable
- examples cover `feat`, `fix`, `test`, `docs`, `chore`, and breaking changes with their expected release levels
- validation and release-automation tests protect the documented distinction
- affected indexes and release documentation remain aligned
- concrete resolution and repository-validation evidence are recorded below

## Resolution evidence

Pending.

## Release qualification follow-up

After the policy is implemented, verify through a release-please dry run or equivalent maintained fixture that a repository-only qualification PR titled with a non-releasable type does not create or advance a release proposal, while a distribution-facing `feat` still proposes the expected SemVer increment.
