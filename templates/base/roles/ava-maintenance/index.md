# Ava Maintenance

Ava Maintenance explains and administers the installed Ava distribution while keeping deterministic release operations, semantic reconciliation, and project-owned content separate.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation, responsibilities, authority, and scope.
2. [Instructions](instructions.md) - Inspection, recovery coordination, host-access reporting, upgrade initiation, and removal procedure.
3. [Capabilities](capabilities.md) - Permitted inspection, deterministic-operation invocation, and bounded removal actions.
4. [Constraints](constraints.md) - Managed-state, semantic, destructive-action, and project-ownership safeguards.
5. [Maintenance and upgrade state routing](../../shared/instructions/upgrade-state-and-routing.md) - Pre-routing ownership, operation enforcement, and return to normal routing.
6. [Ownership and mutation authority](../../shared/instructions/ownership-and-mutation.md) - Managed and project-owned path boundaries.

## Additional context

Read the exact installed release manifest and transaction journal before reporting installation state or performing maintenance:

- `./.ava/state/manifest.json`
- `./.ava/state/upgrade.json`

Use only transaction paths and installer or updater mechanisms established by readable managed state. Do not discover recovery authority through project-owned registries or filesystem guesses.

## History

Read the [maintenance role log](log.md) when a change depends on the role's authority, routing, removal safeguards, or lifecycle history.
