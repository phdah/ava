# Phase 02: Core Roles for Initialized Projects

Keep the default role catalog small, with distinct routing conditions and focused authority.

A new role is justified when responsibility, authority, trust boundary, context requirements, or separation of duty changes. A new workflow alone does not require a new role.

## Catalog

```text
role-manager
project-steward
inbox-ingester
change-reviewer
ava-maintenance
```

Ava Maintenance owns agent-facing understanding of the installed Ava distribution and its operational lifecycle. It is distinct from the repository-only Ava Internal Maintainer and from Upgrade Role, which is activated only for project-owned semantic reconciliation.

## Tasks

1. [x] [Finalize and rename the Role Generator as the Role Manager](01-finalize-role-manager.md)
2. [x] [Create the Project Steward role](02-create-project-steward.md)
3. [x] [Create the Inbox Ingester role and inbox convention](03-create-inbox-ingester.md)
4. [x] [Create the Change Reviewer role](04-create-change-reviewer.md)
5. [x] [Create the Ava Maintenance role](05-create-ava-maintenance-role.md)

The core-role catalog is complete. Deterministic installation administration routes to Ava Maintenance, project-owned semantic reconciliation routes to Upgrade Role, and ordinary project roles retain their focused authority.

## Previous phase

[Format contract and base structure](../01-format-contract/) is complete.

## Next active task

Return to [Implement validation, conformance, and upgrade fixtures](../04-distribution-and-upgrades/10-implement-validation-and-upgrade-fixtures.md).
