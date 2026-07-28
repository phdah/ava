# Ava

Ava is a general-purpose, file-based context platform for AI agents. It structures roles, workflows, instructions, constraints, and knowledge so agents can discover and load the context they need to operate.

A planned Go MCP server will be the primary interface for initializing, inspecting, validating, and maintaining the platform.

> **Status:** Design phase. This repository currently defines the intended direction only. No MCP server, CLI, or agent runtime has been implemented.

## Name

The name Ava is inspired by the AI robot Ava in [*Ex Machina*](https://www.imdb.com/title/tt0470752/). Ava is exceptionally good at playing different roles to achieve her goals. This mirrors the project's role-based structure, where distinct roles support different workflows and make relevant context easy to collect, organize, and retrieve.

## Purpose

Ava will provide agents and users with a structured, version-controlled context platform for defining agent roles, reusable workflows, and the knowledge they need to operate. The platform should make it clear:

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

A workflow should not duplicate the role's durable instructions. It should define the procedure-specific purpose, inputs, operating mode, required context, procedure, and expected output. The selected role supplies the stable behavior and authority under which the workflow runs.

Ava initially permits exactly one active role. Roles do not inherit, compose, activate supporting roles, or delegate authority. Workflows may refine ordinary role behaviour for a bounded procedure, but they cannot expand the role's capabilities or weaken active constraints.

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

Ava's core output is an empty but valid agent context platform skeleton represented as files. An MCP interface will create, inspect, validate, and maintain that structure. Users and agents can then add roles, workflows, capabilities, constraints, policies, and context as separate files.

Each initialized project has a root `AGENTS.md` file that acts as the agent entry point and role router. The agent reads the available role registry, selects the role that best matches the user's request or the workflow's declared role, and loads that role without requiring the user to activate it manually.

The hierarchy should support progressive disclosure:

1. An agent begins at the root `AGENTS.md` entry point.
2. The router loads the shared instruction-resolution contract.
3. The router points to the available roles and other applicable shared instructions.
4. A role-level index identifies the files required for that role.
5. A workflow provides a focused predefined prompt and names its primary role.
6. Role and workflow files link to more specific context only when it is relevant.
7. The agent avoids loading unrelated material unless instructed to do so.

Instruction scope follows this explicit activation chain. A file is not narrower or more authoritative merely because it is located deeper in the directory tree.

This should keep instructions discoverable without forcing every agent to read the entire repository for every task.

## Proposed architecture

Ava is a file-based context platform with MCP as its primary management interface.

The planned MCP server should expose semantic tools for operations such as initializing a project, resolving a role or workflow, scaffolding structured documents, validating the platform, and preparing or applying coherent project changes.

A CLI may exist as an internal or companion interface. It can call the same underlying application services as the MCP tools, making operations available to humans, scripts, and development workflows without making the CLI the core product.

```text
Agent client -- MCP --+
                      +-- Ava application services -- Workspace provider -- Context platform
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
   - Add the required entry points, indexes, and registries.
   - Create scoped change logs only when meaningful conceptual or structural history needs to be preserved.

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
   - Preserve provider-specific concurrency and versioning semantics.

These responsibilities are a working proposal and will be refined before implementation begins.

## OKF v0.2 structure

Ava follows Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) version 0.2, especially its use of:

- hierarchical Markdown documents
- YAML frontmatter for machine-readable metadata
- `index.md` files for progressive disclosure
- `log.md` files for scoped change history
- Markdown links for relationships between concepts
- provenance, generation, verification, lifecycle, and staleness metadata
- Git for portability, history, attribution, and review

Ava adapts these ideas for agent instructions rather than data catalog metadata. It does not use BigQuery-specific concepts, resource identifiers, or a fixed data-oriented taxonomy.

### Metadata contract

The generated [document metadata instruction](templates/base/shared/instructions/document-metadata.md) and [workflow format instruction](templates/base/shared/instructions/workflow-format.md) define the public document and workflow contracts:

- `index.md` and `log.md` are reserved documents
- every other Markdown document requires a descriptive `type`
- Ava-controlled semantic documents also require `title` and `description`
- project-defined document types remain open
- role routing remains semantic and prose-based
- workflows reference exactly one `primary_role` and declare `mode`
- workflow bodies use portable sections for inputs, required context, procedure, and expected output
- OKF provenance, verification, lifecycle, and staleness fields are used directly
- unknown fields and project-defined types remain forward-compatible
- Ava-specific metadata stays minimal and flat

The root `index.md` declares `okf_version: "0.2"`. Ava does not add per-document schema versions.

`ava init` creates a minimal project with stable top-level locations for intake, trusted knowledge, roles, workflows, and shared context:

```text
agent-platform/
|-- AGENTS.md
|-- index.md
|-- inbox/
|   |-- index.md
|   `-- processed/
|       `-- index.md
|-- knowledge/
|   `-- index.md
|-- roles/
|   |-- index.md
|   `-- <built-in-role>/
|       |-- index.md
|       |-- role.md
|       |-- instructions.md
|       |-- capabilities.md
|       `-- constraints.md
|-- workflows/
|   `-- index.md
`-- shared/
    |-- index.md
    `-- instructions/
        |-- index.md
        |-- instruction-resolution.md
        |-- scoped-history.md
        |-- document-metadata.md
        |-- workflow-format.md
        `-- knowledge-organization.md
```

The top-level directories are intentionally broad and extensible. Knowledge is organized beneath `knowledge/`, workflows beneath `workflows/`, and roles beneath `roles/`. New subdirectories and documents are created only when real project content requires them. `log.md` files are not created by default, and repository source templates are not copied into initialized projects.

## Agent traversal model

An initialized platform should provide deterministic guidance for how an agent reads it:

1. Automatically load the root `AGENTS.md` file.
2. Read the shared instruction-resolution contract required by the router.
3. Determine whether the request invokes a registered workflow or is a free-form request.
4. For a workflow, resolve its declared primary role. Otherwise, select one role from the role registry by purpose and activation conditions.
5. Read the active role's `index.md` and all documents marked as required.
6. Read the workflow prompt and workflow-specific context when a workflow is active.
7. Follow explicit links to task-specific instructions and context only when the active task requires them.
8. Resolve ordinary instruction overlap by explicit activation scope rather than directory depth.
9. Keep capabilities and constraints cumulative. Narrower scopes may reduce authority but cannot grant missing capabilities or weaken broader constraints.
10. Before modifying project files, read the scoped-history contract and determine whether the nearest relevant `log.md` must be created or updated.
11. Ask the user when routing or instruction conflicts remain unresolved.
12. Do not infer permission, capability, authority, or instructions from missing documentation.

The current user request supplies the immediate objective and narrowest procedural scope, but it remains bounded by the active role, project constraints, and available workspace capabilities.

The traversal rules themselves should eventually be exposed through MCP discovery and validation tools.

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
- **Obsidian-compatible:** Projects must remain readable and editable as normal Markdown vaults, including source-mode access to nested OKF metadata.

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
