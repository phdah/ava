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
  at: 2026-08-03T21:47:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current next task

[Implement validation, conformance, and upgrade fixtures](todo/04-distribution-and-upgrades/10-implement-validation-and-upgrade-fixtures.md).

The installer, updater, installed project-root convention, default OpenCode permissions, document update metadata, and agent-facing Ava Maintenance role are complete. Freeze the full structural, operational, host, installation, recovery, removal, and upgrade conformance matrix next. Release qualification then proceeds through alpha publication, real-project dogfooding, an RC gate, and the stable `1.0.0` release.

Alpha findings may add bounded fix tasks before release-candidate or stable publication. The roadmap must reflect those tasks rather than treating the first prerelease as feature-complete by definition.

## Working rule

When the user asks to work on a to-do item, read its task file, its active phase index, and only the related repository context needed to complete it.

A task is complete only when the intended repository change has been implemented, indexed, validated, and committed. Update the task status and affected active phase index together when completing it.
