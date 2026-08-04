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
  at: 2026-08-04T14:28:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current next task

[Integrate release-please](todo/05-release-qualification/02-integrate-release-please.md).

The alpha qualification policy and its automated evidence are complete. Before preparing `1.0.0-alpha.1`, the next task is to add release-please for Conventional Commit classification, version and changelog management, release pull requests, tags, and draft release preparation.

The integration must preserve Ava's existing qualification, deterministic assembly, exact source-revision binding, and explicit publication approval. Completing the release-please task advances the roadmap to publishing the first alpha; it does not publish the alpha itself.

Alpha findings may add bounded fix tasks before release-candidate or stable publication. The roadmap must reflect those tasks rather than treating the first prerelease as feature-complete by definition.

## Working rule

When the user asks to work on a to-do item, read its task file, its active phase index, and only the related repository context needed to complete it.

A task is complete only when the intended repository change has been implemented, indexed, validated, and committed. Update the task status and affected active phase index together when completing it.
