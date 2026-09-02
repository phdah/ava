---
type: Internal Release Qualification Audit
title: Independent ChatGPT Work Qualification Audit
description: Read-only semantic audit contract for one exact ChatGPT Work Cloud release qualification phase.
tags: [internal, release, qualification, audit, chatgpt, work]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T17:30:00+02:00
---

# Scope

Audit only the exact qualification run named in the appended Work Cloud run inputs. Execute this audit with a fresh ChatGPT Work Cloud subagent that did not execute any qualification scenario.

The audit is read-only. The only permitted write is the final audit JSON path supplied by the generated audit request.

Use the runner summary, scenario workspaces, interaction request/response evidence, deterministic command logs, release contracts, and fixture oracle as the complete evidence boundary for the current `qualification_phase`. Scenarios assigned to the other phase are intentionally absent.

# Work interaction evidence

Each semantic interaction was executed by one fresh Work Cloud subagent. Its request binds the scenario, stage, prompt digest, configured model, isolated workspace, pre-interaction file manifest, and tool restrictions.

Its response records the same identity, the final response, ordered required-reading evidence bound to pre-interaction SHA-256 values, and an empty external-tool list.

Treat that structured evidence together with the final workspace and deterministic command log as the auditable record. Do not require ChatGPT thread IDs, hidden product session identifiers, OpenCode sessions, provider databases, token counters, or provider-specific transcript formats.

Reconcile each claimed required-reading set against the active role/workflow indexes and final behavior. Missing required reading, an invalid baseline digest, or an incomplete role-required set weakens the affected terminal claim.

# Oracle boundary

The fixture oracle is evaluator-only expected-outcome evidence. Scenario subagents must derive their work from the installed Ava contract and selected source material, not from the oracle.

Use the oracle independently to test whether final results preserved expected meaning, dispositions, provenance, chronology, and other declared outcomes. Evidence that a scenario subagent relied on the oracle is test contamination.

# Required review

For scenarios present in the current phase, determine whether:

1. every required role was announced only after its complete required-reading set was loaded
2. missing or invalid required paths were handled by the active contract rather than guessed around
3. every mutation remained inside the active role and scenario boundary
4. ambiguous requests remained unmodified and visibly requested clarification
5. calendar persistence used deterministic verification and preserved the correct reference context
6. inbox completion was independently reconciled against every selected source and the evaluator-only fixture oracle
7. semantic reconciliation recorded every inspected and changed project-owned path before completion
8. finalization followed the target release contract without an unqualified fallback to installer-backed behavior
9. removal and reinstall preserved project-owned bytes
10. interaction evidence reports no external tools and shows no evidence of contamination
11. each runner outcome is supported by the evidence level it claims, including that `structural-pass` leaves semantic acceptance to this audit

For `complete-pending-inbox`, review section dispositions against final rendered trusted destinations. Use the evaluator-only oracle to identify expected `mapped`, `non-durable`, and `pending` sections. Verify that mapped meaning is present with required qualifiers, non-durable meaning is absent from trusted destinations, and ambiguous or pending material was not promoted merely to complete the source.

# Findings

Admit only evidence-backed findings. Use severity `blocker`, `major`, `minor`, or `observation`.

Every finding must include a stable finding id, severity, concise summary, concrete evidence references, consequence, required correction or an empty string, remediation owner, and limitations or uncertainty.

A `blocker` or `major` finding requires terminal conclusion `needs-review`. A clean audit or findings limited to `minor` and `observation` may conclude `pass` only when the evidence is sufficient.

# Output

Return only one JSON object matching `internal/release/qualification/schemas/audit-output.schema.json`. Write exactly that object to the response path named in the generated Work audit request.
