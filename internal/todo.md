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
  at: 2026-08-06T11:30:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current phase

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains the active umbrella task until the user explicitly declares dogfooding complete.

## Current next task

[Remove empty upgrade transaction containers](todo/05-release-qualification/dogfood/06-remove-empty-upgrade-transaction-containers.md).

[Restore complete prerelease upgrade coverage](todo/05-release-qualification/dogfood/05-restore-complete-prerelease-upgrade-coverage.md) now has its repository implementation: alpha.8 is prepared to support direct upgrades from alpha.5, alpha.6, and alpha.7, protected-source coverage is enforced, and every edge has a reviewed managed, migration, guidance, semantic, and cumulative-note assessment. The finding remains pending until immutable alpha.8 assets pass all three real version-pinned upgrades.

Finding 06 is the next actionable blocker and should be included before that same corrective prerelease is published. It requires terminal updater cleanup to remove `./.ava/state/transactions/` when its final transaction workspace is deleted.

## Dogfood backlog rule

Use the [Alpha Dogfood Findings](todo/05-release-qualification/dogfood/) index as the queue for executable work during dogfooding.

- add each new finding as a numbered bounded task
- work the first actionable pending finding in dependency order unless the user reprioritizes it
- allow a finding whose implementation is complete but awaits shared prerelease validation to remain pending without blocking implementation of the next finding
- update the finding task and backlog index together
- keep completed findings as durable evidence
- do not make release-candidate publication current merely because the backlog is temporarily empty
- only the user may declare the dogfood umbrella complete

## Working rule

When the user asks to work on the next to-do item, read:

1. this entry point
2. the active Phase 5 index
3. the dogfood findings index
4. the current finding task
5. only the related repository context needed to complete it

A finding is complete only when the intended repository change has been implemented, indexed, validated, and committed with resolution evidence. Completing a finding does not complete the parent dogfood task.
