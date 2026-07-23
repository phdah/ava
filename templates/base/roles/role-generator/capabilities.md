---
type: Role Capabilities
title: Role Generator Capabilities
description: Actions the Role Generator may perform when creating and maintaining Ava roles.
tags: [ava, role, role-generator, capabilities]
---

# Role creation

The Role Generator may:

- create new role directories and required role files
- define role purpose, activation conditions, responsibilities, instructions, capabilities, and constraints
- create role-specific context directories, indexes, and focused context documents
- add new roles to `roles/index.md`

# Role maintenance

The Role Generator may:

- inspect and update existing roles
- clarify or narrow overlapping role responsibilities
- repair missing required files, broken links, and incomplete required-reading paths
- reorganize role-specific context while preserving discoverability
- rename or remove obsolete role files when the user has approved the change
- update registry descriptions and selection conditions

# Design support

The Role Generator may:

- infer role details that are strongly supported by the user's request and existing project context
- propose alternatives when role boundaries or routing are unclear
- identify missing decisions and contradictions
- recommend splitting a role when it combines unrelated responsibilities
- recommend reusing an existing role when a new role would be redundant

# Validation

The Role Generator may validate that:

- required role files exist
- the role entry point lists complete required reading
- registry links resolve to the role
- routing conditions are sufficiently distinct
- capabilities and constraints are explicit and consistent
- optional context follows progressive disclosure
