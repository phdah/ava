---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.0.0-alpha.15 to 1.0.0-alpha.16
description: Reconciles project-owned interaction evidence, task routing, and claim provenance with Ava 1.0.0-alpha.16.
guidance_schema: 1
guidance_id: 1.0.0-alpha.15-to-1.0.0-alpha.16
from_version: "1.0.0-alpha.15"
to_version: "1.0.0-alpha.16"
semantic_review_required: true
migration_ids: []
supersedes: []
generated:
  by: agent:openai-opencode
  at: 2026-09-01T20:13:29+02:00
---

# Upgrade Ava project context from 1.0.0-alpha.15 to 1.0.0-alpha.16

## Summary

Ava 1.0.0-alpha.16 adds interaction evidence for conversationally authorized semantic mutations, introduces the Project Task Manager and default project-owned Backlog.md scaffold, and changes precise claim attribution from source-ID markers to numbered grouped references. Existing project-owned roles, workflows, instructions, privacy policies, task conventions, or precise claim citations may remain structurally valid while conflicting with these contracts. Semantic review is therefore required. The updater replaces managed files only and must not infer or rewrite project-owned meaning or create the new project-owned task scaffold during upgrade.

## Changed managed contracts

- `/.ava/base/shared/instructions/interaction-evidence.md` defines when a material conversational fact, authorization, correction, conflict resolution, retirement, or task-state decision requires a processed interaction-evidence record. It defines ancillary recording authority, privacy safeguards, atomic evidence-to-target references, supersession, and prospective-only operation.
- Managed role indexes and capabilities load and apply interaction-evidence requirements for project stewardship, role management, inbox ingestion, task management, upgrades, and change review.
- `/.ava/base/roles/project-task-manager/` and `/.ava/base/shared/instructions/project-task-board.md` define task-record ownership, routing boundaries, configured Backlog.md operation, lifecycle safeguards, and separation between task maintenance and substantive execution.
- Fresh installation may create `/backlog.config.yml`, `/backlog/index.md`, and `/backlog/tasks/index.md` as project-owned create-if-absent scaffolds. Deterministic upgrades do not create or modify them.
- `/.ava/base/shared/instructions/document-metadata.md`, `/.ava/base/shared/instructions/inbox-ingestion-fidelity.md`, managed ingestion instructions, and related knowledge guidance now use document-local numbered grouped source references for precise claim attribution instead of source-ID footnote markers.

No deterministic migration is declared for this edge.

## Affected project-owned concepts

### Interaction evidence and conversational mutation

Inspect active project-owned roles, workflows, shared instructions, privacy or retention policies, provenance rules, and processed-inbox conventions only when they govern semantic mutations based materially on conversational facts or authority. Also inspect existing files under `/inbox/processed/` only when they declare `type: Interaction Evidence` or their filename exactly matches `interaction-<valid-interaction-id>.md`; other files with a similar prefix are outside this condition.

Completion requires compatible evidence-capture thresholds, ancillary recording authority limited to the active role's authorized mutation, privacy-preserving minimization or redaction, evidence and target mutation in one atomic change, reverse references from every target, and explicit supersession rather than historical rewriting. Existing candidates must be classified as genuine interaction evidence, malformed intended evidence, or a pre-existing project-defined type or filename collision. Genuine and intended records must satisfy the target contract; unrelated collision documents remain ordinary project source material only after an explicit compatible type or filename decision. Do not synthesize interaction evidence for mutations made before alpha.16. If project policy intentionally forbids required evidence retention or target references, record a blocking user decision rather than weakening either policy silently.

### Project task routing and ownership

Inspect registered project-owned roles and workflows only when their activation, authority, or primary role covers task records, backlog maintenance, decomposition, priorities, dependencies, acceptance criteria, or lifecycle state. Inspect active project task policies and `backlog.config.yml` when present.

Completion requires unambiguous routing between the managed Project Task Manager and project roles, preservation of substantive execution authority outside task management, use of the configured project-owned backlog directory and lifecycle, preservation of existing task state, and explicit project intent for any overlapping task-management owner. Do not create the default scaffold during upgrade or normalize a valid project configuration merely to match Ava defaults.

### Precise claim provenance

Inspect project-owned Markdown only when it has `sources` metadata and precise claim footnotes using source IDs, direct processed-source links, or another alpha.15 attribution form superseded by the numbered grouped-reference contract. Ordinary explanatory footnotes without claim-provenance meaning require no review.

Completion requires each affected claim to use one document-local numbered grouped marker; every grouped `source:<id>` to resolve through document metadata; every cited passage to support the claim, qualifiers, chronology, certainty, status, and outcome; and unrelated ordinary footnotes to remain semantically distinct. Preserve source records and source metadata while changing only the affected attribution representation.

## Required decisions

### `interaction-evidence-policy`

A user decision is required when an active project privacy, retention, or provenance policy intentionally conflicts with alpha.16's required evidence capture, minimization, target references, or supersession behavior.

### `interaction-evidence-identity`

A user decision is required when an existing processed document declares `type: Interaction Evidence` or uses an exact alpha.16 evidence filename but was created for another project-defined meaning. Do not silently reinterpret, rename, or reclassify it.

### `project-task-owner`

A user decision is required when project-owned role or workflow authority intentionally overlaps the managed Project Task Manager and project context does not establish a compatible narrower boundary or explicit replacement intent.

### `claim-provenance-meaning`

A user decision is required when an existing precise claim citation cannot be mapped to supporting source passages without guessing its intended source, scope, or qualifiers.

## Semantic migration procedure

1. Do not edit managed files. Record every project-owned path inspected or changed in `upgrade.json.project_changes`; unchanged inspections use `inspected` and `retained`, while a later mutation replaces that classification.
2. Apply only the bounded discovery conditions above. Do not scan unrelated project content or create missing backlog scaffolds.
3. Reconcile active conversational-mutation instructions and exact existing evidence candidates with the interaction-evidence identity, shape, threshold, authority, privacy, atomicity, reverse-reference, and supersession contracts.
4. Reconcile task-management role and workflow overlap, execution boundaries, configured board location, and lifecycle semantics without changing task state unless required and authorized.
5. Convert only affected precise claim citations to numbered grouped references while preserving source support and unrelated footnotes.
6. Record each triggered unresolved decision and stop compatibility completion until the user resolves it.
7. Run deterministic structural validation separately from independent semantic review of every changed project-owned instruction or knowledge artifact.

## Validation and completion criteria

- every triggered conversational mutation policy is compatible with required interaction-evidence authority, privacy, atomicity, target-reference, and supersession behavior
- every exact existing interaction-evidence candidate is valid evidence or has an explicitly resolved project-defined identity collision; malformed intended evidence does not evade validation
- no active project-owned role or workflow creates ambiguous task-management routing or transfers substantive execution authority merely because a task record exists
- task operations follow the project-owned configured board and lifecycle, and upgrades do not create or normalize project task scaffolds
- every affected precise claim has one valid numbered grouped marker whose referenced source passages support its exact meaning and qualifiers
- every inspected or changed project-owned path is recorded exactly once with the final applicable classification
- all triggered required decisions are resolved
- deterministic validation passes and independent semantic review reports no unresolved interaction-evidence, privacy, task-routing, ownership, lifecycle, or claim-provenance finding

Only then may semantic compatibility advance to `1.0.0-alpha.16`.

## Rollback implications

Project-owned edits made for alpha.16 interaction evidence, task routing, or numbered claim provenance may not remain semantically compatible with alpha.15. Before rollback completes, re-evaluate those edits against alpha.15's managed contracts. Preserve valid project knowledge and evidence, but do not retain alpha.16-only authority or routing assumptions where they conflict with the restored managed base.
