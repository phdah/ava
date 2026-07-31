# Workflows

This file is the managed registry root for reusable default workflows. Project-owned workflows are discovered separately through `/workflows/index.md` when present.

A workflow is registered only when it is reachable by following discovery links from this index. Each workflow-owning subdirectory must maintain its own `index.md` and list only direct child files and directories.

Each workflow activates exactly one primary role and defines procedure-specific inputs, operating mode, required context, procedure, and expected output without duplicating the role's durable instructions.

Workflow files must follow the shared [workflow format](../shared/instructions/workflow-format.md). Invocation, routing precedence, primary-role resolution, validation, and deprecation follow [workflow registry and routing](../shared/instructions/workflow-routing.md).

Invoke a workflow by its canonical installed path or by an unambiguous lowercase kebab-case filename stem. Workflow titles are descriptive and are not stable invocation identifiers.

Semantic Ava version reconciliation is not a workflow. A role declaring `activation_mode: managed-pre-routing` is invalid as a workflow `primary_role`. Active upgrade state directly selects the managed Upgrade Role before workflow discovery, and normal workflow routing remains blocked until the upgrade protocol permits it.

## Available workflows

### Role lifecycle

- [Create role](create-role.md) - Creates one new role when the registered catalog cannot represent the required responsibility and authority boundary.
- [Update role](update-role.md) - Applies an approved bounded change to an existing role.
- [Repair role](repair-role.md) - Repairs an incomplete or inconsistent role without silently changing its intended authority.

### Project stewardship

- [Configure project](configure-project.md) - Establishes or updates approved project-wide guidance and configuration.
- [Curate project knowledge](curate-project-knowledge.md) - Organizes and improves trusted project knowledge within a bounded scope.
- [Tighten instructions](tighten-instructions.md) - Clarifies project-wide instructions while preserving their meaning and authority.
- [Daily project maintenance](daily-project-maintenance.md) - Inspects a bounded project scope and proposes prioritized maintenance without applying changes.

### Inbox ingestion

- [Ingest inbox](ingest-inbox.md) - Processes all pending direct inbox sources while preserving trust boundaries and provenance.

### Change review

- [Review change](review-change.md) - Performs a read-only semantic review of a bounded project change.
- [Review role change](review-role-change.md) - Performs a read-only semantic review focused on an Ava role change.
