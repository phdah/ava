---
id: ava-5622
title: "Report inspected project-owned paths during interrupted-finalize"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5622
---

## Description

Make Ava Maintenance's interrupted-terminal-cleanup replay report confirm inspection of every project-owned path recorded by semantic reconciliation.

## Migrated task record

Historical metadata: phase 5 finding 22, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.15`, completed after qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local` exposed it.

### Observed behavior and root cause

Candidate `8927a3c` passed 15 of 17 scenarios, but `interrupted-finalize` did not report `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md`. Terminal cleanup authority was correctly bounded, but its reporting contract only required generic removed/preserved/conflicted paths and did not carry durable semantic inspection evidence from terminal `upgrade.json.project_changes` into the completion report.

The fix was reporting-only: Ava Maintenance must not reread project-owned semantic inputs during terminal cleanup because that inspection authority belongs to Upgrade Role. It reports the exact validated paths/outcomes already recorded in the terminal journal.

### Resolution evidence

`templates/base/roles/ava-maintenance/instructions.md` now requires interrupted terminal cleanup to include every project-owned path from validated terminal `project_changes`, including inspection-only retained records, while explicitly prohibiting rereading those semantic inputs. `internal/release/fixtures/ava-maintenance.json` models the four retained records, required report paths, journal evidence source and no-reread boundary. `test_ava_maintenance.py` verifies path set, classification, durable source, no-reread behavior and instruction contract.

A complete fresh 17-scenario corrective qualification was still required to prove the scenario report. AVA-5626 later removed the deterministic fixed-list gate because it did not generalize across edges, but this task's durable-journal-to-report behavior remains in place.