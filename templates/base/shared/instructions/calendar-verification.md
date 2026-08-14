---
type: Shared Instruction
title: Calendar Verification
description: Deterministic verification rules for converting relative calendar language into durable absolute project facts.
tags: [ava, calendar, dates, verification, fidelity]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T12:11:00+02:00
---

# Purpose

Use this instruction only when an active role or workflow is about to persist a newly resolved absolute calendar fact derived from relative or relational language such as `today`, `tomorrow`, `Friday`, `next week`, `next month`, or `next year`.

Do not perform calendar conversion merely because a date appears in a request. Preserve source-stated absolute or historical dates as stated unless the active task independently requires validation or correction.

If durable project context can faithfully preserve the user's relative wording without inventing an absolute date, prefer that representation when the absolute value is unnecessary.

# Reference context

Resolve relative calendar language against the reference context that actually owns the statement.

Use this order:

1. A reference date, instant, timezone, locale, or week convention explicitly supplied by the user for the statement.
2. A source-document reference date or instant when the relative wording belongs to that source and the source establishes the reference context.
3. The host-provided current local date, time, and timezone when the user is speaking relative to the current session.

Do not reinterpret a source-stated historical date or source-relative expression against the current host date merely because the source is being processed now.

A date-only reference does not establish a timezone. A timezone is material when crossing a day boundary could change the resolved date.

# Deterministic verification

Before persisting an absolute result derived from relative calendar language:

1. identify the reference context and intended calendar relation
2. use an available deterministic calendar, date, or time operation to compute or verify the result
3. verify every stated relationship that can be checked, including weekday versus date and day, week, month, or year boundaries
4. persist the absolute result only after the deterministic result agrees with the intended relation

Do not rely on unaided mental date arithmetic when the host provides a deterministic calendar capability.

For the regression case with reference date Thursday, 2026-08-13, `Friday` resolves to `2026-08-14`. `2026-08-15` is Saturday and is inconsistent with the requested weekday, so it must not be persisted as the resolved Friday.

If the host lacks a deterministic calendar capability and the absolute result cannot be established directly from trusted source data, preserve the relative wording or ask the user for the missing absolute date. Do not invent one.

# Ambiguity and preservation

Preserve the relative wording or request clarification when any missing detail materially changes the result, including:

- the reference date or instant
- timezone near a day boundary
- locale-dependent calendar interpretation
- whether a week starts on Monday, Sunday, or another project-defined convention
- ambiguous expressions such as `next Friday` or `next week` when more than one interpretation is plausible
- whether a relative expression belongs to the current session or to a dated source document

Do not silently choose one valid interpretation merely to normalize the text.

# Boundary handling

Deterministic verification must correctly handle relevant calendar boundaries rather than approximating them as fixed durations.

This includes:

- weekday and week boundaries
- month-length changes
- year boundaries
- leap years and leap day
- timezone-driven date rollover when time-of-day is material

Do not model `next month` or `next year` as a fixed number of days unless the user's wording explicitly defines that duration.

# Source and history fidelity

When processing historical or preserved source material:

- retain source-stated absolute dates without re-anchoring them to the current session
- resolve source-relative wording only against a source-established reference context
- preserve uncertainty when the source does not establish enough context for a unique absolute result
- distinguish a source claim from a current project decision or newly verified fact

A source dated 2025-03-10 that says `tomorrow` is anchored to that source date, not to the host date on which ingestion happens.

# Persistence scope

This contract applies to the mutation that would make the resolved absolute calendar fact durable. It does not require calendar operations for:

- unrelated requests
- role selection or routing by itself
- conversational explanations that do not persist a resolved date
- copying an already absolute source-stated date without reinterpretation
- deterministic metadata timestamps supplied directly by the host clock rather than derived from relative natural language

A workflow inherits this rule through its active role. It must not duplicate the calendar procedure or broaden the role's mutation authority.

# Semantic review

When reviewing a change that persists a newly resolved calendar fact, treat the relative wording, established reference context, deterministic calendar relation, and persisted absolute value as one semantic-fidelity claim.

A contradictory weekday and date, such as persisting `Friday 2026-08-15` for a Thursday 2026-08-13 reference, is an evidence-backed semantic fidelity defect. Classify its severity through the Change Reviewer's normal finding-admission and consequence rules rather than treating it as a formatting issue.

# Completion checks

Before completing a relevant persistence operation, verify that:

- an absolute conversion was actually necessary
- the correct reference context was used
- an available deterministic calendar operation verified the resolved result
- weekday, date, week, month, and year relationships are internally consistent when applicable
- leap-day and boundary behavior was handled by calendar semantics rather than approximate arithmetic
- materially ambiguous timezone, locale, reference-date, or week semantics were preserved or clarified rather than invented
- historical source dates were not reinterpreted relative to the current session
- no unrelated request was forced through calendar verification
