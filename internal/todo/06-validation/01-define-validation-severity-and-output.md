---
type: Internal Development Task
title: Define Validation Severity and Output
description: Define stable machine-readable validation severities and finding fields.
tags: [internal, roadmap, validation, findings]
status: pending
phase: 6
order: 1
timestamp: 2026-07-25T00:00:00Z
---

# Define Validation Severity and Output

## Candidate severities

- error
- warning
- recommendation

## Decide

- severity for broken mandatory paths and required-reading links
- severity for broken optional contextual links
- severity for missing optional context or indexes
- when a missing reference invalidates a project versus producing a non-blocking finding

## Candidate output fields

- rule identifier
- affected path
- message
- deterministic fix availability
- semantic decision requirement
- related role or workflow

## Completion criteria

- define stable severity semantics
- distinguish required structure from optional context
- provide representative findings for broken required and optional references
- define the machine-readable finding shape