---
type: Workflow
title: Review role catalog
description: Performs a read-only semantic review of the complete registered role catalog as one routing and authority system.
primary_role: /.ava/base/roles/change-reviewer/role.md
mode: read-only
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Review role catalog

## Purpose

Review the registered managed and project-owned role catalog as a system for responsibility coverage, routing clarity, authority separation, safeguards, and lifecycle consistency.

This workflow is broader than reviewing one role change. It standardizes a complete catalog-level outcome without applying remediation.

## Inputs

### `catalog_scope`

- Required: no
- Description: Registered role paths or registry roots to include in the review.
- Default: all managed and project-owned registered roles

### `review_focus`

- Required: no
- Description: Catalog concerns to prioritize.
- Default: responsibility coverage, routing overlap, authority, safeguards, trust boundaries, and lifecycle consistency

### `authoring_context`

- Required: no
- Description: Information needed to classify whether the review is independent, isolated, or reduced independence.
- Default: unknown

## Procedure

1. Resolve the managed role registry and the project-owned role registry when present, then apply the supplied catalog scope.
2. Determine and disclose the practical independence level of the review.
3. Read each included role's index and complete required instruction set, including any managed pre-routing role needed to assess activation separation.
4. Compare the catalog for responsibility gaps, overlapping activation, ambiguous free-form routing, unsupported authority, weakened safeguards, trust-boundary conflicts, and incomplete lifecycle references.
5. Distinguish semantic findings from deterministic metadata, link, manifest, and filesystem validation.
6. Report evidence-based findings and the role or project owner responsible for remediation without modifying files.

## Expected output

Return the catalog scope, independence level, role coverage summary, findings with severity, affected roles, evidence, consequence, recommended correction, and remediation owner, followed by the review conclusion and material limitations. Report only because this workflow uses `read-only` mode.
