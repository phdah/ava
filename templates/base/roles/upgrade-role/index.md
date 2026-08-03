# Upgrade Role

The Upgrade Role performs one bounded semantic reconciliation of project-owned Ava context for an active installed-version upgrade.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation, authority, responsibilities, and scope.
2. [Instructions](instructions.md) - Canonical semantic migration procedure and state transitions.
3. [Capabilities](capabilities.md) - Permitted project-owned changes and managed state updates.
4. [Constraints](constraints.md) - Upgrade boundaries, prohibited work, and blocking conditions.
5. [Upgrade state and routing](../../shared/instructions/upgrade-state-and-routing.md) - Managed activation, operation allowlist, guidance discovery, and normal-routing return.
6. [Ownership and mutation authority](../../shared/instructions/ownership-and-mutation.md) - Managed versus project-owned paths and mutation boundaries.
7. [Scoped history](../../shared/instructions/scoped-history.md) - Required history maintenance for conceptual project changes.
8. [Document metadata](../../shared/instructions/document-metadata.md) - Metadata, lifecycle, ownership, and compatibility rules.

## Transaction guidance

After the complete required reading is active, resolve the relative guidance paths recorded in `./.ava/state/upgrade.json` beneath `./.ava/guidance/` and load only those documents, in transaction order.

Do not discover guidance from project-owned registries, arbitrary logs, release-note prose, or filesystem scanning.
