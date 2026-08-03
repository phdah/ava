---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current next task

[Define document update metadata](todo/01-format-contract/04-define-document-update-metadata.md).

The installer and updater are implemented, installed project paths use an explicit project-root convention, and the default installer now provides project-owned OpenCode permissions while preserving existing configuration. Define the document-update metadata contract next, then add the agent-facing Ava Maintenance role before freezing the full conformance and upgrade matrix. Release qualification then proceeds through alpha publication, real-project dogfooding, an RC gate, and the stable `1.0.0` release.

Alpha findings may add bounded fix tasks before release-candidate or stable publication. The roadmap must reflect those tasks rather than treating the first prerelease as feature-complete by definition.

## Working rule

When the user asks to work on a to-do item, read its task file, its active phase index, and only the related repository context needed to complete it.

A task is complete only when the intended repository change has been implemented, indexed, validated, and committed. Update the task status and affected active phase index together when completing it.
