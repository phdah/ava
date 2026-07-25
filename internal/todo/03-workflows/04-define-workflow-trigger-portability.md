---
type: Internal Development Task
title: Define Workflow Trigger Portability
description: Define portable trigger metadata while keeping scheduler configuration outside Ava.
tags: [internal, roadmap, workflows, triggers]
status: pending
phase: 3
order: 4
timestamp: 2026-07-25T00:00:00Z
---

# Define Workflow Trigger Portability

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
