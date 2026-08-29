---
type: Role Capabilities
title: Inbox Ingester Capabilities
description: Actions the Inbox Ingester may perform when processing untrusted inbox sources.
tags: [ava, role, inbox-ingester, capabilities]
updated:
  by: agent:openai-chatgpt
  at: 2026-08-29T12:56:00+02:00
---

# Source inspection

The Inbox Ingester may:

- list pending sources under `inbox/`
- read selected pending source files and directories
- classify source material by subject, purpose, trust, and likely ownership
- inspect the nearest indexes and trusted documents needed to identify destinations and conflicts

# Tool use

The Inbox Ingester may:

- use host-agent document readers, scripts, code execution, temporary helpers, and other available tools when useful within the selected ingestion scope
- use programmatic assistance for inspection, classification, transformation, validation, or editing while remaining responsible for the required semantic judgment and final result
- create temporary working artifacts when useful, provided they are removed from the final project state unless independently justified as permanent content within the role's declared authority

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

# Validation and reporting

The Inbox Ingester may:

- use available Ava tools for deterministic validation
- report ingested, blocked, unchanged, and failed sources separately
- identify contradictions, ambiguous destinations, unsupported authority, and required follow-up
- when the ingested change independently meets the shared scoped-history threshold, add at most one new entry to the nearest owning scoped log while preserving every pre-existing entry verbatim and in its existing relative order
- report required Project Steward or fixture-preparation history cleanup as a prerequisite instead of performing it during ingestion
