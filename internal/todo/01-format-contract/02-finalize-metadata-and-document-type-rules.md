---
type: Internal Development Task
title: Finalize Metadata and Document-Type Rules
description: Define required metadata, document types, deprecation, and compatibility behavior.
tags: [internal, roadmap, format, metadata]
status: complete
phase: 1
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T14:41:00Z
---

# Finalize Metadata and Document-Type Rules

## Approved decisions

- Ava targets Open Knowledge Format version 0.2.
- `index.md` and `log.md` are the only reserved documents exempt from normal concept frontmatter.
- Every other Markdown document requires a non-empty `type`.
- Ava-controlled semantic documents also require `title` and `description`.
- Document types remain open and descriptive rather than using a closed Ava enum.
- Role routing remains semantic and prose-based without keywords, priorities, or a routing rule language.
- Every workflow requires one bundle-root-relative `primary_role` reference.
- Workflow inputs, outputs, operating mode, and triggers remain structured Markdown until the workflow-format task defines further machine metadata.
- OKF `sources`, `generated`, `verified`, `status`, and `stale_after` metadata are used directly.
- Ava adds only `primary_role` and `replaced_by` as current format extensions.
- Unknown fields and project-defined types remain valid and must survive round-tripping.
- The bundle root controls OKF compatibility through `okf_version`; documents do not carry individual schema versions.
- Ava-specific metadata remains flat. OKF-standard nested metadata remains valid and editable in Obsidian source mode.

## Authoritative contract

The generated-project contract is documented in [Document metadata](/templates/base/shared/instructions/document-metadata.md).

The contract defines:

- required and optional metadata
- reserved documents
- open document types and Ava-controlled semantic types
- role-routing behavior
- workflow metadata
- provenance, generation, and verification
- lifecycle and replacement behavior
- forward compatibility
- validation errors, warnings, and notices
- Obsidian compatibility
- valid and invalid examples

## Applied integration

- updated the repository and initialized-project bundle roots to OKF 0.2
- added the metadata contract to generated shared instructions
- required every current document-mutating role to load the contract
- aligned role generation, project stewardship, inbox ingestion, and knowledge organization behavior
- updated source provenance to use OKF `sources` metadata while retaining useful Markdown links
- recorded the conceptual change in the repository log

## Completion

- defined equivalent schema and validation rules
- documented required versus optional fields
- added valid and invalid examples
- defined forward-compatible handling of unknown fields and project-defined types
- indexed and linked the authoritative contract
- validated the affected required-reading paths and metadata examples
