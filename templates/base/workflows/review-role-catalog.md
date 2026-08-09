---
type: Workflow
title: Review role catalog
description: Performs a read-only semantic audit of the complete registered role catalog as one routing and authority system.
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

# Review role catalog

## Purpose

Review the registered managed and project-owned role catalog as a system for responsibility coverage, routing clarity, authority separation, safeguards, and lifecycle consistency.

This workflow is an explicitly broad catalog audit rather than ordinary bounded acceptance review. It standardizes a complete catalog-level outcome without applying remediation.

## Inputs

### `catalog_scope`

- Required: no
- Description: Registered role paths or registry roots to include in the review.
- Default: all managed and project-owned registered roles

### `review_focus`

- Required: no
- Description: Catalog concerns to prioritize.
- Default: responsibility coverage, routing overlap, authority, safeguards, trust boundaries, and lifecycle consistency

### `review_standard`

- Required: no
- Description: `audit` for complete catalog improvement discovery or `acceptance` when the user explicitly wants only an acceptance decision for the supplied catalog scope.
- Default: `audit`

### `prior_review`

- Required: no
- Description: Prior catalog findings, conclusion, scope, and remediation evidence when this invocation is a re-review.
- Default: none

### `authoring_context`

- Required: no
- Description: Information needed to classify whether the review is independent, isolated, or reduced independence.
- Default: unknown

## Procedure

1. Resolve the managed role registry and the project-owned role registry when present, then apply the supplied catalog scope.
2. Apply the requested review standard, defaulting to the explicit `audit` standard for this catalog-wide workflow.
3. Determine and disclose the practical independence level of the review.
4. When prior review state is supplied, evaluate every prior finding and its remediation before considering evidence-backed new concerns.
5. Read each included role's index and complete required instruction set, including any managed pre-routing role needed to assess activation separation.
6. Compare the catalog for responsibility gaps, overlapping activation, ambiguous free-form routing, unsupported authority, weakened safeguards, trust-boundary conflicts, and incomplete lifecycle references.
7. Distinguish admitted semantic findings, optional observations, and deterministic metadata, link, manifest, or filesystem validation.
8. Report evidence-based findings and the role or project owner responsible for remediation without modifying files.

## Expected output

Return the catalog scope, review standard, independence level, role coverage summary, admitted findings with severity, affected roles, evidence, consequence, recommended correction, and remediation owner. For re-review, include every prior finding's disposition and changed evidence for any new or reopened finding. Keep optional observations separate. End with the terminal conclusion and material limitations required by the active review standard. Report only because this workflow uses `read-only` mode.
