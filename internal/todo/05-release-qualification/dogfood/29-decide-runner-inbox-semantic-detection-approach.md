---
type: Internal Development Task
title: Decide How Qualification Should Detect Inbox Semantic-Disposition Failures
description: Separate deterministic structural qualification from evaluator-only semantic judgment and add bounded non-oracle inbox fidelity checks.
tags: [internal, roadmap, dogfood, inbox, qualification, runner]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 29
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-24T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-24T17:23:00+02:00
---

# Decide How Qualification Should Detect Inbox Semantic-Disposition Failures

## Observed behavior

Mandatory release qualification for candidate `77977f8` found (`AUD-RUNNER-001`, major, independent audit) that `internal/release/qualification_runner.py` marked the `complete-pending-inbox` scenario as `pass` after only checking that the OpenCode process exited successfully, no direct pending files remained, and installed conformance passed. None of those checks compared destination meaning or section dispositions against the selected sources or the evaluator-only oracle.

That run recorded `complete-pending-inbox` as `pass` even though finding 28 (`AUD-INBOX-001`) demonstrated that the session promoted `non-durable` passages and reported unreconciled disposition totals. The equivalent gap was previously observed as `AVA-AUD-RUNNER-INBOX-006` in the prior qualification attempt and had been deferred as situational. Its recurrence showed that the runner's terminal label overstated what deterministic evidence could prove.

## Reproduction and evidence

Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local`, candidate revision `77977f8`. Runner summary recorded `complete-pending-inbox: pass`; independent audit finding `AUD-RUNNER-001` and companion finding `AUD-INBOX-001` contradicted that semantic implication.

## Classification

`blocker` for the next prerelease. The implementation is complete; a new exact candidate and fresh full qualification remain required before release progression.

## Root cause

The deterministic runner intentionally does not have access to the evaluator-only oracle (`internal/release/fixtures/synthetic-qualification-vault/oracle/baseline.json`) during a scenario. It therefore cannot itself judge semantic fidelity without leaking the answer key into the environment under qualification. Semantic fidelity belongs to the independent audit, while the runner owns deterministic and structural evidence.

The defect was that both kinds of evidence were represented by the same runner `pass` label. A structurally clean run could therefore claim `pass` before evaluator-only semantic evidence existed.

## Decision

On 2026-08-24 the user approved the combination of approaches 2 and 3:

1. **Separate structural and semantic status.** A scenario that requires evaluator-only semantic judgment may finish as `structural-pass` with `semantic_status: pending-audit`. This is mechanically successful and allows the matrix and independent audit to continue, but it is not a semantic pass.
2. **Add bounded non-oracle deterministic checks.** Complete pending-inbox qualification now checks structural fidelity that can be proven without the oracle while leaving source meaning and section-disposition correctness to the independent audit.

The runner summary is not retroactively rewritten after audit. It remains evidence of what the runner itself observed. The hands-off qualification automation combines that evidence with the independent audit to determine `needs-review` versus `awaiting-user-signoff`.

## Scope

The resolving implementation:

- marks `complete-pending-inbox` as requiring semantic audit in the maintained qualification matrix
- adds `structural-pass` as a mechanically passing runner outcome with `semantic_status: pending-audit`
- lets interrupted reruns retain structurally passing scenarios and lets the complete matrix reach the independent audit
- updates hands-off qualification to treat `structural-pass` as runner success without treating it as semantic acceptance
- adds repository-only deterministic inbox checks for processed-source preservation, trusted source traceability, metadata path resolution, and claim-footnote consistency
- documents the runner/audit evidence boundary and adds focused regression coverage

## Completion criteria

- [x] The runner distinguishes structural success from evaluator-only semantic success.
- [x] `complete-pending-inbox` cannot claim semantic `pass` before the independent audit.
- [x] A structurally successful audit-gated scenario does not stop the remaining matrix or prevent the audit from running.
- [x] Every selected direct inbox source is checked for exact preservation under `inbox/processed/`.
- [x] Preserved selected sources are checked for trusted `sources:` traceability and locally resolvable metadata resources.
- [x] Used claim footnotes are checked for matching source ids, exactly one renderable definition, and a link resolving to the same preserved source as metadata.
- [x] The deterministic runner remains oracle-free and does not claim to prove mapped, non-durable, or pending semantic correctness.
- [x] The independent audit remains the semantic gate for `needs-review` versus `awaiting-user-signoff`.
- [x] Focused tests cover the structural checks and runner/automation status boundary.

## Resolution evidence

Implemented on `fix/finding-29-qualification-semantic-status` in:

- `internal/release/qualification_inbox.py`
- `internal/release/qualification_runner.py`
- `internal/release/qualification_automation.py`
- `internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json`
- `internal/release/tests/test_qualification_inbox.py`
- `internal/release/tests/test_qualification_semantic_status.py`
- `internal/release/qualification-runner.md`
- `internal/release/qualification-automation.md`

The implementation PR is the resolution artifact. Fresh candidate qualification is intentionally a subsequent release gate, not part of implementation completion.

## Release qualification follow-up

This is repository-only qualification tooling and does not change distributed Ava behavior. Assemble a brand-new exact corrective-alpha candidate from the updated release PR revision and rerun the complete qualification flow. The run must reach a mechanically clean runner result, a clean independent audit, and explicit user signoff before the corrective alpha can advance.
