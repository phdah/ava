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
  at: 2026-08-10T14:12:32+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for developing Ava itself. It is internal repository context and must never be copied into distributed projects.

Read the [ordered roadmap](todo/index.md) before acting.

## Current phase

[Dogfood the alpha and track findings](todo/05-release-qualification/04-dogfood-alpha-and-track-findings.md) remains active until the user explicitly declares dogfooding complete.

## Current next task

[Permit agent-driven upgrade finalization](todo/05-release-qualification/dogfood/15-permit-agent-driven-upgrade-finalization.md) is the current next task. It must remove the installer-binary framing from Ava Maintenance finalization and explicitly authorize the agent to write the terminal upgrade state directly once semantic compatibility is confirmed complete.

[Repair Inbox Ingester project-root links](todo/05-release-qualification/dogfood/14-repair-inbox-ingester-project-root-links.md) is complete. The Inbox Ingester now names the project-owned inbox through explicit project-root paths, and installed-payload regression coverage prevents the broken role-relative resolution from returning.

[Build the synthetic v1 qualification vault](todo/05-release-qualification/04a-build-synthetic-qualification-vault.md) remains the next supporting qualification task after the pending dogfood blocker is resolved.

[Clarify release semantic-impact assessment](todo/05-release-qualification/dogfood/13-clarify-release-semantic-impact-assessment.md) is complete. Release completion now distinguishes managed behavioral change from possible incompatibility in project-owned context, requires reviewed rationale for both `semantic_review_required` outcomes, and keeps the semantic decision with maintainers rather than deterministic tooling.

[Avoid redundant routing for conversational follow-ups](todo/05-release-qualification/dogfood/12-avoid-redundant-followup-routing.md) is complete. Every request keeps the managed-state gate, pure clarifications may be roleless, same-role scoped follow-ups may retain the already-active role, and new or changed scoped work performs fresh routing.

[Define release-impact-based change types](todo/05-release-qualification/dogfood/10-define-release-impact-based-change-types.md) is complete. Conventional Commit types follow supported distribution impact rather than implementation novelty or repository location.

[Normalize and enforce adjacent-edge release authoring](todo/05-release-qualification/dogfood/11-enforce-adjacent-edge-release-authoring.md) is complete. The retained alpha.5 through alpha.12 graph is normalized, active cumulative `upgrade-impact.json` authoring is removed, and release gates require one immutable previous-to-target edge.

Supporting qualification work remains pending for the synthetic vault and corrective immutable alpha. Finding 12's realistic multi-turn installed-project evidence remains a release gate rather than pending implementation work. Dogfooding remains active and new findings can still preempt the supporting sequence when their classification requires it.

## Working rule

When asked for the next to-do:

1. read this entry point
2. read the active Phase 5 index
3. read the parent dogfood task and findings index
4. if an actionable pending dogfood finding exists, resolve the first one in dependency order
5. otherwise follow the current supporting qualification task from the Phase 5 sequence
6. load only the related repository context

A finding is complete when its bounded repository change, regression coverage, documentation, indexes, and resolution evidence are committed. Later immutable-release evidence is a release gate, not pending implementation status.
