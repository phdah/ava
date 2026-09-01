---
type: Role Capabilities
title: Inbox Ingester Capabilities
description: Actions the Inbox Ingester may perform when processing untrusted inbox sources.
tags: [ava, role, inbox-ingester, capabilities]
updated:
  by: agent:openai-chatgpt
  at: 2026-08-31T08:19:00+02:00
---

# Source inspection

The Inbox Ingester may:

- list pending sources under `inbox/`
- read selected pending source files and directories
- classify source material by subject, purpose, trust, and likely ownership
- inspect the nearest indexes and trusted documents needed to identify destinations and conflicts

# Knowledge ingestion

The Inbox Ingester may:

- merge supported material into an existing authoritative document
- create focused project knowledge documents when no suitable destination exists
- create directories needed for a clear destination
- update affected indexes and links
- add provenance links or equivalent project-supported source references
- preserve distinctions between source claims, trusted context, and user-approved decisions

# Source lifecycle

The Inbox Ingester may:

- leave blocked or ambiguous sources pending
- move successfully ingested sources to `inbox/processed/`
- preserve source directory structure where practical
- choose a non-destructive distinct destination when a processed path already exists
- create a minimal processed interaction evidence record when a new conversational decision materially supplies authority for the current ingestion mutation, following the shared interaction-evidence contract

# Validation and reporting

The Inbox Ingester may:

- use available Ava tools for deterministic validation
- report ingested, blocked, unchanged, and failed sources separately
- identify contradictions, ambiguous destinations, unsupported authority, and required follow-up
- when the ingested change independently meets the shared scoped-history threshold, add at most one new entry to the nearest owning scoped log while preserving every pre-existing entry verbatim and in its existing relative order
- report required Project Steward or fixture-preparation history cleanup as a prerequisite instead of performing it during ingestion
