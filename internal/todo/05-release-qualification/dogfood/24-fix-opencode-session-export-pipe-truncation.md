---
type: Internal Development Task
title: Fix OpenCode Session-Export Pipe Truncation in Qualification Evidence Capture
description: Remove the 65,536-byte pipe truncation limitation affecting qualification session-inventory evidence capture.
tags: [internal, roadmap, dogfood, release, qualification, tooling]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 24
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.15
generated:
  by: agent:openai-opencode
  at: 2026-08-20T00:00:00Z
---

# Fix OpenCode Session-Export Pipe Truncation in Qualification Evidence Capture

## Observed behavior

During release qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local`, session-inventory capture encountered OpenCode's 65,536-byte pipe truncation limit when exporting session content for evidence. An external workaround was applied and verified for this run, but the underlying limitation remains in the qualification tooling.

## Reproduction and evidence

Qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local`. The workaround applied for this run is external to the repository and is not yet a repository-owned fix.

## Classification

This is `required-v1`, blocking the release candidate rather than the immediate next prerelease, because a verified external workaround exists for the current run. It must be fixed before release-candidate qualification is treated as durable, since evidence-capture fidelity for the mandatory qualification matrix should not depend on an undocumented external workaround.

## Root cause

Unknown in detail. The session-export path used to capture nested OpenCode sessions for compact evidence appears to read process output through a fixed-size pipe that truncates at 65,536 bytes for large session exports.

## Scope

- locate the exact session-export/capture code path affected by the pipe-size limit
- remove the truncation limitation (e.g., read to completion, stream to a temp file, or otherwise avoid a fixed-size pipe buffer assumption)
- add regression coverage using a session export larger than 65,536 bytes
- document the fix so future qualification runs do not require an external workaround

## Completion criteria

- session-export capture succeeds for exports larger than 65,536 bytes without an external workaround
- regression coverage exercises an oversized export
- affected documentation and indexes remain aligned

## Resolution evidence

_Complete in the resolving implementation PR._

## Release qualification follow-up

Record confirmation in a future qualification run that session-inventory capture no longer requires an external workaround.
