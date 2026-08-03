---
type: Workflow
title: Audit project context
description: Performs a bounded project-context health audit and returns prioritized maintenance proposals without modifying project files.
primary_role: /.ava/base/roles/project-steward/role.md
mode: suggestion
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Audit project context

## Purpose

Audit a bounded part of the project's trusted context and produce a prioritized maintenance proposal with evidence, ownership, and unresolved decisions.

This workflow standardizes a repeatable audit outcome. It does not replace ordinary Project Steward maintenance requests and does not apply the proposed changes.

## Inputs

### `scope`

- Required: yes
- Description: Bundle-root-relative files, directories, indexes, or named project concern to inspect.

### `change_window`

- Required: no
- Description: Optional time, commit, or change boundary used to focus the audit.
- Default: none

### `focus`

- Required: no
- Description: Specific maintenance concerns to prioritize during the audit.
- Default: stale, duplicated, contradictory, orphaned, misplaced, or unclear context

## Procedure

1. Resolve the supplied scope, change window, and focus without expanding them into an unrestricted project scan.
2. Traverse the nearest relevant indexes and inspect only trusted project content needed for the audit.
3. Identify supported maintenance findings and separate them from deterministic validation, role-specific work, inbox ingestion, semantic review of a change, and upgrade reconciliation.
4. Record evidence, likely consequence, confidence, and the role or owner responsible for each supported action.
5. Rank maintenance actions by impact, urgency, and confidence.
6. Produce a bounded proposal without creating, updating, moving, or deleting project files.

## Expected output

Return the inspected scope and limitations, prioritized findings with evidence and responsible owner, deterministic checks that should be run separately, and any unresolved decisions. Do not apply changes because this workflow uses `suggestion` mode.
