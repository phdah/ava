---
type: Workflow
title: Curate project knowledge
description: Organizes, consolidates, corrects, and connects trusted project knowledge within an approved bounded scope.
primary_role: /roles/project-steward/role.md
mode: mutation
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Curate project knowledge

## Purpose

Improve trusted project knowledge within a bounded scope without ingesting untrusted sources or changing unsupported policy.

## Inputs

### `scope`

- Required: yes
- Description: Named files, directory, concept, domain, or trusted knowledge area to curate.

### `curation_goal`

- Required: no
- Description: Specific outcome to prioritize during curation.
- Default: improve clarity, consistency, and discovery

## Procedure

1. Traverse the nearest relevant indexes and inspect only trusted knowledge within the supplied scope.
2. Identify stale, duplicated, contradictory, orphaned, misplaced, or weakly connected content.
3. Preserve unresolved conflicts, uncertain deletions, unsupported claims, and role-specific material for the appropriate decision or owner.
4. Consolidate, correct, move, link, or create focused canonical content only where the authoritative destination is clear.
5. Preserve provenance and unknown metadata, update affected indexes and links, and record major scoped history when required.
6. Validate the resulting knowledge structure and discovery paths.

## Expected output

Return the knowledge changes applied, content preserved or deferred, provenance handling, affected indexes, validation performed, and any unresolved decision. Apply supported changes because this workflow uses `mutation` mode.
