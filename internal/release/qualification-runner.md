---
type: Internal Release Qualification Procedure
title: One-Command Synthetic Qualification Runner
description: Manual maintainer procedure for running the complete repository-external synthetic Ava qualification matrix from one pinned local command.
tags: [internal, release, qualification, runner, opencode]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T12:48:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-29T13:20:00+02:00
---

# Purpose

`qualify-synthetic.sh` is the manual maintainer entry point for the complete synthetic qualification matrix. It composes the maintained fixture, pinned release assets, deterministic installer operations, authentic resume and abort checkpoints, installed conformance, bounded OpenCode prompts, calendar regression, semantic reconciliation, finalization, removal, and reinstallation.

This command is repository-only release qualification tooling. It is not an Ava user command and is never assembled into release assets.

Run it from a local maintainer checkout. Do not invoke the complete runner from GitHub Actions, release-please, pull-request checks, or `internal/release/test.sh`.

# Required inputs

Use exact local paths, not release URLs or `latest` aliases:

- finalized qualification root with `oracle/finalized-inventory.json` and materialized `variants/index.json`
- empty or runner-owned execution root outside the repository and outside every input root
- pinned source release asset directory
- pinned target release asset directory
- repository-external test project, used only as a byte-integrity boundary
- OpenCode executable
- explicit OpenCode `provider/model`

The target must declare exactly one supported source-to-target upgrade edge and must require semantic review. The latter is required because the maintained matrix must exercise authentic rollback, semantic reconciliation, and finalization states rather than fabricating them.

# Preflight

Before any mutation, the runner:

1. requires Python 3.11 or newer and a clean Ava checkout
2. rejects qualification data, asset directories, the test project, execution output, or transcripts inside the Ava repository
3. rejects any asset path containing a `latest` path component
4. verifies the exact seven release assets and every `SHA256SUMS` digest
5. verifies source and target release identity and the declared upgrade edge
6. verifies the finalized qualification vault and all eight materialized variant families
7. checks OpenCode availability and the explicit model identifier
8. refuses a non-empty execution root unless its ownership sentinel matches the selected qualification root

`--preflight-only` prints the resolved inputs and deterministic scenario plan, then exits without creating or changing the execution root or any project.

# Complete command

For the current qualification locations, use:

```sh
internal/release/qualify-synthetic.sh \
  --qualification-root ~/stuff/ava-qualification-vault \
  --execution-root ~/stuff/ava-qualification-run \
  --source-assets /absolute/path/to/pinned/source-assets \
  --target-assets /absolute/path/to/pinned/target-assets \
  --test-project ~/stuff/project-vault \
  --opencode opencode \
  --model <provider/model>
```

Inspect the exact plan without mutation first:

```sh
internal/release/qualify-synthetic.sh \
  --qualification-root ~/stuff/ava-qualification-vault \
  --execution-root ~/stuff/ava-qualification-run \
  --source-assets /absolute/path/to/pinned/source-assets \
  --target-assets /absolute/path/to/pinned/target-assets \
  --test-project ~/stuff/project-vault \
  --opencode opencode \
  --model <provider/model> \
  --preflight-only
```

Use `--transcript-dir /absolute/repository-external/path` when a separate copy of OpenCode JSONL output is wanted. Command results and scenario state are always retained inside the owned execution root for diagnosis.

# Isolation and reruns

The finalized qualification root and supplied test project are read-only inputs. Every scenario runs against a runner-owned copy of its materialized variant under `<execution-root>/scenarios/`.

A new execution root may be absent or empty. Once initialized it contains `.ava-qualification-runner.json`, which binds that directory to the selected qualification root and finalized corpus digest. The runner refuses any other non-empty directory and refuses reuse if the finalized corpus no longer matches the recorded digest.

Mechanically passing scenarios are retained and reused on an interrupted rerun without reporting them as skipped qualification outcomes. This includes both ordinary `pass` outcomes and audit-gated `structural-pass` outcomes. A non-passing or interrupted scenario is recreated only from its corresponding materialized variant before another attempt. The runner never resets the finalized corpus, the original variants, the source or target assets, or the supplied test project.

# Maintained scenario order

The machine-readable order and exact OpenCode prompts live in `fixtures/synthetic-qualification-vault/qualification-matrix.json`. It covers:

1. empty fresh installation
2. mature mixed-project preservation
3. private, work, calendar, and ambiguous registered-role routing
4. complete pending-inbox ingestion
5. modified, missing, corrupt, and unexpected managed-content failures
6. authentic resume, abort, rollback, and finalization
7. pending semantic reconciliation
8. role-led uninstall followed by pinned reinstall

The calendar regression fixes the reference context as Thursday, 2026-08-13 and requires persisted `Friday` plus `2026-08-14`; `2026-08-15` is an explicit failure.

Managed-damage conformance is accepted only when the exact maintained stable rule is observed:

- modified: `AVA-MANAGED-CHECKSUM`
- missing: `AVA-MANAGED-MISSING`
- corrupt journal: `AVA-UPGRADE-READ`
- unexpected managed payload: `AVA-MANAGED-UNEXPECTED`

Conformance runs through `python3 -m internal.release.conformance` with the repository root on `PYTHONPATH`. A blocking conformance exit counts as a pass only for those deliberately damaged scenarios and only when the injected evidence remains unchanged.

Resume and abort use `checkpoint.py` to create authentic transaction states and then invoke the real selected target `ava-install.sh --resume` or `--abort`. Rollback is invoked exactly once through the real target installer. Finalization is exercised through Ava Maintenance after Upgrade Role has completed semantic reconciliation.

OpenCode is invoked only for the exact scenario prompt in its isolated copied project. The runner never passes a global auto-approval flag. If required semantic work remains partial or blocked, the outcome is `user-decision-required` and the complete run exits nonzero.

For complete pending-inbox ingestion, the runner snapshots every selected direct inbox source before ingestion and then checks deterministic fidelity after the session: every selected source must be preserved exactly once under `inbox/processed/`, preserved sources must remain traceable from trusted `sources:` metadata, metadata resources must resolve to the preserved source, and every used claim footnote must have a matching source id, one renderable definition, and a link resolving to the same preserved source.

These deterministic checks do not judge whether mapped meaning was preserved or whether `non-durable` or `pending` material was handled semantically correctly. The runner has no access to the evaluator-only oracle. The complete pending-inbox scenario therefore ends as `structural-pass` with `semantic_status: pending-audit` when its deterministic checks succeed. Its semantic result remains owned by the independent audit.

# Result

`summary.json` records the pinned source and target identities plus every scenario outcome. The terminal prints the same concise scenario summary. Scenarios not run after an earlier non-passing result are explicitly reported as `skipped`.

The runner command succeeds when every scenario reaches a mechanically passing outcome, meaning `pass` or `structural-pass`, the finalized corpus inventory is byte-identical, and the supplied test project remains byte-identical. A failed command, mismatched rule, unsafe mutation, unexpected skip, or unresolved required user decision returns nonzero.

A `structural-pass` is deliberately not a semantic pass. The hands-off qualification automation must still run the independent audit before the release can reach `awaiting-user-signoff`; blocker or major audit findings produce `needs-review`.

The runner intentionally does not turn its local evidence into publication authority. Validate the resulting qualification evidence and obtain the required user semantic signoff before advancing the release path.
