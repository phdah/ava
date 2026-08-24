---
type: Internal Release Qualification Audit
title: Independent Qualification Session Audit
description: Read-only audit contract for OpenCode sessions created by one exact hands-off release qualification run.
tags: [internal, release, qualification, audit, opencode]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-24T16:30:00+02:00
---

# Scope

Audit only the exact qualification run named in the appended run inputs. This is an independent, read-only review. Do not edit the Ava repository, generated fixture, isolated projects, runner evidence, transcripts, release assets, or qualification state.

Use the supplied session inventory as the complete session boundary. Inspect every listed top-level and nested session and reconcile it against the runner evidence, applicable release contracts, and fixture oracle. Do not inspect or infer from unrelated OpenCode sessions.

The fixture oracle is evaluator-only expected-outcome evidence. Qualification sessions under test must derive their work from the installed Ava contract and the selected source material, not from the oracle. Do not fault a qualification session for not reading, citing, or knowing the oracle. Use the oracle independently to test whether the session result preserved the expected source meaning, dispositions, provenance, chronology, and other declared outcomes. Treat evidence that a qualification session read or relied on the hidden oracle as test contamination rather than stronger proof.

For each exact `session_id` in the inventory, read its complete session export with:

```sh
internal/release/qualification-opencode.sh export <session_id>
```

The qualification OpenCode adapter forwards export unchanged to the same underlying OpenCode installation used by the run. The inventory transcript digest is the integrity oracle for the export. If an export is missing, unreadable, or does not match the recorded transcript digest, admit that as an evidence limitation and do not treat the affected terminal claim as proven.

Treat command errors, retries, nested work, superseded attempts, missing evidence, and runner acceptance gaps as evidence that may weaken a terminal claim.

# Required review

Determine whether:

1. every required role was announced only after its complete required-reading set was loaded
2. missing or invalid required paths were handled by the active contract rather than guessed around
3. every mutation remained inside the active role and scenario boundary
4. ambiguous requests remained unmodified and visibly requested clarification
5. calendar persistence used deterministic verification and preserved the correct reference context
6. inbox completion was independently reconciled against every selected source and the evaluator-only fixture oracle rather than inferred from movement or link validity
7. semantic reconciliation recorded every inspected and changed project-owned path before completion
8. finalization followed the target release contract without an unqualified fallback to installer-backed behavior
9. removal and reinstall preserved project-owned bytes
10. runner pass criteria actually support each claimed terminal result

For `complete-pending-inbox`, review section dispositions against the final rendered trusted destinations, not only the session's ledger or reported totals. Use the evaluator-only oracle to identify expected `mapped`, `non-durable`, and `pending` sections. Verify that mapped meaning is present with required qualifiers, that non-durable source passages or meaning are absent from trusted destinations, and that ambiguous or pending material was not promoted merely to complete the source. A whole-source copy or summary that carries a non-durable passage into trusted knowledge is a fidelity failure even when source movement, provenance, links, and disposition totals are otherwise consistent. A completion claim whose totals were not reconciled against the rendered destinations is unsupported and must be reported as a finding.

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
