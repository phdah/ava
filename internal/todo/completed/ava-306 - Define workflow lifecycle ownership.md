---
id: ava-306
title: "Define workflow lifecycle ownership"
status: "Done"
labels: ["internal", "roadmap", "phase-03"]
ordinal: 306
---

## Description

Define responsibility for creating, maintaining, repairing, migrating, and retiring workflows. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Define Workflow Lifecycle Ownership
description: Evaluate and formalize responsibility for creating, maintaining, repairing, migrating, and retiring workflows.
tags: [internal, roadmap, workflows, roles, lifecycle, migrations]
status: complete
phase: 3
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T13:52:00+02:00
---

# Define Workflow Lifecycle Ownership

This task is complete and finishes Phase 3.

## Implemented ownership decision

The Project Steward owns creation, update, repair, reorganization, rename, deprecation, replacement, removal, and migration of project-owned workflows.

A dedicated Workflow Manager role was not added. Workflow lifecycle work uses the same project-wide authority, trusted context, discovery structures, and policy boundary already assigned to the Project Steward. A separate role would overlap without adding a distinct trust boundary, context requirement, or separation of duty.

Adjacent ownership remains explicit:

- the Role Manager owns role definitions and role lifecycle
- the Change Reviewer performs independent semantic review
- the Upgrade Role applies release-specific semantic changes to project-owned workflows during active upgrade mode and exclusively updates semantic compatibility state
- deterministic installers and updaters replace Ava-managed workflows and run mechanical migrations
- deterministic validators check structure, metadata, links, registries, and references

## Lifecycle procedure

The shared [Workflow lifecycle](/templates/base/shared/instructions/workflow-lifecycle.md) contract defines:

- required inspection of workflow registries, the primary role, related workflows, required context, affected references, release guidance, triggers, and known external binding ownership
- creation, update, repair, reorganization, rename, deprecation, replacement, removal, and migration behavior
- approval boundaries for primary-role changes, mode changes, destructive behavior, trigger behavior, compatibility-sensitive changes, identity changes, and uncertain removal
- maintenance of registries, canonical paths, indexes, references, `replaced_by`, lifecycle metadata, scoped logs, and upgrade completion evidence
- separation between project-owned semantic maintenance, managed release replacement, Upgrade Role migration, and deterministic validation

The Project Steward loads this procedure progressively only when workflow lifecycle work is relevant.

## Workflow catalog decision

No workflow-maintenance workflow was added. Routine workflow lifecycle work remains free-form Project Steward work, and a registered workflow would duplicate the role's durable procedure.

No semantic-upgrade workflow was added. Active semantic Ava version reconciliation continues to select the managed Upgrade Role directly before ordinary workflow or role routing.

## Compatibility alignment

Managed workflow lifecycle follows the Ava SemVer, deprecation, release-note, and release-guidance contracts.

Project-owned workflows remain outside managed replacement. When a release changes workflow format, routing, role paths, trigger discovery, or behavior, installed release guidance identifies affected project-owned concepts and the Upgrade Role applies the bounded semantic migration before compatibility is marked complete.

## Updated documentation

- [Project Steward role](/templates/base/roles/project-steward/)
- [Managed role registry](/templates/base/roles/index.md)
- [Shared workflow lifecycle contract](/templates/base/shared/instructions/workflow-lifecycle.md)
- [Shared instruction registry](/templates/base/shared/instructions/index.md)
- [Project Steward update log](/templates/base/roles/project-steward/log.md)

## Next task

Implement Installer and Updater.