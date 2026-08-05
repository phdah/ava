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
  at: 2026-08-05T09:00:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current phase

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains the active umbrella task until the user explicitly declares dogfooding complete.

## Current next task

[Restore supported prerelease upgrade paths](todo/05-release-qualification/dogfood/01-restore-prerelease-upgrade-paths.md).

The alpha.4 release omitted upgrade edges from supported source prereleases, so projects installed on alpha.3 cannot upgrade through the published installer. Resolve this blocker before publishing another prerelease.

## Dogfood backlog rule

Use the [Alpha Dogfood Findings](todo/05-release-qualification/dogfood/) index as the queue for executable work during dogfooding.

- add each new finding as a numbered bounded task
- resolve the first pending finding before selecting later work unless the user reprioritizes it
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
