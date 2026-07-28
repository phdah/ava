---
type: Workflow
title: Repair role
description: Repairs an incomplete or internally inconsistent Ava role without silently broadening its authority or changing its intended purpose.
primary_role: /roles/role-manager/role.md
mode: mutation
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Repair role

## Purpose

Restore one existing role to a complete, navigable, and internally consistent state while preserving its established intent and authority.

## Inputs

### `role_path`

- Required: yes
- Description: Bundle-root-relative path to the role directory or its `role.md` document.

### `repair_scope`

- Required: no
- Description: Specific defect or part of the role structure to repair.
- Default: complete role structure

## Procedure

1. Read the role's complete available instruction set and determine its established intended behaviour.
2. Compare the role with the mandatory role structure, registry entry, required-reading manifest, and affected references.
3. Separate clear repair work from ambiguity that would change purpose, authority, safeguards, routing, or lifecycle.
4. Repair only supported defects and preserve unresolved semantic decisions for the user.
5. Update affected registry entries, links, manifests, and scoped history when required.
6. Validate the repaired role structure and consistency.

## Expected output

Return the defects found, repairs applied, preserved ambiguities, affected files and references, and validation performed. Apply supported repairs because this workflow uses `mutation` mode.
