---
type: Internal Development Task
title: Define Project and Discovery Tools
description: Define semantic operations for project inspection, role and workflow resolution, and context discovery.
tags: [internal, roadmap, mcp, discovery]
status: pending
phase: 5
order: 2
timestamp: 2026-07-25T00:00:00Z
---

# Define Project and Discovery Tools

## Candidate semantic operations

```text
initialize_project
inspect_project
validate_project
list_roles
resolve_role
get_role_bundle
list_workflows
resolve_workflow
get_workflow_bundle
discover_context
```

Avoid adding generic `list_files` merely because a provider supports listing. Expose it only when it is necessary as a public interoperability operation.
