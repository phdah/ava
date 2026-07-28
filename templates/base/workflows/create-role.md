---
type: Workflow
title: Create role
description: Creates one new Ava role when the existing role catalog cannot represent the required responsibility and authority boundary.
primary_role: /roles/role-manager/role.md
mode: mutation
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Create role

## Purpose

Create one focused Ava role from an approved role intent when reuse or adjustment of an existing role is not sufficient.

## Inputs

### `role_intent`

- Required: yes
- Description: Intended outcome, responsibilities, authority, safeguards, and activation boundary for the proposed role.

### `role_name`

- Required: no
- Description: Preferred human-readable name for the role.
- Default: none

## Procedure

1. Compare the requested role intent with the registered role catalog and identify material overlap.
2. Recommend reuse or adjustment instead of creation when an existing role already owns the required boundary.
3. When a new role remains appropriate, resolve any material ambiguity affecting authority, safeguards, or routing.
4. Create the mandatory role files, deterministic required-reading manifest, and registry entry.
5. Update affected links and scoped history when required, then validate the complete role structure.

## Expected output

Return the created role path, its routing boundary, the files and registry entries applied, the validation performed, and any unresolved decision. Apply approved changes because this workflow uses `mutation` mode.
