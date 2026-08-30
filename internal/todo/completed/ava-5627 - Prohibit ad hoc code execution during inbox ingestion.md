---
id: ava-5627
title: "Prohibit ad hoc code execution during inbox ingestion"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker", "superseded"]
ordinal: 5627
---

## Description

Historical implementation finding that prohibited ad hoc code during inbox ingestion after a qualification session used `.tmp_ingest.py`. Its mechanism-level restriction was later explicitly rejected by the user and removed by AVA-5634; its original fidelity concerns remain covered by AVA-5628 and AVA-5629.

## Migrated task record

Historical metadata: phase 5 finding 27, `blocker`, affected version `1.0.0-alpha.15`, candidate `77977f8`, implementation-complete before later supersession.

### Observed behavior and original diagnosis

Independent audit of `complete-pending-inbox` found minor `AUD-SCOPE-001`: the Inbox Ingester created, executed and deleted project-root `.tmp_ingest.py` to bulk-process the 305-file inbox. The same mechanism contributed to major fidelity finding `AUD-INBOX-001` because it used whole-source/filename-keyword routing instead of required per-section dispositions. Existing role scope did not explicitly discuss code/script creation as an ingestion mechanism.

### Original implementation

The resolving change added role instructions/constraints requiring direct source/section reasoning and explicitly prohibiting ad hoc scripts, generated code, temporary implementation files and programmatic bulk transformation. Qualification observed project-root entries during the full prompt and failed on newly created helpers even if deleted before final conformance. `test_qualification_runner.py` reproduced the `.tmp_ingest.py` create/delete pattern; role log and qualification docs recorded the boundary. A fresh full release qualification was required because distributed role content changed.

### Supersession

The user later rejected this mechanism-level restriction as inconsistent with Ava's purpose. AVA-5634 removes the prohibition and the runner guard without adding replacement execution-mechanism guidance. This finding remains completed historical evidence of the original implementation and audit event, but its rule is no longer authoritative. Source preservation, provenance, semantic fidelity, final state, reconciled dispositions and independent semantic audit remain governed by AVA-5628, AVA-5629 and the existing Inbox Ingester contracts.