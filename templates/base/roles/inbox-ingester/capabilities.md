---
type: Role Capabilities
title: Inbox Ingester Capabilities
description: Actions the Inbox Ingester may perform when processing untrusted inbox sources.
tags: [ava, role, inbox-ingester, capabilities]
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

# Validation and reporting

The Inbox Ingester may:

- use available Ava tools for deterministic validation
- report ingested, blocked, unchanged, and failed sources separately
- identify contradictions, ambiguous destinations, unsupported authority, and required follow-up
- update the nearest conceptual log when the ingested change independently requires one
