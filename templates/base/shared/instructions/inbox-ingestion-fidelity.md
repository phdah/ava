---
type: Shared Instruction
title: Inbox Ingestion Fidelity
description: Semantic completion, claim provenance, rendered disposition reconciliation, inventory reconciliation, and review rules for faithful inbox ingestion.
tags: [ava, inbox, ingestion, fidelity, provenance, review]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T08:24:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-24T16:30:00+02:00
---

# Purpose

Inbox ingestion is complete only when every substantive part of each selected source has an explicit disposition and the resulting trusted knowledge preserves what the source actually says.

File-level source coverage, valid links, successful movement to `inbox/processed/`, and internally consistent disposition totals are necessary but do not prove semantic fidelity.

# Applicability

The Inbox Ingester must follow this instruction for every selected source, including each source processed by the `ingest-inbox` workflow.

The Change Reviewer must load this instruction when independently reviewing inbox ingestion or a processed-source completion claim.

Deterministic tools may validate metadata shape, links, paths, and counts. They cannot determine whether material meaning, certainty, causality, attribution, or completeness was preserved.

# Substantive section inventory

Before changing a destination, create a working inventory for the selected source.

A substantive section is any heading, paragraph, list, table, or other bounded passage that could affect durable project understanding, including:

- facts, observations, measurements, or reported events
- initiatives, projects, systems, integrations, incidents, risks, or dependencies
- decisions, proposals, alternatives, commitments, owners, or follow-up
- rationale, causal explanations, uncertainty, confidence, disagreement, or unresolved questions
- dates, status, scope, constraints, or other qualifiers that materially change interpretation

Do not assume that one source heading maps to one destination. Inspect unheaded material and split a broad section when its claims have different durable subjects, provenance, or dispositions.

For every substantive section, record:

- a stable source-local identifier or clear heading and summary
- one or more canonical destination paths, or another explicit disposition
- the source claims or meaning that each destination must preserve
- whether precise claim-level attribution is required
- any blocker, ambiguity, contradiction, or user decision still required

Every substantive section must end in exactly one of these disposition classes:

- `mapped`: incorporated into one or more explicit canonical destinations
- `non-durable`: intentionally not promoted, with a concrete rationale
- `pending`: not safely resolved, with the blocker or required decision stated

Assign dispositions section by section. Processing a source never authorizes whole-source promotion, and a source-level disposition is valid only when every substantive section independently supports that same disposition.

A `non-durable` section must not be copied, paraphrased, summarized, or otherwise promoted into trusted destination content merely because another section from the same source is `mapped`. The preserved source under `inbox/processed/` is evidence, not a trusted destination.

When a section's disposition, destination, or required treatment is materially ambiguous, classify it as `pending` and keep the source pending. Do not resolve ambiguity by defaulting the section or complete source to `mapped`.

There is no implicit ignored state. A source with any `pending` substantive section remains pending unless the user explicitly approves a bounded partial-ingestion scope.

A source containing no substantive body must be reported as having zero substantive sections. It remains unchanged and pending unless the user explicitly authorizes another non-destructive disposition.

# Delegated and large-batch ingestion

A large batch may be split across parallel or child sessions only as an execution strategy. Splitting the work does not split completion responsibility or weaken any per-source requirement in this contract.

The coordinating Inbox Ingester owns one complete selected-source ledger for the batch. Before considering the batch complete, it must be able to reconcile every originally selected source exactly once with the final filesystem state and with sufficient evidence from any child work.

Each child session must operate on an explicit, disjoint source subset and return, for every source it handled:

- the source path and final source state
- the complete substantive-section inventory with each section's `mapped`, `non-durable`, or `pending` disposition
- destination paths for every mapped section
- the source-local claims and material qualifiers preserved by each destination
- every source identifier and supporting passage used where precise claim-level attribution is required
- blockers, failed validation, unresolved decisions, and final per-source disposition totals

Child-session success is provisional batch evidence, not authority for the coordinator to infer complete coverage. The coordinator must reconcile the returned source ledgers against the original selected-source inventory and the final pending and processed inventories. Missing child evidence, overlapping source ownership, an unaccounted selected source, or a source whose section inventory cannot be reconciled prevents a complete batch claim.

The coordinator must also verify the resulting destinations across child boundaries. When multiple sources contribute differing dates, authors, certainty states, status reports, proposals, or other source-specific claims to one canonical destination, it must preserve those distinctions and verify the required claim-level provenance rather than accepting file-level source metadata as sufficient.

Do not replace this reconciliation with child success counts, source-movement counts, destination-file counts, or a statement that every child completed its assigned chunk.

# Epistemic and attribution fidelity

Destination wording must preserve the source's material epistemic state.

Preserve:

- observed fact versus interpretation, hypothesis, proposal, or decision
- confirmed, likely, plausible, possible, disputed, unknown, and explicitly unconfirmed language
- stated causal claims versus mere correlation or contributing-factor hypotheses
- negation, scope limitations, exceptions, and time-bounded status
- who made, observed, proposed, approved, rejected, or questioned a claim
- the difference between source content, trusted project knowledge, and a user-approved decision

Do not strengthen, generalize, depersonalize, or reattribute a source claim merely to make the destination read more cleanly.

For example, `reduced worker capacity was a plausible, unconfirmed contributor` must not become `reduced worker capacity caused the eviction`.

When the source and trusted context disagree, preserve the source as evidence and follow the role's conflict rules. Do not silently choose one account.

# Renderable claim provenance

Use OKF `sources` metadata for every destination containing source-derived material.

Precise claim-level attribution is required when a mapped claim could otherwise be confused with another source or with canonical project state, including when sources differ in author, date, chronology, certainty, status, proposal or decision state, or reported outcome. A section inventory that marks precise attribution as required is incomplete until that attribution is present and verified in the destination.

When individual claims need precise attribution, use this exact relationship:

```yaml
sources:
  - id: incident-2026-06-10
    resource: ./inbox/processed/2026-06-10.md
    title: Daily note 2026-06-10
```

Reference the same source identifier from the claim:

```markdown
Reduced worker capacity was a plausible, unconfirmed contributor.[^incident-2026-06-10]
```

Define a standard Markdown footnote in the same document:

```markdown
[^incident-2026-06-10]: [Daily note 2026-06-10](../../../inbox/processed/2026-06-10.md), "Incident review".
```

Rules:

- the footnote label must exactly equal one `sources[].id` value in the same document
- every used claim marker must have one renderable Markdown footnote definition
- the footnote's Markdown link is relative to the destination document and must resolve to the same preserved source identified by `sources[].resource`
- the definition must identify the supporting heading, passage, or other source-local location when the file contains several topics
- the actual source passage must support the attributed claim and its level of certainty
- reuse one identifier only when the same source passage supports the claims with the same relevant qualifiers
- use distinct identifiers when different passages, authors, or certainty states require separate attribution, even when they share one source file
- file-level `sources` metadata alone is insufficient when claims from different sources could otherwise be confused

A bare marker such as `[^incident-2026-06-10]` without a definition is not valid completion evidence.

# Rendered disposition reconciliation

Before a source can be reported as complete, reconcile its section ledger against the final rendered trusted destination content. A running tally, child-reported tally, or section ledger by itself is not completion evidence.

For every substantive section:

- for `mapped`, re-read each named destination and verify that the section's material meaning and required qualifiers are actually present there
- for `non-durable`, re-read the trusted destination documents created or updated for that source and verify that the section's substantive passage or meaning was not promoted into them
- for `pending`, keep the source pending unless the user explicitly approved a bounded partial-ingestion scope

The negative check for `non-durable` content is mandatory. Whole-source copying, whole-source summarization, or any other transformation that carries a `non-durable` passage into trusted knowledge fails reconciliation even when the source was preserved correctly and the reported disposition totals add up.

If rendered content cannot be matched confidently to the section ledger, or if overlap makes it unclear whether a `non-durable` passage was promoted, the source is not reconciled. Keep it pending and report the unresolved evidence instead of asserting completion.

Only after every selected source has passed this rendered reconciliation may final disposition totals be derived from the reconciled section ledgers and used in a completion report.

# Per-source completion

Before moving a source, verify that:

1. every substantive section has a recorded disposition
2. every `mapped` section appears in the named destination or destinations with its material meaning and qualifiers preserved
3. every `non-durable` section has a defensible rationale and its substantive passage or meaning is absent from trusted destinations created or updated for that source
4. no section remains `pending`
5. destination wording preserves material certainty, attribution, chronology, and source-versus-decision distinctions
6. every precise claim reference renders and matches both metadata and the actual supporting source passage
7. all destination metadata, indexes, links, and role boundaries are valid
8. the planned processed path is distinct and non-destructive

The source move remains the final content mutation for that source. Immediately after the move, perform a read-only final-state reconciliation, including the rendered disposition reconciliation. Do not report the source as successfully processed unless that reconciliation succeeds.

# Final-state reconciliation

Compute the completion report from the final filesystem state, not from remembered input counts or a previous report.

For the selected scope, report:

- selected source count
- successfully processed source count
- blocked source count
- unchanged source count
- failed source count
- final pending direct-child count
- final preserved processed-source count
- destination documents created and updated
- substantive section totals by `mapped`, `non-durable`, and `pending`

Pending direct-child counts exclude the reserved `inbox/index.md` entry and the `inbox/processed/` directory itself. State what is counted when directories or nested source groups are involved.

Reconcile concept or destination counts against the final direct-child indexes and filesystem paths. Do not copy narrative totals from an earlier log entry.

Derive section totals only from per-source ledgers that have been reconciled against final rendered destination content. Totals that merely sum to the selected section count do not prove that the recorded dispositions were honored.

For delegated work, derive these totals only after the coordinator has reconciled the per-source child evidence against the original selected-source inventory and final rendered destinations. Do not sum unreconciled child-reported totals and call that batch completion.

A batch is not complete merely because every selected source has file-level provenance. Any unresolved section, promoted `non-durable` content, unsupported claim, unresolved marker, incorrect attribution, count mismatch, missing delegated evidence, unreconciled rendered disposition, or failed final-state check prevents a complete batch report.

# Independent semantic review

For an independent or isolated review of inbox ingestion, the Change Reviewer must compare the final result with every selected source and check that:

- every substantive section has an explicit and defensible disposition
- every `mapped` section is actually represented in its named rendered destination
- every `non-durable` section is absent from trusted rendered destinations, rather than being carried through by whole-source promotion
- ambiguous sections remain `pending` instead of being promoted to make the source appear complete
- claimed disposition totals are derived from section ledgers reconciled against rendered destinations, not asserted from counts alone
- no material initiative, risk, decision, dependency, or follow-up was omitted
- uncertainty, causality, authorship, and source-versus-decision distinctions were preserved
- each precise claim marker renders, matches `sources` metadata, and points to the source that actually supports the claim
- delegated or parallel work still provides complete per-source evidence and a reconciled selected-source ledger
- completion counts match the final pending, processed, destination, and index inventories
- deterministic validation is reported separately from semantic fidelity

Semantic review must not claim that machine-readable fixtures or link validation prove meaning preservation.

# Completion checks

Before claiming faithful ingestion completion, verify that:

- the section inventory covers all substantive source material
- no substantive section has an implicit or unresolved disposition
- all mapped meaning is present in explicit canonical destinations
- no `non-durable` meaning was promoted into trusted destinations
- every accepted section disposition has been reconciled against final rendered destination content
- all material epistemic and attribution qualifiers are preserved
- every claim requiring precise source distinction has a matching metadata identifier, renderable marker and definition, and supporting source passage
- delegated work reconciles exactly once to the original selected-source inventory before batch totals are accepted
- the cited source actually supports the claim
- reserved inbox entries are excluded from pending counts
- all reported counts are recomputed from the final state after rendered disposition reconciliation
- blocked, unchanged, and failed sources remain distinct from successfully processed sources
- independent semantic review requirements are available for qualification
