---
type: Internal Development Task
title: Define Workflow Lifecycle Ownership
description: Evaluate and formalize responsibility for creating, maintaining, repairing, and retiring workflows.
tags: [internal, roadmap, workflows, roles, lifecycle]
status: pending
phase: 3
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T14:45:00Z
---

# Define Workflow Lifecycle Ownership

## Current state

The Project Steward currently owns project-wide workflow definitions and discovery structures. This supports ordinary workflow creation and updates, but the repository does not yet define a workflow lifecycle procedure comparable to the Role Manager's explicit role-lifecycle procedure.

The semantic-tool roadmap separately plans `plan_workflow_change`, `apply_workflow_change`, `scaffold_workflow`, and `validate_workflow`. Those tools should implement deterministic mechanics without silently deciding semantic ownership or authority.

This task follows the workflow purpose and built-in catalog review so lifecycle ownership is defined only for workflows that satisfy the accepted workflow criteria.

## Evaluate

- whether workflow creation and lifecycle maintenance should remain within the Project Steward's existing authority boundary
- whether a dedicated Workflow Manager role is justified by a distinct responsibility, authority, trust boundary, context requirement, or separation-of-duty need
- whether workflow lifecycle work needs distinct free-form routing conditions from general project stewardship
- how workflow ownership differs from role lifecycle work, independent semantic review, and deterministic validation
- whether the revised catalog should include workflow-maintenance procedures

Do not create a new default role merely because workflows have distinct procedures. A dedicated role requires a materially different authority boundary and user approval.

## Define

- creation, update, repair, reorganization, rename, deprecation, replacement, removal, and migration behavior for workflows
- required inspection of the workflow registry, primary role, related workflows, required context, and affected references
- approval boundaries for mode changes, authority implications, destructive behavior, trigger behavior, compatibility, and uncertain removal
- maintenance of workflow registry entries, canonical paths, `replaced_by` references, indexes, and scoped logs
- boundaries between semantic workflow maintenance and Ava's deterministic workflow tools

## Completion criteria

- make workflow lifecycle ownership explicit and non-overlapping in the role registry
- either strengthen the Project Steward's lifecycle instructions or propose a dedicated role for user approval
- define a complete workflow lifecycle procedure without duplicating the public workflow format or routing contracts
- decide whether built-in workflow-maintenance workflows should be added
- align the decision with the planned role and workflow maintenance tools
- update affected role, workflow, and roadmap documentation
