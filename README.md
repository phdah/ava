---
type: Project Overview
title: Ava
description: Design and purpose of the Ava MCP-based agent platform and repository.
tags: [ava, mcp, agent-platform, okf]
timestamp: 2026-07-24T00:00:00Z
---

# Ava

Ava is a planned Go MCP server for initializing and maintaining a general-purpose, file-based agent platform.

> **Status:** Design phase. This repository currently defines the intended direction only. No MCP server, CLI, or agent runtime has been implemented.

## Purpose

Ava will provide agents and users with structured tools for defining agent roles, reusable workflows, and the knowledge they need to operate. The generated platform should make it clear:

- which agent roles exist
- what each role is responsible for
- what each role may, must, and must not do
- which instructions and context files a role must read
- which predefined workflows exist and which role each workflow activates
- how an agent should discover additional task-specific context
- how changes to roles, workflows, instructions, and context are recorded

The goal is not to hide agent behavior inside code or one large prompt. The goal is to represent it as a navigable, version-controlled hierarchy of small, explicit documents.

## Core model

Ava distinguishes four concepts:

1. **Roles** define durable responsibilities, authority, constraints, required instructions, and context.
2. **Workflows** are reusable, predefined prompts that activate one primary role for a particular procedure or outcome.
3. **Tools** perform explicit operations. Deterministic structural work should be implemented as tools rather than simulated through agent instructions.
4. **Workspaces** provide access to the files and version-control operations on which roles, workflows, and tools operate.

The intended relationship is:

```text
workflow -> activates exactly one primary role
role -> may support many workflows
role -> uses Ava semantic tools and workspace capabilities
```

A workflow should not duplicate the role's durable instructions. It should define the procedure-specific request, inputs, trigger information, operating mode, and expected output. The selected role supplies the stable behavior and authority under which the workflow runs.

Examples:

```text
create-role                 -> Role Manager
configure-project           -> Project Steward
curate-project-knowledge    -> Project Steward
tighten-instructions        -> Project Steward
daily-project-maintenance   -> Project Steward
ingest-inbox                -> Inbox Ingester
review-change               -> Change Reviewer
```

Workflows may be invoked interactively or by external schedulers such as cron, GitHub Actions, or an agent client's task system. Ava may define and validate trigger metadata, but scheduled execution is initially outside Ava's runtime responsibilities.

## Core idea

Ava will expose MCP tools that create, inspect, and maintain an empty but valid agent platform skeleton. Users and agents can then add roles, workflows, capabilities, constraints, policies, and context as separate files.

Each initialized project has a root `AGENTS.md` file that acts as the agent entry point and role router. The agent reads the available role registry, selects the role that best matches the user's request or the workflow's declared role, and loads that role without requiring the user to activate it manually.

The hierarchy should support progressive disclosure:

1. An agent begins at the root `AGENTS.md` entry point.
2. The router points to the available roles and shared instructions.
3. A role-level index identifies the files required for that role.
4. A workflow provides a focused predefined prompt and names its primary role.
5. Role and workflow files link to more specific context only when it is relevant.
6. The agent avoids loading unrelated material unless instructed to do so.

This should keep instructions discoverable without forcing every agent to read the entire repository for every task.

## Proposed architecture

Ava should be MCP-first.

The MCP server is the primary Ava interface used by agent clients. It should expose semantic tools for operations such as initializing a project, resolving a role or workflow, scaffolding structured documents, validating the platform, and preparing or applying coherent project changes.

A CLI may exist as an internal or companion interface. It can call the same underlying application services as the MCP tools, making operations available to humans, scripts, and development workflows without making the CLI the core product.

```text
Agent client -- MCP --+
                      +-- Ava application services -- Workspace provider -- Agent platform
Human or script - CLI-+
```

The MCP and CLI interfaces should remain thin. The hierarchy, format rules, semantic operations, validation, and change planning should be implemented once beneath both interfaces.

## Workspace access and external connections

Ava should not hard-code project storage to the local filesystem or duplicate every generic file tool exposed by another connection.

Instead, Ava application services should operate through a workspace-provider contract with capabilities such as:

```text
list
read
write
move
delete
status
commit
```

Potential providers include:

- a local filesystem provider
- a GitHub API provider implemented by Ava
- a host-mediated GitHub MCP connection
- future repository or document-system providers

This creates two valid integration modes:

### Client-coordinated mode

The agent client invokes Ava MCP tools for format knowledge, role and workflow resolution, validation, and change planning. It invokes a GitHub MCP connection for repository reads and writes.

This is the simplest initial mode when the client already has a GitHub connection. Ava does not need direct GitHub credentials, but the client must coordinate the two tool sets.

### Ava-managed provider mode

Ava wraps repository access behind its workspace contract and performs semantic operations against a configured provider. A GitHub implementation may call the GitHub API directly or use an explicit host-supported delegation mechanism.

MCP servers should not be assumed to call arbitrary tools from other MCP servers automatically. Cross-server delegation depends on the host. Ava therefore needs an explicit provider contract rather than relying on implicit MCP-to-MCP composition.

The public Ava MCP catalog should favor semantic operations such as `validate_project`, `resolve_workflow`, or `apply_role_update`. Generic file operations should normally remain provider capabilities beneath those tools. Direct workspace operations may still be exposed when they are needed for interoperability or debugging.

## Intended MCP responsibilities

The exact MCP tool names and command structure have not been decided, but Ava is expected to support capabilities such as:

1. **Platform initialization**
   - Create the minimal root structure for a new agent platform.
   - Add the required entry points, indexes, registries, and change logs.

2. **Role generation and selection**
   - Create a new agent role from a standard structure.
   - Describe its purpose, responsibilities, capabilities, constraints, and required context.
   - Automatically select the best matching role for a user request.
   - Resolve the role explicitly named by a workflow.

3. **Workflow generation and selection**
   - Create reusable predefined prompts.
   - Require each workflow to identify one primary role.
   - Describe workflow inputs, operating mode, expected output, and optional trigger metadata.
   - Validate workflow-to-role routing.

4. **File and directory scaffolding**
   - Create instruction, context, policy, workflow, and reference documents in the correct directories.
   - Keep generated files small and focused.

5. **Knowledge discovery**
   - List available roles, workflows, instructions, policies, and context.
   - Resolve which files an agent should read for a role, workflow, or task.
   - Return references to relevant files rather than loading the entire platform.

6. **Index and registry maintenance**
   - Generate or update `index.md` files and role or workflow registries.
   - Keep humans and agents able to discover relevant content without scanning the full tree.

7. **Change log maintenance**
   - Generate or update `log.md` files at appropriate levels of the hierarchy.
   - Record meaningful additions, updates, deprecations, and structural changes.

8. **Validation**
   - Validate required metadata, reserved filenames, links, indexes, registries, required-reading paths, and hierarchy rules.
   - Detect missing or ambiguous agent instructions before they are consumed.
   - Distinguish deterministic structural errors from semantic decisions requiring an agent or user.

9. **Workspace-backed change application**
   - Inspect provider capabilities before planning an operation.
   - Prepare coherent changes independently of the storage backend.
   - Apply changes through the configured workspace provider.
   - Preserve provider-specific concurrency, versioning, and commit semantics.

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
|-- workflows/
|   |-- index.md
|   |-- log.md
|   `-- <workflow>.md
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
2. Determine whether the request invokes a registered workflow or is a free-form request.
3. For a workflow, resolve its declared primary role.
4. Otherwise, read the role registry and select the role whose purpose and activation conditions best match the request.
5. Read that role's `index.md` and all documents marked as required.
6. Read the workflow prompt and workflow-specific context when a workflow is active.
7. Follow links to task-specific context when needed.
8. Prefer the nearest applicable instruction when scopes overlap.
9. Consult the relevant `log.md` when change history or recency matters.
10. Ask the user only when no role clearly matches or competing interpretations would materially change the result.
11. Do not infer permission or capability from missing instructions.

The traversal rules themselves should eventually be generated as part of the base platform and exposed through MCP discovery tools.

## Design goals

- **Human-readable:** The platform must remain understandable with standard filesystem and Markdown tools.
- **Agent-readable:** Agents must be able to discover and parse instructions without a proprietary SDK.
- **MCP-native:** Agent clients should be able to create, inspect, and maintain the platform through explicit MCP tools.
- **Progressive:** Agents should load the minimum relevant context rather than the complete repository.
- **Explicit:** Responsibilities, permissions, constraints, workflows, and dependencies should be written down.
- **Strictly structured:** Directories and reserved files should have predictable meanings.
- **Extensible:** New document, workflow, provider, and role types should be possible without redesigning the platform.
- **Diffable:** Changes should be reviewable in Git.
- **Portable:** The generated structure should not depend on a specific model provider, agent runtime, editor, or storage backend.
- **Interface-independent:** MCP and CLI operations should use the same underlying rules and services.
- **Provider-independent:** Semantic Ava operations should not be coupled to GitHub or local filesystem details.
- **Validatable:** Ava should detect structural, metadata, routing, and instruction-path errors.

## Initial non-goals

Ava is not initially intended to provide:

- an agent execution runtime
- model inference or provider integrations
- a scheduler
- multi-agent orchestration
- secrets or credential management
- a fixed universal taxonomy for every type of agent
- domain-specific integrations such as databases, APIs, or cloud platforms

External connections and workspace providers may be used by an Ava-managed platform, but they should not define the core format.

## Internal development roles

Repository-specific development roles live under [`internal/`](internal/).

These roles exist only to help develop Ava itself. They are not part of the platform format produced for users and must never be copied into generated projects, templates, examples, or default role catalogs.

The first internal role is the [Ava Internal Maintainer](internal/roles/ava-internal/).

## Roadmap direction

The implementation roadmap is tracked in [`internal/todo.md`](internal/todo.md). Its main design areas are:

1. format contract and base project structure
2. core role catalog
3. workflow format, registry, and built-in workflows
4. workspace-provider contract and GitHub integration modes
5. semantic MCP tool catalog
6. deterministic validation and change planning
7. shared application services
8. MCP and companion CLI implementation
9. testing, compatibility, and migrations

## Open design questions

The following should be resolved before implementing the MCP server:

- What is the exact minimal directory tree created by project initialization?
- Which files are mandatory for every role?
- Which metadata fields are mandatory for every workflow?
- Which YAML frontmatter fields are required?
- How should role routing metadata and activation conditions be represented?
- May a workflow delegate to supporting roles, or only activate one primary role?
- How should workflow inputs and outputs be represented?
- How should role inheritance or composition work?
- How are shared instructions overridden at narrower scopes?
- Should indexes and logs be fully generated, partially generated, or manually maintained?
- Which changes require a `log.md` entry?
- How strict should validation be when links or optional context are missing?
- How should deprecated roles, workflows, and instructions be represented?
- Which parts of the structure are stable format contracts and which remain user-defined?
- Which MCP tools should be resources, read operations, or mutating operations?
- Which generic workspace operations, if any, should be public Ava MCP tools?
- How should a client declare or discover the active workspace provider?
- How should GitHub MCP delegation differ from a direct GitHub API provider?
- How should provider capabilities, authentication, concurrency, and commit semantics be represented?
- How should Ava determine the active project?
- Should the MCP server manage one workspace or multiple workspaces?
- Which MCP operations should also be exposed through the CLI?

## Current phase

The current objective is to refine the purpose, terminology, hierarchy, role and workflow model, workspace abstraction, traversal rules, and MCP interface. The base file structure, MCP server, and optional CLI should only be implemented after those concepts are sufficiently clear.
