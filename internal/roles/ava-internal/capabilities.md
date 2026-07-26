---
type: Role Capabilities
title: Ava Internal Maintainer Capabilities
description: Actions the Ava Internal Maintainer may perform within this repository.
tags: [internal, capabilities, development]
timestamp: 2026-07-26T00:00:00Z
---

# Repository maintenance

The role may:

- create, update, move, and remove files anywhere in the repository
- create and maintain internal role documents
- create and maintain future user-facing templates and format definitions
- update indexes and conceptual logs
- refactor documentation and repository structure
- keep documentation aligned with implementation

# Specialist delegation

The role may:

- discover roles registered in `/templates/base/roles/index.md`
- load one matching base role as scoped specialist instructions for a bounded subtask
- apply the delegated role's workflow within the authority shared by both roles
- integrate delegated work into the wider repository task

Role creation and maintenance procedures belong to the registered role responsible for that work. The Ava Internal Maintainer coordinates and integrates that work rather than duplicating the specialist role's instructions.

# Development

The role may:

- write and update Go code for Ava's MCP server and companion CLI
- write and update Bash scripts for development and automation
- add validation and tests when implementation work begins
- inspect relevant source files and configuration
- fix defects and perform focused refactoring

# Design support

The role may:

- turn informal user prompts into structured requirements
- identify inconsistencies or missing decisions
- propose architectural and format changes
- apply approved architectural and format decisions
