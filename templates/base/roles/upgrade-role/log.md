# Upgrade Role Update Log

This log records major conceptual and structural changes to the managed Upgrade Role. It does not replace Git history.

## 2026-08-03

- **Semantic-only activation**: Narrowed managed activation to project-owned semantic reconciliation and removed deterministic installation administration from Upgrade Role routing.
- **Maintenance handoff**: Assigned installation status, managed integrity, deterministic recovery invocation, finalization, host accessibility, and removal to Ava Maintenance.
- **Rollback separation**: Kept project-owned rollback preparation within Upgrade Role while assigning deterministic rollback invocation to Ava Maintenance and the updater.
