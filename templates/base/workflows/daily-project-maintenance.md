---
type: Workflow
title: Daily project maintenance
description: Performs a bounded recurring project health inspection and proposes prioritized maintenance without changing project files.
primary_role: /roles/project-steward/role.md
mode: suggestion
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Daily project maintenance

## Purpose

Inspect a bounded project scope for maintenance needs and produce a prioritized proposal without applying workspace changes.

## Inputs

### `scope`

- Required: yes
- Description: Named files, directories, indexes, or project concern to inspect during this maintenance run.

### `change_window`

- Required: no
- Description: Time or change boundary used to focus the inspection.
- Default: since the previous successful maintenance run

## Procedure

1. Resolve the supplied scope and change window without expanding them into a complete project scan.
2. Inspect relevant indexes and trusted project content for stale, duplicated, contradictory, orphaned, misplaced, or unclear material.
3. Separate deterministic validation needs, role-specific work, inbox ingestion, and independent review from Project Steward maintenance.
4. Rank supported maintenance actions by impact, urgency, and confidence.
5. Produce a bounded proposal and identify decisions or follow-up owners without mutating project files.

## Expected output

Return a prioritized maintenance proposal, inspected scope, evidence for each recommendation, deferred ownership, and unresolved decisions. Do not apply changes because this workflow uses `suggestion` mode.
