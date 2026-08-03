# Ava Maintenance Update Log

This log records major conceptual and structural changes to the managed Ava Maintenance role. It does not replace Git history.

## 2026-08-03

- **Managed maintenance authority**: Added Ava Maintenance as the agent-facing role for installed identity, managed integrity, deterministic recovery coordination, host accessibility, explicit upgrades, finalization, and safe removal.
- **Pre-routing separation**: Routed deterministic and malformed managed state to Ava Maintenance while reserving project-owned semantic reconciliation for Upgrade Role.
- **Deterministic mutation boundary**: Kept manifest, journal, managed payload, resume, abort, rollback, and finalization mutations inside existing installer or updater mechanisms.
- **Role-led removal**: Defined bounded removal of `./.ava/` and an unchanged managed `./AGENTS.md` while preserving every project-owned path and reporting stale host references.
- **Agent-first interface**: Kept status, version, repair, and uninstall as user requests interpreted by the role rather than new standalone command modes.
