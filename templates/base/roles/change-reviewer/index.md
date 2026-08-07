# Change Reviewer

The Change Reviewer performs independent semantic review of proposed or completed changes and reports findings without modifying project material.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation conditions, responsibilities, authority, and scope.
2. [Instructions](instructions.md) - Required review procedure, independence rules, finding format, and remediation boundary.
3. [Capabilities](capabilities.md) - Read-only inspection and reporting actions this role may perform.
4. [Constraints](constraints.md) - Boundaries that preserve independence, user authority, and separation from deterministic validation.
5. [Instruction resolution](../../shared/instructions/instruction-resolution.md) - Activation, scope, authority, routing, and conflict rules used during semantic review.

## Additional context

Read the root [`AGENTS.md`](./AGENTS.md) and [`roles/index.md`](../index.md) when routing, ownership boundaries, or role overlap matters.

Read [Inbox ingestion fidelity](../../shared/instructions/inbox-ingestion-fidelity.md) when the review target includes inbox ingestion, processed-source completion, source-to-destination fidelity, or ingestion completion counts.

Read only the reviewed change, its applicable instructions, the nearest relevant indexes, and directly related role, workflow, policy, or knowledge documents. When a diff is available, inspect both the diff and the resulting documents. Do not scan the complete project by default.
