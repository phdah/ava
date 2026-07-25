---
type: Internal Development Task
title: Define Deterministic Repair Boundaries
description: Separate unambiguous automatic repairs from decisions requiring a role or user.
tags: [internal, roadmap, validation, repair]
status: pending
phase: 6
order: 3
timestamp: 2026-07-25T00:00:00Z
---

# Define Deterministic Repair Boundaries

Ava may automatically repair issues only when the correct result is deterministic.

## Examples that may be safe

- adding a missing registry link with one unambiguous target
- correcting a generated index
- normalizing required metadata with known values

## Examples requiring a role or user

- resolving contradictory instructions
- choosing between duplicate canonical documents
- granting new authority
- deleting uncertain knowledge
- changing role or workflow purpose
