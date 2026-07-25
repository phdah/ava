# Ava Internal Roadmap

This directory contains the ordered implementation roadmap for Ava. Each executable to-do has its own file so a future Ava Internal Maintainer session can select and complete one bounded task at a time.

## Accepted architecture direction

```text
workflow -> activates exactly one primary role
role -> may support many workflows
role -> uses Ava semantic tools and workspace capabilities
Ava semantic tool -> uses shared application services
application service -> operates through a workspace provider
```

- Roles contain durable purpose, responsibilities, authority, instructions, capabilities, constraints, and required context.
- Workflows are reusable predefined prompts for a procedure or outcome.
- A workflow names one primary role and should not duplicate that role's base instructions.
- Workflow triggers may be interactive, scheduled, or event-driven, but Ava is not initially the scheduler or agent runtime.
- Deterministic structural work should be implemented as Ava application or MCP capabilities rather than encoded as separate agent roles.
- Generic file and version-control operations should be supplied by a workspace provider rather than hard-coded to one backend.
- Ava's public MCP tools should primarily expose semantic platform operations rather than duplicate every generic file operation.
- Internal Ava development roles remain separate from all roles generated into initialized projects.

## Roadmap order

1. [Format contract and base structure](01-format-contract/) - 0 of 3 complete
2. [Core roles for initialized projects](02-core-roles/) - 2 of 4 complete
3. [Workflow system](03-workflows/) - 0 of 4 complete
4. [Workspace access and provider abstraction](04-workspace-provider/) - 0 of 3 complete
5. [Semantic MCP tool catalog](05-semantic-tools/) - 0 of 5 complete
6. [Deterministic validation](06-validation/) - 0 of 3 complete
7. [Shared Go application services](07-application-services/) - 0 of 4 complete
8. [MCP implementation](08-mcp/) - 0 of 3 complete
9. [Companion CLI](09-cli/) - 0 of 2 complete
10. [Testing, compatibility, and migrations](10-compatibility/) - 0 of 3 complete

Tasks may be completed out of order when they unblock design work, but implementation must not establish a public contract before the relevant design task is resolved.

## Task status

- `pending`: the task has not met its completion criteria.
- `complete`: the intended change has been implemented, indexed, validated, and committed.

Update a task's frontmatter and its phase index together when its status changes.

## Shared completion work

Complete these concerns as part of the relevant individual tasks rather than creating separate roles or roadmap items:

- keep `templates/base/roles/index.md` accurate
- keep the future workflow registry accurate
- verify every role has deterministic required reading
- keep role and workflow routing conditions distinct
- validate required files, metadata, links, and references
- update affected template and repository indexes
- update conceptual logs only when a task introduces a major conceptual or structural change
- ensure no files or instructions under `/internal/` are copied into generated projects
- keep public Ava behavior independent of the internal development role
