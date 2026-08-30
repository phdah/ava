---
id: ava-104
title: "Define document update metadata"
status: "Done"
labels: ["internal", "roadmap", "phase-01"]
ordinal: 104
---

## Description

Define meaningful document-update metadata and provenance. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Define Document Update Metadata
description: Define how meaningful document mutations record the latest update actor and time without replacing creation provenance.
tags: [internal, roadmap, format, metadata, provenance, updates]
status: completed
phase: 1
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T11:34:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-03T21:29:00+02:00
---

# Define Document Update Metadata

## Decision

Ava uses the optional `updated` metadata extension for the latest meaningful mutation:

```yaml
updated:
  by: agent:project-steward
  at: 2026-08-03T10:00:00+02:00
```

- `generated` records creation provenance and is preserved during later mutations.
- `updated` records only the latest meaningful mutation after creation.
- Frontmatter does not retain an update history. Git remains the complete audit trail.
- A meaningful mutation changes how a reasonable reader or agent should understand, route, trust, maintain, or act on a document.
- Formatting, whitespace, meaning-preserving wording, stable-identity link repair, serialization normalization, and similar trivial edits do not advance `updated`.
- Mixed edits are meaningful when any part changes semantics, authority, trust, identity, classification, discovery, or behaviour.
- `generated.by`, `updated.by`, and `verified[].by` use `<kind>:<stable-identifier>` with `human`, `agent`, or `tool` kinds.
- Deterministic migrations use a `tool:` actor. Semantic migrations use the active agent identity.
- Whole-document verification older than the latest meaningful update is stale.
- `sources`, lifecycle fields, scoped logs, and ownership retain their independent meanings.
- Existing documents adopt the rule on their next meaningful mutation rather than through a bulk metadata migration.
- Legacy `timestamp` and unknown update-like fields are preserved unless an explicit rule establishes their meaning.
- Reserved `index.md` and `log.md` files and the root `README.md` do not gain frontmatter solely for edit provenance.

## Authoritative contract

[Document metadata](/templates/base/shared/instructions/document-metadata.md) now defines:

- the canonical schema and actor format
- creation versus update provenance
- the meaningful-mutation threshold
- interactions with verification, sources, lifecycle, scoped history, ownership, and Git
- legacy and unknown metadata handling
- reserved-document behaviour
- errors, warnings, and notices with stable rule identifiers
- valid and invalid examples

[Ownership and mutation authority](/templates/base/shared/instructions/ownership-and-mutation.md) requires every permitted mutation to preserve creation provenance and maintain latest meaningful-update provenance.

All current document-mutating managed roles already load the authoritative document metadata contract through their required-reading indexes. Mutation workflows inherit the same requirement through their primary role and resolved shared instructions.

## Validation and fixtures

Added [machine-readable fixtures](/internal/release/fixtures/document-update-metadata.json) and Python coverage for:

- document creation
- first meaningful mutation
- trivial mutation
- repeated meaningful mutation
- legacy `timestamp`
- reserved documents
- malformed `updated`
- regressive timestamps
- stale verification

Stable update-metadata diagnostics are reserved under `AVA-META-*` identifiers for the full conformance validator.

## Migration

No bulk repository or installed-project migration is required. Existing valid metadata remains valid and unknown fields survive round-tripping. A document receives or advances `updated` when it is next meaningfully mutated under the new contract.

## Completion

- [x] creation and latest-update provenance have distinct meanings
- [x] the canonical schema and actor format are explicit
- [x] the meaningful-mutation threshold is defined
- [x] document-mutating roles and workflows resolve the authoritative rule
- [x] reserved-document behaviour is explicit
- [x] existing valid and unknown metadata is preserved
- [x] validation severity and stable rule identifiers are defined
- [x] valid, invalid, migration, repetition, and reserved-document fixtures are covered
- [x] roadmap, indexes, conceptual history, and release-test discovery are aligned