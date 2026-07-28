---
type: Workflow
title: Tighten instructions
description: Clarifies and shortens existing project-wide instructions without changing their meaning, authority, permissions, constraints, or routing.
primary_role: /roles/project-steward/role.md
mode: mutation
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Tighten instructions

## Purpose

Improve the precision and economy of existing project-wide instructions while preserving every semantic and authority boundary.

## Inputs

### `scope`

- Required: yes
- Description: Project-wide instruction files or instruction topic to tighten.

### `preserve_examples`

- Required: no
- Description: Whether useful examples should remain when they clarify normative behaviour.
- Default: yes

## Procedure

1. Read the complete active instruction context needed to interpret the supplied scope.
2. Identify repetition, filler, narrow wording, unclear ownership, and wording that obscures permissions or constraints.
3. Rewrite only where meaning, authority, safeguards, exceptions, routing, and unknown metadata can be preserved.
4. Keep one authoritative statement for each rule and use links instead of duplicated normative text where appropriate.
5. Update affected indexes or links and validate the tightened instruction set for internal consistency.

## Expected output

Return the instructions changed, the redundancies or ambiguities removed, preserved safeguards and semantics, validation performed, and any unresolved decision. Apply safe tightening because this workflow uses `mutation` mode.
