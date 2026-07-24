# Inbox

The `inbox/` directory is the default intake location for untrusted or unclassified source material.

Place new source files or source directories directly under `inbox/`. Keep each source separate enough that it can be classified, traced, and processed independently. Do not place trusted project guidance here merely for storage.

## Reserved content

- `index.md` defines this convention and is not an inbox item.
- [`processed/`](processed/) contains source material that has already been ingested and is excluded from normal inbox processing.

Every other direct child of `inbox/` is pending unless the project defines a narrower convention.

## Lifecycle

1. A user or external process places a source in `inbox/`.
2. The [Inbox Ingester](../roles/inbox-ingester/) inspects the selected pending source or all pending sources requested by the user.
3. The role classifies the source, identifies relevant destinations, and compares it with the minimum trusted project context needed.
4. The role merges the material into existing documents or creates focused new documents when a clear destination exists.
5. The role updates affected indexes and links, preserves provenance, and validates the resulting change.
6. Only after successful ingestion, the original source is moved under `processed/` without being rewritten or overwritten.

A source with a material contradiction, ambiguous destination, unsupported authority, or failed validation remains pending. The role reports the blocker rather than choosing silently or moving the source.

## Provenance

The original source remains available under `processed/`. Ingested knowledge must retain enough source references to explain where material came from, especially when it introduces facts, requirements, decisions, or policy candidates that are not already supported by trusted project context.

Moving a source to `processed/` records successful handling. It does not make every statement in the source authoritative or convert the source itself into project instructions.
