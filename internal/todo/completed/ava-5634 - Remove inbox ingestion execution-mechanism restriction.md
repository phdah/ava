---
id: ava-5634
title: "Remove inbox ingestion execution-mechanism restriction"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5634
---

## Description

Revert AVA-5627's mechanism-level restriction while preserving Inbox Ingester authority, trust boundaries, semantic fidelity, provenance, source handling, and qualification safeguards.

## Migrated task record

Historical metadata: phase 5 finding 34, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.15`, completed after explicit user decision.

### Decision and motivation

AVA-5627 addressed a real semantic-fidelity failure by prescribing how ingestion could be performed. The user determined that this mechanism-level restriction was inconsistent with Ava's intended responsibility: Ava should define authority, trust boundaries, required outcomes and semantic correctness rather than execution strategy. AVA-5628 and AVA-5629 established the appropriate result-based safeguards through per-passage dispositions, rendered reconciliation, bounded structural evidence and independent semantic audit.

### Scope and completion criteria

Remove only AVA-5627's execution-strategy language from Inbox Ingester instructions/constraints, add no replacement mechanism guidance, remove qualification checks/regression whose sole purpose was enforcing that mechanism, and preserve all independent authority/trust/fidelity/provenance/source-preservation/validation/final-state requirements. Permanent project mutation remains bounded by declared role authority. The finding supersedes only AVA-5627's execution restriction, not the semantic defects and safeguards in AVA-5628/AVA-5629.

### Resolution evidence

Inbox Ingester `instructions.md` and `constraints.md` removed the AVA-5627 boundary without replacement policy; `capabilities.md` was unchanged. The role log records the narrow reversal, while rendered disposition reconciliation remains. `qualification_runner.py` removed the transient direct-project-root watcher/inbox mechanism guard; complete inbox qualification still requires processed-source preservation, provenance, structural fidelity, installed conformance and audit-gated `structural-pass`. `test_qualification_runner.py` removed the execution-restriction test and pins independent semantic-audit requirements. Runner docs/release log now describe only outcome-based requirements. Repository tests passed and the release roadmap returned to assembling a fresh exact candidate; AVA-5625 remained post-v1/non-blocking.