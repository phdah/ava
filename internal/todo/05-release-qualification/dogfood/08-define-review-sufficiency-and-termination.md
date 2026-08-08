---
type: Internal Development Task
title: Define review sufficiency and termination criteria
description: Make Ava reviews capable of reaching a stable acceptable conclusion instead of continually discovering progressively smaller improvements.
tags: [internal, roadmap, dogfood, review, roles]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 8
classification: required-v1
blocks: release-candidate
affected_version: repository source on main observed 2026-08-08
generated:
  by: agent:openai-chatgpt
  at: 2026-08-08T14:43:32+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T00:27:47+02:00
---

# Define review sufficiency and termination criteria

## Observed behavior

Repeated semantic review can enter an open-ended review-and-remediation loop. A review identifies issues, the owning role corrects them, and a later review then reports additional and progressively smaller concerns rather than determining that the reviewed structure is sufficiently correct for its intended scope.

The previous Change Reviewer permitted a conclusion with no semantic findings and prohibited invented findings. In practice, however, the review contract did not clearly distinguish acceptance review from improvement discovery, define an admission threshold for findings, or state when a re-review must terminate successfully.

## Reproduction and evidence

The behavior was observed while dogfooding Ava against its own role and instruction structure on 2026-08-08:

1. request a semantic review of a bounded structure
2. remediate the reported findings through the owning role
3. request another review of the corrected structure
4. repeat the cycle as later reviews surface further lower-impact improvements

The observed failure was not that every reported concern was necessarily false. The failure was that the reviewer appeared optimized to produce another improvement rather than answer whether the change was acceptable within a defined threshold.

Relevant contracts included:

- `templates/base/roles/change-reviewer/role.md`
- `templates/base/roles/change-reviewer/instructions.md`
- `templates/base/roles/change-reviewer/capabilities.md`
- `templates/base/roles/change-reviewer/constraints.md`
- `templates/base/workflows/review-change.md`
- `templates/base/workflows/review-role-catalog.md`

## Classification

This was a `required-v1` finding that blocked the release candidate.

The issue did not need to block the corrective prerelease because it did not weaken installation, upgrade, routing, authority, or safety guarantees. It did affect a core Ava product behavior: reviews must support a useful decision and must be able to conclude that bounded work is sufficiently correct.

## Root cause

The previous review contract permitted zero findings but did not define a complete sufficiency model. In particular, it lacked explicit semantics for:

- acceptance review versus improvement or audit review
- the minimum evidence, consequence, confidence, and impact needed to admit a finding
- optional observations that do not affect acceptance
- re-review of previously reported findings without restarting an unrestricted review from zero
- a stable termination condition after remediation
- conclusions that state whether the applicable review threshold was met

The complete Change Reviewer instruction chain confirmed that these gaps were concentrated in the role's detailed review semantics and its two managed workflows. No project-wide shared evaluative rule was required.

## Scope

The resolving PR was required to design and implement a bounded review sufficiency contract that:

- uses established review patterns around acceptance thresholds, review strictness, confidence, optional suggestions, and incremental re-review
- defines explicit review standards, with ordinary bounded review defaulting to an acceptance decision
- defines a finding admission test that excludes preferences, speculative improvements, and alternative valid designs
- defines when non-blocking observations may be reported and when they should be omitted
- makes re-review monotonic by checking earlier findings and remediation before broadening into new concerns
- defines a stable review threshold and terminal conclusion without claiming user approval or deterministic validity
- preserves comprehensive audit behavior when the user explicitly requests it
- keeps detailed review semantics owned by the Change Reviewer rather than duplicating them in unrelated root instructions

## Completion criteria

- [x] ordinary bounded review can conclude that the active acceptance threshold is met when no material finding remains
- [x] the contract distinguishes required findings from optional observations and from mere alternative preferences
- [x] repeated review begins from the prior findings and remediation state rather than automatically restarting unrestricted discovery
- [x] a new finding during re-review requires concrete new evidence and must independently exceed the active review threshold
- [x] resolved concerns are not reopened without changed evidence, changed scope, changed authority, or a regression
- [x] exhaustive improvement or audit review remains available only through an explicit scope or review standard
- [x] conclusions communicate whether the review threshold was met while preserving the Change Reviewer's advisory authority
- [x] regression fixtures cover a clean first review, remediation followed by a satisfied re-review, a genuine regression introduced during remediation, and an explicitly exhaustive audit
- [x] affected role, workflow, validation, documentation, and index contracts remain aligned
- [x] the resolving PR records concrete resolution and repository-validation evidence

## Resolution evidence

The Change Reviewer now defines two review standards:

- `acceptance`, the default for ordinary bounded review
- `audit`, available only through explicit user or workflow scope

Every candidate finding must pass a four-part admission test covering evidence, consequence, confidence, and the active threshold. Preferences, speculative improvements, stylistic refinements, and alternative valid designs are not findings. Minor findings remain evidence-backed but non-blocking. Optional observations are omitted by default during acceptance review and, when explicitly requested or produced during audit, are separated from findings and cannot require remediation or prevent acceptance.

Re-review is now a continuation of the prior review. It classifies each earlier finding as resolved, unresolved, or superseded before inspecting the remediation. A new or reopened finding requires changed evidence, changed scope, changed authority, or a genuine regression and must independently pass the admission test. The review terminates successfully once prior blocking and major findings are closed, no admitted new blocking or major finding exists, and no user-owned decision prevents the conclusion.

The bounded `review-change` workflow defaults to `acceptance` and accepts prior review state. The catalog-wide `review-role-catalog` workflow explicitly defaults to `audit`. Both workflows require prior-finding disposition and changed evidence for new re-review findings.

`internal/release/fixtures/review-sufficiency.json` freezes the clean first review, satisfied re-review, remediation regression, and explicit exhaustive audit cases. `internal/release/tests/test_review_sufficiency.py` protects the standards, admission test, optional-observation boundary, monotonic termination, workflow defaults, and advisory authority. The test is included in `internal/release/test.sh`, the fixture is indexed, and the conformance procedure documents the contract.

A separate shared rule for other evaluative roles was not added. The Change Reviewer is the only managed role with independent semantic review authority, and keeping the detailed threshold in its instruction chain avoids creating duplicate or prematurely generalized semantics.

## Repository validation

The focused review-sufficiency test module passes all five regression tests against the implemented role, workflow, and fixture contracts. The complete repository suite remains the pull request qualification gate.

## Release qualification follow-up

Exercise the completed behavior through an installed corrective prerelease by reviewing a bounded role or instruction change, applying its findings through the owning role, and requesting a re-review. Qualification must demonstrate that the reviewer reaches the defined successful terminal conclusion when the earlier findings are resolved and no new concern exceeds the active threshold.
