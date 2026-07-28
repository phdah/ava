---
type: Workflow
title: Update role
description: Applies an approved bounded change to an existing Ava role while preserving unrelated decisions and routing boundaries.
primary_role: /roles/role-manager/role.md
mode: mutation
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Update role

## Purpose

Update one existing role to reflect an approved change to its definition, instructions, authority, safeguards, structure, or role-specific context.

## Inputs

### `role_path`

- Required: yes
- Description: Bundle-root-relative path to the existing role directory or its `role.md` document.

### `requested_change`

- Required: yes
- Description: Approved semantic or structural change to apply to the role.

## Procedure

1. Resolve the registered role and read its complete required instruction set.
2. Inspect closely related roles and affected references when the requested change may alter routing or ownership.
3. Identify material ambiguity before changing authority, safeguards, destructive behaviour, or role identity.
4. Apply the smallest coherent update while preserving unrelated role decisions and unknown metadata.
5. Update the registry, manifests, links, migrations, and scoped history when the change requires them.
6. Validate the resulting role structure and internal consistency.

## Expected output

Return the role updated, the semantic and structural changes applied, affected references, validation performed, and any unresolved decision. Apply approved changes because this workflow uses `mutation` mode.
