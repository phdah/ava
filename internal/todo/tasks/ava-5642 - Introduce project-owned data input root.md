---
id: ava-5642
title: Introduce project-owned data input root
status: To Do
assignee: []
created_date: '2026-09-07 10:26'
updated_date: '2026-09-07 11:14'
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

Ava should scaffold only the general-purpose data roots needed by the format itself. Fresh installation should create `data/index.md` and an empty `data/templates/` collection containing only `data/templates/index.md`. Domain-specific branches such as `personal/`, `running/`, `daily/`, or `garmin/` are project-owned examples and must not be pre-created by Ava.

`data/templates/` exists so users can keep reusable input-oriented templates alongside their data structure, including Obsidian templates or equivalent project-defined templates. Ava should define only the location and its preservation/discovery semantics, not prescribe an Obsidian-specific format, filename, frontmatter shape, or template taxonomy.

## Implementation reference

When implementing this task, inspect [`phdah/knowledge-vault` commit `2e30554d5fee9cf027887dafd00639d63cbc2a7e`](https://github.com/phdah/knowledge-vault/commit/2e30554d5fee9cf027887dafd00639d63cbc2a7e) as a concrete dogfood example of the intended data semantics and progressive directory structure.

That commit demonstrates a running-specific setup with `data/personal/running/daily/`, `data/personal/running/garmin/`, and `data/templates/`; direct-child `index.md` files; persistent source-shaped files; an Obsidian-style reusable note template; and durable knowledge derived separately without moving or deleting the underlying data. Use it as implementation inspiration only. The Ava feature must remain domain-neutral and must not encode running, personal-data, Garmin, Obsidian, or other application-specific structure into the distributed scaffold.

In particular, the reference repository contains a concrete `data/templates/template.md`, but Ava installation should not install that example template. It should create only `data/templates/index.md`, leaving the templates collection otherwise empty for project-owned use.

## Required behavior

1. Define the public semantics and ownership boundary for the project-owned `data/` root.
2. Add `data/` to the installed project layout and project scaffolding with safe create-if-absent behavior consistent with other project-owned roots.
3. Fresh installation must create `data/index.md` and `data/templates/index.md`, with `data/templates/` otherwise empty and no domain-specific data branches pre-created.
4. Define progressive discovery for `data/`, including an appropriate root index contract without imposing a general taxonomy on project data.
5. Define `data/templates/` as a project-owned location for reusable data-adjacent templates, including Obsidian templates, without making Ava depend on Obsidian or prescribing template contents.
6. Update shared routing and maintenance guidance so roles can distinguish `data/`, `knowledge/`, and `inbox/` correctly.
7. Ensure Project Steward knowledge curation does not automatically canonicalize, consolidate, move, or rewrite material merely because it exists under `data/`.
8. Allow project-owned roles to explicitly load relevant `data/` paths as task or role context while preserving the rule against broad default scanning.
9. Preserve existing project-owned `data/` content, including templates, byte-for-byte across installation and upgrades unless the user explicitly requests a project-context mutation.
10. Update distribution documentation, templates, validation, fixtures, and tests needed to make the new root a supported Ava 1.1 capability.
11. Review SemVer impact and keep the implementation backward-compatible for the `1.1.0` milestone. If the required design would instead break Ava's stable format contract and require `2.0.0`, stop and return the scope for milestone re-evaluation rather than implementing the breaking design under `m-1`.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `data/` is defined as project-owned trusted input context distinct from both `inbox/` and canonical `knowledge/`
- [ ] #2 Fresh installation creates `data/index.md` and an otherwise-empty `data/templates/` containing only `data/templates/index.md`
- [ ] #3 No personal, running, Garmin, Obsidian, or other domain-specific data structure or template content is installed by default
- [ ] #4 Installation and upgrades preserve existing project-owned `data/` content, including templates
- [ ] #5 Roles can explicitly discover and consume relevant data without a default full-directory scan
- [ ] #6 Project Steward and related maintenance instructions preserve source-shaped `data/` content unless an explicit user request authorizes mutation
- [ ] #7 Public layout, ownership, routing, and knowledge/input documentation consistently describe the new root and templates collection
- [ ] #8 Validation and qualification coverage exercises projects with existing and newly scaffolded `data/` content
- [ ] #9 Implementation explicitly reviews the referenced `knowledge-vault` commit as dogfood context while generalizing its running-specific structure into Ava-wide semantics
- [ ] #10 The completed design remains backward-compatible and suitable for the `v1.1.0` milestone, or implementation stops for explicit major-version re-evaluation
<!-- AC:END -->
