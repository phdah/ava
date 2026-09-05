---
id: ava-201
title: "Finalize and rename the Role Generator as the Role Manager"
status: "Done"
labels: ["internal", "roadmap", "phase-02"]
ordinal: 201
---

## Description

Finalize the Role Manager lifecycle role. This task contains the complete pre-Backlog task record and the phase-level role-catalog context that previously lived separately.

## Migrated task record

---
type: Internal Development Task
title: Finalize and Rename the Role Generator as the Role Manager
description: Rename and broaden the existing role lifecycle role while preserving clear authority boundaries.
tags: [internal, roadmap, roles, role-manager]
status: complete
phase: 2
order: 1
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T22:20:00Z
---

# Finalize and Rename the Role Generator as the Role Manager

## Why

The role creates, updates, repairs, and reorganizes roles. "Role Manager" reflects that broader lifecycle more accurately than "Role Generator".

## Applied decisions

- renamed the generated role from `roles/role-generator/` to `roles/role-manager/`
- made role creation, updates, repair, reorganization, approved identity changes, deprecation, and removal one explicit lifecycle responsibility
- retained the five-file mandatory role structure: `index.md`, `role.md`, `instructions.md`, `capabilities.md`, and `constraints.md`
- required every role index to expose the complete mandatory reading set and any shared instructions needed for all uses of the role
- made role-specific `context/` optional, indexed when present, and conditionally loaded through explicit links
- made role-scoped `log.md` optional and governed by the scoped-history contract
- added overlap decisions for reusing, narrowing, combining, splitting, or creating roles
- kept project-wide configuration, general trusted knowledge maintenance, inbox ingestion, independent review, and deterministic validation outside Role Manager authority
- defined the role as the primary authority for role-lifecycle workflows such as `create-role`, `update-role`, and `repair-role` without transferring ownership of general workflow definition

## Applied integration

- replaced the Role Generator entry in the generated role registry with the Role Manager
- migrated cross-role ownership references and shared metadata examples to the new role name and path
- added a role-scoped log for the identity and lifecycle change
- removed the obsolete `templates/base/roles/role-generator/` directory after migrating references
- kept the Role Manager inside `templates/base/roles/`, so it remains part of the final `ava init` base catalog

## Completion

- [x] renamed `templates/base/roles/role-generator/` to `templates/base/roles/role-manager/`
- [x] updated the role definition and registry entry
- [x] migrated existing references
- [x] clarified routing boundaries against the other core roles
- [x] finalized the mandatory role-file set and optional role-context rules
- [x] confirmed the role's required files and required-reading manifest are complete
- [x] ensured the role remains included in the final `ava init` base catalog

## Migrated phase roadmap context

# Phase 02: Core Roles for Initialized Projects

Keep the default role catalog small, with distinct routing conditions and focused authority.

A new role is justified when responsibility, authority, trust boundary, context requirements, or separation of duty changes. A new workflow alone does not require a new role.

The completed catalog was `role-manager`, `project-steward`, `inbox-ingester`, `change-reviewer`, and `ava-maintenance`.

Ava Maintenance owns agent-facing understanding of the installed Ava distribution and its operational lifecycle. It is distinct from the repository-only Ava Internal Maintainer and from Upgrade Role, which is activated only for project-owned semantic reconciliation.

The core-role catalog is complete. Deterministic installation administration routes to Ava Maintenance, project-owned semantic reconciliation routes to Upgrade Role, and ordinary project roles retain their focused authority.