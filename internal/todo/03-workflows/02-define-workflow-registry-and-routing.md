---
type: Internal Development Task
title: Define the Workflow Registry and Routing Contract
description: Define deterministic workflow discovery, role resolution, precedence, and deprecation behavior.
tags: [internal, roadmap, workflows, routing]
status: pending
phase: 3
order: 2
timestamp: 2026-07-25T00:00:00Z
---

# Define the Workflow Registry and Routing Contract

## Rules

- every workflow must resolve to exactly one existing primary role
- one role may support multiple workflows
- a workflow must not duplicate the role's durable instructions
- workflow routing takes precedence over free-form role selection when a registered workflow is explicitly invoked
- missing, ambiguous, or deprecated role references must fail validation
- delegation, if supported, must be explicit rather than inferred

## Completion criteria

- choose the registry format and location
- define router behavior for interactive and workflow-driven requests
- update generated `AGENTS.md`
- validate workflow links and role references
- define deprecation and migration behavior
