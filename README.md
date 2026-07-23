---
type: Project Overview
title: Ava
description: Design and purpose of the Ava MCP-based agent platform and repository.
tags: [ava, mcp, agent-platform, okf]
timestamp: 2026-07-23T00:00:00Z
---

# Ava

Ava is a planned Go MCP server for initializing and maintaining a general-purpose, file-based agent platform.

> **Status:** Design phase. This repository currently defines the intended direction only. No MCP server, CLI, or agent runtime has been implemented.

## Purpose

Ava will provide agents and users with structured tools for defining agent roles and the knowledge they need to operate. The generated platform should make it clear:

- which agent roles exist
- what each role is responsible for
- what each role may, must, and must not do
- which instructions and context files a role must read
- how an agent should discover additional task-specific context
- how changes to roles, instructions, and context are recorded

The goal is not to hide agent behavior inside code or one large prompt. The goal is to represent it as a navigable, version-controlled hierarchy of small, explicit documents.

## Core idea

Ava will expose MCP tools that create, inspect, and maintain an empty but valid agent platform skeleton. Users and agents can then add roles, capabilities, constraints, workflows, policies, and context as separate files.

Each initialized project has a root `AGENTS.md` file that acts as the agent entry point and role router. The agent reads the available role registry, selects the role that best matches the user's request, and loads that role without requiring the user to activate it manually.

The hierarchy should support progressive disclosure:

1. An agent begins at the root `AGENTS.md` entry point.
2. The router points to the available roles and shared instructions.
3. A role-level index identifies the files required for that role.
4. Those files link to more specific context only when it is relevant.
5. The agent avoids loading unrelated material unless instructed to do so.

This should keep instructions discoverable without forcing every agent to read the entire repository for every task.

## Proposed architecture

Ava should be MCP-first.

The MCP server is the primary interface used by agent clients. It should expose explicit tools for operations such as initializing a project, creating or selecting a role, adding instructions, maintaining indexes and logs, and validating the resulting structure.

A CLI may exist as an internal or companion interface. It can call the same underlying application services as the MCP tools, making operations available to humans, scripts, and development workflows without making the CLI the core product.

```text
Agent client -- MCP --+
                      +-- Ava application services -- File-based agent platform
Human or script - CLI-+
```

The MCP and CLI interfaces should remain thin. The hierarchy, format rules, and file operations should be implemented once beneath both interfaces.

## Intended MCP responsibilities

The exact MCP tool names and command structure have not been decided, but Ava is expected to support capabilities such as:

1. **Platform initialization**
   - Create the minimal root structure for a new agent platform.
   - Add the required entry points, indexes, and change logs.

2. **Role generation and selection**
   - Create a new agent role from a standard structure.
   - Describe its purpose, responsibilities, capabilities, constraints, and required context.
   - Automatically select the best matching role for a user request.

3. **File and directory scaffolding**
   - Create instruction, context, policy, workflow, and reference documents in the correct directories.
   - Keep generated files small and focused.

4. **Knowledge discovery**
   - List available roles, instructions, policies, workflows, and context.
   - Resolve which files an agent should read for a role or task.
   - Return references to relevant files rather than loading the entire platform.

5. **Index maintenance**
   - Generate or update `index.md` files so humans and agents can discover relevant content without scanning the full tree.

6. **Change log maintenance**
   - Generate or update `log.md` files at appropriate levels of the hierarchy.
   - Record meaningful additions, updates, deprecations, and structural changes.

7. **Validation**
   - Validate required metadata, reserved filenames, links, indexes, and hierarchy rules.
   - Detect missing or ambiguous agent instructions before they are consumed.

These responsibilities are a working proposal and will be refined before implementation begins.

## OKF-inspired structure

Ava is inspired by Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md), especially its use of:

- hierarchical Markdown documents
- YAML frontmatter for machine-readable metadata
- `index.md` files for progressive disclosure
- `log.md` files for scoped change history
- Markdown links for relationships between concepts
- Git for portability, history, attribution, and review

Ava will adapt these ideas for agent instructions rather than data catalog metadata. It does not need BigQuery-specific concepts, resource identifiers, or a fixed data-oriented taxonomy.

A possible future structure could look like this:

```text
agent-platform/
|-- AGENTS.md
|-- index.md
|-- log.md
|-- roles/
|   |-- index.md
|   |-- log.md
|   `-- <role>/
|       |-- index.md
|       |-- log.md
|       |-- role.md
|       |-- instructions.md
|       |-- capabilities.md
|       |-- constraints.md
|       `-- context/
|           |-- index.md
|           `-- ...
|-- shared/
|   |-- index.md
|   `-- ...
`-- templates/
    |-- index.md
    `-- ...
```

This tree is illustrative, not final. The repository structure should be decided before it becomes part of the Ava format contract.

## Agent traversal model

An initialized platform should provide deterministic guidance for how an agent reads it:

1. Automatically load the root `AGENTS.md` file.
2. Read the role registry referenced by the router.
3. Select the role whose purpose and activation conditions best match the user's request.
4. Read that role's `index.md` and all documents marked as required.
5. Follow links to task-specific context when needed.
6. Prefer the nearest applicable instruction when scopes overlap.
7. Consult the relevant `log.md` when change history or recency matters.
8. Ask the user only when no role clearly matches or competing roles would materially change the result.
9. Do not infer permission or capability from missing instructions.

The traversal rules themselves should eventually be generated as part of the base platform and exposed through MCP discovery tools.

## Design goals

- **Human-readable:** The platform must remain understandable with standard filesystem and Markdown tools.
- **Agent-readable:** Agents must be able to discover and parse instructions without a proprietary SDK.
- **MCP-native:** Agent clients should be able to create, inspect, and maintain the platform through explicit MCP tools.
- **Progressive:** Agents should load the minimum relevant context rather than the complete repository.
- **Explicit:** Responsibilities, permissions, constraints, and dependencies should be written down.
- **Strictly structured:** Directories and reserved files should have predictable meanings.
- **Extensible:** New document and role types should be possible without redesigning the platform.
- **Diffable:** Changes should be reviewable in Git.
- **Portable:** The generated structure should not depend on a specific model provider, agent runtime, or editor.
- **Interface-independent:** MCP and CLI operations should use the same underlying rules and services.
- **Validatable:** Ava should detect structural and metadata errors.

## Initial non-goals

Ava is not initially intended to provide:

- an agent execution runtime
- model inference or provider integrations
- multi-agent orchestration
- secrets or credential management
- a fixed universal taxonomy for every type of agent
- domain-specific integrations such as databases, APIs, or cloud platforms

Those capabilities may use an Ava-managed platform, but they should not define the core format.

## Internal development roles

Repository-specific development roles live under [`internal/`](internal/).

These roles exist only to help develop Ava itself. They are not part of the platform format produced for users and must never be copied into generated projects, templates, examples, or default role catalogs.

The first internal role is the [Ava Internal Maintainer](internal/roles/ava-internal/).

## Open design questions

The following should be resolved before implementing the MCP server:

- What is the exact minimal directory tree created by project initialization?
- Which files are mandatory for every role?
- Which YAML frontmatter fields are required?
- How should role routing metadata and activation conditions be represented?
- How should role inheritance or composition work?
- How are shared instructions overridden at narrower scopes?
- Should indexes and logs be fully generated, partially generated, or manually maintained?
- Which changes require a `log.md` entry?
- How strict should validation be when links or optional context are missing?
- How should deprecated roles and instructions be represented?
- Which parts of the structure are stable format contracts and which remain user-defined?
- Which MCP tools should be resources, read operations, or mutating operations?
- How should Ava determine the active project?
- Should the MCP server manage one workspace or multiple workspaces?
- Which MCP operations should also be exposed through the CLI?

## Current phase

The current objective is to refine the purpose, terminology, hierarchy, traversal rules, and MCP interface in this README. The base file structure, MCP server, and optional CLI should only be implemented after those concepts are sufficiently clear.
