---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T11:37:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into distributed projects.

Read the [ordered roadmap](todo/index.md) before acting.

## Current phase

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains active until the user explicitly declares dogfooding complete.

## Current next task

[Avoid redundant routing for conversational follow-ups](todo/05-release-qualification/dogfood/12-avoid-redundant-followup-routing.md) is the current next finding. It is required-v1 routing work and requires explicit approval of the refined routing contract before implementation.

[Define release-impact-based change types](todo/05-release-qualification/dogfood/10-define-release-impact-based-change-types.md) is complete. Conventional Commit types now follow supported distribution impact rather than implementation novelty or repository location.

[Normalize and enforce adjacent-edge release authoring](todo/05-release-qualification/dogfood/11-enforce-adjacent-edge-release-authoring.md) is complete. The retained alpha.5 through alpha.12 graph is normalized, active cumulative `upgrade-impact.json` authoring is removed, and release gates now require one immutable previous-to-target edge.

Supporting qualification work remains pending for the synthetic vault and corrective immutable alpha. Completing finding 10 advances the dogfood backlog but does not complete dogfooding or automatically authorize publication.

## Working rule

When asked for the next to-do, read:

1. this entry point
2. the active Phase 5 index
3. the parent dogfood task
4. the findings index
5. the first actionable pending finding
6. only the related repository context

A finding is complete when its bounded repository change, regression coverage, documentation, indexes, and resolution evidence are committed. Later immutable-release evidence is a release gate, not pending implementation status.
