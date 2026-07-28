---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T10:32:00Z
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects produced by `ava init`.

Read the [ordered roadmap](todo/index.md) to discover phases and individual task files.

## Current next task

[Create the initial built-in workflow catalog](todo/03-workflows/03-create-built-in-workflow-catalog.md).

## Working rule

When the user asks to work on a to-do item, read its task file, its phase index, and only the related repository context needed to complete it.

A task is complete only when the intended repository change has been implemented, indexed, validated, and committed. Update the task status and affected phase index when completing it.
