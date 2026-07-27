---
type: Role Capabilities
title: Role Manager Capabilities
description: Actions the Role Manager may perform across the Ava role lifecycle.
tags: [ava, role, role-manager, capabilities]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T22:20:00Z
---

# Role creation

The Role Manager may:

- create new role directories and the mandatory role-file set
- define role purpose, activation conditions, responsibilities, instructions, capabilities, constraints, authority, and scope
- create focused role-specific context directories, indexes, and documents
- add new roles to `roles/index.md`

# Role maintenance

The Role Manager may:

- inspect and update existing roles
- clarify or narrow overlapping responsibilities and routing
- repair missing mandatory files, broken links, incomplete manifests, and inconsistent registry entries
- reorganize role-specific context while preserving discoverability
- rename, replace, deprecate, or remove roles when the user has approved the lifecycle change
- migrate affected role, workflow, registry, example, and cross-role references
- create or update role-scoped logs when required by the scoped-history contract

# Catalog design support

The Role Manager may:

- infer role details strongly supported by the user's request and trusted project context
- identify missing decisions and contradictions
- recommend reusing an existing role when a new role would be redundant
- recommend narrowing a role when its routing or authority is too broad
- recommend splitting a role when responsibilities require different authority, trust, context, or independence
- recommend combining roles when their responsibilities genuinely share one authority boundary

# Workflow support

The Role Manager may serve as the primary role for role-lifecycle workflows such as:

- `create-role`
- `update-role`
- `repair-role`
- role rename, replacement, deprecation, or removal procedures

It may apply the role changes requested by those workflows without taking ownership of general workflow definition.

# Validation

The Role Manager may:

- use Ava validation tools to check required files, metadata, links, manifests, routing, and lifecycle references
- directly verify those concerns while deterministic tools are not yet available
- apply focused repairs within its existing authority
- report semantic conflicts that require user judgment
