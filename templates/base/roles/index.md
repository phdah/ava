# Roles

This file is the role registry used by the root [`AGENTS.md`](../AGENTS.md) router.

Select roles automatically from the user's request. Read a selected role's `index.md` before acting.

## Available roles

### [Role Generator](role-generator/)

Creates and updates Ava roles and keeps the role registry consistent.

Select this role when the user asks to:

- create or define a new role
- modify an existing role
- define role responsibilities, instructions, capabilities, or constraints
- add or reorganize role-specific context
- repair an incomplete or inconsistent role structure

Do not select this role merely because another role is being used. Select it only when the requested work concerns role definition or maintenance itself.

Do not select the Project Steward for these requests. Project-wide configuration must not silently redefine role purpose, authority, or routing.

### [Project Steward](project-steward/)

Maintains trusted project-wide guidance, workflows, and knowledge.

Select this role when the user asks to:

- configure or clarify project purpose, terminology, shared policies, instructions, or conventions
- create or update project-wide workflows or trusted context
- organize root or shared discovery structures
- curate, consolidate, or repair existing trusted project knowledge
- tighten project-wide instructions without changing their meaning or authority
- perform a user-requested or workflow-scoped project maintenance audit
- run `configure-project`, `curate-project-knowledge`, `tighten-instructions`, or `daily-project-maintenance`

Do not select this role to create or redefine roles, ingest untrusted files from `inbox/`, or independently review a change.

When a request mixes project-wide and role-specific changes, select the role responsible for the primary outcome and keep the other role's authority explicit rather than silently merging their responsibilities.
