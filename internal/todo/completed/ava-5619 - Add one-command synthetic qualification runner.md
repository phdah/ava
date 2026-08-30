---
id: ava-5619
title: "Add one-command synthetic qualification runner"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5619
---

## Description

Provide one manual maintainer shell entry point that prepares and executes the synthetic installation, routing, integrity, recovery, upgrade, removal, and reinstallation qualification matrix from a local terminal.

## Migrated task record

Historical metadata: phase 5 finding 19, `required-v1`, blocking release candidate, affected version `1.0.0-alpha.14`, completed after AVA-5617 and AVA-5618.

### Observed behavior and boundary

Synthetic qualification previously required many separate commands for corpus/variants/assets, installation, OpenCode prompts, damage/conformance, semantic lifecycle, recovery, removal, hashing and terminal verification. Manual repetition caused setup/order mistakes, including duplicate rollback invocation and a conformance run without repository `PYTHONPATH`. The complete runner is intentionally a manual local maintainer operation, not GitHub Actions, release-please, PR checks, `internal/release/test.sh`, a distributed CLI, or persistent runtime.

### Implementation

`internal/release/qualify-synthetic.sh` is the single POSIX entry point. `qualification_runner.py` owns preflight, safe isolated workspaces, pinned asset verification, deterministic orchestration, bounded OpenCode execution, assertions, interrupted reruns and terminal summary. `qualification-matrix.json` freezes eight variant families, 17 scenarios, prompts, calendar regression and stable managed-damage rule IDs. `qualification-runner.md` documents full command, preflight-only mode, input boundaries, reruns and interpretation.

The runner reads but does not mutate the finalized qualification root/supplied test project; every scenario uses a runner-owned copy under an explicit external execution root whose sentinel is bound to the finalized corpus digest. It rejects mutable latest selection, ambiguous assets, repository-local generated output and unsafe pre-existing roots. Conformance runs with repository `PYTHONPATH`; expected damage passes only for exact expected rule IDs with evidence preserved; resume/abort reuse AVA-5617 authentic checkpoints; calendar regression requires Friday `2026-08-14` and rejects `2026-08-15`; rollback is exactly once; uninstall/reinstall prove project-owned byte preservation and healthy final state.

Tests cover argument/pinned checks, latest refusal, root safety, corpus ownership, interrupted reruns, matrix coverage, rollback planning, CI separation, internal-only placement and nonzero summary behavior without needing external model-backed execution. Release assembly excludes runner/artifacts, while ordinary repository tests and boundary validation remain in the PR gate.

### Completion and release follow-up

Completion established one documented command, preflight-only planning, deterministic all-family execution, exact OpenCode prompts, expected-failure handling, explicit unresolved-decision reporting, nonzero terminal failures/skips/mismatches, and release exclusion. Published qualification still had to run the completed entry point against selected corrective-alpha assets and use explicit user signoff as final semantic acceptance. That is release evidence, not pending implementation.