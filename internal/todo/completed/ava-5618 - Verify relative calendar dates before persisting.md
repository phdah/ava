---
id: ava-5618
title: "Verify relative calendar dates before persisting"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5618
---

## Description

Require deterministic calendar verification when an Ava role converts relative day, date, week, month, or year language into durable absolute project context.

## Migrated task record

Historical metadata: phase 5 finding 18, `required-v1`, blocking release candidate, affected version `1.0.0-alpha.14`, completed after implementation.

### Observed behavior and root cause

On Thursday 2026-08-13, a registered Work Context Steward was asked to record a cache review due Friday but persisted `2026-08-15` (Saturday) instead of `2026-08-14`. Routing and mutation boundaries were correct, but durable content became false because general fidelity contracts did not specifically require deterministic verification when relative calendar language was converted to an absolute value.

### Implemented resolution

The managed base added `templates/base/shared/instructions/calendar-verification.md`. For persistence derived from relative/relational calendar language, the role must establish the correct reference context, use an available deterministic operation to verify the value and material calendar relationship, and persist only a consistent result. Missing/ambiguous reference context is preserved or clarified, not invented, and source-relative wording stays anchored to its source context.

Role Manager, Project Steward, Inbox Ingester and Upgrade Role expose this as conditional relevant context; Change Reviewer loads it only when calendar fidelity is material. The root router does not load it globally, avoiding irrelevant calendar checks.

`internal/release/fixtures/calendar-verification.json` freezes the exact regression and representative day/week/month/year/leap-day/historical/unresolved cases. `test_calendar_verification.py` validates the compact contract, correct Friday resolution, conditional role loading, semantic-review behavior and assembled payload; it is wired into `internal/release/test.sh` and boundary validation.

Completion established deterministic verification before derived calendar persistence, source-reference handling, clarification/preservation on ambiguity, rejection of the 2026-08-15 inconsistency, Change Reviewer semantic-fidelity treatment, and relevant-only installed routing. Published qualification still had to repeat the registered-role scenario in a clean session and confirm the persisted absolute date matches the supplied weekday/reference date.