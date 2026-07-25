---
type: Internal Development Task
title: Finalize and Rename the Role Generator as the Role Manager
description: Rename and broaden the existing role lifecycle role while preserving clear authority boundaries.
tags: [internal, roadmap, roles, role-manager]
status: pending
phase: 2
order: 1
timestamp: 2026-07-25T00:00:00Z
---

# Finalize and Rename the Role Generator as the Role Manager

## Why

The role creates, updates, repairs, and reorganizes roles. "Role Manager" reflects that broader lifecycle more accurately than "Role Generator".

## Current state

A Role Generator exists under `templates/base/roles/role-generator/`. This task includes reviewing it, renaming it, and updating all affected links and registry entries.

## Intended responsibilities

- create and update project roles from user intent
- define purpose, activation, responsibilities, instructions, capabilities, and constraints
- create focused role-specific context when needed
- maintain the generated project's role registry
- detect overlap and recommend reusing, narrowing, combining, or splitting roles
- repair incomplete role structures within its existing scope
- support role-related workflows such as `create-role`, `update-role`, and `repair-role`

## Boundaries

- must not define or change Ava's public format contract
- must not silently decide destructive authority, security boundaries, or sensitive access
- must not perform the normal work of the roles it creates
- must remain distinct from project-wide configuration and general knowledge maintenance
- should use deterministic Ava validation tools rather than reproducing link or schema validation in prose

## Completion criteria

- rename `templates/base/roles/role-generator/` to `templates/base/roles/role-manager/`
- update the role definition and registry entry
- preserve or explicitly migrate existing references
- clarify routing boundaries against the other core roles
- confirm all required role files are complete
- ensure the role is included in the final `ava init` base catalog
