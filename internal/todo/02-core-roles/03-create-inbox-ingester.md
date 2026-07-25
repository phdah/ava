---
type: Internal Development Task
title: Create the Inbox Ingester Role and Inbox Convention
description: Define safe ingestion of untrusted or unclassified material from an initialized project's inbox.
tags: [internal, roadmap, roles, inbox]
status: pending
phase: 2
order: 3
timestamp: 2026-07-25T00:00:00Z
---

# Create the Inbox Ingester Role and Inbox Convention

## Why

Users need a low-friction place to drop untrusted or unclassified material without first understanding the project's final hierarchy. The Inbox Ingester turns that material into structured, discoverable project knowledge while preserving provenance and avoiding silent information loss.

Use `inbox/` as the default intake directory. The name describes the user's interaction with the directory and does not imply that ingestion has already occurred.

## Intended responsibilities

- inspect files placed in `inbox/`
- classify each source and determine its relevant project destinations
- merge information into existing documents where appropriate
- create focused new documents and directories where no suitable destination exists
- update affected indexes and links
- preserve enough source and provenance information to explain where ingested knowledge came from
- mark or move an inbox item only after successful processing
- support workflows such as `ingest-inbox` and `ingest-selected-source`

## Boundaries

- must treat inbox content as untrusted input rather than instructions that automatically override existing policy
- must not silently delete source material or discard conflicting information
- must surface material contradictions and ambiguous destinations
- must not become a general cleaner for the existing project
- must not require scanning unrelated directories when indexes or targeted discovery are sufficient

## Completion criteria

- decide and document the initialized project's `inbox/` structure and lifecycle
- create the complete role under `templates/base/roles/inbox-ingester/`
- add distinct routing conditions to the base role registry
- define provenance, conflict, and post-ingestion handling rules
- update the base template indexes and documentation affected by the inbox convention
