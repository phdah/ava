---
id: ava-5635
title: Reduce footnote verbosity in inbox-ingestion claim provenance
status: Done
assignee: []
created_date: '2026-09-01 16:54'
labels:
  - internal
  - roadmap
  - inbox-ingestion
  - format
milestone: m-0
dependencies: []
references:
  - ava-5604
  - ava-5620
type: enhancement
ordinal: 6634
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Standard Markdown footnotes for claim-level source provenance, as defined in `templates/base/shared/instructions/inbox-ingestion-fidelity.md` ("Renderable claim provenance"), currently produce very bloated generated documents at scale. Two concrete problems, confirmed against a real generated document with roughly 60 daily sources:

1. **Marker-chain density.** A single sentence needing multiple supporting sources (common when sources are ingested per day) ends up with one `[^label]` marker per source stacked in a row, e.g. 30 markers on one sentence. The current rule requires "the footnote label must exactly equal one `sources[].id` value", so there is no lighter-weight way to attribute a claim to several sources at once.
2. **Definition duplication.** Every footnote definition repeats the `resource` path and `title` that already exist in the matching `sources[].id` frontmatter entry, so the same link/title data is written twice per source: once in frontmatter, once in the footnote definition.

There is no existing auto-linking/rendering component anywhere in the repository that already turns `sources[].id` references into clickable links (confirmed by search); Markdown footnotes are the sole linking mechanism today, so this is a genuine format problem to fix, not a redundant mechanism to remove.

## Decision (approved by user)

- Replace one-marker-per-source chains with a single grouped, numbered-style footnote marker per claim/sentence. The marker no longer needs to equal a single `sources[].id` literally; its definition instead groups every source that supports that claim.
- Footnote definitions no longer repeat `resource` or `title` (those stay in frontmatter `sources[]`); a definition keeps only the source-local detail needed for precise attribution (e.g. supporting heading/passage) together with enough of a reference to the underlying `sources[].id` value(s) that a deterministic check can still verify every marker traces to a real, resolvable source and that no marker is left unresolved.
- Every requirement AVA-5604 established must still hold: no bare/unresolved markers, no loss of per-source certainty/support, ability to tell exactly which source(s) back a claim, and one renderable footnote definition per used marker.

## Affected spec surface

- `templates/base/shared/instructions/inbox-ingestion-fidelity.md` ("Renderable claim provenance" section) - primary rule definition, needs a full rewrite with a new worked example.
- `templates/base/shared/instructions/document-metadata.md` (Provenance and trust section)
- `templates/base/shared/instructions/knowledge-organization.md`
- `templates/base/workflows/ingest-inbox.md`
- `templates/base/roles/inbox-ingester/instructions.md`
- `internal/release/qualification_inbox.py` (`validate_inbox_structural_fidelity`) - deterministic validator currently checks label-equals-id; must be rewritten for the grouped format.
- `internal/release/fixtures/inbox-ingestion-fidelity.json` and the `test_inbox_ingestion_fidelity` test suite.

## Out of scope

- Migrating already-generated project documents that use the old per-source named-footnote format.
- Changing which sources must be cited, or reducing evidentiary fidelity requirements established by AVA-5604 / AVA-5620.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 inbox-ingestion-fidelity.md's "Renderable claim provenance" rules define the new grouped-footnote format with at least one worked example, and no longer require a footnote label to equal a single sources[].id
- [x] #2 The new rules keep a deterministic way to trace every footnote marker's group back to real sources[].id values, with no bare or unresolved markers permitted
- [x] #3 Footnote definitions in the updated spec/examples omit resource and title text already present in the corresponding sources[] frontmatter entries, keeping only source-local attribution detail
- [x] #4 A single claim needing multiple supporting sources is represented with one grouped footnote marker instead of one marker per source in all updated spec examples and role/workflow instructions
- [x] #5 document-metadata.md, knowledge-organization.md, ingest-inbox.md, and inbox-ingester/instructions.md are updated so their footnote guidance is consistent with the new format with no stale references to the old label-equals-id rule
- [x] #6 internal/release/qualification_inbox.py's structural-fidelity validator enforces the new grouped format instead of the label-equals-id check, and still rejects unresolved or unsupported markers
- [x] #7 internal/release/fixtures/inbox-ingestion-fidelity.json and test_inbox_ingestion_fidelity cover both valid grouped-footnote documents and the previously-covered failure shapes translated to the new format, and the full test suite passes
- [x] #8 Completion evidence records how this public format-contract change was handled under the repository's existing release/semantic-impact procedure
<!-- AC:END -->

## Resolution evidence

Claim-level provenance now uses one positive-decimal Markdown footnote marker per claim. Each definition begins with `Sources:` and groups one or more backticked `source:<sources[].id>` references, each paired with source-local support detail. The corresponding `sources[]` frontmatter remains the canonical mapping for preserved-source `resource` paths and `title` values, so definitions no longer duplicate that navigation data.

`internal/release/qualification_inbox.py` resolves every grouped source reference through destination metadata, requires exactly one definition for each used marker, and rejects non-numbered markers, malformed groups, unknown or repeated source IDs, and source links repeated inside definitions. The validator deliberately continues to leave semantic support and certainty checks to independent review. Fixtures and release tests cover a valid two-source group plus unresolved markers, unknown references, old source-ID marker labels, missing source-local detail, repeated links, repeated source IDs, and the existing preservation failures.

The managed shared instructions, Inbox Ingester instructions, ingestion workflow, and root repository history are aligned with the new public format contract. This implementation does not migrate already-generated project documents, as explicitly scoped by the task.

Release handling remains release-edge specific. This PR records the managed contract delta but does not author or pre-decide an adjacent release record. Under `internal/release/procedure.md`, the eventual release-please PR must assess the exact previous-to-target managed delta and independently decide `semantic_review_required`, including whether any bounded project-owned reconciliation is required for that release edge.

Validation is provided by PR #118's required `Python tests` workflow, which runs `python3 internal/todo/validate.py` and the complete `internal/release/test.sh` suite for the pull-request revision.
