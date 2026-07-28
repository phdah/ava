---
type: Workflow
title: Configure project
description: Establishes or updates approved project-wide purpose, terminology, policies, conventions, instructions, or discovery guidance.
primary_role: /roles/project-steward/role.md
mode: mutation
status: stable
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Configure project

## Purpose

Apply approved project-wide configuration within a bounded scope while keeping shared guidance separate from role-specific authority.

## Inputs

### `configuration_scope`

- Required: yes
- Description: Project-wide topic, policy area, convention, instruction set, or discovery structure to configure.

### `approved_configuration`

- Required: yes
- Description: User-approved decisions or requirements that the project configuration must express.

## Procedure

1. Read the nearest relevant indexes and existing authoritative project-wide guidance for the requested scope.
2. Identify content that belongs to a role, inbox ingestion, independent review, or another excluded owner.
3. Resolve material ambiguity affecting authority, access, policy, safeguards, or routing before mutation.
4. Apply the smallest coherent project-wide configuration that expresses the approved decisions.
5. Update affected discovery links and scoped history when required, then validate the changed documents.

## Expected output

Return the configuration applied, files and indexes changed, excluded or deferred concerns, validation performed, and any unresolved decision. Apply approved changes because this workflow uses `mutation` mode.
