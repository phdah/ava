---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T13:27:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into projects distributed by Ava.

Read the [ordered roadmap](todo/index.md) to discover active phases and individual task files.

## Current next task

[Define the upgrade and migration protocol](todo/04-distribution-and-upgrades/04-define-upgrade-and-migration-protocol.md).

## Working rule

When the user asks to work on a to-do item, read its task file, its active phase index, and only the related repository context needed to complete it.

A task is complete only when the intended repository change has been implemented, indexed, validated, and committed. Update the task status and affected active phase index together when completing it.
