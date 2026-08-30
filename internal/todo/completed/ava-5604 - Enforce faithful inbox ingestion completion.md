---
id: ava-5604
title: "Enforce faithful inbox ingestion completion"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5604
---

## Description

Prevent substantive omissions, unsupported certainty, incorrect attribution, and inaccurate completion reports before inbox sources are marked processed. This task preserves the finding rationale, dependency, completion criteria, and resolution evidence.

## Migrated task record

Historical metadata: phase 5 finding 4, classification `required-v1`, blocking release candidate, affected version `1.0.0-alpha.5`, completed after implementation.

### Observed behavior and evidence

A batch ingestion referenced every substantive daily note at file level but marked all sources processed despite material omissions, altered certainty, incorrect claim attribution, unresolved footnote markers, and inaccurate counts. The alpha.5 project had 46 dated processed sources, including 16 empty-body files. All 30 substantive sources appeared in destination `sources.resource` metadata and all 23 generated concepts had file-level metadata, but this did not prove faithful semantic ingestion.

Examples included substantive Airflow/Renovate, Snowflake access, and Kubernetes policy initiatives with no focused destination; an unconfirmed contributor rewritten as a cause; claims citing sources that did not contain them; unresolved source-id footnote markers; and a log reporting 47 sources/eight team concepts when the filesystem contained 46/seven.

### Classification and root cause

This was `required-v1`. Source preservation and broad provenance worked well enough for continued corrective-alpha work, but reliable ingestion could not reach RC while processed sources could omit or materially alter content. The role lacked an explicit multi-topic semantic completion procedure, per-section dispositions, epistemic preservation, final-state reconciliation, and a fully specified claim-level footnote representation.

### Dependency and approved scope

This work followed AVA-5603 hierarchy promotion. It required a substantive-section inventory, explicit `mapped`/`non-durable`/`pending` dispositions, preservation of uncertainty/authorship/source-versus-decision distinctions, renderable claim attribution tied to source metadata, support verification against the actual source, final inventory/count reconciliation, and realistic multi-source coverage without pretending semantic fidelity is reducible to deterministic validation.

### Completion criteria and release follow-up

Repository completion required accounting for every substantive section, regression coverage for long multi-topic and uncertainty/attribution/count cases, standard Markdown footnotes bound to matching `sources` identifiers and supporting passages, final-inventory reporting, executable role/workflow/provenance/count/semantic-review boundaries, and aligned task/history evidence. Published follow-up required representative corrective-release ingestion, semantic fidelity verification, count reconciliation, and isolated independent review. Those published checks remained release evidence rather than reopening the bounded task.

### Resolution evidence

Merged PR #67 implemented the change and it was published in `1.0.0-alpha.10`. `inbox-ingestion-fidelity.md` defines complete section inventories, explicit dispositions, epistemic preservation, and final-state reconciliation. Inbox Ingester loads it as required reading. `ingest-inbox.md` requires inventory before mutation, renderable provenance, source-state reconciliation, and final-inventory reporting. Change Reviewer uses the same fidelity contract while keeping semantic review separate from deterministic validation. Standard Markdown footnotes are bound to matching OKF `sources[].id`, preserved source paths, source-local passages, and actual certainty. `internal/release/fixtures/inbox-ingestion-fidelity.json` covers the observed failure shapes and `internal.release.tests.test_inbox_ingestion_fidelity` contains nine passing tests in the maintained release suite.

The historical note that Finding 07 was then the current blocker is preserved as context only; current work is selected from native Backlog state.