---
type: Internal Development Task
title: Define review sufficiency and termination criteria
description: Make Ava reviews capable of reaching a stable acceptable conclusion instead of continually discovering progressively smaller improvements.
tags: [internal, roadmap, dogfood, review, roles]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 8
classification: required-v1
blocks: release-candidate
affected_version: repository source on main observed 2026-08-08
generated:
  by: agent:openai-chatgpt
  at: 2026-08-08T14:43:32+02:00
---

# Define review sufficiency and termination criteria

## Observed behavior

Repeated semantic review can enter an open-ended review-and-remediation loop. A review identifies issues, the owning role corrects them, and a later review then reports additional and progressively smaller concerns rather than determining that the reviewed structure is sufficiently correct for its intended scope.

The current Change Reviewer already permits a conclusion with no semantic findings and prohibits invented findings. In practice, however, the review contract does not clearly distinguish acceptance review from improvement discovery, define an admission threshold for findings, or state when a re-review must terminate successfully.

## Reproduction and evidence

The behavior was observed while dogfooding Ava against its own role and instruction structure on 2026-08-08:

1. request a semantic review of a bounded structure
2. remediate the reported findings through the owning role
3. request another review of the corrected structure
4. repeat the cycle as later reviews surface further lower-impact improvements

The observed failure is not that every reported concern is necessarily false. The failure is that the reviewer appears optimized to produce another improvement rather than answer whether the change is acceptable within a defined threshold.

Relevant current contracts include:

- `templates/base/roles/change-reviewer/role.md`
- `templates/base/roles/change-reviewer/instructions.md`
- `templates/base/roles/change-reviewer/capabilities.md`
- `templates/base/roles/change-reviewer/constraints.md`
- `templates/base/workflows/review-change.md`
- `templates/base/workflows/review-role-catalog.md`

## Classification

This is a `required-v1` finding that blocks the release candidate.

The issue does not need to block the next corrective prerelease because it does not currently weaken installation, upgrade, routing, authority, or safety guarantees. It does affect a core Ava product behavior: reviews must support a useful decision and must be able to conclude that bounded work is sufficiently correct. Shipping v1 with structurally endless review loops would make role-guided maintenance unstable and difficult to complete.

## Root cause

The current review contract permits zero findings but does not define a complete sufficiency model. In particular, it lacks explicit semantics for:

- acceptance review versus improvement or audit review
- the minimum evidence, consequence, confidence, and impact needed to admit a finding
- optional observations that do not affect acceptance
- re-review of previously reported findings without restarting an unrestricted review from zero
- a stable termination condition after remediation
- conclusions that state whether the applicable review threshold was met

The resolving task must confirm this diagnosis against the complete active review instruction chain rather than assuming these are the only affected contracts.

## Scope

The resolving PR must design and implement a bounded review sufficiency contract. It should:

- research established pull-request review agents and human code-review guidance for useful patterns around acceptance thresholds, review strictness, confidence, optional suggestions, and re-review behavior
- define explicit review standards or modes where needed, with ordinary bounded review defaulting to an acceptance decision rather than exhaustive improvement discovery
- define a finding admission test that excludes preferences, speculative improvements, and alternative valid designs from acceptance-blocking findings
- define when non-blocking observations may be reported and when they should be omitted
- make re-review monotonic by checking earlier findings and remediation before broadening into new concerns
- define a stable review threshold and terminal conclusion that can be reached without claiming user approval or deterministic validity
- preserve comprehensive audit behavior when the user explicitly requests it
- determine whether a small general rule is needed for other evaluative roles or workflows to declare their own sufficiency and completion criteria
- keep detailed review semantics owned by the Change Reviewer rather than duplicating them in unrelated root instructions

Do not implement these changes in this finding-registration PR.

## Completion criteria

- ordinary bounded review can conclude that the active acceptance threshold is met when no material finding remains
- the contract distinguishes required findings from optional observations and from mere alternative preferences
- repeated review begins from the prior findings and remediation state rather than automatically restarting unrestricted discovery
- a new finding during re-review requires concrete new evidence and must independently exceed the active review threshold
- resolved concerns are not reopened without changed evidence, changed scope, or a regression
- exhaustive improvement or audit review remains available only through an explicit scope or review standard
- conclusions communicate whether the review threshold was met while preserving the Change Reviewer's advisory authority
- regression fixtures cover a clean first review, remediation followed by a satisfied re-review, a genuine regression introduced during remediation, and an explicitly exhaustive audit
- affected role, workflow, shared-instruction, validation, documentation, and index contracts remain aligned
- the resolving PR records concrete resolution and repository-validation evidence

## Resolution evidence

Pending implementation.

## Release qualification follow-up

Exercise the completed behavior through an installed corrective prerelease by reviewing a bounded role or instruction change, applying its findings through the owning role, and requesting a re-review. Qualification must demonstrate that the reviewer reaches the defined successful terminal conclusion when the earlier findings are resolved and no new concern exceeds the active threshold.
