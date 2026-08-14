---
type: Internal Release Qualification Audit
title: Independent Qualification Session Audit
description: Read-only audit contract for OpenCode sessions created by one exact hands-off release qualification run.
tags: [internal, release, qualification, audit, opencode]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
---

# Scope

Audit only the exact qualification run named in the appended run inputs. This is an independent, read-only review. Do not edit the Ava repository, generated fixture, isolated projects, runner evidence, transcripts, release assets, or qualification state.

Use the supplied session inventory as the complete session boundary. Inspect every listed top-level and nested session and reconcile it against the runner evidence, applicable release contracts, and fixture oracle. Treat command errors, retries, nested work, superseded attempts, missing evidence, and runner acceptance gaps as evidence that may weaken a terminal claim.

# Required review

Determine whether:

1. every required role was announced only after its complete required-reading set was loaded
2. missing or invalid required paths were handled by the active contract rather than guessed around
3. every mutation remained inside the active role and scenario boundary
4. ambiguous requests remained unmodified and visibly requested clarification
5. calendar persistence used deterministic verification and preserved the correct reference context
6. inbox completion was independently reconciled against every selected source and the fixture oracle rather than inferred from movement or link validity
7. semantic reconciliation recorded every inspected and changed project-owned path before completion
8. finalization followed the target release contract without an unqualified fallback to installer-backed behavior
9. removal and reinstall preserved project-owned bytes
10. runner pass criteria actually support each claimed terminal result

# Findings

Admit only evidence-backed findings. Use severity `blocker`, `major`, `minor`, or `observation`.

Every finding must include:

- a stable finding id
- severity
- concise summary
- concrete evidence references
- consequence
- required correction, or an empty string when no correction is required
- remediation owner: `repository`, `release-assets`, `fixture`, `runner`, `agent-behavior`, or `user-decision`
- limitations or uncertainty

A `blocker` or `major` finding requires terminal conclusion `needs-review`. A clean audit or findings limited to `minor` and `observation` may conclude `pass` only when the evidence is sufficient for the automated qualification claim.

# Output

Return only one JSON object matching `internal/release/qualification/schemas/audit-output.schema.json`. Do not wrap it in Markdown and do not include prose before or after it.
