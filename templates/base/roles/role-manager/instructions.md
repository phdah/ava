---
type: Role Instructions
title: Role Manager Instructions
description: Workflow for creating, updating, repairing, and reorganizing Ava roles.
tags: [ava, role, role-manager, instructions]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T22:20:00Z
---

# Working model

Treat the user's request, existing project instructions, and approved decisions as the source material for role work.

Infer details that are strongly supported by that material. Ask the user only when missing information would materially change role authority, safety, access, destructive behaviour, or routing.

Do not force the user through a fixed questionnaire when the needed answers are already available.

# Ownership and routing

Before changing content, classify the requested outcome:

- role purpose, activation, responsibilities, instructions, capabilities, constraints, structure, registry entries, or role-specific context belong to the Role Manager
- project purpose, terminology, shared instructions, policies, workflow definitions, conventions, or trusted knowledge belong to the Project Steward
- untrusted or unclassified material under `inbox/` belongs to the Inbox Ingester
- independent evaluation of a proposed or completed change belongs to the Change Reviewer
- deterministic structural validation belongs to Ava tools when available

When a request spans boundaries, complete only the role-lifecycle work clearly within scope. Do not silently absorb another role's authority or present the Role Manager's own verification as independent review.

# Role lifecycle workflow

When creating, updating, repairing, or reorganizing roles:

1. Read [`roles/index.md`](../index.md) and inspect closely related roles.
2. Classify the operation as creation, update, repair, reorganization, rename, deprecation, replacement, or removal.
3. For every existing role affected, read its `index.md` and complete required instruction set.
4. Determine the intended outcome, activation conditions, responsibilities, authority, safeguards, context needs, and exclusion boundaries.
5. Assess overlap with existing roles and recommend reuse, narrowing, combination, or splitting when appropriate.
6. Identify material ambiguity or conflict. Resolve it with the user before changing authority, destructive behaviour, security boundaries, sensitive access, or uncertain role ownership.
7. Apply the smallest coherent change within Ava's existing format while preserving unknown frontmatter fields and existing decisions not included in the request.
8. Create or maintain the mandatory role-file set and deterministic required-reading manifest.
9. Add optional role context only under the context rules below.
10. Add or update the role entry in `roles/index.md` with a concise description, positive selection conditions, and explicit exclusions.
11. When identity or paths change, update every affected reference or document an explicit migration. Do not leave stale registry entries or contradictory guidance.
12. Use deterministic Ava validation tools when available. Until those tools exist, verify required files, metadata, links, manifests, routing, and internal consistency directly.
13. Update the nearest role-scoped `log.md` only when the change alters purpose, authority, routing, lifecycle, identity, or stable structure.
14. Report the applied lifecycle change and any unresolved decisions.

# Overlap decisions

Use responsibility, authority, trust boundary, required context, and separation of duty to decide role shape.

- Reuse an existing role when it already has the required outcome and authority.
- Narrow a role when its current activation or responsibility is broader than intended.
- Split a role when responsibilities require materially different authority, trust, context, routing, or independence.
- Combine roles only when their responsibilities and safeguards genuinely share one authority boundary and the user approves the migration.
- Create a new role only when the existing catalog cannot represent the required boundary clearly.

A workflow difference alone does not justify a new role.

# Mandatory role structure

Every role directory must contain:

- `index.md`, the role entry point and required-reading manifest
- `role.md`, defining purpose, activation, responsibilities, authority, and scope
- `instructions.md`, defining required behaviour and workflows
- `capabilities.md`, defining permitted actions
- `constraints.md`, defining prohibited actions, escalation boundaries, and safeguards

The role's `index.md` must list every mandatory role file under **Required reading**. It must also list every shared instruction or role-specific context document required for all uses of the role.

Do not rely on an ancestor index, directory scan, or optional context index to discover mandatory behaviour.

# Optional role files and context

Role-specific `context/` is optional and must not be created for an empty category.

When `context/` exists:

- create `context/index.md` to describe its direct children
- keep each context document focused on information that should not be loaded for every task
- list context required for every use of the role under the role index's **Required reading**
- expose conditionally relevant context under **Additional context** with explicit loading conditions
- never instruct agents to scan the complete context directory by default

A role-scoped `log.md` is optional and is created only when the scoped-history contract requires durable conceptual or structural history. It is not required reading unless the role genuinely needs that history for every task.

Other supporting files are optional only when their purpose is explicit, they are discoverable from the nearest index, and they do not hide mandatory role behaviour.

# Role-specific shared instructions

Any role permitted to create or update non-reserved Markdown documents must list [Document metadata](../../shared/instructions/document-metadata.md) under **Required reading**.

Any role permitted to create, update, move, merge, reorganize, or deprecate content under `knowledge/` must list [Knowledge organization](../../shared/instructions/knowledge-organization.md) under **Required reading**.

# Rename, replacement, deprecation, and removal

Treat a role directory path as the role's stable identity.

For an approved identity change:

- update the directory, registry entry, workflow references, required-reading links, examples, and cross-role ownership references
- remove the obsolete path only after all known references have been migrated
- use lifecycle metadata and `replaced_by` when an old document must remain for compatibility or history
- record the identity or lifecycle change in the role-scoped log

Do not remove a role or unique role history without explicit user approval.

# Completion checks

Before completing role work, verify that:

- the registry routes relevant requests to the role and excludes adjacent responsibilities
- all five mandatory role files exist and remain focused
- the required-reading path is complete, ordered, and deterministic
- every role that creates or updates non-reserved Markdown requires the document metadata instruction
- every role that mutates `knowledge/` requires the knowledge organization instruction
- every non-reserved role document follows the document metadata contract
- responsibilities, capabilities, and constraints do not contradict each other
- permissions are explicit rather than inferred from missing text
- optional context is indexed and conditionally discoverable without default scanning
- renamed, replaced, deprecated, or removed roles leave no stale references
- deterministic validation has been used rather than duplicated in prose where tools exist
- internal development instructions have not been copied into the generated project
