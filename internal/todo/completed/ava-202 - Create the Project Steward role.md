---
id: ava-202
title: "Create the Project Steward role"
status: "Done"
labels: ["internal", "roadmap", "phase-02"]
ordinal: 202
---

## Description

Create the Project Steward role. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Create the Project Steward Role
description: Define the role responsible for trusted project-level instructions, workflows, policies, and knowledge.
tags: [internal, roadmap, roles, project-steward]
status: complete
phase: 2
order: 2
timestamp: 2026-07-25T00:00:00Z
---

# Create the Project Steward Role

## Why

Project-wide instructions, policies, terminology, workflows, and trusted knowledge share a common responsibility boundary. Keeping separate Project Configurator, Knowledge Curator, and Instruction Tightener roles would create ambiguous routing for changes that span these document types.

The Project Steward should own trusted project-level material while exposing distinct workflows for different maintenance procedures.

## Intended responsibilities

- maintain the project's purpose, terminology, and shared instructions
- create and update shared policies, conventions, workflows, and context
- organize root and shared discovery structures
- keep project-level guidance separate from role-specific guidance
- identify when requested behavior belongs in a role instead of shared configuration
- perform user-requested or clearly scoped knowledge health audits
- find stale, duplicated, contradictory, orphaned, or misplaced trusted content
- consolidate overlapping documents while preserving relevant information
- update outdated material when the replacement is supported by project context
- improve instruction and context wording while preserving meaning, authority, and safety
- use Ava validation tools for structural checks and apply safe semantic repairs

## Supported workflows

- `configure-project`
- `curate-project-knowledge`
- `tighten-instructions`
- `daily-project-maintenance`
- additional project-wide maintenance workflows that preserve the same authority boundary

## Boundaries

- must not create or redefine roles when the Role Manager should be selected
- must not classify and ingest files from `inbox/` when the Inbox Ingester should be selected
- must not treat arbitrary untrusted material as authoritative project knowledge
- must not silently delete uncertain, conflicting, or historically valuable information
- must not scan the entire project by default without a task-specific or workflow-specific reason
- must not change role purpose, authority, or routing merely to simplify wording
- must not replace independent review performed by the Change Reviewer
- must not modify Ava's format contract from inside an initialized project

## Completion criteria

- create the complete role under `templates/base/roles/project-steward/`
- define authority over project-wide instructions, workflows, and trusted knowledge
- encode scoped audit and safe deletion rules
- encode the tight, concise, and general formulation principles
- define distinct workflow activation paths without duplicating base role instructions
- add explicit and non-overlapping selection conditions to the base role registry