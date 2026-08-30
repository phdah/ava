---
id: ava-5628
title: "Require reconciled per-passage disposition evidence before inbox completion"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5628
---

## Description

Stop Inbox Ingester from promoting non-durable source passages into trusted knowledge and from claiming disposition totals that were never reconciled against rendered destination content.

## Migrated task record

Historical metadata: phase 5 finding 28, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.15`, exposed by candidate `77977f8` after a similar prior audit failure.

### Observed behavior and root cause

Independent audit reported major `AUD-INBOX-001`: final trusted knowledge contained passages the evaluator oracle marked `non-durable`, including recurring cooking “Next time” and dog-care “window spot” material, while the session claimed `1,895 mapped`, `349 non-durable`, `0 pending` without an executed reconciliation supporting the 349. The same defect class had appeared in the previous qualification attempt.

The fidelity contract already required every substantive section to become exactly one of `mapped`, `non-durable`, or `pending` and said non-durable sections are intentionally not promoted. It did not require the completion claim to reconcile those dispositions against actual rendered destination content, so a session could assert totals while whole-source promotion contradicted them.

### Approved scope and completion criteria

Completion had to derive disposition totals only after read-only reconciliation against rendered destinations; verify every mapped section in its named destination; verify each non-durable section absent from trusted destinations created/updated for that source; keep ambiguity pending rather than promote it for completion; prohibit non-durable promotion regardless of mechanism; add regression for whole-source promotion/unreconciled claims; and keep this semantic safeguard independent of AVA-5627's later-superseded execution-mechanism rule.

### Resolution evidence

The shared Inbox Ingestion Fidelity contract now requires rendered disposition reconciliation before source/batch completion. `complete-pending-inbox` prompts require positive mapped verification, negative non-durable verification, and pending ambiguity. Independent qualification audit compares evaluator-only oracle dispositions to final rendered destinations and treats whole-source promotion or unsupported totals as findings. `test_inbox_disposition_evidence.py` pins these requirements and proves the synthetic fixture contains mixed mapped/non-durable cases where whole-source promotion is observably wrong. Repository validation passed on the resolving PR head.

Because distributed instruction content changed, a brand-new full 17-scenario qualification plus independent audit remained required, with both complete-inbox execution and semantic review clean.