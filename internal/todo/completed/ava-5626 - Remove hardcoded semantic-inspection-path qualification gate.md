---
id: ava-5626
title: "Remove hardcoded semantic-inspection-path qualification gate"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5626
---

## Description

Remove the deterministic qualification postcondition that required a fixed project-owned inspection-path set because it did not generalize across release edges.

## Migrated task record

Historical metadata: phase 5 finding 26, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.15`, exposed by run `20260821T100350003229Z-alpha14-to-alpha15-corrective-local`.

### Observed behavior and root cause

`interrupted-finalize` and `pending-semantic-reconciliation` failed on one missing path each relative to a fixed four-path list copied from an earlier alpha.13-to-alpha.14 session, even though the agents had inspected all paths actually relevant to the current edge, including inbox and knowledge indexes. The generic missing files were content-free scaffold paths unrelated to current guidance.

AVA-5621's deterministic `qualification_postconditions.py` compared semantic scenarios to a fixed matrix list that was never derived per edge. This contradicted Upgrade Role's bounded guidance-driven discovery and could cause both false failures and false passes. Adequacy of the actual inspected set is semantic judgment owned by independent audit, which already evaluates guidance and transcript evidence.

### Resolution evidence

`qualification_postconditions.py` and its test module were removed. `qualify-synthetic.sh` now executes the scenario runner directly, `test.sh` no longer compiles/runs the removed gate, and `qualification-matrix.json` no longer stores hardcoded expected inspected/reported path lists. The useful schema and Upgrade Role contracts from AVA-5621/AVA-5623 remain protected by `InspectionOnlyProjectChangeContractTests` in `test_semantic_upgrade.py`. `internal/release/log.md` records the reversal and rationale.

Completion established no remaining fixed expected-inspection-path references, direct runner exit semantics, preserved `inspected/retained` and reporting invariants, logged reversal, and passing repository tests.

A fresh full corrective qualification was still required after outstanding findings were resolved; semantic inspection adequacy remains an independent-audit responsibility.