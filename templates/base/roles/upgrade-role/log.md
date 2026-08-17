# Upgrade Role Update Log

This log records major conceptual and structural changes to the managed Upgrade Role. It does not replace Git history.

## 2026-08-15

- **Inspection accounting**: Required every guidance-driven project-owned path inspected during semantic reconciliation to have one durable `project_changes` record before semantic completion, including `inspected/retained` for paths that require no content mutation.
- **Mutation replacement**: Required an inspection-only record to become the actual change classification when the same path is later changed, avoiding duplicate path records and preserving rollback scope only for real edits.

## 2026-08-03

- **Semantic-only activation**: Narrowed managed activation to project-owned semantic reconciliation and removed deterministic installation administration from Upgrade Role routing.
- **Maintenance handoff**: Assigned installation status, managed integrity, deterministic recovery invocation, finalization, host accessibility, and removal to Ava Maintenance.
- **Rollback separation**: Kept project-owned rollback preparation within Upgrade Role while assigning deterministic rollback invocation to Ava Maintenance and the updater.
