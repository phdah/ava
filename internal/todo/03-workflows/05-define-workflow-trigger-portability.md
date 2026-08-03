---
type: Internal Development Task
title: Define Workflow Trigger Portability
description: Define portable trigger metadata while keeping scheduler configuration outside Ava.
tags: [internal, roadmap, workflows, triggers]
status: pending
phase: 3
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Define Workflow Trigger Portability

This is the current next task. Complete it before workflow lifecycle ownership and before returning to Phase 4 installer implementation.

## Decide

- which trigger metadata Ava recognizes
- how schedule, manual, and event trigger descriptions are represented
- how external systems discover executable workflows
- how environment-specific scheduler configuration remains outside portable workflow prompts
- whether trigger metadata is advisory or validated

## Potential external executors

- cron
- GitHub Actions
- ChatGPT tasks
- CI systems
- custom agent clients

## Next task

[Define Workflow Lifecycle Ownership](06-define-workflow-lifecycle-ownership.md).
