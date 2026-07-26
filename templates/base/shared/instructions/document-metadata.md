---
type: Shared Instruction
title: Document Metadata
description: Required metadata, document types, routing references, provenance, lifecycle, validation, and compatibility rules.
tags: [ava, metadata, okf, documents, compatibility]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T22:20:00Z
---

# Purpose

Ava projects follow Open Knowledge Format version 0.2 and add only the metadata needed for deterministic Ava behaviour.

Keep metadata open and extensible. Agents should make the best semantic classification available from the project context instead of forcing every document into a closed Ava taxonomy.

# Conformance layers

Ava distinguishes two validation layers.

## OKF conformance

A non-reserved Markdown document is OKF-conformant when:

- it begins with valid YAML frontmatter
- its frontmatter contains a non-empty `type`
- its metadata values use valid YAML shapes

Unknown fields and project-defined document types do not invalidate the document.

## Ava validity

An OKF-conformant project is Ava-valid when its Ava-controlled structures are also coherent, including:

- mandatory initialized paths and reserved files exist
- known Ava semantic documents contain their required fields
- role required-reading paths resolve
- workflows reference exactly one registered primary role
- known Ava metadata fields have valid values and shapes

A document may remain a valid generic OKF concept even when Ava does not assign special behaviour to its type.

# Reserved documents

`index.md` and `log.md` are reserved OKF documents and do not require normal concept frontmatter.

The bundle-root `index.md` must declare the OKF version:

```yaml
---
okf_version: "0.2"
---
```

Other Ava filenames, including `AGENTS.md`, `role.md`, `instructions.md`, `capabilities.md`, and `constraints.md`, are ordinary concept documents and require normal frontmatter.

# Required metadata

Every non-reserved Markdown document requires:

```yaml
---
type: <descriptive type>
---
```

Ava-controlled semantic documents also require `title` and `description`:

```yaml
---
type: Agent Role
title: Project Steward
description: Maintains trusted project guidance, workflows, and knowledge.
---
```

The following types are Ava-controlled semantic types:

- `Agent Router`
- `Agent Role`
- `Role Instructions`
- `Role Capabilities`
- `Role Constraints`
- `Shared Instruction`
- `Workflow`

Project knowledge may use any descriptive type that accurately represents the concept, such as `Person`, `Project`, `Decision`, `Agreement`, `Training Block`, or `Data Pipeline`.

Do not introduce a generic `Knowledge Concept` type when a more meaningful classification is available.

# Optional standard metadata

Documents may use OKF metadata where relevant:

- `title`: human-readable title
- `description`: concise purpose or identity
- `tags`: YAML list of search and classification terms
- `resource`: external or canonical resource identifier
- `status`: lifecycle state
- `sources`: provenance sources
- `generated`: generation actor and time
- `verified`: verification actors and times
- `stale_after`: time after which the content should be reviewed

Use ISO 8601 dates and timestamps.

New or meaningfully modified documents should use:

```yaml
generated:
  by: agent:<identifier>
  at: 2026-07-26T14:41:00Z
```

Existing `timestamp` fields are legacy metadata. Preserve them until the document is meaningfully modified, then replace them with `generated` metadata.

# Role routing

Role routing remains semantic and prose-based.

Do not add keyword lists, regular expressions, numeric priorities, confidence thresholds, or a routing rule language to role metadata.

The root router reads `roles/index.md`, compares the request with each role's stated purpose and activation conditions, and selects the best match. A role's directory path is its stable identity, so a separate `role_id` is not required.

# Workflow metadata

Every workflow requires:

```yaml
---
type: Workflow
title: Configure project
description: Establishes or clarifies project-wide purpose and shared guidance.
primary_role: /roles/project-steward/role.md
status: stable
---
```

Rules:

- `primary_role` is required.
- It must be a bundle-root-relative path to exactly one registered role document.
- The workflow file path is the workflow identity.
- Inputs, operating mode, expected output, and trigger information remain in structured Markdown until a later workflow task defines a machine schema.
- A workflow must not duplicate the primary role's durable instructions.

# Provenance and trust

Use OKF `sources` metadata for material derived from preserved source content:

```yaml
sources:
  - id: original-notes
    resource: /inbox/processed/project-notes.md
    title: Original project notes
    author: human:project-owner
```

Use the source `id` with Markdown footnotes when individual claims require precise attribution.

Use `generated` to identify the actor and time that produced the current document version. Use `verified` only after an actor has actually verified the content:

```yaml
verified:
  - by: human:project-owner
    at: 2026-07-26T15:00:00Z
```

Missing `verified` metadata means unverified, not invalid.

Preserve original source files through the inbox lifecycle. A processed source remains evidence and does not become authoritative merely because it has been processed.

# Lifecycle and replacement

Valid lifecycle states are:

- `draft`
- `stable`
- `deprecated`

Missing `status` means `stable`.

A deprecated document remains valid for history and existing links. When a direct replacement exists, include the Ava extension:

```yaml
status: deprecated
replaced_by: /roles/project-steward/role.md
```

`replaced_by` must be a bundle-root-relative path. Explain the deprecation rationale in the document body and record major lifecycle changes in the nearest relevant `log.md`.

Do not add `deprecated_at`, removal versions, or nested Ava lifecycle structures until a migration task requires them.

# Forward compatibility

Ava producers and editors must preserve unknown frontmatter fields and unknown valid YAML structures when rewriting a document.

Unknown project-defined types and fields must not block normal OKF conformance. Strict diagnostic tooling may report them as non-blocking notices, but must not remove or rewrite them without an explicit rule.

Do not add a document-level schema version. The bundle-root `okf_version` controls OKF compatibility. Ava may add one project-level `ava_version` later when it publishes a separate compatibility contract.

# Validation rules

Treat these as errors:

- missing or invalid frontmatter on a non-reserved Markdown document
- missing or empty `type`
- malformed known OKF or Ava fields
- missing mandatory initialized paths or reserved files
- broken required-reading paths
- missing `title` or `description` on an Ava-controlled semantic document
- workflow `primary_role` missing, malformed, unresolved, or referencing more than one role

Treat these as warnings or non-blocking notices:

- references to deprecated concepts
- content past `stale_after`
- broken optional contextual links
- missing optional indexes outside mandatory initialized structure
- unknown fields or project-defined types reported by strict diagnostic tooling

# Obsidian compatibility

Use UTF-8 Markdown, YAML frontmatter, standard Markdown links, lowercase kebab-case filenames, and ISO dates and timestamps.

Keep Ava-specific metadata flat. OKF-standard nested metadata such as `sources`, `generated`, and `verified` remains allowed and authoritative even when Obsidian's Properties interface cannot edit every nested value. The files must remain readable and editable in Obsidian source mode.

# Valid examples

## Project-defined knowledge type

```yaml
---
type: Data Pipeline
title: Customer event ingestion
description: Canonical description of the customer event ingestion pipeline.
tags: [data, ingestion]
---
```

This is valid because project-defined descriptive types are open.

## Deprecated role with replacement

```yaml
---
type: Agent Role
title: Legacy Curator
description: Deprecated role retained for existing links.
status: deprecated
replaced_by: /roles/project-steward/role.md
---
```

## Source-backed knowledge

```yaml
---
type: Decision
title: Retain processed inbox sources
description: Project decision to preserve original source material after ingestion.
sources:
  - id: ingestion-notes
    resource: /inbox/processed/ingestion-notes.md
generated:
  by: agent:project-steward
  at: 2026-07-26T14:41:00Z
---
```

# Invalid examples

## Missing type

```yaml
---
title: Unclassified document
---
```

Invalid because every non-reserved Markdown document requires `type`.

## Workflow without one resolvable role

```yaml
---
type: Workflow
title: Configure project
description: Configures the project.
primary_role:
  - /roles/project-steward/role.md
  - /roles/role-manager/role.md
---
```

Invalid because a workflow must reference exactly one primary role.

## Closed-taxonomy rejection

A validator must not reject this only because the type is not known to Ava:

```yaml
---
type: Renovation Plan
title: Kitchen renovation
description: Canonical plan for the kitchen renovation.
---
```

Rejecting it would violate Ava's open document-type model.
