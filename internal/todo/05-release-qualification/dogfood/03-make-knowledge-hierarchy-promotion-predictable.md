---
type: Internal Development Task
title: Make Knowledge Hierarchy Promotion Predictable
description: Define semantic hierarchy-promotion guidance so ingestion routes stable subjects without allowing mixed flat collections to grow indefinitely.
tags: [internal, roadmap, dogfood, knowledge, hierarchy, classification]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 3
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-05T13:07:09+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T19:15:00+02:00
---

# Make Knowledge Hierarchy Promotion Predictable

## Observed behavior

The Inbox Ingester created a usable initial hierarchy, but placed 15 engineering initiatives, external integrations, and meeting-shaped concepts as direct siblings under `knowledge/work/projects/`. Its index already needs three stable headings to distinguish those groups, and future ingestion would continue growing one mixed flat collection.

## Reproduction and evidence

In the alpha.5 project at `~/stuff/project-vault/`, `knowledge/work/projects/index.md` divides direct files into `Engineering Initiatives`, `External Integrations`, and `Meeting Notes` while all remain physical siblings.

The generated concepts also preserve source-artifact classifications where stable subject identities are available:

- Vilja and Aura Cloud describe durable external data interfaces but are typed and filed as meeting notes beneath projects
- Norway Analytics API and 1DK represent initiatives or projects but use meeting-note or project-note types
- Agaton, Norway Unified Experience, and Meta App Norway require a project-owned decision about whether their stable identities are projects, integrations, systems, or independently useful meeting records

The current structure remains navigable at this size. The defect is the lack of a predictable promotion decision before repeated ingestion turns source volume into a mixed canonical collection.

## Classification

This is `required-v1` and blocks the release candidate. Progressive disclosure and canonical knowledge retrieval are v1 goals. The exact taxonomy remains project-owned, but Ava must provide enough semantic guidance for agents to avoid indefinitely flat, source-shaped collections.

## Root cause

The knowledge-organization contract says to create directories when they provide a useful current classification decision, but does not explain when stable index groups should become physical child collections. It also does not state strongly enough that canonical identity should follow the durable subject rather than the source artifact type.

## Approved direction

Use semantic promotion rather than a file-count threshold:

- classify canonical concepts by stable subject identity, not by whether the source was a meeting note
- merge meeting-derived knowledge into the owning project, integration, system, decision, or process by default
- create a standalone meeting concept only when the event has independently useful decisions, commitments, or lifecycle
- promote a stable semantic subgroup to a child directory when it becomes a useful routing decision among current direct children
- do not create one directory per project until that project has multiple independently maintained concepts
- keep exact scopes, domains, collection names, and ambiguous subject decisions project-owned

For the observed vault, the smallest likely structure is `knowledge/work/projects/` for bounded initiatives, `knowledge/work/integrations/` for durable external systems and interfaces, plus the existing `incidents/` and `team/` collections.

## Scope

- add generic semantic-promotion and source-artifact guidance to the managed knowledge-organization contract
- align Inbox Ingester classification and completion checks with that guidance
- preserve the rule against speculative empty taxonomies and numeric split thresholds
- add examples that distinguish a project, integration, recurring subject, and independently useful meeting record
- keep all concrete project taxonomy decisions outside the managed base
- cover hierarchy growth and index traversal in realistic semantic review fixtures or dogfood scenarios

## Completion criteria

- an agent can explain from managed guidance when an index subgroup should remain a heading and when it should become a child collection
- meeting-derived information defaults to the stable owning subject rather than a source-shaped canonical concept
- exact project taxonomy remains project-owned and no numeric file-count threshold is introduced
- every generated directory index remains a direct-child routing node without descendant duplication
- regression context covers the observed mix of initiatives, integrations, and meeting notes
- repeated ingestion of representative daily notes produces a scalable subject hierarchy accepted through independent semantic review
- the finding index records the implementing PR, published version, and realistic-project validation before this task is completed

## Resolution evidence

Draft PR [#65](https://github.com/phdah/ava/pull/65) implements the repository change.

- `templates/base/shared/instructions/knowledge-organization.md` now distinguishes durable canonical concepts from collection-level routing decisions and defines an ordered semantic-promotion procedure without numeric thresholds.
- Inbox Ingester checks stable headings and repeated semantic classes before appending another sibling, blocks processing when promotion is required, and leaves the source pending for Project Steward reorganization.
- Project Steward owns trusted-branch reorganization while preserving metadata, provenance, links, direct-child indexes, and scoped conceptual history.
- Change Reviewer has explicit independent semantic checks for durable subject identity, mature subgroup promotion, project-owned ambiguity, and non-speculative hierarchy.
- `internal/release/fixtures/knowledge-hierarchy-promotion.json` covers the observed mix of initiatives, integrations, meeting-shaped input, temporary headings, cross-links, and ambiguous classification.
- `internal.release.tests.test_knowledge_hierarchy_promotion` enforces the fixture, role boundary, and managed instruction contracts through `internal/release/test.sh`.

Published-version and repeated realistic-project validation remain explicit release qualification follow-up. Under the dogfood backlog rule, those post-merge checks may append evidence here without returning this bounded implementation task to `pending`.
