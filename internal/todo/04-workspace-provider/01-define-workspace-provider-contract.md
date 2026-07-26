---
type: Internal Development Task
title: Define the Workspace-Provider Contract
description: Define provider-independent workspace capabilities, project selection, safety, concurrency, and errors.
tags: [internal, roadmap, workspace, providers]
status: pending
phase: 4
order: 1
timestamp: 2026-07-25T00:00:00Z
---

# Define the Workspace-Provider Contract

## Purpose

Ava semantic operations must be independent of where project files live.

## Candidate capabilities

```text
list
read
write
move
delete
status
commit
```

The contract should describe behavior rather than one provider's API.

## Decide

- workspace identity and root selection
- how Ava discovers or receives the active project
- whether a server or client session addresses one workspace or multiple named workspaces
- how operations select their workspace when multiple workspaces are supported
- path normalization
- capability discovery
- read-only versus writable providers
- optimistic concurrency and version identifiers
- atomic or grouped changes
- commit message and attribution support
- provider error normalization
- authentication responsibility
- large file and binary behavior
- symlink and traversal safety
- whether provider methods are internal only or partly exposed through MCP

## Completion criteria

- define a Go interface or equivalent contract
- define required and optional capabilities
- define active-project and workspace-selection semantics
- document provider-independent semantics
- add conformance tests usable by future providers