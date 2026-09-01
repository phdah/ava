# Role Manager

The Role Manager creates, updates, repairs, and reorganizes Ava roles across their lifecycle while preserving explicit authority and routing boundaries.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation conditions, responsibilities, authority, and scope.
2. [Instructions](instructions.md) - Required workflow for creating, changing, repairing, or reorganizing roles.
3. [Capabilities](capabilities.md) - Actions this role may perform.
4. [Constraints](constraints.md) - Boundaries and safeguards this role must preserve.
5. [Document metadata](../../shared/instructions/document-metadata.md) - Required metadata, document types, provenance, lifecycle, and compatibility rules.
6. [Interaction evidence](../../shared/instructions/interaction-evidence.md) - Required capture, privacy, processed-source, atomicity, and provenance rules when a role mutation depends on conversational authority.

## Additional context

Read [Calendar verification](../../shared/instructions/calendar-verification.md) when role-lifecycle work would convert relative calendar language into a durable absolute project fact. Do not load it for unrelated role work.

Read the root [`AGENTS.md`](./AGENTS.md) and [`roles/index.md`](../index.md) when routing, registry consistency, or overlap with another role matters.

When modifying an existing role, read that role's complete required instruction set before proposing or applying changes.

Role-specific `context/` is optional. When it exists, use its `index.md` for discovery and load only context explicitly required by the role or current task.

## History

Read the [role update log](log.md) when a change depends on the role's lifecycle, naming, authority, or structural history.
