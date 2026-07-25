---
type: Internal Development Task
title: Define the Workflow Format Contract
description: Define the portable schema and behavior of reusable Ava workflows.
tags: [internal, roadmap, workflows, format]
status: pending
phase: 3
order: 1
timestamp: 2026-07-25T00:00:00Z
---

# Define the Workflow Format Contract

## Purpose

A workflow is a reusable predefined prompt that activates exactly one primary role for a specific procedure or outcome.

## Decide

- mandatory workflow metadata
- workflow identifier and title rules
- primary role reference
- prompt body representation
- required and optional inputs
- read-only, suggestion, and mutation modes
- expected output representation
- optional trigger metadata
- workflow-specific context links
- whether workflows may reference supporting workflows
- whether workflows may request explicit delegation to another role

## Initial metadata direction

```yaml
---
type: Agent Workflow
title: Daily project maintenance
role: project-steward
mode: apply
trigger:
  type: schedule
  expression: daily
---
```

Trigger metadata is descriptive and portable. Ava should not initially execute schedules itself.

## Completion criteria

- document the workflow schema
- add workflow examples
- define invalid and ambiguous cases
- add workflow validation requirements
- update the illustrative project structure
