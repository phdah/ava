---
type: Workflow
title: Review change
description: Performs a bounded read-only semantic review of a proposed or completed project change.
primary_role: /.ava/base/roles/change-reviewer/role.md
mode: read-only
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Review change

## Purpose

Evaluate the semantic effects of one proposed or completed project change without modifying the project or performing remediation.

This workflow standardizes review evidence, severity, independence disclosure, and remediation ownership for a bounded change.

## Inputs

### `change_target`

- Required: yes
- Description: Patch, commit, pull request, changed files, or other bounded project change to review.

### `review_scope`

- Required: no
- Description: Specific semantic concerns or project area to prioritize.
- Default: semantic effects within the changed scope

### `authoring_context`

- Required: no
- Description: Information needed to classify whether the review is independent, isolated, or reduced independence.
- Default: unknown

## Procedure

1. Resolve the change target, requested scope, expected outcome, and whether the change is proposed or already applied.
2. Determine and disclose the practical independence level of the review.
3. Inspect the changed material, applicable instructions, and only the related context needed to understand its semantic effect.
4. Evaluate relevant authority, safeguards, ownership, routing, instruction consistency, trust boundaries, and decision completeness.
5. Report evidence-based findings, remediation ownership, conclusion, inspected scope, and material limitations without changing files.

## Expected output

Return findings with severity, evidence, consequence, recommended correction, and responsible remediation owner, followed by the review conclusion and independence level. Report only because this workflow uses `read-only` mode.
