---
type: Internal Development Task
title: Add One-Command Synthetic Qualification Runner
description: Provide one manual maintainer shell entry point that prepares and executes the synthetic installation, routing, integrity, recovery, upgrade, removal, and reinstallation qualification matrix from a local terminal.
tags: [internal, roadmap, dogfood, qualification, automation, shell, opencode]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 19
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T11:46:55+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-14T12:48:00+02:00
---

# Add One-Command Synthetic Qualification Runner

## Observed behavior

The synthetic-vault evaluation required the operator to run a long sequence of separate commands for corpus finalization, variant materialization, pinned asset acquisition, installation, OpenCode routing prompts, managed-content damage, conformance, semantic reconciliation, finalization, rollback, uninstall, reinstallation, project-owned hashing, and terminal-state verification.

The manual sequence successfully exposed product and fixture findings, but it also required repeated shell setup, copied paths, hand-maintained ordering, and interpretation of expected failures. One rollback was invoked twice after the first role-led invocation had already succeeded, and a conformance command failed when run without the repository root on `PYTHONPATH`. Repeating the same matrix for the corrective alpha, release candidate, and stable release would have remained unnecessarily error-prone.

## Classification

This was `required-v1` and blocked the release candidate until the maintained qualification matrix had one repeatable operator entry point. The runner is internal release tooling, not a distributed Ava CLI or persistent runtime.

The complete runner is a manual maintainer operation. It is not invoked by GitHub Actions, release-please automation, pull-request checks, or `internal/release/test.sh`. Those environments do not provide the external qualification corpus, pinned local asset directories, OpenCode sessions, model access, interactive approvals, or user semantic signoff required by the matrix.

## Ordering

Implemented after:

1. [Finding 17](17-add-resume-abort-qualification-checkpoints.md) supplied deterministic resume and abort checkpoints.
2. [Finding 18](18-verify-relative-calendar-dates.md) defined the corrected calendar-fidelity scenario.

The runner consumes both maintained mechanisms rather than duplicating or bypassing them.

## Implementation

Implemented as repository-only release qualification tooling:

- `internal/release/qualify-synthetic.sh` is the single POSIX maintainer entry point.
- `internal/release/qualification_runner.py` owns preflight, safe workspace isolation, pinned asset verification, deterministic orchestration, bounded OpenCode execution, state assertions, interrupted reruns, and final summary status.
- `internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json` records the exact deterministic eight-family order, 17 maintained scenarios, bounded prompts, calendar regression, and stable managed-damage rule IDs.
- `internal/release/qualification-runner.md` documents the complete local command, preflight-only mode, input boundaries, rerun ownership, and interpretation contract.
- bounded tests cover argument shape, pinned asset checksums, mutable `latest` refusal, execution-root safety, finalized-corpus ownership, interrupted reruns, deterministic matrix coverage, exactly-once rollback planning, CI separation, internal-only placement, and nonzero summary behavior.

The runner reads the finalized qualification root and supplied test project without mutating them. Every scenario executes in a runner-owned copy below the explicit external execution root. The ownership sentinel binds that root to the finalized corpus digest so an interrupted rerun cannot silently accept a changed baseline.

Conformance runs through `python3 -m internal.release.conformance` with the repository root on `PYTHONPATH`. Managed-damage scenarios pass only for the exact expected stable rule ID while preserving the injected failure evidence. Resume and abort use Finding 17's checkpoint harness and the real selected target installer operations. The Finding 18 regression requires `Friday` and `2026-08-14` and rejects `2026-08-15`.

## Completion criteria

- [x] One documented shell command executes the complete maintained synthetic qualification sequence from explicit pinned inputs.
- [x] Documentation identifies the complete command as a manual maintainer operation run from a local terminal.
- [x] No GitHub Actions workflow, release-please job, pull-request check, or `internal/release/test.sh` invocation executes the complete runner.
- [x] The runner refuses mutable latest-release selection, ambiguous assets, repository-local generated output, and unsafe pre-existing execution roots.
- [x] A preflight-only mode reports planned scenarios and inputs without modifying any project.
- [x] The finalized corpus is verified and remains byte-identical before and after every run.
- [x] All eight variant families and their maintained subscenarios are prepared and executed in deterministic order.
- [x] Finding 17's authentic resume and abort checkpoints are exercised through the real installer operations.
- [x] Finding 18's relative calendar scenario verifies the persisted weekday and absolute date.
- [x] OpenCode-required scenarios use exact maintained prompts and report when user approval or semantic judgment prevents unattended completion.
- [x] Expected managed-damage conformance failures count as scenario passes only when their exact stable rule IDs are observed and injected evidence remains unchanged.
- [x] Rollback is invoked exactly once and proves the source installation, semantic state, transaction cleanup, and normal routing.
- [x] Uninstall and reinstall prove byte-identical project-owned preservation and healthy final installed conformance.
- [x] The final summary identifies every scenario outcome and exits nonzero for an unexpected skip, mismatch, command failure, or unresolved required decision.
- [x] Automated tests cover bounded argument validation, safe boundaries, expected-failure handling, command planning, interrupted reruns, and summary exit status without OpenCode, external qualification data, model credentials, or complete-matrix execution.
- [x] Release assembly excludes the runner and every generated execution artifact.
- [x] The complete release suite and repository boundary validation pass through the maintained pull-request `python-tests` gate.

## Qualification follow-up

Run the completed entry point against the selected corrective-alpha assets, review its concise result summary, and use explicit user signoff as the final semantic acceptance gate. This immutable-asset execution remains a release qualification gate, not pending repository implementation.
