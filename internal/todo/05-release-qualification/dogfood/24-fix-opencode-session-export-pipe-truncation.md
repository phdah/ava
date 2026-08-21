---
type: Internal Development Task
title: Fix OpenCode Session-Export Pipe Truncation in Qualification Evidence Capture
description: Remove the 65,536-byte pipe truncation limitation affecting qualification session-inventory evidence capture.
tags: [internal, roadmap, dogfood, release, qualification, tooling]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 24
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.15
generated:
  by: agent:openai-opencode
  at: 2026-08-20T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-21T08:50:00+02:00
---

# Fix OpenCode Session-Export Pipe Truncation in Qualification Evidence Capture

## Observed behavior

During release qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local`, session-inventory capture encountered OpenCode's 65,536-byte pipe truncation limit when qualification captured large JSON output through a subprocess pipe. OpenCode produced complete JSON when writing to a regular file, while the same command was truncated at exactly 65,536 bytes when its stdout was a pipe.

An external `/tmp` wrapper buffered OpenCode `db` output to a regular file and verified that the qualification data itself was valid. That workaround is no longer required by the repository implementation.

## Reproduction and evidence

The affected path is the maintained [`qualification-opencode.sh`](../../../release/qualification-opencode.sh) adapter used by `qualify-release.sh` for session inventory and export capture. The adapter previously let the real OpenCode process inherit qualification automation's stdout pipe for both the session-list database query and `opencode export`.

A regression fake now deliberately truncates its own output to 65,536 bytes whenever it detects FIFO stdout, while emitting valid JSON larger than 65,536 bytes to a regular file. Both large session-list and large export adapter tests must recover the complete valid payload.

## Classification

This remains a `required-v1` finding discovered during the alpha.15 qualification cycle. It originally blocked the release candidate rather than the immediate corrective alpha because an external workaround existed. The repository-owned fix is now implementation-complete before the corrective-alpha rerun.

## Root cause

Qualification automation captures adapter stdout through a pipe. The adapter previously invoked OpenCode's JSON-producing session-list `db` query and `export` command with that pipe inherited as OpenCode's stdout. In the affected OpenCode environment, JSON output to a pipe is truncated at 65,536 bytes even though output to a regular file is complete.

The fix keeps the qualification automation contract unchanged but changes the adapter boundary: those OpenCode JSON commands now write first to a temporary regular file and only then are re-emitted by the adapter to qualification automation. OpenCode therefore never writes the affected large JSON directly to the pipe.

## Scope

- [x] locate the exact session inventory/export capture path affected by the pipe-size limit
- [x] buffer session-list database JSON through a temporary regular file before re-emitting it
- [x] buffer `opencode export` JSON through a temporary regular file before re-emitting it
- [x] add regression coverage using JSON output larger than 65,536 bytes that deliberately truncates when written directly to a pipe
- [x] document that normal qualification no longer requires the external workaround

## Completion criteria

- [x] session-list and session-export capture succeed for payloads larger than 65,536 bytes without an external workaround
- [x] regression coverage exercises oversized pipe-sensitive JSON for both capture paths
- [x] affected documentation and indexes remain aligned

## Resolution evidence

[`internal/release/qualification-opencode.sh`](../../../release/qualification-opencode.sh) now buffers the real OpenCode session-list database query and `export` command into a `mktemp` regular file before emitting the complete bytes to the caller. The adapter continues to preserve the existing command arguments and uses the existing Python-side JSON parsing as the validation boundary.

[`internal/release/tests/test_qualification_opencode_adapter.py`](../../../release/tests/test_qualification_opencode_adapter.py) adds a pipe-sensitive fake OpenCode implementation whose otherwise valid JSON exceeds 65,536 bytes and truncates only when its stdout is a FIFO. Regression tests prove both session inventory and session export remain complete and parseable through the repository adapter.

## Release qualification follow-up

The next fresh full qualification run must use the normal repository-owned command path without `AVA_QUALIFICATION_OPENCODE` pointing at the former external large-JSON shim. Successful complete session inventory and independent audit in that run provide release evidence for this fix; that follow-up does not return this implementation task to pending.
