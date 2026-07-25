---
type: Internal Development Task
title: Define Package Boundaries
description: Define Go package areas while keeping MCP and CLI as thin adapters.
tags: [internal, roadmap, go, architecture]
status: pending
phase: 7
order: 1
timestamp: 2026-07-25T00:00:00Z
---

# Define Package Boundaries

## Candidate areas

```text
format
roles
workflows
validation
changes
workspace
providers
mcp
cli
```

MCP and CLI packages should remain thin adapters around shared services.
