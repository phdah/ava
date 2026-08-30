---
id: ava-5629
title: "Decide how qualification should detect inbox semantic-disposition failures"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5629
---

## Description

Separate deterministic structural qualification from evaluator-only semantic judgment and add bounded non-oracle inbox fidelity checks.

## Migrated task record

Historical metadata: phase 5 finding 29, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.15`, completed after user approval of combined approaches 2 and 3 on 2026-08-24.

### Observed behavior and root cause

Candidate `77977f8` recorded `complete-pending-inbox: pass` after process success, empty direct pending inbox and installed conformance, while independent audit found non-durable promotion and unreconciled dispositions. The same runner gap had appeared in the previous attempt. The runner intentionally has no evaluator oracle, so it cannot judge semantic fidelity without leaking the answer key. The defect was using one `pass` label for both structural/mechanical evidence and semantic acceptance.

### Approved decision

Audit-gated scenarios may end `structural-pass` with `semantic_status: pending-audit`. This allows the mechanically successful matrix to continue to independent audit but does not claim semantic pass. The runner summary remains evidence of what the runner observed and is not rewritten after audit; hands-off automation combines runner and independent audit evidence to choose `needs-review` versus `awaiting-user-signoff`.

Complete-inbox also receives bounded oracle-free structural checks: exact selected-source preservation in `inbox/processed/`, trusted source traceability, locally resolvable metadata resource paths, and claim-footnote consistency including matching source IDs, one renderable definition and links to the same preserved source. It does not attempt to prove mapped/non-durable/pending semantic correctness.

### Resolution evidence

Implementation spans `qualification_inbox.py`, `qualification_runner.py`, `qualification_automation.py`, the maintained qualification matrix, `test_qualification_inbox.py`, `test_qualification_semantic_status.py`, `qualification-runner.md` and `qualification-automation.md`. Interrupted reruns retain structurally passing scenarios, automation treats structural-pass as runner success but not semantic acceptance, and focused tests protect the status/evidence boundary.

This is repository-only qualification tooling. A new exact corrective-alpha candidate still had to run the complete flow to a mechanically clean runner, clean independent audit and explicit user signoff.