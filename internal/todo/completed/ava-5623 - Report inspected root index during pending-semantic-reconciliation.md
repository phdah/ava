---
id: ava-5623
title: "Report inspected root index during pending-semantic-reconciliation"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5623
---

## Description

Make Upgrade Role's pending-semantic-reconciliation completion report explicitly confirm inspection of project-owned paths recorded as inspection-only.

## Migrated task record

Historical metadata: phase 5 finding 23, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.15`, exposed by qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local`.

### Observed behavior and root cause

Candidate `8927a3c` passed 15 of 17 scenarios, but `pending-semantic-reconciliation` failed because the report did not confirm inspection of `/index.md`. Durable accounting from AVA-5621 was already correct: Upgrade Role recorded guidance-driven inspected paths in `upgrade.json.project_changes`. The gap was human-readable reporting: listing a path or `change_type: inspected` did not explicitly state that the path was actually inspected and retained unchanged.

This differs from AVA-5622, which repaired Ava Maintenance terminal-cleanup reporting from journal evidence. This task repairs Upgrade Role's own semantic-reconciliation report.

### Resolution evidence

`templates/base/roles/upgrade-role/instructions.md` now requires every inspection-only journal record to be reported explicitly as an exact path inspected during semantic reconciliation and retained without mutation; merely listing the path/classification is insufficient. The qualification matrix originally pinned `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md` as expected reported project-owned paths, and `test_qualification_postconditions.py` verified both reporting wording and path set.

Fresh complete qualification was still required to prove the scenario. AVA-5626 later removed the hardcoded matrix path declarations and deterministic fixed-list comparison because they did not generalize across release edges. The Upgrade Role completion-report wording introduced here remains authoritative.