---
id: ava-5603
title: "Make knowledge hierarchy promotion predictable"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5603
---

## Description

Define semantic hierarchy-promotion guidance so ingestion routes stable subjects without allowing mixed flat collections to grow indefinitely. This task preserves the complete finding rationale, approved direction, completion criteria, and resolution evidence.

## Migrated task record

Historical metadata: phase 5 finding 3, classification `required-v1`, blocking the release candidate, affected version `1.0.0-alpha.5`, completed after implementation.

### Observed behavior

Inbox Ingester created a usable initial hierarchy but placed 15 engineering initiatives, external integrations, and meeting-shaped concepts as direct siblings under `knowledge/work/projects/`. The index needed separate `Engineering Initiatives`, `External Integrations`, and `Meeting Notes` headings while all files remained physical siblings, making future growth predictably flat and mixed.

Stable subjects were also sometimes classified by source artifact shape: durable integrations and initiatives could be typed/filed as meeting or project notes, while several project identities still needed a project-owned decision about whether they were projects, integrations, systems, or independently useful meeting records.

### Classification and root cause

This was `required-v1` because progressive disclosure and canonical retrieval are v1 goals. The exact taxonomy remains project-owned, but Ava needed predictable semantic guidance. The knowledge-organization contract did not sufficiently explain when an index subgroup should become a child collection or emphasize that canonical identity follows the durable subject rather than the source artifact type.

### Approved direction

- classify canonical concepts by stable subject identity, not source format
- merge meeting-derived knowledge into the owning project, integration, system, decision, or process by default
- create standalone meeting concepts only when the event has independently useful decisions, commitments, or lifecycle
- promote a stable semantic subgroup when it becomes a useful routing decision among current direct children
- do not create one directory per project until that project has multiple independently maintained concepts
- keep exact scopes, domains, collection names, and ambiguous decisions project-owned
- use semantic promotion rather than numeric file-count thresholds

For the observed vault, the likely minimal split was projects for bounded initiatives, integrations for durable external systems/interfaces, plus existing incidents and team collections.

### Scope and completion criteria

The task required generic promotion/source-artifact guidance in the managed knowledge-organization contract, aligned Inbox Ingester checks, preservation of anti-speculation rules, examples across project/integration/recurring subject/meeting cases, project-owned concrete taxonomy, and realistic semantic-review coverage. Completion required explainable heading-versus-child decisions, stable-subject ownership for meeting-derived knowledge, no numeric threshold, direct-child-only indexes, regression context for the observed mix, repeated-ingestion scalability, and recorded PR/published/realistic evidence.

### Resolution evidence

Merged PR #65 implemented the repository change and it was published in `1.0.0-alpha.10`. `knowledge-organization.md` now distinguishes canonical concepts from collection routing and defines ordered semantic promotion without numeric thresholds. Inbox Ingester checks stable headings and repeated semantic classes before adding siblings and leaves sources pending for Project Steward reorganization when promotion is required. Project Steward owns trusted-branch reorganization while preserving metadata, provenance, links, direct-child indexes, and scoped history. Change Reviewer received independent semantic checks for subject identity, subgroup promotion, ambiguity, and non-speculative hierarchy. `internal/release/fixtures/knowledge-hierarchy-promotion.json` and `internal.release.tests.test_knowledge_hierarchy_promotion` cover the observed cases and role boundary.

Published-version and repeated realistic-project validation remained release-qualification follow-up rather than reopening the completed bounded implementation task.