---
type: Internal Development Task
title: Define Workflow Lifecycle Ownership
description: Evaluate and formalize responsibility for creating, maintaining, repairing, migrating, and retiring workflows.
tags: [internal, roadmap, workflows, roles, lifecycle, migrations]
status: pending
phase: 3
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T11:26:00Z
---

# Define Workflow Lifecycle Ownership

## Current state

The Project Steward currently owns project-wide workflow definitions and discovery structures. This supports ordinary workflow creation and updates, but the repository does not yet define a workflow lifecycle procedure comparable to the Role Manager's explicit role-lifecycle procedure.

The distribution roadmap separately defines deterministic base replacement, structural migration, validation, and conflict detection. Those mechanics must not silently decide semantic workflow purpose, authority, or project-specific changes.

This task follows the workflow purpose review and the distribution ownership and migration contracts so lifecycle ownership is defined only for justified workflows and respects the managed versus project-owned boundary.

## Evaluate

- whether workflow creation and lifecycle maintenance should remain within the Project Steward's existing authority boundary
- whether a dedicated Workflow Manager role is justified by a distinct responsibility, authority, trust boundary, context requirement, or separation-of-duty need
- whether workflow lifecycle work needs distinct free-form routing conditions from general project stewardship
- how workflow ownership differs from role lifecycle work, independent semantic review, release migration guidance, and deterministic installer behavior
- whether the revised catalog should include workflow-maintenance or semantic project-upgrade procedures

Do not create a new default role merely because workflows have distinct procedures. A dedicated role requires a materially different authority boundary and user approval.

## Define

- creation, update, repair, reorganization, rename, deprecation, replacement, removal, and migration behavior for workflows
- required inspection of the workflow registry, primary role, related workflows, required context, release guidance, and affected references
- approval boundaries for mode changes, authority implications, destructive behavior, trigger behavior, compatibility, and uncertain removal
- maintenance of workflow registry entries, canonical paths, `replaced_by` references, indexes, scoped logs, and semantic migration completion state
- boundaries between semantic workflow maintenance and deterministic installer, updater, and validator responsibilities

## Completion criteria

- make workflow lifecycle ownership explicit and non-overlapping in the role registry
- either strengthen the Project Steward's lifecycle instructions or propose a dedicated role for user approval
- define a complete workflow lifecycle procedure without duplicating public workflow format, routing, release, or migration contracts
- decide whether built-in workflow-maintenance or semantic-upgrade workflows should be added
- align workflow migration behavior with Ava SemVer and release guidance
- update affected role, workflow, and roadmap documentation
