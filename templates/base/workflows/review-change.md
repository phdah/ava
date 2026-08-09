---
type: Workflow
title: Review change
description: Performs a bounded read-only semantic review of a proposed or completed project change.
primary_role: ./.ava/base/roles/change-reviewer/role.md
mode: read-only
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T00:27:47+02:00
---

# Review change

## Purpose

Evaluate the semantic effects of one proposed or completed project change without modifying the project or performing remediation.

This workflow standardizes the review standard, finding threshold, re-review state, evidence, severity, independence disclosure, remediation ownership, and terminal conclusion for a bounded change.

## Inputs

### `change_target`

- Required: yes
- Description: Patch, commit, pull request, changed files, or other bounded project change to review.

### `review_scope`

- Required: no
- Description: Specific semantic concerns or project area to prioritize.
- Default: semantic effects within the changed scope

### `review_standard`

- Required: no
- Description: `acceptance` for a bounded acceptance decision or `audit` for explicitly exhaustive improvement discovery.
- Default: `acceptance`

### `prior_review`

- Required: no
- Description: Prior findings, conclusion, scope, and remediation evidence when this invocation is a re-review.
- Default: none

### `authoring_context`

- Required: no
- Description: Information needed to classify whether the review is independent, isolated, or reduced independence.
- Default: unknown

## Procedure

1. Resolve the change target, requested scope, expected outcome, and whether the change is proposed or already applied.
2. Apply the requested review standard, defaulting to `acceptance`.
3. Determine and disclose the practical independence level of the review.
4. When prior review state is supplied, evaluate prior findings and remediation before considering evidence-backed new concerns.
5. Inspect the changed material, applicable instructions, and only the related context needed to understand its semantic effect.
6. Evaluate relevant authority, safeguards, ownership, routing, instruction consistency, trust boundaries, and decision completeness.
7. Admit findings only when they pass the Change Reviewer's evidence, consequence, confidence, and threshold test.
8. Report findings, permitted optional observations, remediation ownership, terminal conclusion, inspected scope, and material limitations without changing files.

## Expected output

Return the review standard and independence level, then admitted findings with severity, evidence, consequence, recommended correction, and responsible remediation owner. For re-review, include the disposition of every prior finding and identify the changed evidence for every admitted new or reopened finding. Keep optional observations separate. End with the terminal conclusion required by the active review standard. Report only because this workflow uses `read-only` mode.
