---
type: Internal Release Qualification Audit
title: Independent Qualification Interaction Audit
description: Read-only audit contract for host-neutral interaction evidence created by one exact release qualification phase.
tags: [internal, release, qualification, audit]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T16:26:00+02:00
---

# Scope

Audit only the exact qualification run named in the appended run inputs. This is an independent, read-only review. Do not edit the Ava repository, generated fixture, isolated projects, runner evidence, transcripts, release assets, or qualification state.

The appended inputs identify the `qualification_phase`. Use the supplied runner summary and interaction inventory as the complete interaction boundary for that phase. Inspect every listed top-level and nested interaction. Scenarios explicitly assigned to the other qualification phase are intentionally absent and are not missing evidence. Apply each required review item only when the current phase contains a scenario to which it is relevant.

The interaction inventory is host-neutral. Each interaction has an opaque `interaction_id`, optional `parent_interaction_id`, scenario binding, prompt digest, model identity, workspace root, materialized `transcript_path`, transcript digest, and terminal state. Do not require a particular agent runtime, session identifier shape, database representation, export command, token counter, or provider-specific transcript structure.

For every interaction, read the complete materialized transcript at `transcript_path` and verify its bytes against `transcript_sha256`. The host adapter may retain additional adapter-specific raw evidence under the external execution root, but that evidence is supplemental. If a required transcript is missing, unreadable, or fails its digest, admit that as an evidence limitation and do not treat the affected terminal claim as proven.

The fixture oracle is evaluator-only expected-outcome evidence. Qualification interactions under test must derive their work from the installed Ava contract and the selected source material, not from the oracle. Do not fault a qualification interaction for not reading, citing, or knowing the oracle. Use the oracle independently to test whether the interaction result preserved the expected source meaning, dispositions, provenance, chronology, and other declared outcomes. Treat evidence that a qualification interaction read or relied on the hidden oracle as test contamination rather than stronger proof.

Treat command errors, retries, nested work, superseded attempts, missing evidence, and runner acceptance gaps as evidence that may weaken a terminal claim.

# Required review

For the scenarios present in the current phase, determine whether:

1. every required role was announced only after its complete required-reading set was loaded
2. missing or invalid required paths were handled by the active contract rather than guessed around
3. every mutation remained inside the active role and scenario boundary
4. ambiguous requests remained unmodified and visibly requested clarification
5. calendar persistence used deterministic verification and preserved the correct reference context
6. inbox completion was independently reconciled against every selected source and the evaluator-only fixture oracle rather than inferred from movement or link validity
7. semantic reconciliation recorded every inspected and changed project-owned path before completion
8. finalization followed the target release contract without an unqualified fallback to installer-backed behavior
9. removal and reinstall preserved project-owned bytes
10. each runner outcome is supported by the evidence level it claims, including that `structural-pass` proves only deterministic structure and leaves `semantic_status: pending-audit` for this independent review

For `complete-pending-inbox`, review section dispositions against the final rendered trusted destinations, not only the interaction's ledger or reported totals. Use the evaluator-only oracle to identify expected `mapped`, `non-durable`, and `pending` sections. Verify that mapped meaning is present with required qualifiers, that non-durable source passages or meaning are absent from trusted destinations, and that ambiguous or pending material was not promoted merely to complete the source. A whole-source copy or summary that carries a non-durable passage into trusted knowledge is a fidelity failure even when source movement, provenance, links, and disposition totals are otherwise consistent. A completion claim whose totals were not reconciled against the rendered destinations is unsupported and must be reported as a finding.

A runner `structural-pass` for this scenario is not evidence that the semantic checks above passed. It means the runner's bounded non-oracle checks succeeded and deliberately hands the remaining semantic claim to this audit. Do not fault the runner merely for leaving that semantic status pending; fault it only if its structural claim is unsupported or if qualification automation treats the pending semantic status as final semantic acceptance without this audit.

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
