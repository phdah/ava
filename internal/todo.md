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
  at: 2026-08-04T16:48:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current next task

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md).

The first alpha publication task is complete in the repository state produced by the merged change. The next task is to exercise the alpha through realistic Ava and OpenCode usage, classify findings, and add bounded roadmap tasks for defects that must be resolved before the release candidate or stable release.

The first-alpha bootstrap uses a one-shot exact-version override because its bounded post-bootstrap history intentionally contains no releasable unit. Remove that override before later release planning.

Alpha findings may add bounded fix tasks before release-candidate or stable publication. The roadmap must reflect those tasks rather than treating the first prerelease as feature-complete by definition.

## Working rule

When the user asks to work on a to-do item, read its task file, its active phase index, and only the related repository context needed to complete it.

A task is complete only when the intended repository change has been implemented, indexed, validated, and committed. Update the task status and affected active phase index together when completing it.
