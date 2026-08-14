---
type: Internal Development Task
title: Add One-Command Synthetic Qualification Runner
description: Provide one manual maintainer shell entry point that prepares and executes the synthetic installation, routing, integrity, recovery, upgrade, removal, and reinstallation qualification matrix from a local terminal.
tags: [internal, roadmap, dogfood, qualification, automation, shell, opencode]
status: pending
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
  at: 2026-08-14T12:10:40+02:00
---

# Add One-Command Synthetic Qualification Runner

## Observed behavior

The synthetic-vault evaluation currently requires the operator to run a long sequence of separate commands for corpus finalization, variant materialization, pinned asset acquisition, installation, OpenCode routing prompts, managed-content damage, conformance, semantic reconciliation, finalization, rollback, uninstall, reinstallation, project-owned hashing, and terminal-state verification.

The manual sequence successfully exposed product and fixture findings, but it also required repeated shell setup, copied paths, hand-maintained ordering, and interpretation of expected failures. One rollback was invoked twice after the first role-led invocation had already succeeded, and a conformance command failed when run without the repository root on `PYTHONPATH`. Repeating the same matrix for the corrective alpha, release candidate, and stable release would remain unnecessarily error-prone.

## Classification

This is `required-v1` and blocks the release candidate until the maintained qualification matrix has one repeatable operator entry point. The runner is internal release tooling, not a distributed Ava CLI or persistent runtime.

The complete runner is a manual maintainer operation. It must not be invoked by GitHub Actions, release-please automation, pull-request checks, or `internal/release/test.sh`. Those environments do not currently provide the external qualification corpus, pinned local asset directories, OpenCode sessions, model access, interactive approvals, or user semantic signoff required by the matrix.

## Ordering

Implement this after:

1. [Finding 17](17-add-resume-abort-qualification-checkpoints.md) supplies deterministic resume and abort checkpoints.
2. [Finding 18](18-verify-relative-calendar-dates.md) defines the corrected calendar-fidelity scenario.

The runner must consume those maintained mechanisms rather than duplicating or bypassing them.

## Scope

- add one documented POSIX shell entry point under the internal release qualification scope
- define the entry point as a manual local-terminal command rather than a GitHub Actions or release-automation job
- accept explicit finalized-corpus, execution-root, pinned source-asset, pinned target-asset, test-project, OpenCode, and model inputs where relevant
- preflight required tools, versions, paths, asset identities, checksums, repository cleanliness assumptions, and external-output boundaries before mutation
- preserve the finalized baseline and create or reset only explicitly owned isolated qualification workspaces
- orchestrate fresh and mature installation, registered-role routing, managed-content damage, resume, abort, rollback, semantic reconciliation, finalization, uninstall, and reinstall scenarios in maintained order
- invoke repository conformance through the supported module entry point and distinguish expected blocking findings from unexpected command failures
- invoke bounded OpenCode prompts only in isolated projects with explicit scenario authority and without broad global auto-approval
- verify project-owned hashes, managed checksums, journal states, semantic states, role selection, mutation boundaries, and expected terminal outcomes
- emit a concise scenario-by-scenario pass, fail, skipped, or user-decision-required summary and return nonzero when qualification fails
- keep detailed transcripts optional while preserving enough local state to diagnose a failed scenario
- permit CI to test only bounded argument parsing, command planning, safe-path enforcement, expected-failure interpretation, and summary behavior with isolated fixtures or stubs
- prohibit CI tests from launching OpenCode, requiring model credentials, downloading qualification assets, accessing the repository-external corpus, or executing the complete matrix
- remain excluded from assembled release assets and avoid adding a user-facing command surface

## Completion criteria

- [ ] One documented shell command executes the complete maintained synthetic qualification sequence from explicit pinned inputs.
- [ ] Documentation identifies the complete command as a manual maintainer operation run from a local terminal.
- [ ] No GitHub Actions workflow, release-please job, pull-request check, or `internal/release/test.sh` invocation executes the complete runner.
- [ ] The runner refuses mutable latest-release selection, ambiguous assets, repository-local generated output, and unsafe pre-existing execution roots.
- [ ] A preflight-only mode reports planned scenarios and inputs without modifying any project.
- [ ] The finalized corpus is verified and remains byte-identical before and after every run.
- [ ] All eight variant families and their maintained subscenarios are prepared and executed in deterministic order.
- [ ] Finding 17's authentic resume and abort checkpoints are exercised through the real installer operations.
- [ ] Finding 18's relative calendar scenario verifies the persisted weekday and absolute date.
- [ ] OpenCode-required scenarios use exact maintained prompts and report when user approval or semantic judgment prevents unattended completion.
- [ ] Expected managed-damage conformance failures count as scenario passes only when their exact stable rule IDs are observed and injected evidence remains unchanged.
- [ ] Rollback is invoked exactly once and proves the source installation, semantic state, transaction cleanup, and normal routing.
- [ ] Uninstall and reinstall prove byte-identical project-owned preservation and healthy final installed conformance.
- [ ] The final summary identifies every scenario outcome and exits nonzero for an unexpected skip, mismatch, command failure, or unresolved required decision.
- [ ] Automated tests cover bounded argument validation, safe boundaries, expected-failure handling, command planning, interrupted reruns, and summary exit status without OpenCode, external qualification data, model credentials, or complete-matrix execution.
- [ ] Release assembly excludes the runner and every generated execution artifact.
- [ ] The complete release suite and repository boundary validation pass.

## Qualification follow-up

Run the completed entry point against the selected corrective-alpha assets, review its concise result summary, and use explicit user signoff as the final semantic acceptance gate.
