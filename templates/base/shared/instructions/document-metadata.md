---
type: Shared Instruction
title: Document Metadata
description: Required metadata, document types, routing references, provenance, lifecycle, validation, ownership, and compatibility rules.
tags: [ava, metadata, okf, documents, compatibility, ownership]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-01T18:58:00+02:00
---

# Purpose

Ava projects follow Open Knowledge Format version 0.2 and add only the metadata needed for deterministic Ava behaviour.

Keep metadata open and extensible. Agents should make the best semantic classification available from the project context instead of forcing every document into a closed Ava taxonomy.

Installed ownership and path authority follow [Ownership and mutation authority](ownership-and-mutation.md). Ava release versions, semantic compatibility, and deprecation timelines follow Ava's public versioning contract; release-specific actions are supplied through installed guidance. Document metadata must not be used to silently transfer ownership between Ava and the project.

All metadata paths beginning with `./` are resolved from the project root. A leading slash denotes an operating-system absolute path and is invalid for project-local metadata.

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

- the managed root `./AGENTS.md` and `./.ava/` state are valid for the installed version
- the managed base index at `./.ava/base/index.md` exists and declares the OKF version
- managed files agree with `./.ava/state/manifest.json`
- project-owned extension paths are not claimed by the managed manifest
- known Ava semantic documents contain their required fields
- role required-reading paths resolve
- workflows are registered and reference exactly one registered, non-deprecated primary role
- known Ava metadata fields have valid values and shapes

A document may remain a valid generic OKF concept even when Ava does not assign special behaviour to its type.

# Reserved documents

`index.md` and `log.md` are reserved OKF documents and do not require normal concept frontmatter.

The Ava-managed base index at `./.ava/base/index.md` must declare the OKF version:

```yaml
---
okf_version: "0.2"
---
```

A project-root `./index.md` is project-owned when present. It may also declare `okf_version`, but it is not the installed Ava version record and must not be added to the managed manifest merely because it resembles an Ava scaffold.

The repository root `README.md` is human-facing documentation and intentionally omits normal concept frontmatter.

Reserved `index.md` and `log.md` files and the root `README.md` do not add `generated` or `updated` solely to represent edit provenance. Git records their complete edit history. Dated log entries record qualifying conceptual history according to [Scoped history](scoped-history.md).

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
- `generated`: creation actor and time
- `verified`: verification actors and times
- `stale_after`: time after which the content should be reviewed

Ava additionally defines the optional `updated` field for latest meaningful-update provenance.

Use ISO 8601 dates and timestamps with an explicit offset when a time is recorded.

# Actor identifiers

`generated.by`, `updated.by`, and `verified[].by` use the same actor identifier format:

```text
<kind>:<stable-identifier>
```

Supported kinds are:

- `human` for a person or human-owned identity
- `agent` for an AI agent identity or durable role identity
- `tool` for deterministic software

Identifiers use lowercase letters, digits, dots, underscores, hyphens, and slash-separated stable sub-identifiers. Examples:

```yaml
generated:
  by: human:project-owner
  at: 2026-08-01T09:00:00+02:00

updated:
  by: agent:project-steward
  at: 2026-08-03T10:00:00+02:00

updated:
  by: tool:ava-migration/1.0.0-to-1.1.0
  at: 2026-08-03T10:00:00+02:00
```

A deterministic migration uses `tool:<identifier>` rather than inventing a separate actor kind. An agent applying semantic migration guidance uses its `agent:<identifier>` identity.

Do not invent a human, agent, or tool identity that cannot be established from the active context.

# Creation provenance

`generated` records who originally created the canonical document and when. It does not describe the latest edit and must not be rewritten during later mutations.

A newly created non-reserved document produced by an Ava role, workflow, or deterministic Ava tool must include:

```yaml
generated:
  by: agent:<identifier>
  at: 2026-08-03T10:00:00+02:00
```

Existing documents without `generated` remain valid when creation provenance is unknown. Later editors must not fabricate creation provenance merely to fill the field.

# Latest meaningful update provenance

`updated` is an Ava metadata extension. It records only the actor and time of the latest meaningful mutation after document creation:

```yaml
updated:
  by: agent:<identifier>
  at: 2026-08-03T10:00:00+02:00
```

Rules:

- omit `updated` when the document is first created because `generated` already identifies that event
- preserve `generated` exactly during later mutations
- add `updated` on the first meaningful mutation
- replace the previous `updated` value on each later meaningful mutation
- do not store an update array or bounded update history in frontmatter
- do not change `updated` for a trivial mutation
- do not let `updated.at` precede `generated.at` or regress from a previous `updated.at`
- when clock resolution produces the same timestamp, the complete `updated` value must still identify the actual latest actor and must not remain stale

Git remains the complete audit trail. Scoped logs record only qualifying conceptual or structural history and do not duplicate every `updated` event.

# Meaningful mutation threshold

A mutation is meaningful when it changes how a reasonable reader or agent should understand, route, trust, maintain, or act on the document.

Update `updated` when a change does any of the following:

- adds, removes, or replaces substantive content
- changes a factual claim, project decision, policy, requirement, instruction, permission, capability, constraint, or safeguard
- changes purpose, scope, authority, ownership meaning, routing, activation, operating mode, procedure, expected output, required input, or required context
- changes canonical identity, classification, lifecycle status, replacement relationship, deprecation timing, or compatibility meaning
- changes material source attribution, verification meaning, or the evidence supporting a claim
- changes links, indexes, filenames, or structure in a way that changes discovery, identity, or interpretation
- resolves a material contradiction or semantic defect

A mutation is trivial when it provably preserves content meaning, authority, trust, identity, classification, discovery, and behaviour. Examples include:

- whitespace or wrapping changes
- formatting-only Markdown changes
- spelling, grammar, or style corrections that preserve meaning
- mechanical link repair where the referenced canonical identity is unchanged
- metadata key ordering or serialization normalization
- line-ending or encoding normalization
- index synchronization that only reflects an already represented child and does not change discovery semantics

When a mixed edit contains any meaningful change, treat the complete document mutation as meaningful and update `updated` once.

# Interaction with other metadata

## Verification

`updated` does not imply verification.

`verified` describes verification of the current document content. A meaningful mutation invalidates any whole-document verification whose timestamp precedes `updated.at`. Remove stale verification entries or replace them only after actual re-verification.

Missing `verified` metadata means unverified, not invalid.

## Sources

Preserve valid `sources` entries during mutation. Add, update, or remove a source only when the material evidence or source-derived claims change. `updated` does not replace source provenance.

## Lifecycle

Changes to `status`, `replaced_by`, `deprecated_since`, or `removal_not_before` are meaningful and require `updated`.

## Scoped history

An `updated` change does not automatically require a `log.md` entry. Use the stricter conceptual and structural threshold in [Scoped history](scoped-history.md).

# Legacy and unknown update fields

`timestamp` is legacy and semantically ambiguous. Preserve it during trivial edits.

On a meaningful mutation:

- do not reinterpret `timestamp` as creation or update provenance without evidence
- add or maintain canonical `updated` for the current mutation
- convert `timestamp` to `generated.at` only when the project can establish that it represented creation time and can also establish the original actor
- otherwise preserve `timestamp` and report a non-blocking migration warning until a user or authoritative migration rule resolves it

Unknown fields such as `modified`, `last_updated`, or project-specific update structures remain forward-compatible metadata. Preserve them. Do not automatically map, delete, or normalize them into `updated` without an explicit project or release rule. A validator may report a notice that a likely alias exists alongside or instead of canonical `updated`.

Existing repository and template documents are not bulk-migrated. They adopt this rule on their next meaningful mutation. A meaningful mutation to an existing non-reserved document must preserve known creation provenance and add or advance canonical `updated`.

# Ownership metadata boundary

Ownership is determined by installed path, manifest record, installing or adopting authority, and the accepted adoption transaction.

Do not infer ownership from:

- document `type`
- `generated`, `updated`, or `verified` timestamps
- filename
- similarity to a default document
- repository history
- whether the file existed before installation

A local edit to an Ava-managed file does not make it project-owned. It creates a managed-file conflict. Project-specific changes belong in project-owned extension paths.

# Role routing

Role routing remains semantic and prose-based for free-form requests.

Do not add keyword lists, regular expressions, numeric priorities, confidence thresholds, or a routing rule language to role metadata.

The root router reads the managed role registry at `./.ava/base/roles/index.md` and the project-owned role registry at `./roles/index.md` when present. It compares a free-form request with each registered role's stated purpose and activation conditions and selects the best match.

A role's canonical project-root-relative path is its stable identity, so a separate `role_id` is not required. Managed default roles use paths under `./.ava/base/roles/`; project roles use paths under `./roles/`.

Explicit workflow invocation bypasses free-form role selection and resolves the workflow's declared `primary_role` according to [Workflow registry and routing](workflow-routing.md).

# Workflow metadata

Every workflow requires:

```yaml
---
type: Workflow
title: Configure project
description: Establishes or clarifies project-wide purpose and shared guidance.
primary_role: ./.ava/base/roles/project-steward/role.md
mode: mutation
status: stable
---
```

Rules:

- `primary_role` is required.
- It must be an explicit project-root-relative path to exactly one registered, non-deprecated `role.md` document.
- It may reference a managed role under `./.ava/base/roles/` or a project-owned role under `./roles/`.
- `mode` is required and must be `read-only`, `suggestion`, or `mutation`.
- The workflow file path is the workflow identity.
- A managed workflow must be reachable through `./.ava/base/workflows/index.md`.
- A project-owned workflow must be reachable through `./workflows/index.md`.
- A workflow must not duplicate the primary role's durable instructions.
- A deprecated workflow may declare `replaced_by`, but the router must report rather than automatically invoke the replacement.
- The complete body structure, input representation, mode semantics, expected output, context links, composition boundaries, and validation rules are defined by [Workflow format](workflow-format.md).
- Registry discovery, invocation identity, routing precedence, primary-role resolution, failure handling, and deprecation are defined by [Workflow registry and routing](workflow-routing.md).

Canonical path invocation remains unambiguous across ownership classes. A name that matches more than one registered role or workflow must be reported as ambiguous rather than resolved by managed or project-owned precedence.

# Provenance and trust

Use OKF `sources` metadata for material derived from preserved source content:

```yaml
sources:
  - id: original-notes
    resource: ./inbox/processed/project-notes.md
    title: Original project notes
    author: human:project-owner
```

When individual claims require precise attribution, put one numbered Markdown footnote marker on the claim. Define that marker with one or more backticked `source:<sources[].id>` references plus source-local support detail. Keep source `resource` paths and `title` values canonical in `sources` metadata rather than repeating them in the footnote definition.

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
replaced_by: ./roles/project-steward/role.md
```

`replaced_by` must be an explicit project-root-relative canonical path. Explain the deprecation rationale in the document body and record major lifecycle changes in the nearest relevant `log.md`.

A replacement reference does not itself activate or authorize the replacement. In particular, workflow and role routing must not automatically follow `replaced_by`; the caller must explicitly select the replacement and the router must resolve it normally.

Ava-managed public documents, roles, and workflows that are deprecated by a release must also declare:

```yaml
status: deprecated
deprecated_since: 1.4.0
removal_not_before: 2.0.0
replaced_by: ./.ava/base/roles/project-steward/role.md
```

Rules:

- `deprecated_since` is the first stable Ava version that declared the deprecation.
- `removal_not_before` is the earliest stable MAJOR version in which removal is permitted.
- Both fields use canonical SemVer without build metadata.
- `removal_not_before` must be later than `deprecated_since` and must have a greater MAJOR component.
- `replaced_by` remains optional when no direct replacement exists.
- Release notes and upgrade guidance must explain migration impact and removal timing.
- Removal or behavior-changing replacement requires the SemVer classification defined by the versioning and compatibility contract.

A deprecated metadata field cannot declare frontmatter. Its authoritative contract, release notes, and upgrade guidance must instead record its deprecation version, earliest removal version, replacement when present, and migration impact.

Project-owned concepts may use these fields when their lifecycle is intentionally tied to an Ava release. They are not required to invent an Ava removal version for ordinary project-specific deprecation.

# Forward compatibility

Ava producers and editors must preserve unknown frontmatter fields and unknown valid YAML structures when rewriting a document.

Unknown project-defined types and fields must not block normal OKF conformance. Strict diagnostic tooling may report them as non-blocking notices, but must not remove or rewrite them without an explicit rule.

Do not add a document-level schema version. The managed base `okf_version` controls OKF compatibility. The installed Ava distribution version belongs in `./.ava/state/manifest.json`; it must not be duplicated as document metadata or conflated with semantic compatibility of project-owned context.

# Validation rules

Stable update-metadata rule identifiers are defined here for future conformance tooling and fixtures.

Treat these as errors:

- `AVA-META-UPDATE-SHAPE`: `updated` is not a mapping with exactly one non-empty `by` actor and one valid ISO 8601 `at` timestamp
- `AVA-META-UPDATE-ACTOR`: a known provenance actor does not follow the supported actor identifier format
- `AVA-META-UPDATE-BEFORE-CREATION`: `updated.at` precedes `generated.at`
- `AVA-META-UPDATE-REGRESSION`: a changed document moves `updated.at` backwards from its previous value
- `AVA-META-UPDATE-STALE`: a change-aware validator identifies a meaningful mutation but canonical `updated` was not added or advanced
- `AVA-META-GENERATED-REWRITTEN`: a mutation rewrites established creation provenance without an explicit correction decision
- `AVA-META-VERIFICATION-STALE`: a `verified` entry predates the latest meaningful update and still claims verification of the current document
- missing or invalid frontmatter on a non-reserved Markdown document
- missing or empty `type`
- malformed known OKF or Ava fields
- missing managed bootstrap, base, state, or other mandatory installed paths
- a managed path missing from the manifest
- a managed payload missing its checksum or differing from its recorded checksum
- a managed state entry containing a payload checksum or violating its schema or allowed transitions
- a project-owned extension path claimed by the managed manifest
- broken required-reading paths
- missing `title` or `description` on an Ava-controlled semantic document
- a workflow omitted from the correct managed or project-owned registry
- workflow `primary_role` missing, malformed, unresolved, unregistered, deprecated, or referencing more than one role
- workflow `mode` missing or unsupported
- workflow body structure or semantics that violate the workflow-format contract
- invalid or automatically followed workflow or role `replaced_by` routing
- malformed, regressive, or inconsistent `deprecated_since` or `removal_not_before` metadata
- ambiguous name-based routing across managed and project-owned registries

Treat these as warnings:

- `AVA-META-UPDATE-LEGACY-TIMESTAMP`: a meaningful mutation retains an unresolved legacy `timestamp`
- `AVA-META-UPDATE-TRIVIAL-CHURN`: a change-aware validator finds that `updated` changed but the document diff is trivial only
- references to deprecated concepts
- invocation of a draft workflow
- multiple registered workflows sharing a filename stem when not invoked by that stem
- content past `stale_after`
- broken optional contextual links
- missing optional project-owned indexes

Treat these as non-blocking notices:

- `AVA-META-UPDATE-ALIAS`: an unknown likely update alias such as `modified` or `last_updated` is preserved
- unknown fields or project-defined types reported by strict diagnostic tooling

Static validation can validate field shape and temporal consistency. `AVA-META-UPDATE-STALE`, `AVA-META-GENERATED-REWRITTEN`, and `AVA-META-UPDATE-TRIVIAL-CHURN` require a previous document state or diff-aware validation.

# Obsidian compatibility

Use UTF-8 Markdown, YAML frontmatter, standard Markdown links, lowercase kebab-case filenames, and ISO dates and timestamps.

Keep Ava-specific metadata flat. OKF-standard nested metadata such as `sources`, `generated`, and `verified`, plus the Ava `updated` structure, remain allowed and authoritative even when Obsidian's Properties interface cannot edit every nested value. The files must remain readable and editable in Obsidian source mode.

# Valid examples

## New document

```yaml
---
type: Decision
title: Retain processed inbox sources
description: Canonical decision to preserve source material after ingestion.
generated:
  by: agent:project-steward
  at: 2026-08-01T09:00:00+02:00
---
```

## Meaningfully updated document

```yaml
---
type: Decision
title: Retain processed inbox sources
description: Canonical decision to preserve source material after ingestion.
generated:
  by: human:project-owner
  at: 2026-08-01T09:00:00+02:00
updated:
  by: agent:project-steward
  at: 2026-08-03T10:00:00+02:00
---
```

## Project-defined knowledge type

```yaml
---
type: Data Pipeline
title: Customer event ingestion
description: Canonical description of the customer event ingestion pipeline.
tags: [data, ingestion]
---
```

## Managed workflow using a default role

```yaml
---
type: Workflow
title: Configure project
description: Configures the project.
primary_role: ./.ava/base/roles/project-steward/role.md
mode: mutation
---
```

## Source-backed knowledge

```yaml
---
type: Decision
title: Retain processed inbox sources
description: Canonical decision to preserve source material after ingestion.
sources:
  - id: ingestion-notes
    resource: ./inbox/processed/ingestion-notes.md
generated:
  by: agent:project-steward
  at: 2026-08-01T09:00:00+02:00
updated:
  by: agent:inbox-ingester
  at: 2026-08-03T10:00:00+02:00
---
```

# Invalid examples

## Latest edit overwrites creation provenance

```yaml
---
type: Decision
generated:
  by: agent:project-steward
  at: 2026-08-03T10:00:00+02:00
---
```

This is invalid when the document was originally created earlier by another actor. Preserve the original `generated` and use `updated` for the latest meaningful mutation.

## Malformed updated value

```yaml
---
type: Decision
updated: 2026-08-03
---
```

## Update before creation

```yaml
---
type: Decision
generated:
  by: human:project-owner
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:project-steward
  at: 2026-08-02T10:00:00+02:00
---
```

## Stale verification

```yaml
---
type: Decision
updated:
  by: agent:project-steward
  at: 2026-08-03T10:00:00+02:00
verified:
  - by: human:project-owner
    at: 2026-08-02T10:00:00+02:00
---
```

## Ownership inferred from metadata

A file is not Ava-managed merely because its metadata resembles a default role or because `generated.by` or `updated.by` names Ava. Only the installed ownership contract and manifest establish managed authority.
