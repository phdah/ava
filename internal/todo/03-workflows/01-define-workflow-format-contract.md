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

- mandatory workflow metadata beyond the established metadata contract
- workflow identifier and title rules
- prompt body representation
- required and optional inputs
- read-only, suggestion, and mutation modes
- expected output representation
- optional trigger metadata
- workflow-specific context links
- whether workflows may reference supporting workflows
- whether workflows may request explicit delegation to another role

## Established metadata constraints

The completed metadata task already requires every workflow to use `type: Workflow`, provide `title` and `description`, and reference exactly one registered role through `primary_role`:

```yaml
---
type: Workflow
title: Daily project maintenance
description: Performs a bounded recurring project maintenance procedure.
primary_role: /roles/project-steward/role.md
status: draft
---
```

Inputs, operating mode, expected output, and trigger information remain in structured Markdown until this task decides whether any of them need portable machine-readable fields. Trigger metadata, if introduced, is descriptive and portable. Ava should not initially execute schedules itself.

## Completion criteria

- document the workflow schema
- define input and expected-output representation
- add workflow examples
- define invalid and ambiguous cases
- add workflow validation requirements
- update the illustrative project structure