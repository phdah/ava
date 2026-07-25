---
type: Internal Development Task
title: Define GitHub Integration Modes
description: Define client-coordinated, Ava-managed, and explicitly delegated GitHub integration.
tags: [internal, roadmap, workspace, github]
status: pending
phase: 4
order: 2
timestamp: 2026-07-25T00:00:00Z
---

# Define GitHub Integration Modes

Ava should support an existing GitHub connection without assuming implicit MCP-to-MCP calls.

## Mode A: Client-coordinated GitHub MCP

- the agent client uses Ava MCP for semantic operations and format knowledge
- the client uses its GitHub MCP connection for repository reads and writes
- Ava may return read requirements, validation findings, or a structured change plan for the client to execute
- no GitHub credentials are held by Ava

## Mode B: Ava-managed GitHub provider

- Ava implements the workspace contract using the GitHub API
- Ava owns explicit GitHub configuration and credentials
- Ava can provide a single semantic tool call that reads, validates, changes, and commits through the provider

## Mode C: Host-supported delegated provider

- Ava delegates workspace operations to another MCP connection only when the host explicitly supports tool delegation
- the design must not assume this capability exists in every MCP client

## Completion criteria

- document the trade-offs and initial supported mode
- avoid coupling the core format to GitHub
- define how the active provider is selected
- define commit and concurrency behavior
- define how semantic changes are represented when the client performs the actual writes
