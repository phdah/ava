---
type: Internal Development Task
title: Dogfood the Alpha and Track Findings
description: Exercise published prereleases through real Ava and OpenCode usage, manage findings durably, and continue until the user explicitly closes dogfooding.
tags: [internal, roadmap, alpha, dogfooding, defects, opencode]
status: pending
phase: 5
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T17:30:00+02:00
---

# Dogfood the Alpha and Track Findings

## Purpose and authority

The alpha exists to expose failures not found by fixtures or design review. Findings are managed through the [Alpha Dogfood Findings](dogfood/) backlog.

Only the user may mark this umbrella task complete. A passing suite, empty backlog, or another prerelease does not complete dogfooding automatically.

## Required scenario coverage

Dogfooding covers installation into empty and mature projects, repeated OpenCode sessions, role and workflow routing, context maintenance, inbox ingestion, independent review, damaged-state diagnosis, transaction recovery, semantic upgrades, uninstall, reinstall, and every supported published transition.

The synthetic qualification vault supplies a reproducible baseline, but realistic projects remain required.

## Backlog operation

For each finding:

1. record behavior and evidence
2. classify it as `blocker`, `required-v1`, or approved `post-v1`
3. create one bounded task
4. add it to the findings index
5. resolve the first actionable item in dependency order

Implementation completion and immutable-release qualification are separate. Repository code, tests, documentation, indexes, and resolution evidence complete a finding. Published-asset checks remain release gates.

## Release authoring during dogfooding

Every new prerelease uses the canonical adjacent catalog:

1. inherit all previous edges and guidance unchanged
2. author exactly one previous-to-target edge
3. assess only that edge
4. add only transition-local guidance and migrations
5. retain or explicitly retire supported sources
6. qualify older sources through composition

`upgrade-impact.json` and cumulative target-specific guidance are historical compatibility evidence, not active authoring inputs.

## Current state

Findings 01 through 09 and 11 are complete. Finding 10 is the current pending required-v1 item. The synthetic vault and corrective immutable release qualification remain pending supporting work.

The next release must provide immutable evidence for finding 11 by proving unchanged catalog inheritance, one-edge authoring, at least three composed historical sources, and exact-once semantic guidance.
