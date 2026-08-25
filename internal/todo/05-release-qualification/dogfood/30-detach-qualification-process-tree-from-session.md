---
type: Internal Development Task
title: Detach Qualification Automation's Process Tree From the Operator Session Lifecycle
description: Provide a sanctioned way to run qualify-release.sh fully detached from the invoking shell/session so a closed laptop, dropped connection, or killed tool call does not silently kill a multi-hour qualification run.
tags: [internal, roadmap, dogfood, release, qualification, reliability, process]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 30
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-25T20:02:00+02:00
---

# Detach Qualification Automation's Process Tree From the Operator Session Lifecycle

## Observed behavior

On 2026-08-24, qualification run `20260824T155755925230Z-alpha14-to-alpha15-corrective-local` died silently around the 2-hour mark mid-scenario, with no `summary.json` and no process left alive, coinciding with the operator's laptop closing. Because the run could not be resumed (see finding 31), the operator had to plan on restarting all 17 scenarios from scratch, at real multi-hour cost. Over two days, this recurring failure mode made completing a single qualification run largely unworkable in practice.

## Reproduction and evidence

Run `20260824T155755925230Z-alpha14-to-alpha15-corrective-local`: no corresponding entry exists under `internal/release/qualification/runs/` because `write_compact_evidence()` (`qualification_automation.py:982-1057`) only runs after the entire synchronous `qualify-synthetic.sh` subprocess returns to `qualification_automation.py`'s `main()`. A parent process killed by session/laptop termination never reaches that point, so no compact evidence, no `summary.json`, and no terminal state are ever recorded for a run that dies this way.

## Classification

`blocker` for the next prerelease: `internal/release/procedure.md` mandates a full `qualify-release.sh` run before any release-please PR may merge. Two consecutive days of attempts failed to produce one completed corrective-alpha run because of this failure mode, which makes it impossible to reach the mandatory qualification gate at all.

## Root cause

`qualify-release.sh` execs `qualification_automation.py`, which is a single foreground Python process. It itself runs the multi-hour `qualify-synthetic.sh` matrix and every nested `opencode` invocation through plain `subprocess.run(...)` calls (`qualification_automation.py:223-243`, `qualification_runner.py:434-497`) with no `setsid`/`start_new_session`, no process-group detachment, and no supervising init-like wrapper. Nothing in `internal/release/*.sh`, `qualification-automation.md`, or `procedure.md` documents or provides a detached invocation path (`nohup`, `setsid`, `systemd-run`, `tmux`, or equivalent). When the invoking session or terminal dies, the entire process tree - the automation process, the runner, and every live or spawned `opencode` process - dies with it, because none of it was ever moved into its own session or kept alive by a supervisor independent of the invoking shell.

## Scope

- add a sanctioned, documented way to launch `qualify-release.sh` fully detached from the invoking shell/session (for example a thin wrapper using `setsid`/`nohup` with explicit stdout/stderr redirection to a run-scoped log file under the external run root, or a documented `systemd-run --user --scope` / `tmux new-session -d` invocation)
- have the launch path print, before returning control, the child PID, its detached log file path, and (once resolvable) the run's external evidence root, so an operator or monitoring session never needs to keep a foreground shell alive to know where to look
- document the sanctioned launch and check-on-a-run commands in `qualification-automation.md` and `procedure.md`, replacing the current implicit assumption that `qualify-release.sh` runs to completion inside one foreground shell
- add regression coverage (or, given a real multi-hour run cannot be exercised as a unit test, a scripted integration check) proving a detached child process survives closing/killing the parent shell/session

## Completion criteria

- [x] a documented command starts qualification fully detached from the invoking shell/session and returns immediately with a PID and log path
- [x] killing or closing the invoking shell/session (verified with a real process-group test, for example sending SIGHUP to the launcher's process group) does not terminate the detached qualification process tree
- [x] `qualification-automation.md` and `procedure.md` document the detached launch and status-check commands as the standard operator flow
- [x] regression coverage exercises the detachment mechanism
- [x] repository test suite passes

## Resolution evidence

`internal/release/qualify-release-detached.sh` is now the sanctioned operator launcher. It requires `nohup` and `setsid`, creates a repository-external launch root, redirects qualification output to `qualification.log`, records the detached process PID, starts `qualify-release.sh` in a separate session with stdin detached from the terminal, and groups the automation's external run root below the same launch root. It prints the PID, log, launch root, and exact evidence root when initialization has already created it.

`internal/release/tests/test_qualification_detached.py` launches the real detached wrapper against a controlled fake qualification child, sends SIGHUP to the invoking shell's process group, proves the detached child remains alive, and waits for it to complete. `internal/release/test.sh` syntax-checks the launcher and runs that regression with the repository suite.

`internal/release/qualification-automation.md` and `internal/release/procedure.md` now make detached launch the standard operator flow and document `kill -0`, log inspection, evidence-root discovery, and `AVA_QUALIFICATION_RUN_ROOT_PARENT`.
