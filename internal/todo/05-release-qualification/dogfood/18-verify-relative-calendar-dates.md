---
type: Internal Development Task
title: Verify Relative Calendar Dates Before Persisting
description: Require deterministic calendar verification when an Ava role converts relative day, date, week, month, or year language into durable absolute project context.
tags: [internal, roadmap, dogfood, dates, calendar, fidelity, knowledge]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 18
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T11:35:46+02:00
---

# Verify Relative Calendar Dates Before Persisting

## Observed behavior

During the registered-role synthetic qualification scenario on Thursday, 2026-08-13, the user asked the Work Context Steward to record that the Aurora cache review was due Friday. The role persisted `2026-08-15`, which was Saturday. The correct Friday date was `2026-08-14`.

Role selection and the private/work mutation boundary were correct, but the resulting durable project fact was false. Another model had resolved the same relative date correctly in the realistic project, demonstrating that the current instructions leave calendar conversion to model reasoning rather than requiring deterministic verification.

## Classification

This is `required-v1` and blocks the release candidate until relevant calendar conversions have an explicit verification contract. Persisting an incorrect deadline violates source fidelity even when routing and ownership are correct.

## Root cause

The shared knowledge and metadata contracts require semantic fidelity, but they do not specifically require an agent to verify the relationship between relative calendar language and any absolute date it chooses to persist. A role may therefore convert `Friday`, `tomorrow`, `next week`, or similar language through unaided reasoning and write an internally inconsistent result.

## Scope

- define the reference instant and timezone used when relative calendar language must become an absolute project fact
- require a deterministic calendar operation when verifying weekday, date, week, month, or year relationships and the host provides the necessary capability
- preserve the user's relative wording or ask for clarification when the reference instant, timezone, locale, or intended period is materially ambiguous
- avoid unnecessary conversion when durable context can faithfully retain the user's wording without an absolute date
- preserve source-stated historical dates without reinterpreting them relative to the current session
- apply the rule to every role or workflow that persists a newly resolved calendar fact, without making unrelated requests perform calendar checks
- add semantic-review coverage for contradictory weekday and date combinations

## Completion criteria

- [ ] Shared instructions define when relative calendar language requires deterministic verification before persistence.
- [ ] The contract distinguishes the current host date from source-document dates and user-specified reference dates.
- [ ] Relevant roles use an available deterministic calendar operation rather than unaided date arithmetic before writing an absolute result.
- [ ] Missing or ambiguous timezone, locale, reference date, or week interpretation causes preservation or clarification rather than invention.
- [ ] A Thursday 2026-08-13 request for `Friday` resolves to 2026-08-14 and rejects 2026-08-15 as inconsistent.
- [ ] Regression cases cover day and week boundaries, month and year boundaries, leap-day handling, and an intentionally unresolved relative date.
- [ ] Change Reviewer treats a contradictory persisted weekday and date as a semantic fidelity finding.
- [ ] Installed payload and routing coverage confirm that calendar verification occurs only for relevant persistence work.
- [ ] The complete release suite and repository boundary validation pass.

## Qualification follow-up

After implementation, repeat the bounded registered-role calendar scenario in a clean session and confirm that the persisted absolute date agrees with the supplied relative weekday and reference date.
