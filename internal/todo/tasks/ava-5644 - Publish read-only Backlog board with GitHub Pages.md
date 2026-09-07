---
id: ava-5644
title: Publish read-only Backlog board with GitHub Pages
status: To Do
assignee: []
created_date: '2026-09-07 20:42'
labels:
  - internal
  - roadmap
  - backlog
  - github-pages
  - developer-experience
milestone: m-1
dependencies: []
references: []
type: enhancement
ordinal: 6643
---

## Description

Publish Ava's internal Backlog.md roadmap as a read-only GitHub Pages site so the current board can be inspected without cloning the repository or running the local Backlog.md browser.

The published view should be generated from the repository's canonical `internal/todo/` Backlog.md data during CI and deployed as static assets. It should reflect the current roadmap state on `main`, including active tasks, statuses, milestones, and other useful task metadata supported by the exported data.

This is intentionally a read-only convenience view. Do not add browser-side GitHub write credentials, direct task mutation, or a second roadmap source of truth. Repository Markdown remains canonical, and roadmap edits continue through the normal Backlog.md/Git workflow.

Prefer using Backlog.md's machine-readable output, such as `backlog task list --json`, as the source for a small static board renderer rather than attempting to host the local Backlog.md server directly on GitHub Pages.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A GitHub Pages deployment publishes a static, read-only view of Ava's canonical `internal/todo/` Backlog.md roadmap
- [ ] #2 The published board is regenerated from repository state on `main` and does not introduce a second manually maintained roadmap representation
- [ ] #3 The view exposes the useful current roadmap structure, including active tasks, statuses, milestones, and task details available from the Backlog.md data
- [ ] #4 The implementation requires no browser-side GitHub write credentials and does not support mutating roadmap files from the Pages site
- [ ] #5 The implementation uses a static export/rendering approach suitable for GitHub Pages rather than trying to host Backlog.md's local browser server directly
- [ ] #6 Documentation identifies the published board URL and keeps the normal Backlog.md/Git workflow authoritative for roadmap changes
<!-- AC:END -->
