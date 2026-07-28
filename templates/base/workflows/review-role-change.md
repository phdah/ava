---
type: Workflow
title: Review role change
description: Performs a bounded read-only semantic review focused on changes to an Ava role, its routing, authority, safeguards, or lifecycle.
primary_role: /roles/change-reviewer/role.md
mode: read-only
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Review role change

## Purpose

Evaluate one proposed or completed role change for semantic consistency, authority safety, routing clarity, and lifecycle completeness without applying remediation.

## Inputs

### `change_target`

- Required: yes
- Description: Patch, commit, pull request, changed files, or other bounded role change to review.

### `role_path`

- Required: yes
- Description: Bundle-root-relative path to the affected role directory or its `role.md` document.

### `authoring_context`

- Required: no
- Description: Information needed to classify whether the review is independent, isolated, or reduced independence.
- Default: unknown

## Procedure

1. Resolve the change target, affected role, expected outcome, and whether the change is proposed or already applied.
2. Determine and disclose the practical independence level of the review.
3. Read the affected role's required instruction set, relevant registry entry, related roles, and changed material.
4. Evaluate purpose, activation, responsibilities, capabilities, constraints, routing, required reading, trust boundaries, lifecycle, and affected references.
5. Report evidence-based findings, remediation ownership, conclusion, inspected scope, and material limitations without changing files.

## Expected output

Return findings with severity, affected role scope, evidence, consequence, recommended correction, and responsible remediation owner, followed by the review conclusion and independence level. Report only because this workflow uses `read-only` mode.
