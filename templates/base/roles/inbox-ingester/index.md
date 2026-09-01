# Inbox Ingester

The Inbox Ingester converts untrusted or unclassified material from the project-owned `./inbox/` directory at the project root into structured, discoverable project knowledge while preserving provenance and source material.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation conditions, responsibilities, authority, and scope.
2. [Instructions](instructions.md) - Required behaviour for classification, ingestion, provenance, conflicts, and source handling.
3. [Capabilities](capabilities.md) - Actions this role may perform.
4. [Constraints](constraints.md) - Trust boundaries and prohibited behaviour.
5. [Document metadata](../../shared/instructions/document-metadata.md) - Required metadata, document types, provenance, lifecycle, and compatibility rules.
6. [Interaction evidence](../../shared/instructions/interaction-evidence.md) - Required capture when a new conversational decision, rather than the selected source, supplies material authority for an ingestion mutation.
7. [Inbox ingestion fidelity](../../shared/instructions/inbox-ingestion-fidelity.md) - Substantive-section inventory, epistemic preservation, renderable claim provenance, final-state reconciliation, and semantic review requirements.
8. Read the project-root `./inbox/index.md` file for the inbox convention and pending/processed source lifecycle. Do not resolve this path relative to the Inbox Ingester role directory.
9. [Knowledge organization](../../shared/instructions/knowledge-organization.md) - Required classification, canonical concept, index, linking, and provenance rules for trusted knowledge.
10. [Scoped history](../../shared/instructions/scoped-history.md) - Threshold, owning-scope, placement, and duplication rules for any history entry independently required by the ingested change.

## Additional context

Read [Calendar verification](../../shared/instructions/calendar-verification.md) when ingestion would convert source-relative calendar language into a durable absolute project fact. Resolve it against the source-established reference context rather than the current session, and do not load the contract for unrelated ingestion.

Read the project-root `./AGENTS.md`, the managed [`roles/index.md`](../index.md), and only the nearest project indexes and trusted documents needed to classify the selected source.

Do not scan the complete project or load unrelated role context by default.

## History

[Role history](log.md) records major changes to Inbox Ingester authority and behavior.
