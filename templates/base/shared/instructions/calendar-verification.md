---
type: Shared Instruction
title: Calendar Verification
description: Deterministic verification rules for derived calendar facts.
tags: [ava, calendar, dates, verification, fidelity]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T12:11:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-14T12:41:00+02:00
---

# Calendar Verification

Use this instruction only when a task would persist a calendar value derived from relative or relational calendar language, such as a weekday, relative date, week number, month, or year.

Before persisting the derived value:

1. establish the reference date, time, or source context the statement depends on
2. verify the derived calendar value with an available deterministic date or calendar operation
3. verify any stated calendar relationships that matter, such as weekday/date agreement or week number
4. persist the value only when the verified result is consistent

Do not rely on mental calendar arithmetic when a deterministic operation is available.

If missing or ambiguous reference context could change the result, preserve the original wording or ask for clarification rather than inventing an absolute value. Source-relative wording must remain anchored to its source context rather than the current session.

This verification is not required for unrelated work or for copying an already absolute source-stated calendar value without reinterpretation.

When reviewing a persisted derived calendar fact, treat a contradiction between the stated calendar relationship and the persisted value as a semantic-fidelity defect under the Change Reviewer's ordinary finding rules.
