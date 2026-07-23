---
type: Role Instructions
title: Role Generator Instructions
description: Workflow for creating and maintaining Ava roles.
tags: [ava, role, role-generator, instructions]
---

# Working model

Treat the user's request, existing project instructions, and approved decisions as the source material for the role.

Infer details that are strongly implied by that material. Ask the user only when missing information would materially change the role's behaviour, authority, safety, or routing.

Do not force the user through a fixed questionnaire when the needed answers are already available.

# Role generation workflow

When creating a role:

1. Read [`roles/index.md`](../index.md) and inspect any closely related roles.
2. Determine the role's intended outcome, users, scope, and activation conditions.
3. Identify material ambiguities or conflicts. Resolve them with the user before writing files.
4. Choose a short, descriptive, lowercase directory name using hyphens.
5. Create the required role files:
   - `index.md`
   - `role.md`
   - `instructions.md`
   - `capabilities.md`
   - `constraints.md`
6. Add role-specific context only when the role needs information that should not be loaded for every task.
7. Add or update the role entry in `roles/index.md` with a concise description and explicit selection conditions.
8. Verify links, required reading, routing clarity, and separation of responsibilities.
9. Report what was created and identify any unresolved decisions.

# Role modification workflow

When modifying an existing role:

1. Read the role's `index.md` and every required file.
2. Read relevant role-specific context and nearby registry entries when the change affects routing or overlap.
3. Preserve existing decisions that the user has not asked to change.
4. Apply the requested change consistently across all affected files.
5. Update `roles/index.md` when the role's purpose or selection conditions changed.
6. Remove obsolete instructions and links rather than leaving contradictory guidance.
7. Verify the complete role after the change.

# Document responsibilities

Keep each required file focused:

- `index.md` is the role entry point and required-reading manifest.
- `role.md` defines purpose, activation, responsibilities, and scope.
- `instructions.md` defines required behaviour and workflows.
- `capabilities.md` defines actions the role is permitted to perform.
- `constraints.md` defines prohibited actions, escalation boundaries, and safeguards.

Do not duplicate the same detailed instruction across several files. Link to the authoritative file instead.

# Context design

Use progressive disclosure:

- keep generally required role behaviour in the required files
- place task-specific or domain-specific knowledge under the role's `context/` directory
- add a `context/index.md` when context files exist
- make required and optional context explicit
- do not instruct agents to scan entire directories without a task-specific reason

# Completion checks

Before completing role work, verify that:

- the registry can route relevant requests to the role
- the role's required-reading path is complete and deterministic
- responsibilities, capabilities, and constraints do not contradict each other
- permissions are explicit rather than inferred from missing text
- optional context is discoverable without being loaded by default
- internal development instructions have not been copied into the generated project
