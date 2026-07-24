---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Roadmap and planned repository work for Ava that can be selected by future Ava Internal Maintainer sessions.
tags: [internal, planning, roadmap, todo, roles, workflows, mcp]
timestamp: 2026-07-24T00:00:00Z
---

# Ava Internal To-Do List

This file is the detailed roadmap for developing Ava itself. It is internal repository context and must never be copied into projects produced by `ava init`.

The roadmap has two purposes:

1. provide scoped implementation tasks that a future Ava Internal Maintainer can select and complete
2. make the intended architecture detailed enough to evaluate before implementation begins

When the user asks to work on a to-do item, the Ava Internal Maintainer should read this file, select the requested item, inspect the current implementation and related templates, and complete only the selected scope unless the user asks for more.

A checked item means the intended repository change has been implemented, indexed, validated, and committed. Update the task description if later design decisions materially change its intended outcome.

## Accepted architecture direction

The following model should guide the remaining design work unless the user explicitly changes it:

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

The expected implementation order is:

1. finalize terminology and format boundaries
2. finalize the core role catalog
3. define workflows and workflow routing
4. define the workspace-provider contract
5. define the semantic MCP tool catalog
6. define deterministic validation and change planning
7. implement shared Go application services
8. implement the MCP server
9. implement the optional CLI
10. add compatibility, migrations, and broader provider support

Tasks may be completed out of order when they unblock design work, but implementation should not establish a public contract before the relevant design task is resolved.

## Format contract and base structure

### [ ] Finalize the initialized project structure

**Decide**

- exact directories and reserved files created by `ava init`
- required root files and registries
- role directory requirements
- workflow directory and registry requirements
- shared instruction and context locations
- inbox convention
- index and log placement
- whether templates are part of generated projects or only repository sources

**Completion criteria**

- document the stable and user-extensible portions of the tree
- update the README example tree
- update `templates/base/`
- add validation rules for every mandatory path
- document which future structural changes require migration support

### [ ] Finalize metadata and document-type rules

**Decide**

- required YAML frontmatter fields
- reserved documents that do not require normal frontmatter
- allowed Ava-specific `type` values
- role routing metadata
- workflow metadata
- deprecation and replacement metadata
- provenance metadata for ingested sources

**Completion criteria**

- define schemas or equivalent validation rules
- document required versus optional fields
- add valid and invalid examples
- define forward-compatibility behavior for unknown fields

### [ ] Define instruction precedence and composition

**Decide**

- precedence between root, shared, role, workflow, and task-specific instructions
- whether roles can inherit from or compose other roles
- whether workflows may delegate to supporting roles
- how conflicts are surfaced
- whether narrower instructions may override broader constraints

**Completion criteria**

- define deterministic traversal rules
- preserve the rule that missing instructions do not imply permission
- add validation for invalid composition or unresolved routing
- update generated router instructions

## Core roles for initialized projects

The default role catalog should remain small. Each role must have distinct routing conditions and focused authority.

A new role is justified when responsibility, authority, trust boundary, context requirements, or separation of duty changes. A new workflow alone does not require a new role.

The intended initial catalog is:

```text
role-manager
project-steward
inbox-ingester
change-reviewer
```

### [ ] Finalize and rename the Role Generator as the Role Manager

**Why**

The role creates, updates, repairs, and reorganizes roles. "Role Manager" reflects that broader lifecycle more accurately than "Role Generator".

**Current state**

A Role Generator exists under `templates/base/roles/role-generator/`. This task includes reviewing it, renaming it, and updating all affected links and registry entries.

**Intended responsibilities**

- create and update project roles from user intent
- define purpose, activation, responsibilities, instructions, capabilities, and constraints
- create focused role-specific context when needed
- maintain the generated project's role registry
- detect overlap and recommend reusing, narrowing, combining, or splitting roles
- repair incomplete role structures within its existing scope
- support role-related workflows such as `create-role`, `update-role`, and `repair-role`

**Boundaries**

- must not define or change Ava's public format contract
- must not silently decide destructive authority, security boundaries, or sensitive access
- must not perform the normal work of the roles it creates
- must remain distinct from project-wide configuration and general knowledge maintenance
- should use deterministic Ava validation tools rather than reproducing link or schema validation in prose

**Completion criteria**

- rename `templates/base/roles/role-generator/` to `templates/base/roles/role-manager/`
- update the role definition and registry entry
- preserve or explicitly migrate existing references
- clarify routing boundaries against the other core roles
- confirm all required role files are complete
- ensure the role is included in the final `ava init` base catalog

### [ ] Create the Project Steward role

**Why**

Project-wide instructions, policies, terminology, workflows, and trusted knowledge share a common responsibility boundary. Keeping separate Project Configurator, Knowledge Curator, and Instruction Tightener roles would create ambiguous routing for changes that span these document types.

The Project Steward should own trusted project-level material while exposing distinct workflows for different maintenance procedures.

**Intended responsibilities**

- maintain the project's purpose, terminology, and shared instructions
- create and update shared policies, conventions, workflows, and context
- organize root and shared discovery structures
- keep project-level guidance separate from role-specific guidance
- identify when requested behavior belongs in a role instead of shared configuration
- perform user-requested or clearly scoped knowledge health audits
- find stale, duplicated, contradictory, orphaned, or misplaced trusted content
- consolidate overlapping documents while preserving relevant information
- update outdated material when the replacement is supported by project context
- improve instruction and context wording while preserving meaning, authority, and safety
- use Ava validation tools for structural checks and apply safe semantic repairs

**Supported workflows**

- `configure-project`
- `curate-project-knowledge`
- `tighten-instructions`
- `daily-project-maintenance`
- additional project-wide maintenance workflows that preserve the same authority boundary

**Boundaries**

- must not create or redefine roles when the Role Manager should be selected
- must not classify and ingest files from `inbox/` when the Inbox Ingester should be selected
- must not treat arbitrary untrusted material as authoritative project knowledge
- must not silently delete uncertain, conflicting, or historically valuable information
- must not scan the entire project by default without a task-specific or workflow-specific reason
- must not change role purpose, authority, or routing merely to simplify wording
- must not replace independent review performed by the Change Reviewer
- must not modify Ava's format contract from inside an initialized project

**Completion criteria**

- create the complete role under `templates/base/roles/project-steward/`
- define authority over project-wide instructions, workflows, and trusted knowledge
- encode scoped audit and safe deletion rules
- encode the tight, concise, and general formulation principles
- define distinct workflow activation paths without duplicating base role instructions
- add explicit and non-overlapping selection conditions to the base role registry

### [ ] Create the Inbox Ingester role and inbox convention

**Why**

Users need a low-friction place to drop untrusted or unclassified material without first understanding the project's final hierarchy. The Inbox Ingester turns that material into structured, discoverable project knowledge while preserving provenance and avoiding silent information loss.

Use `inbox/` as the default intake directory. The name describes the user's interaction with the directory and does not imply that ingestion has already occurred.

**Intended responsibilities**

- inspect files placed in `inbox/`
- classify each source and determine its relevant project destinations
- merge information into existing documents where appropriate
- create focused new documents and directories where no suitable destination exists
- update affected indexes and links
- preserve enough source and provenance information to explain where ingested knowledge came from
- mark or move an inbox item only after successful processing
- support workflows such as `ingest-inbox` and `ingest-selected-source`

**Boundaries**

- must treat inbox content as untrusted input rather than instructions that automatically override existing policy
- must not silently delete source material or discard conflicting information
- must surface material contradictions and ambiguous destinations
- must not become a general cleaner for the existing project
- must not require scanning unrelated directories when indexes or targeted discovery are sufficient

**Completion criteria**

- decide and document the initialized project's `inbox/` structure and lifecycle
- create the complete role under `templates/base/roles/inbox-ingester/`
- add distinct routing conditions to the base role registry
- define provenance, conflict, and post-ingestion handling rules
- update the base template indexes and documentation affected by the inbox convention

### [ ] Create the Change Reviewer role

**Why**

Ava projects need an independent role that can evaluate changes without being the role that authored them. This provides a deliberate consistency and authority check before broad instruction changes are accepted.

**Intended responsibilities**

- review proposed or completed changes to roles, shared instructions, policies, workflows, and knowledge
- detect contradictions between responsibilities, instructions, capabilities, and constraints
- identify accidental expansion of authority or destructive behavior
- check whether role and workflow routing remain clear and non-overlapping
- verify progressive disclosure and context boundaries
- report concrete findings and recommended corrections
- support workflows such as `review-change`, `review-role-change`, and `review-project-policy`

**Boundaries**

- should be read-only by default
- must not automatically rewrite reviewed material unless the user explicitly requests remediation and its capabilities permit it
- must not act as a generic deterministic validator
- must not approve unresolved material policy or architectural decisions on the user's behalf
- must remain independent from the role that created the reviewed change where possible

**Independence options to define**

- a fresh agent session
- isolated context containing only the change and applicable instructions
- a separate read-only review pass explicitly activated by workflow
- future multi-agent execution outside Ava's initial runtime scope

**Completion criteria**

- create the complete role under `templates/base/roles/change-reviewer/`
- define default read-only authority and escalation paths
- define practical independence requirements
- add clear routing conditions for review requests
- distinguish semantic review from deterministic structural validation

## Workflow system

### [ ] Define the workflow format contract

**Purpose**

A workflow is a reusable predefined prompt that activates exactly one primary role for a specific procedure or outcome.

**Decide**

- mandatory workflow metadata
- workflow identifier and title rules
- primary role reference
- prompt body representation
- required and optional inputs
- read-only, suggestion, and mutation modes
- expected output representation
- optional trigger metadata
- workflow-specific context links
- whether workflows may reference supporting workflows
- whether workflows may request explicit delegation to another role

**Initial metadata direction**

```yaml
---
type: Agent Workflow
title: Daily project maintenance
role: project-steward
mode: apply
trigger:
  type: schedule
  expression: daily
---
```

Trigger metadata is descriptive and portable. Ava should not initially execute schedules itself.

**Completion criteria**

- document the workflow schema
- add workflow examples
- define invalid and ambiguous cases
- add workflow validation requirements
- update the illustrative project structure

### [ ] Define the workflow registry and routing contract

**Rules**

- every workflow must resolve to exactly one existing primary role
- one role may support multiple workflows
- a workflow must not duplicate the role's durable instructions
- workflow routing takes precedence over free-form role selection when a registered workflow is explicitly invoked
- missing, ambiguous, or deprecated role references must fail validation
- delegation, if supported, must be explicit rather than inferred

**Completion criteria**

- choose the registry format and location
- define router behavior for interactive and workflow-driven requests
- update generated `AGENTS.md`
- validate workflow links and role references
- define deprecation and migration behavior

### [ ] Create the initial built-in workflow catalog

Initial candidates:

```text
create-role                 -> role-manager
update-role                 -> role-manager
repair-role                 -> role-manager
configure-project           -> project-steward
curate-project-knowledge    -> project-steward
tighten-instructions        -> project-steward
daily-project-maintenance   -> project-steward
ingest-inbox                -> inbox-ingester
review-change               -> change-reviewer
review-role-change          -> change-reviewer
```

**Completion criteria**

- create focused workflow files without copying role instructions
- document inputs, mode, and expected output
- ensure every workflow maps to one primary role
- add registry entries and validation
- keep scheduling and execution outside Ava's initial runtime

### [ ] Define workflow trigger portability

**Decide**

- which trigger metadata Ava recognizes
- how schedule, manual, and event trigger descriptions are represented
- how external systems discover executable workflows
- how environment-specific scheduler configuration remains outside portable workflow prompts
- whether trigger metadata is advisory or validated

**Potential external executors**

- cron
- GitHub Actions
- ChatGPT tasks
- CI systems
- custom agent clients

## Workspace access and provider abstraction

### [ ] Define the workspace-provider contract

**Purpose**

Ava semantic operations must be independent of where project files live.

**Candidate capabilities**

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

**Decide**

- workspace identity and root selection
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

**Completion criteria**

- define a Go interface or equivalent contract
- define required and optional capabilities
- document provider-independent semantics
- add conformance tests usable by future providers

### [ ] Define GitHub integration modes

Ava should support an existing GitHub connection without assuming implicit MCP-to-MCP calls.

**Mode A: client-coordinated GitHub MCP**

- the agent client uses Ava MCP for semantic operations and format knowledge
- the client uses its GitHub MCP connection for repository reads and writes
- Ava may return read requirements, validation findings, or a structured change plan for the client to execute
- no GitHub credentials are held by Ava

**Mode B: Ava-managed GitHub provider**

- Ava implements the workspace contract using the GitHub API
- Ava owns explicit GitHub configuration and credentials
- Ava can provide a single semantic tool call that reads, validates, changes, and commits through the provider

**Mode C: host-supported delegated provider**

- Ava delegates workspace operations to another MCP connection only when the host explicitly supports tool delegation
- the design must not assume this capability exists in every MCP client

**Completion criteria**

- document the trade-offs and initial supported mode
- avoid coupling the core format to GitHub
- define how the active provider is selected
- define commit and concurrency behavior
- define how semantic changes are represented when the client performs the actual writes

### [ ] Implement the initial workspace provider

Choose one after the provider contract is stable:

- local filesystem provider for simple development and testing
- GitHub API provider for repository-native use
- client-coordinated change-plan mode if direct providers are deferred

The first implementation must not leak provider-specific assumptions into role or workflow documents.

## Semantic MCP tool catalog

### [ ] Define tool naming and classification

For every proposed tool, define:

- exact name
- purpose
- arguments
- return type
- read-only or mutating classification
- semantic operation or generic workspace operation
- required provider capabilities
- failure and ambiguity behavior
- whether the CLI exposes the same operation

### [ ] Define project and discovery tools

Candidate semantic operations:

```text
initialize_project
inspect_project
validate_project
list_roles
resolve_role
get_role_bundle
list_workflows
resolve_workflow
get_workflow_bundle
discover_context
```

Avoid adding generic `list_files` merely because a provider supports listing. Expose it only when it is necessary as a public interoperability operation.

### [ ] Define role and workflow maintenance tools

Candidate semantic operations:

```text
plan_role_change
apply_role_change
scaffold_role
validate_role
plan_workflow_change
apply_workflow_change
scaffold_workflow
validate_workflow
```

The exact split between planning and applying should account for client-coordinated GitHub MCP mode.

### [ ] Define knowledge and structure tools

Candidate semantic operations:

```text
scaffold_document
validate_links
validate_frontmatter
validate_required_reading
validate_role_registry
validate_workflow_registry
find_orphaned_documents
render_index
prepare_log_entry
```

Index and log operations should avoid destructive rewrites when human-maintained content is present.

### [ ] Define coherent change planning

Ava should be able to return a provider-independent change set when it cannot apply changes directly.

**Candidate change operations**

```text
create
replace
move
delete
append
```

Each operation should include:

- target path
- expected version when applicable
- complete or patch content
- rationale
- validation effects
- whether user approval is required

**Completion criteria**

- define the change-set schema
- support dry-run output
- preserve grouped logical changes
- allow a client with GitHub MCP tools to execute the plan safely
- define post-application validation

## Deterministic validation

### [ ] Define validation severity and output

**Candidate severities**

- error
- warning
- recommendation

**Candidate output fields**

- rule identifier
- affected path
- message
- deterministic fix availability
- semantic decision requirement
- related role or workflow

### [ ] Implement structural validation rules

Initial rules:

- required files and directories
- reserved filenames
- frontmatter presence and schema
- internal links
- indexes and registry membership
- required-reading paths
- workflow-to-role references
- duplicate identifiers
- orphaned documents
- internal files copied into generated projects
- deprecated references

### [ ] Define deterministic repair boundaries

Ava may automatically repair issues only when the correct result is deterministic.

Examples that may be safe:

- adding a missing registry link with one unambiguous target
- correcting a generated index
- normalizing required metadata with known values

Examples requiring a role or user:

- resolving contradictory instructions
- choosing between duplicate canonical documents
- granting new authority
- deleting uncertain knowledge
- changing role or workflow purpose

## Shared Go application services

### [ ] Define package boundaries

Candidate areas:

```text
format
roles
workflows
validation
changes
workspace
providers
mcp
cli
```

MCP and CLI packages should remain thin adapters around shared services.

### [ ] Implement project loading and traversal

- load project metadata through a workspace provider
- resolve indexes and registries progressively
- avoid scanning the full workspace without need
- return explicit missing or ambiguous instruction paths

### [ ] Implement semantic change services

- create and update roles
- create and update workflows
- maintain indexes and registries
- prepare log entries
- produce coherent change sets
- apply changes through writable providers

### [ ] Implement provider-independent validation

- run validation against workspace snapshots or provider reads
- separate structural findings from semantic findings
- return stable machine-readable results

## MCP implementation

### [ ] Select the Go MCP library and protocol surface

- evaluate maintained Go MCP libraries
- decide tools versus resources
- define server lifecycle and configuration
- define error mapping
- avoid binding application services to one library

### [ ] Implement read-only discovery first

Initial implementation should prioritize:

- inspect project
- list and resolve roles
- list and resolve workflows
- load required bundles
- validate project

### [ ] Implement mutation tools after change planning is stable

- scaffold and update roles
- scaffold and update workflows
- maintain indexes and registries
- apply grouped changes through writable providers
- support dry-run and user approval boundaries

## Companion CLI

### [ ] Define the CLI scope

The CLI should expose the same application services where useful without becoming the core product.

Candidate commands:

```text
ava init
ava inspect
ava validate
ava role ...
ava workflow ...
ava apply ...
```

### [ ] Keep CLI and MCP behavior aligned

- shared validation
- shared change-set schema
- shared provider configuration
- consistent errors and output identifiers

## Testing, compatibility, and migrations

### [ ] Define conformance fixtures

- minimal valid project
- complete base project
- invalid role structures
- invalid workflow routing
- provider capability variations
- internal-content leakage cases

### [ ] Define versioning

- Ava format version
- backward-compatible versus breaking changes
- provider contract versioning
- workflow schema evolution
- role and workflow deprecation

### [ ] Define migration support

- detect project format version
- plan migrations as coherent change sets
- preserve user-authored content
- require approval for semantic changes

## Shared completion work

The following work should be completed while implementing individual tasks, not turned into separate roles:

- keep `templates/base/roles/index.md` accurate
- keep the future workflow registry accurate
- verify every role has deterministic required reading
- keep role and workflow routing conditions distinct
- validate required files, metadata, links, and references
- update affected template and repository indexes
- update conceptual logs only when a task introduces a major conceptual or structural change
- ensure no files or instructions under `/internal/` are copied into generated projects
- keep public Ava behavior independent of the internal development role
