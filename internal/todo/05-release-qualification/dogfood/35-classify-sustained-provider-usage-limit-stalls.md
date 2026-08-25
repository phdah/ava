---
type: Internal Development Task
title: Detect and Report Sustained Model-Provider Usage-Limit Stalls
description: Distinguish a sustained provider-side stall from an ordinary transient retry and surface it to the operator instead of leaving it visible only in raw OpenCode UI/log output.
tags: [internal, roadmap, dogfood, release, qualification, reliability, provider]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 35
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
---

# Detect and Report Sustained Model-Provider Usage-Limit Stalls

## Observed behavior

Model-provider usage/rate limits can stall the qualification process for sustained periods with no visible signal beyond a UI retry counter. On 2026-08-25, two concurrent sessions (the monitoring session and the independent audit session itself) both hit `AI_APICallError: The usage limit has been reached` repeatedly; the audit session specifically made zero progress for 40+ minutes across 11 logged retries. Nothing in the pipeline detects a sustained provider-side stall, distinguishes it from a transient one, or informs the operator without them reading raw logs.

## Reproduction and evidence

2026-08-25 independent-audit session associated with run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local`: 11 logged `AI_APICallError: The usage limit has been reached` retries over 40+ minutes with no forward progress, observed concurrently in both the monitoring session and the independent audit session.

## Classification

`required-v1` for the release candidate: a single qualification attempt now requires enough concurrent/sequential live model sessions (17 scenarios plus nested children plus one independent-audit session) that provider throttling is a real, recurring risk on any heavy-usage day. It does not block every run, only heavy-usage days, so it is required before the release candidate rather than an immediate blocker of every attempt.

## Root cause

`run_command()` in both `qualification_automation.py` and `qualification_runner.py` calls `subprocess.run(...)` with no timeout and no visibility into retry behavior of its own (`qualification_automation.py:223-243`, `qualification_runner.py:434-497`). Whatever retry behavior exists is internal to the `opencode` CLI process and only visible in that process's own UI/log output, which the qualification harness captures as opaque stdout/stderr text but never inspects for a stall signature. Nothing anywhere in the pipeline distinguishes "the provider is retrying normally" from "the provider has been stuck retrying for 40 minutes with zero progress."

## Scope

- capture and inspect `opencode run`/`opencode export` stdout/stderr for a recognizable provider usage-limit/retry signature (for example `AI_APICallError`, "usage limit") while a command is in flight, not only after it returns
- classify a command as `provider-stalled` once retries of that signature persist past a documented threshold (for example N consecutive retries or M minutes with no new forward-progress output), distinct from an ordinary transient retry
- surface that classification through the run-status artifact from finding 32 so an operator or monitoring session can see "stalled on provider throttling" without reading raw OpenCode logs
- do not attempt to change or suppress the underlying OpenCode retry behavior itself; this finding only adds detection and reporting

## Completion criteria

- [ ] the harness detects a sustained, not merely transient, provider usage-limit stall from OpenCode's own output
- [ ] a sustained stall is reported through the run-status artifact as a distinct state from `running`/`crashed`/`awaiting-decision`
- [ ] the detection threshold distinguishing transient from sustained stalls is documented
- [ ] regression coverage exercises stall detection against captured or replayed stall-signature output
- [ ] repository test suite passes

## Resolution evidence

_Complete in the resolving implementation PR._
