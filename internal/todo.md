---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T00:13:04+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current phase

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains the active umbrella task until the user explicitly declares dogfooding complete.

## Current next task

[Build the synthetic v1 qualification vault](todo/05-release-qualification/04a-build-synthetic-qualification-vault.md) is the current task. It must generate a reproducible 200-400-file raw corpus covering six coherent months of Adam's fictional private and work life in Stockholm, including one February apartment move and machine-checkable expected outcomes.

After the vault, [qualify and publish the corrective alpha](todo/05-release-qualification/04b-qualify-and-publish-corrective-alpha.md). That qualification must collect immutable evidence for completed findings 03 through 07, including the exact warranty prompt and unresolved-routing scenario. After the corrective prerelease is qualified, complete [Define review sufficiency and termination criteria](todo/05-release-qualification/dogfood/08-define-review-sufficiency-and-termination.md) before release-candidate publication.

Release PR [#68](https://github.com/phdah/ava/pull/68) for `1.0.0-alpha.11` has been merged. The repository release manifest now records `1.0.0-alpha.11`; immutable publication and qualification evidence remain governed by the release workflow and the [corrective alpha qualification task](todo/05-release-qualification/04b-qualify-and-publish-corrective-alpha.md).

[Enforce role routing before every response](todo/05-release-qualification/dogfood/07-enforce-role-routing-before-every-response.md) is complete in its resolving implementation PR. The managed router now makes state gating and role routing unconditional before substantive handling, and regression coverage protects the exact warranty bypass through source, assembled installed, and OpenCode conformance paths. Real immutable-release validation remains part of corrective-alpha qualification.

[Enforce faithful inbox ingestion completion](todo/05-release-qualification/dogfood/04-enforce-faithful-inbox-ingestion-completion.md) is complete through merged PR [#67](https://github.com/phdah/ava/pull/67) and published `1.0.0-alpha.10`. Repeated realistic ingestion, final count reconciliation, and independent semantic review remain corrective-release qualification evidence.

[Make knowledge hierarchy promotion predictable](todo/05-release-qualification/dogfood/03-make-knowledge-hierarchy-promotion-predictable.md) is complete through merged PR #65. Repeated realistic ingestion and independent semantic review remain release qualification follow-up.

[Restore complete prerelease upgrade coverage](todo/05-release-qualification/dogfood/05-restore-complete-prerelease-upgrade-coverage.md) is complete through merged PR #60.

[Remove empty upgrade transaction containers](todo/05-release-qualification/dogfood/06-remove-empty-upgrade-transaction-containers.md) is complete through PR #62.

Completed fixes may still require real corrective-release evidence before the next prerelease can qualify. That evidence belongs to release qualification and does not keep or return their implementation tasks to pending.

[Repair installed context link resolution](todo/05-release-qualification/dogfood/02-repair-installed-context-link-resolution.md) is complete after real immutable alpha.7 validation loaded the complete Inbox Ingester required-reading chain from exact installed-project paths.

## Dogfood backlog rule

Use the [Alpha Dogfood Findings](todo/05-release-qualification/dogfood/) index as the queue for executable work during dogfooding.

- add each new finding as a numbered bounded task
- work the first actionable pending finding in dependency order unless the user reprioritizes it
- work supporting qualification tasks linked from the Phase 5 index after any blocker they depend on; do not assign them finding IDs unless their execution exposes a defect
- mark a finding completed in the resolving implementation PR once its repository change, tests, documentation, indexes, and resolution evidence are complete
- append later published-asset or realistic-project qualification evidence without keeping or returning the implementation task to pending
- update the finding task and backlog index together
- keep completed findings as durable evidence
- do not make release-candidate publication current merely because the backlog is temporarily empty
- only the user may declare the dogfood umbrella complete

## Working rule

When the user asks to work on the next to-do item, read:

1. this entry point
2. the active Phase 5 index
3. the parent dogfood task
4. the dogfood findings index when a finding is pending or relevant
5. the current bounded finding or supporting qualification task
6. only the related repository context needed to complete it

A finding is complete when the intended repository change has been implemented, indexed, repository-validated, and committed with resolution evidence. Published-asset or realistic-project qualification may be appended later and is tracked as a release gate rather than task status. Completing a finding does not complete the parent dogfood task.
