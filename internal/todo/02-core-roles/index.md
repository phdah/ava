# Phase 02: Core Roles for Initialized Projects

Keep the default role catalog small, with distinct routing conditions and focused authority.

A new role is justified when responsibility, authority, trust boundary, context requirements, or separation of duty changes. A new workflow alone does not require a new role.

## Intended catalog

```text
role-manager
project-steward
inbox-ingester
change-reviewer
ava-maintenance
```

The Ava Maintenance role owns agent-facing understanding of the installed Ava distribution and its operational lifecycle. It is distinct from the repository-only Ava Internal Maintainer and from the managed Upgrade Role used during semantic reconciliation.

## Tasks

1. [x] [Finalize and rename the Role Generator as the Role Manager](01-finalize-role-manager.md)
2. [x] [Create the Project Steward role](02-create-project-steward.md)
3. [x] [Create the Inbox Ingester role and inbox convention](03-create-inbox-ingester.md)
4. [x] [Create the Change Reviewer role](04-create-change-reviewer.md)
5. [ ] [Create the Ava Maintenance role](05-create-ava-maintenance-role.md)

Document update metadata, installed paths, and OpenCode configuration are complete. Task 5 is now the current v1 blocker before the final conformance matrix and first alpha.

## Current active task

[Create the Ava Maintenance role](05-create-ava-maintenance-role.md).

## Previous phase

[Format contract and base structure](../01-format-contract/) is complete.

## Next phase

[Workflow system](../03-workflows/) is complete. After task 5, return to the final [distribution conformance task](../04-distribution-and-upgrades/10-implement-validation-and-upgrade-fixtures.md).
