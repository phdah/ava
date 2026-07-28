---
type: Internal Development Task
title: Define the Workflow Format Contract
description: Define the portable schema and behavior of reusable Ava workflows.
tags: [internal, roadmap, workflows, format]
status: completed
phase: 3
order: 1
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T10:00:00Z
---

# Define the Workflow Format Contract

## Purpose

A workflow is a reusable predefined prompt that activates exactly one primary role for a specific procedure or outcome.

## Completed outcome

The public [workflow format contract](/templates/base/shared/instructions/workflow-format.md) now defines:

- required workflow metadata, including `primary_role` and `mode`
- workflow path identity, filename rules, and title rules
- `read-only`, `suggestion`, and `mutation` semantics
- ordered Markdown sections for purpose, inputs, required context, procedure, expected output, and optional trigger notes
- structured required and optional input representation
- human-readable expected-output requirements
- workflow-specific context links
- prohibition of supporting workflows, supporting roles, delegation, and role transitions
- invalid, ambiguous, warning, and blocking validation cases
- valid and invalid examples

Portable trigger metadata remains intentionally deferred to [Define workflow trigger portability](04-define-workflow-trigger-portability.md). The format contract preserves unknown trigger-related metadata but assigns it no current Ava semantics.

## Established metadata constraints

Every workflow uses `type: Workflow`, provides `title` and `description`, references exactly one registered `role.md` through `primary_role`, and declares one supported operating mode:

```yaml
---
type: Workflow
title: Daily project maintenance
description: Performs a bounded recurring project maintenance procedure.
primary_role: /roles/project-steward/role.md
mode: mutation
status: draft
---
```

## Completion criteria

- [x] document the workflow schema
- [x] define input and expected-output representation
- [x] add workflow examples
- [x] define invalid and ambiguous cases
- [x] add workflow validation requirements
- [x] update the illustrative project structure
