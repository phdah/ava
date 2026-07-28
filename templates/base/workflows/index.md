# Workflows

This file is the canonical registry root for reusable project workflows.

A workflow is registered only when it is reachable by following discovery links from this index. Each workflow-owning subdirectory must maintain its own `index.md` and list only direct child files and directories.

Each workflow activates exactly one primary role and defines procedure-specific inputs, operating mode, required context, procedure, and expected output without duplicating the role's durable instructions.

Workflow files must follow the shared [workflow format](../shared/instructions/workflow-format.md). Invocation, routing precedence, primary-role resolution, validation, and deprecation follow [workflow registry and routing](../shared/instructions/workflow-routing.md).

Invoke a workflow by its canonical bundle-root-relative path or by an unambiguous lowercase kebab-case filename stem. Workflow titles are descriptive and are not stable invocation identifiers.

## Available workflows

No workflows have been added yet.
