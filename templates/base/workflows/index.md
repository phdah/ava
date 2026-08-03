# Workflows

This file is the managed registry root for reusable default workflows. Project-owned workflows are discovered separately through `/workflows/index.md` when present.

A workflow is an optional, explicitly invoked procedural scope. It must add repeatable value through a bounded outcome, meaningful inputs, an operating mode, procedure-specific context or ordering, and a standardized expected output. Ordinary work already covered by a role should route directly to that role instead of requiring a command-like workflow alias.

A workflow is registered only when it is reachable by following discovery links from this index. Each workflow-owning subdirectory must maintain its own `index.md` and list only direct child files and directories.

Each workflow activates exactly one primary role and defines procedure-specific inputs, operating mode, required context, procedure, and expected output without duplicating the role's durable instructions.

Workflow files must follow the shared [workflow format](../shared/instructions/workflow-format.md). Invocation, routing precedence, primary-role resolution, validation, and deprecation follow [workflow registry and routing](../shared/instructions/workflow-routing.md).

Invoke a workflow by its canonical installed path or by an unambiguous lowercase kebab-case filename stem. Workflow titles are descriptive and are not stable invocation identifiers.

Installation, managed-file replacement, checksum verification, deterministic migration, structural validation, and semantic Ava version reconciliation are not workflows. Active upgrade state directly selects the managed Upgrade Role before workflow discovery.

## Available workflows

### Batch ingestion

- [Ingest inbox](ingest-inbox.md) - Processes every pending direct inbox source independently while preserving trust boundaries and provenance.

### Semantic review

- [Review change](review-change.md) - Performs a standardized read-only semantic review of one bounded project change.
- [Review role catalog](review-role-catalog.md) - Reviews the complete registered role catalog for coverage, routing, authority, safeguards, and lifecycle consistency.

### Project context audit

- [Audit project context](audit-project-context.md) - Produces a prioritized maintenance proposal for a bounded project-context scope without applying changes.
