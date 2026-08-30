---
id: ava-5621
title: "Record semantic inspection paths before completion"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5621
---

## Description

Require Upgrade Role to record every guidance-driven project-owned inspection as durable journal evidence before semantic compatibility can become complete.

## Migrated task record

Historical metadata: phase 5 finding 21, `required-v1`, blocking release candidate, affected version `1.0.0-alpha.14`, completed after implementation and later partially superseded by AVA-5626.

### Observed behavior and root cause

Full alpha.13-to-alpha.14 qualification reached runner all-pass, but independent audit found `interrupted-finalize` had inspected four project-owned paths and completed semantics with `upgrade.json.project_changes: []`, recorded as major `QUA-SEMANTIC-PATHS-003`. A companion scenario did record the four paths. Upgrade Role had representation only for mutated paths (`created`, `modified`, `deleted`, `moved`), so unchanged semantic inspections could be omitted or falsely classified.

### Approved scope

Add inspection-only project change representation; record every guidance-driven inspected project-owned path before completion; keep one record per path and replace `inspected` with actual mutation type if later changed; block completion on missing/unresolved accounting; exclude inspection-only evidence from rollback edit work; declare scenario expectations and deterministic postconditions; keep independent audit as semantic authority.

### Resolution evidence

`distribution/schemas/upgrade.schema.json` added `change_type: inspected`. Upgrade Role defines `inspected/retained`, exact-once inspected-or-changed accounting, replacement on later mutation, and rollback exclusion. The synthetic matrix originally required `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md` for both semantic scenarios. `qualification_postconditions.py` and `qualify-synthetic.sh` originally converted successful runs to failure on missing/duplicate/unresolved expected accounting, with `test_qualification_postconditions.py` coverage.

Release follow-up required corrective-release semantic reconciliation/finalization with complete path accounting and no major audit finding.

### Supersession

AVA-5626 later removed the fixed four-path deterministic qualification gate because it did not generalize across release edges and produced false failures. The `inspected`/`retained` journal representation and Upgrade Role requirement to record actual guidance-driven inspections introduced by this task remain authoritative.