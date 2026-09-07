---
id: ava-5643
title: Do not index inbox lifecycle contents
status: To Do
assignee: []
created_date: '2026-09-07 15:12'
labels:
  - internal
  - roadmap
  - inbox
  - documentation
milestone: m-1
dependencies: []
references: []
type: enhancement
ordinal: 6642
---

## Description

Add a very small instruction clarifying that `inbox/` lifecycle contents are not maintained as navigational source indexes.

The existing root `inbox/index.md` may remain as the static inbox convention entry point, but it must not enumerate pending or processed sources. Do not create or maintain an `inbox/processed/index.md` source catalog.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Distributed inbox-ingestion instructions explicitly say not to create or maintain source indexes for `inbox/` or `inbox/processed/`
- [ ] #2 The existing root `inbox/index.md` remains a static convention document rather than a per-source catalog
- [ ] #3 The change stays narrowly scoped to this instruction and any directly necessary validation or qualification coverage
<!-- AC:END -->
