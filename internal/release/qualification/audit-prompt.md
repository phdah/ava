---
type: Internal Release Qualification Audit
title: Optional Behavioral Qualification Audit
description: Optional semantic audit contract for targeted synthetic agent-behavior QA; not part of normal release acceptance.
tags: [internal, release, qualification, audit, behavioral, optional]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T20:30:00+02:00
---

# Status

This audit contract is **optional behavioral QA**.

The normal Ava release gate no longer requires synthetic consumer-agent interactions or an independent LLM audit. Release acceptance is based on the deterministic final qualification plus explicit user signoff and required GitHub Actions checks.

Retain this document for deliberate behavioral investigations, larger milestone qualification, or future generic host-adapter work.

# Scope

When an optional behavioral run is explicitly requested, audit only the exact scenarios and evidence supplied for that run. The auditor must not infer that a behavioral result is release acceptance evidence.

Use the runner summary, scenario workspaces, interaction evidence, deterministic command logs, release contracts, and fixture oracle as the bounded evidence set.

# Oracle boundary

The fixture oracle is evaluator-only expected-outcome evidence. Scenario agents must derive their work from the installed Ava contract and selected source material, not from the oracle.

Use the oracle independently to test whether final results preserved expected meaning, dispositions, provenance, chronology, and other declared outcomes. Evidence that a scenario agent relied on the oracle is test contamination.

# Suggested review

For the optional scenarios that were actually run, determine whether:

1. required routing and role instructions were loaded before role-scoped work
2. mutations remained inside the intended project-owned boundary
3. ambiguous requests requested clarification rather than guessing
4. calendar behavior preserved verified dates and reference context
5. inbox ingestion preserved source fidelity and did not promote ambiguous material
6. semantic reconciliation preserved project-owned meaning and surfaced unresolved decisions
7. role-led maintenance preserved project-owned bytes
8. observed behavior matches the scenario's maintained postconditions

# Findings

Admit only evidence-backed findings. Use severity `blocker`, `major`, `minor`, or `observation`.

A behavioral finding may justify a release fix when it exposes a real product defect, but the optional audit itself is not a mechanical release gate.

# Output

When structured output is requested, return one JSON object matching `internal/release/qualification/schemas/audit-output.schema.json`.
