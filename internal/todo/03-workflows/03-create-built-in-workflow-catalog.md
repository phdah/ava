---
type: Internal Development Task
title: Create the Initial Built-In Workflow Catalog
description: Create focused workflow files for the initial core-role procedures.
tags: [internal, roadmap, workflows, catalog]
status: completed
phase: 3
order: 3
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T13:01:48Z
---

# Create the Initial Built-In Workflow Catalog

## Completed outcome

The generated project template now includes ten registered stable workflows:

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

The catalog remains flat under `/templates/base/workflows/` and uses each workflow filename stem as its unambiguous shorthand invocation name.

The mutation workflows apply only changes already permitted by their primary roles. `daily-project-maintenance` uses `suggestion` mode so recurring maintenance cannot mutate a project automatically. The review workflows use `read-only` mode and keep remediation separate from evaluation.

Each workflow defines focused inputs, a bounded procedure, and a mode-consistent expected output without copying its primary role's durable instructions. `/templates/base/workflows/index.md` registers every workflow through direct-child discovery.

The catalog was checked for required metadata, title and filename alignment, ordered body sections, valid input declarations, supported modes, unique filename stems, one registered non-deprecated primary role per workflow, registry reachability, and broken links.

Scheduling and execution remain outside Ava's runtime and are deferred to [Define workflow trigger portability](04-define-workflow-trigger-portability.md).

## Completion criteria

- [x] create focused workflow files without copying role instructions
- [x] document inputs, mode, and expected output
- [x] ensure every workflow maps to one primary role
- [x] add registry entries and validation
- [x] keep scheduling and execution outside Ava's initial runtime
