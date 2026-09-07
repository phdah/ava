---
id: ava-5642
title: Introduce project-owned data input root
status: To Do
assignee: []
created_date: '2026-09-07 10:26'
labels:
  - internal
  - roadmap
  - data
  - context
  - distribution
milestone: m-1
dependencies: []
references: []
type: enhancement
ordinal: 6641
---

## Description

Introduce `data/` as a first-class project-owned Ava context root for trusted input material that should remain source-shaped rather than being canonicalized into `knowledge/`.

The feature should establish a clear three-way distinction:

- `inbox/` contains untrusted or unclassified source material awaiting ingestion.
- `data/` contains trusted project-owned input material that roles may consume directly while preserving its project-defined organization and source shape.
- `knowledge/` contains canonical, durable concepts maintained under Ava's knowledge-organization contract.

Typical `data/` content may include append-only daily observations, machine-generated files, structured exports, JSON, tables, logs, or other project-owned inputs whose value depends on retaining their original organization. Roles may reference relevant data explicitly, but the existence of `data/` must not cause unrelated roles to scan it by default.

## Required behavior

1. Define the public semantics and ownership boundary for the project-owned `data/` root.
2. Add `data/` to the installed project layout and project scaffolding with safe create-if-absent behavior consistent with other project-owned roots.
3. Define progressive discovery for `data/`, including an appropriate root index contract without imposing a general taxonomy on project data.
4. Update shared routing and maintenance guidance so roles can distinguish `data/`, `knowledge/`, and `inbox/` correctly.
5. Ensure Project Steward knowledge curation does not automatically canonicalize, consolidate, move, or rewrite material merely because it exists under `data/`.
6. Allow project-owned roles to explicitly load relevant `data/` paths as task or role context while preserving the rule against broad default scanning.
7. Preserve existing project-owned `data/` content byte-for-byte across installation and upgrades unless the user explicitly requests a project-context mutation.
8. Update distribution documentation, templates, validation, fixtures, and tests needed to make the new root a supported Ava 1.1 capability.
9. Review SemVer impact and keep the implementation backward-compatible for the `1.1.0` milestone. If the required design would instead break Ava's stable format contract and require `2.0.0`, stop and return the scope for milestone re-evaluation rather than implementing the breaking design under `m-1`.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `data/` is defined as project-owned trusted input context distinct from both `inbox/` and canonical `knowledge/`
- [ ] #2 Fresh installation/scaffolding supports the `data/` root without overwriting existing project content
- [ ] #3 Installation and upgrades preserve existing project-owned `data/` content
- [ ] #4 Roles can explicitly discover and consume relevant data without a default full-directory scan
- [ ] #5 Project Steward and related maintenance instructions preserve source-shaped `data/` content unless an explicit user request authorizes mutation
- [ ] #6 Public layout, ownership, routing, and knowledge/input documentation consistently describe the new root
- [ ] #7 Validation and qualification coverage exercises projects with existing and newly scaffolded `data/` content
- [ ] #8 The completed design remains backward-compatible and suitable for the `v1.1.0` milestone, or implementation stops for explicit major-version re-evaluation
<!-- AC:END -->
