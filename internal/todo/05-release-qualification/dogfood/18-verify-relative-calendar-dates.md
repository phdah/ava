---
type: Internal Development Task
title: Verify Relative Calendar Dates Before Persisting
description: Require deterministic calendar verification when an Ava role converts relative day, date, week, month, or year language into durable absolute project context.
tags: [internal, roadmap, dogfood, dates, calendar, fidelity, knowledge]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 18
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T11:35:46+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-14T12:41:00+02:00
---

# Verify Relative Calendar Dates Before Persisting

## Observed behavior

During the registered-role synthetic qualification scenario on Thursday, 2026-08-13, the user asked the Work Context Steward to record that the Aurora cache review was due Friday. The role persisted `2026-08-15`, which was Saturday. The correct Friday date was `2026-08-14`.

Role selection and the private/work mutation boundary were correct, but the resulting durable project fact was false. Another model had resolved the same relative date correctly in the realistic project, demonstrating that the current instructions leave calendar conversion to model reasoning rather than requiring deterministic verification.

## Classification

This is `required-v1` and blocks the release candidate until relevant calendar conversions have an explicit verification contract. Persisting an incorrect deadline violates source fidelity even when routing and ownership are correct.

## Root cause

The shared knowledge and metadata contracts require semantic fidelity, but they did not specifically require an agent to verify the relationship between relative calendar language and any absolute date it chose to persist. A role could therefore convert `Friday`, `tomorrow`, `next week`, or similar language through unaided reasoning and write an internally inconsistent result.

## Implemented resolution

The managed base now includes a conditional [Calendar verification](../../../../templates/base/shared/instructions/calendar-verification.md) contract. When a role would persist a calendar value derived from relative or relational language, it must establish the relevant reference context, verify the derived value and any material calendar relationship with an available deterministic operation, and persist only a consistent result. Missing or ambiguous reference context is preserved or clarified rather than invented, and source-relative wording remains anchored to its source context.

Role Manager, Project Steward, Inbox Ingester, and Upgrade Role expose the contract only as conditional additional context for relevant persistence. Change Reviewer loads it only when calendar fidelity is material to the reviewed change. The root router does not load it globally, so unrelated requests do not perform calendar checks.

`internal/release/fixtures/calendar-verification.json` freezes the regression and representative boundary cases. `internal/release/tests/test_calendar_verification.py` verifies the compact contract, the exact regression, conditional role loading, semantic-review behavior, and assembled managed payload. The release test entry point includes the new suite.

## Completion criteria

- [x] Shared instructions require deterministic verification before persisting a derived calendar value.
- [x] Relevant reference context is established before verification, including source-relative context when applicable.
- [x] Relevant roles use an available deterministic calendar operation rather than unaided date arithmetic before writing a derived value.
- [x] Missing or ambiguous reference context that could change the result causes preservation or clarification rather than invention.
- [x] A Thursday 2026-08-13 request for `Friday` resolves to 2026-08-14 and rejects 2026-08-15 as inconsistent.
- [x] Regression cases cover representative day, week, month, year, leap-day, historical-source, and unresolved-relative-date behavior.
- [x] Change Reviewer treats a contradictory persisted weekday and date as a semantic fidelity finding.
- [x] Installed payload and routing coverage confirm that calendar verification occurs only for relevant persistence work.
- [x] The complete release suite and repository boundary validation are wired through the maintained `internal/release/test.sh` gate for this change.

## Qualification follow-up

Implementation completion does not replace the later published-asset qualification gate. Repeat the bounded registered-role calendar scenario in a clean session during qualification and confirm that the persisted absolute date agrees with the supplied relative weekday and reference date.
