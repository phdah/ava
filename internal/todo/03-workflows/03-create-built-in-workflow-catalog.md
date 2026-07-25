---
type: Internal Development Task
title: Create the Initial Built-In Workflow Catalog
description: Create focused workflow files for the initial core-role procedures.
tags: [internal, roadmap, workflows, catalog]
status: pending
phase: 3
order: 3
timestamp: 2026-07-25T00:00:00Z
---

# Create the Initial Built-In Workflow Catalog

## Initial candidates

```text
create-role                 -> role-manager
update-role                 -> role-manager
repair-role                 -> role-manager
configure-project           -> project-steward
curate-project-knowledge    -> project-steward
tighten-instructions        -> project-steward
daily-project-maintenance   -> project-steward
ingest-inbox                -> inbox-ingester
review-change               -> change-reviewer
review-role-change          -> change-reviewer
```

## Completion criteria

- create focused workflow files without copying role instructions
- document inputs, mode, and expected output
- ensure every workflow maps to one primary role
- add registry entries and validation
- keep scheduling and execution outside Ava's initial runtime
