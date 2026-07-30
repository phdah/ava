---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover accepted work, proposed replacement work, superseded planning, and individual task files.

## Current decision

The distribution-first architecture in draft PR #11 is awaiting explicit user approval.

## Conditional next task

After approval, [define the distribution and ownership boundary](todo/04-distribution-and-upgrades/01-define-distribution-and-ownership-boundary.md).

Until approval, do not treat the proposed phase as accepted architecture or begin its implementation tasks.

## Working rule

When the user asks to work on a to-do item, read its task file, its phase index, and only the related repository context needed to complete it.

A task is complete only when the intended repository change has been implemented, indexed, validated, and committed. Update the task status and affected active phase index together when completing it.

Do not select tasks from phases marked as superseded. Do not select proposed architecture tasks without explicit user approval.