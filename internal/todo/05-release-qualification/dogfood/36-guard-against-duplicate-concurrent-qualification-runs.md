---
type: Internal Development Task
title: Guard Against Launching a Duplicate Concurrent Qualification Run
description: Wire up the already-declared "running" pair status so a second qualification run cannot be started against a candidate that may already have one in flight, wasting constrained provider quota.
tags: [internal, roadmap, dogfood, release, qualification, reliability, concurrency]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 36
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
---

# Guard Against Launching a Duplicate Concurrent Qualification Run

## Observed behavior

Because a dead or stalled run leaves no clear terminal signal (findings 30-32), there is real risk of accidentally starting a duplicate concurrent qualification run against the same candidate without realizing an earlier attempt might still be alive, or might already be dead and just appear to be, wasting even more of the same constrained provider quota (finding 35).

## Reproduction and evidence

`internal/release/qualification/current-state.json` already declares a `"running"` value in `qualification_automation.py`'s `PAIR_STATUSES` enum (`qualification_automation.py:38-46`), but nothing in `qualification_automation.py` ever writes that status when a run starts. `write_compact_evidence()` (`qualification_automation.py:982-1057`) is the only place `pair_state["status"]` is set, and it only runs once, after the run has already finished. No code path anywhere checks the active pair's current status before launching a new run.

## Classification

`required-v1` for the release candidate: this does not itself block completing a run, but it is a safety guard against wasting quota during the recurring operational difficulty documented in findings 30, 31, 32, and 35.

## Root cause

`PAIR_STATUSES` includes `"running"` as a defined schema value, but the automation never transitions a pair into that state at run start and never checks for it before starting, so the schema already anticipated this guard without anyone wiring it up.

## Scope

- at run start, before launching the runner, record the active pair's status as `running` in `current-state.json`, including the launching run's id and a start timestamp, and refuse to start a second run for the same pair while an existing `running` record is still live (cross-checking process liveness/heartbeat from finding 32's status artifact rather than trusting a stale `running` flag forever)
- clear or transition the `running` marker to the pair's terminal `automated_state` when `write_compact_evidence()` runs, and also when a launch is aborted before the runner starts
- provide a clear, documented override, not a silent default, for the rare legitimate case of intentionally starting a second run against a different candidate revision for the same pair id
- add regression coverage proving a second launch attempt against a pair already marked `running` with a live heartbeat is refused, and that a stale `running` record with a dead or expired heartbeat does not permanently block future runs

## Completion criteria

- [ ] the active pair's state records `running` with a live heartbeat/PID reference while a run is in flight
- [ ] a second launch attempt against the same pair while a live `running` record exists is refused with a clear error
- [ ] a stale `running` record from a dead process or expired heartbeat does not permanently block future runs
- [ ] regression coverage exercises both the guard and its stale-state recovery
- [ ] repository test suite passes

## Resolution evidence

_Complete in the resolving implementation PR._
