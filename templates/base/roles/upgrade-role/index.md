# Upgrade Role

The Upgrade Role performs one bounded semantic reconciliation of project-owned Ava context for an active installed-version upgrade.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation, authority, responsibilities, and scope.
2. [Instructions](instructions.md) - Canonical semantic migration procedure and state transitions.
3. [Capabilities](capabilities.md) - Permitted project-owned changes and managed state updates.
4. [Constraints](constraints.md) - Upgrade boundaries, prohibited work, and blocking conditions.
5. [Maintenance and upgrade state routing](../../shared/instructions/upgrade-state-and-routing.md) - Managed activation, maintenance separation, operation ownership, guidance discovery, and normal-routing return.
6. [Ownership and mutation authority](../../shared/instructions/ownership-and-mutation.md) - Managed versus project-owned paths and mutation boundaries.
7. [Scoped history](../../shared/instructions/scoped-history.md) - Required history maintenance for conceptual project changes.
8. [Document metadata](../../shared/instructions/document-metadata.md) - Metadata, lifecycle, ownership, and compatibility rules.

## Additional context

Read [Calendar verification](../../shared/instructions/calendar-verification.md) only when semantic reconciliation would convert relative calendar language into a durable absolute project fact. Do not load it for unrelated upgrade reconciliation.

## Transaction guidance

After the complete required reading is active, resolve the relative guidance paths recorded in `./.ava/state/upgrade.json` beneath `./.ava/guidance/` and load only those documents, in transaction order.

Do not discover guidance from project-owned registries, arbitrary logs, release-note prose, or filesystem scanning.

## History

Read the [Upgrade Role log](log.md) when a change depends on its semantic authority or managed activation boundary.
