---
type: Internal Development Task
title: Let Qualification Automation Resume a Dead Run's Completed Scenarios
description: Wire up the qualification runner's existing per-scenario checkpoint state so a later automation invocation can resume a dead or interrupted run instead of restarting all 17 scenarios from scratch.
tags: [internal, roadmap, dogfood, release, qualification, reliability, resume]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 31
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
---

# Let Qualification Automation Resume a Dead Run's Completed Scenarios

## Observed behavior

When qualification run `20260824T155755925230Z-alpha14-to-alpha15-corrective-local` died mid-scenario after roughly two hours (finding 30), there was no way to resume it. The operator had to plan on restarting the complete 17-scenario matrix from scenario 1, discarding hours of already-completed, side-effect-free scenario evidence, at real multi-hour cost per failure.

## Reproduction and evidence

`qualification_runner.py` already implements per-scenario checkpoint state: `load_state`/`save_state` persist `runner-state.json` under the execution root (`qualification_runner.py:353-364`), `scenario_workspace()` reuses a scenario's workspace and skips re-running it when its last recorded outcome is `pass`/`structural-pass` for that same `--execution-root` (`qualification_runner.py:367-382`), and `run()` saves state after every scenario (`qualification_runner.py:829-846`).

However, `qualification_automation.py`'s `main()` always derives a brand-new `run_root = parent / f"ava-qualification-{run_id}"` from a fresh UTC timestamp on every invocation (`qualification_automation.py:1092-1101`), and `execution_root_for_identity()` nests the execution root under that fresh run_root. No CLI flag lets a later invocation point at a dead run's already-computed `execution_root`, so the existing scenario-level resume in `qualification_runner.py` is structurally unreachable from the operator-facing `qualify-release.sh` entry point.

## Classification

`blocker` for the next prerelease: restarting all 17 scenarios after every crash makes each qualification attempt cost multiple hours end-to-end at real, recurring quota and time cost. Combined with finding 30's detachment gap and finding 35's provider-throttling risk, this is what made the two-day investigation conclude the pipeline was "largely unworkable in practice."

## Root cause

The qualification runner's scenario-level checkpoint mechanism only activates when re-invoked with the same `--execution-root`. The operator-facing automation layer that wraps it never exposes or reuses a prior run's execution root, so every `qualify-release.sh` invocation is, from the runner's perspective, indistinguishable from a fresh run even when a prior attempt's `execution_root` and `runner-state.json` are still intact on disk.

## Scope

- add a `qualification_automation.py` option (for example `--resume-run-root <path>`) that, given a prior run's external run root, reuses its already-resolved `assets/`, `fixture/`, and `execution/<identity>` directories instead of re-resolving or re-downloading release assets and regenerating the fixture, then re-invokes `qualify-synthetic.sh` with that same `--execution-root` so already-passed scenarios are skipped by the existing checkpoint logic
- validate that a resumed run's execution identity (source, target, fixture, matrix, runner, automation hashes) exactly matches the current repository state before resuming, refusing resume when anything relevant has changed (reuse `execution_identity()`)
- preserve the existing fresh-run path unchanged; resume must be strictly additive
- add regression coverage that interrupts a runner mid-matrix, resumes it through the automation layer, and asserts already-passed scenarios are not re-executed while the run still reaches a terminal `automated_state`

## Completion criteria

- [ ] a documented automation option resumes a prior run using its existing external run root
- [ ] resuming skips already-passed scenarios and only re-runs the interrupted scenario and any scenarios after it
- [ ] resume is refused with a clear error when the recorded execution identity no longer matches the current repository, assets, or fixture
- [ ] regression coverage exercises interrupted-then-resumed automation runs
- [ ] repository test suite passes

## Resolution evidence

_Complete in the resolving implementation PR._
