# Ava Maintenance Update Log

This log records major conceptual and structural changes to the managed Ava Maintenance role. It does not replace Git history.

## 2026-08-20

- **Recoverable terminal cleanup**: Required managed pre-routing to block normal work when a safe terminal operation leaves transaction storage, and authorized Ava Maintenance to replay only cleanup proven by a terminal transaction ID or exact restored-safe-terminal source evidence, followed by guarded non-recursive empty-container removal.

## 2026-08-10

- **Agent-driven upgrade finalization**: Made Ava Maintenance the finalization mechanism after semantic compatibility is complete. The role validates the protocol preconditions, atomically writes only the terminal journal state, removes only the exact transaction directory derived from the journal's `transaction_id`, and verifies normal routing is enabled without searching for an installer binary.
- **Bounded mutation exception**: Kept explicit upgrade, resume, abort, rollback, repair, and all non-terminal journal transitions inside existing deterministic installer or updater mechanisms. Direct state mutation remains forbidden outside successful terminal finalization.

## 2026-08-03

- **Managed maintenance authority**: Added Ava Maintenance as the agent-facing role for installed identity, managed integrity, deterministic recovery coordination, host accessibility, explicit upgrades, finalization, and safe removal.
- **Pre-routing separation**: Routed deterministic and malformed managed state to Ava Maintenance while reserving project-owned semantic reconciliation for Upgrade Role.
- **Deterministic mutation boundary**: Kept manifest, journal, managed payload, resume, abort, rollback, and finalization mutations inside existing installer or updater mechanisms.
- **Role-led removal**: Defined bounded removal of `./.ava/` and an unchanged managed `./AGENTS.md` while preserving every project-owned path and reporting stale host references.
- **Agent-first interface**: Kept status, version, repair, and uninstall as user requests interpreted by the role rather than new standalone command modes.
