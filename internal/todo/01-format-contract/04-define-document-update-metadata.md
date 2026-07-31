---
type: Internal Development Task
title: Define Document Update Metadata
description: Define how meaningful document mutations record the latest update actor and time without replacing creation provenance.
tags: [internal, roadmap, format, metadata, provenance, updates]
status: pending
phase: 1
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T11:34:00+02:00
---

# Define Document Update Metadata

## Why

Ava documents can record their creation provenance through `generated.by` and `generated.at`, but the current metadata contract does not define equivalent provenance for later mutations.

Git history remains authoritative for the complete change history, but readers and agents should be able to identify when a document was last meaningfully updated and which actor made that update without replacing or misusing the original `generated` metadata.

## Define

- the canonical metadata name and shape for the latest meaningful update, including actor and timestamp
- whether the field is an OKF-standard field or an Ava extension
- whether the structure should mirror `generated`, for example `updated.by` and `updated.at`
- whether only the latest update is recorded or whether any bounded update history belongs in frontmatter
- which mutations require updating the metadata
- which changes are too trivial to count, such as formatting-only edits, mechanical link repair, or metadata normalization
- whether agent-authored, human-authored, migration-authored, and deterministic-tool mutations use the same actor identifier rules
- how mutation metadata interacts with `verified`, `sources`, lifecycle status, scoped `log.md`, and Git history
- how unknown existing update fields are preserved and reconciled
- whether legacy `timestamp` fields participate in creation or update migration
- how reserved `index.md` and `log.md` files, and the root `README.md`, represent update provenance when they intentionally omit normal concept frontmatter

## Behavioral requirements

- preserve `generated` as creation provenance when a document is mutated
- do not rewrite `generated.at` to represent the latest edit
- require document-mutating roles and workflows to maintain update metadata when the defined mutation threshold is met
- keep timestamp and actor formatting consistent with the existing provenance contract
- avoid frontmatter churn for changes that do not materially update document content or meaning
- preserve unknown fields and valid existing provenance during rewrites
- keep Git history as the complete audit trail rather than duplicating unbounded history in every document

## Apply

- update the authoritative document metadata contract
- update every role, workflow, or shared instruction that defines document mutation behavior
- add valid and invalid examples
- define validation errors, warnings, or notices for malformed, missing, stale, or inconsistent update metadata
- decide whether current repository and template documents require a migration or only adopt the rule on future meaningful mutation
- add fixtures for creation, meaningful mutation, trivial mutation, repeated mutation, legacy metadata, and reserved-document behavior

## Completion criteria

- creation provenance and latest-update provenance have distinct documented meanings
- the canonical metadata schema and actor format are explicit
- the mutation threshold is deterministic enough for agents and validation tooling to apply consistently
- document-mutating roles preserve creation metadata and maintain update metadata correctly
- reserved-document behavior is explicit
- existing valid metadata survives round-tripping
- validation and examples cover required, optional, malformed, and migration cases
- the metadata contract, affected role instructions, roadmap, indexes, and conceptual documentation remain aligned
