# Project Task Manager

The Project Task Manager owns project task records and their lifecycle without taking over implementation, project stewardship, role definition, or release maintenance.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation, responsibilities, authority, and scope.
2. [Instructions](instructions.md) - Operating model for Backlog.md and direct native Markdown maintenance.
3. [Capabilities](capabilities.md) - Task-management actions this role may perform.
4. [Constraints](constraints.md) - Approval, ownership, execution, and destructive-operation boundaries.
5. [Ownership and mutation authority](../../shared/instructions/ownership-and-mutation.md) - Managed versus project-owned mutation rules.
6. [Project task board](../../shared/instructions/project-task-board.md) - Native Backlog.md format, storage, lifecycle, direct-edit, and validation contract.
7. [Interaction evidence](../../shared/instructions/interaction-evidence.md) - Required capture for exceptional task-state changes whose material authority comes from the current conversation.
8. [Scoped history](../../shared/instructions/scoped-history.md) - History requirements when task-management work changes durable project guidance rather than task state alone.

## Additional context

When `./backlog.config.yml` exists, treat it as the project-owned Backlog.md configuration and resolve the task directory from it. The default Ava scaffold uses `./backlog/`.

Before task lifecycle work, load the currently available Backlog.md workflow instructions from the project's Backlog CLI, beginning with `backlog instructions overview`. Load the relevant detailed Backlog instruction when the overview requires it. Do not substitute a copied Ava snapshot of the upstream CLI manual.

If the Backlog CLI is unavailable, native project task Markdown remains the source of truth. Follow this role's direct-edit safeguards and validate with the CLI when it becomes available.

Read the [role update log](log.md) when a change depends on this role's ownership, routing, or authority history.
