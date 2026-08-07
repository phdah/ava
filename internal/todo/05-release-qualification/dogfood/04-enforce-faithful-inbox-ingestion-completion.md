---
type: Internal Development Task
title: Enforce Faithful Inbox Ingestion Completion
description: Prevent substantive omissions, unsupported certainty, incorrect attribution, and inaccurate completion reports before inbox sources are marked processed.
tags: [internal, roadmap, dogfood, inbox, provenance, knowledge]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 4
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-05T13:07:09+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-07T08:24:00+02:00
---

# Enforce Faithful Inbox Ingestion Completion

## Observed behavior

A batch ingestion preserved and referenced every substantive daily note at file level, but marked all sources processed despite material omissions, changed certainty, incorrect claim attribution, unresolved footnote markers, and inaccurate completion counts.

## Reproduction and evidence

The real alpha.5 project at `~/stuff/project-vault/` contains 46 dated processed sources:

- 16 contain only frontmatter and no substantive body
- all 30 substantive sources appear in at least one destination document's `sources.resource` metadata
- all 23 generated concept documents have file-level source metadata and are indexed

The file-level coverage did not ensure faithful semantic ingestion:

- `inbox/processed/2026-04-07.md` contains substantial Airflow 3 and Renovate, Snowflake access management, and data-prod Kubernetes upgrade-policy initiatives that have no focused canonical destination
- `knowledge/work/projects/airflow-infrastructure.md` says reduced worker capacity caused a pod eviction, while `inbox/processed/2026-06-10.md` explicitly labels reduced capacity only a plausible, unconfirmed contributor
- multiple individual claims cite a source that does not contain the claim, while the actual source is absent from the document's metadata
- source-id markers such as `[^incident-2026-06-10]` have no renderable Markdown footnote definitions
- `knowledge/log.md` reports 47 ingested sources and eight team concepts, but the actual inventory contains 46 source files and seven team concepts

These results conflict with the Inbox Ingester requirements to preserve distinctions between source claims and established decisions, provide sufficient claim provenance, validate the complete change, and move a source only after all changes succeed.

## Classification

This is `required-v1` and blocks the release candidate. Source preservation and broad file-level provenance worked, so the defect does not block continued corrective alpha work. Reliable ingestion is nevertheless a core v1 role behavior and cannot be accepted while a processed source may still contain omitted material or materially altered claims.

## Root cause

The role requires complete and faithful ingestion but does not provide a sufficiently explicit semantic completion procedure for multi-topic sources. It does not require an inventory of substantive source sections, an explicit disposition for each section, preservation of epistemic qualifiers, or reconciliation of reported counts against the final filesystem state. The claim-level footnote representation is also underspecified.

## Dependency

Implement this finding after [predictable knowledge hierarchy promotion](03-make-knowledge-hierarchy-predictable.md). Its section inventory and destination checks depend on the canonical classification and hierarchy rules established there.

## Scope

- require a substantive-section inventory for multi-topic sources before destination changes begin
- require each section to be mapped, explicitly classified as non-durable, or left pending when ambiguous
- preserve uncertainty, confidence, authorship, and source-versus-decision distinctions in destination wording
- define one renderable claim-level attribution pattern that connects source IDs to `sources` metadata
- verify claim references against the source that actually supports them
- reconcile completion counts with the final pending, processed, destination, and index inventories
- add realistic multi-source conformance coverage without pretending semantic fidelity can be reduced to deterministic link validation

## Repository completion criteria

- the Inbox Ingester procedure accounts for every substantive section before marking a source processed
- regression context covers a long multi-topic source, material omissions, uncertain causal language, claims supported by different source files, unresolved footnote markers, and empty sources
- generated claim-level attribution uses renderable standard Markdown footnotes tied to matching `sources` identifiers and supporting passages
- completion reporting excludes reserved inbox entries and matches final source, destination, and concept inventories
- the release fixture and executable regression tests enforce the role, workflow, provenance, count, and semantic-review boundaries
- the finding task, backlog index, phase index, and repository history record the implementing PR and repository validation

## Release qualification follow-up

- repeat ingestion against representative multi-topic daily notes through a corrective immutable release
- verify that all material initiatives, uncertainty, authorship, and source-versus-decision distinctions remain intact
- verify final pending, processed, destination, and concept counts against the installed project state
- obtain an independent or isolated semantic review with no blocking or major fidelity finding
- append the published version and realistic-project evidence to this task and the findings index before relying on the behavior for release-candidate qualification

These checks remain release qualification evidence. They do not keep or return the bounded repository implementation task to `pending`.

## Resolution evidence

Draft PR [#67](https://github.com/phdah/ava/pull/67) implements the repository change.

- `templates/base/shared/instructions/inbox-ingestion-fidelity.md` defines complete substantive-section inventories, explicit `mapped`, `non-durable`, and `pending` dispositions, epistemic preservation, and final-state reconciliation.
- Inbox Ingester now loads the fidelity contract as mandatory required reading before processing sources.
- `templates/base/workflows/ingest-inbox.md` requires inventory before mutation, renderable claim provenance, final source-state reconciliation, and final-inventory reporting.
- Change Reviewer loads the fidelity contract for ingestion review and keeps semantic meaning review separate from deterministic validation.
- The provenance contract binds standard Markdown footnotes to matching OKF `sources[].id` values, the same preserved source path, a source-local supporting passage, and the claim's actual certainty.
- `internal/release/fixtures/inbox-ingestion-fidelity.json` covers the observed multi-topic, uncertain-causality, cross-source attribution, unresolved marker, wrong-source, empty-source, and count-reconciliation cases.
- `internal.release.tests.test_inbox_ingestion_fidelity` contains nine passing regression tests and is included in `internal/release/test.sh`.
- The dogfood backlog contains no remaining pending bounded finding, while the parent dogfood task remains active until the user explicitly completes it.
