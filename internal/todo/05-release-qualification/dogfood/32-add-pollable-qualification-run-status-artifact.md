---
type: Internal Development Task
title: Add a Pollable Qualification Run Status Artifact Instead of a Bounded-Timeout Monitoring Loop
description: Replace the ad hoc bounded-timeout "while kill -0 <pid>; do sleep 300; done" monitoring pattern with an incrementally written, cheaply pollable run-status artifact that distinguishes crashed, decision-required, provider-stalled, and normal-progress states.
tags: [internal, roadmap, dogfood, release, qualification, reliability, monitoring]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 32
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
---

# Add a Pollable Qualification Run Status Artifact Instead of a Bounded-Timeout Monitoring Loop

## Observed behavior

The operator-facing monitoring pattern used across both investigation attempts was a bash tool call shaped like `while kill -0 <pid>; do sleep 300; done`, wrapped in a bounded tool timeout observed at both 7200000ms and 3600000ms on different runs. Because a full run now realistically takes longer than either window (see finding 33), the monitoring session predictably timed out before the run finished, requiring a human to notice and manually prompt it to check again. There is no push notification, resumable long-poll, or otherwise reliable way to be told "the run finished" without an operator re-triggering a check.

Separately, the runner's own pass/fail signal does not distinguish between "the underlying process crashed or died," "a scenario legitimately stopped because of a real capability gap and asked for a decision," and "everything is fine, just slow." All three surface, if at all, only through an operator manually inspecting sqlite databases, raw process tables, and OpenCode log files.

## Reproduction and evidence

No repository script, doc, or automation state file offers any pollable indication of progress while a run is in flight. `qualification_automation.py` writes compact evidence only after the entire synchronous subprocess tree returns (`write_compact_evidence`, `qualification_automation.py:982-1057`, called from `main()` around line 1270). `qualification_runner.py`'s `runner-state.json` is updated incrementally per scenario (`qualification_runner.py:363-364`, `829-846`) but lives at an unpredictable, content-hashed path (`execution_root_for_identity`, `qualification_automation.py:483-486`) that is never printed or otherwise surfaced until the run finishes and the final `external evidence: <run_root>` line is printed.

## Classification

`blocker` for the next prerelease: without a cheap, reliable way to ask "is it still going, and in what state," every run requires an operator to babysit a foreground bounded-timeout tool call that structurally cannot outlive the multi-hour run it is meant to monitor. This is the direct mechanism that produced the "requires a human to notice and manually prompt it to check again" pattern observed on both 2026-08-24 and 2026-08-25.

## Root cause

No run-scoped status artifact is written incrementally to a well-known, immediately-announced path, and nothing distinguishes crash, decision-required, provider-stalled, and normal-progress states in whatever partial evidence does exist. In the absence of a real mechanism, the operating session improvised a `kill -0` polling loop inside a single bounded tool call, which is the wrong tool for a multi-hour background task regardless of the timeout chosen: it can prove "alive" or "not alive" but nothing else, and it cannot itself outlive the run.

## Scope

- have `qualification_automation.py` (and, per-scenario, `qualification_runner.py`) write and update a small `status.json` under the run's external root, announced immediately at run start (ideally via finding 30's detached-launch output), recording: current scenario id/index, last-heartbeat timestamp, elapsed time, and a coarse `state` field distinguishing at least `running`, `crashed` (process gone without a terminal write), `awaiting-decision` (a scenario returned `user-decision-required`), `provider-stalled` (see finding 35), and `complete:<automated_state>`
- document a cheap, one-shot poll command (for example `cat <run_root>/status.json`) as the sanctioned way to check progress, and explicitly retire the bounded-timeout foreground `kill -0`-style monitoring loop
- derive `crashed` detection from process liveness plus a stale-heartbeat threshold rather than requiring the poller itself to block
- add regression coverage that the status artifact transitions correctly through a normal run, an interrupted run, and a decision-required scenario

## Completion criteria

- [ ] a run-scoped status artifact is written and updated incrementally during a run at a path announced at run start
- [ ] the artifact distinguishes running, crashed, awaiting-decision, provider-stalled, and complete states
- [ ] `qualification-automation.md` documents the sanctioned poll command and explicitly retires the bounded-timeout `kill -0` monitoring pattern
- [ ] regression coverage exercises the status artifact's state transitions
- [ ] repository test suite passes

## Resolution evidence

_Complete in the resolving implementation PR._
