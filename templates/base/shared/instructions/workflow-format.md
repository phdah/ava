---
type: Shared Instruction
title: Workflow Format
description: Portable structure, operating modes, inputs, outputs, context links, and validation rules for Ava workflows.
tags: [ava, workflows, format, validation]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Purpose

A workflow is a reusable predefined prompt for one bounded procedure or outcome. It activates exactly one primary role and supplies procedure-specific scope, inputs, operating mode, required context, steps, and expected output.

A workflow must remain readable as ordinary Markdown while exposing enough stable structure for host agents and available validation tools to validate and invoke it consistently.

Workflow registration, invocation identity, routing precedence, role resolution, and deprecation follow [Workflow registry and routing](workflow-routing.md).

# Identity and naming

The workflow file path is its stable identity. Do not add a separate `workflow_id` field.

Workflow filenames must use lowercase kebab-case and describe the procedure as an action, such as:

```text
configure-project.md
curate-project-knowledge.md
review-change.md
```

The metadata `title` is the human-readable name. It must be non-empty and should describe the same action as the filename. Titles do not need to be globally unique because identity comes from the path.

A workflow becomes invokable only when it is registered through `/workflows/index.md`. A canonical path identifies one registered workflow; a filename stem may be used only when it resolves unambiguously under the workflow-routing contract.

# Required metadata

Every workflow must follow [Document metadata](document-metadata.md) and include:

```yaml
---
type: Workflow
title: Configure project
description: Establishes or updates project-wide purpose and shared guidance.
primary_role: /roles/project-steward/role.md
mode: mutation
status: stable
---
```

Rules:

- `type` must be `Workflow`.
- `title` and `description` must be non-empty strings.
- `primary_role` must be a bundle-root-relative path to exactly one registered, non-deprecated `role.md` document.
- `mode` must be `read-only`, `suggestion`, or `mutation`.
- `status` follows the shared lifecycle contract and remains optional.
- A deprecated workflow may declare one bundle-root-relative `replaced_by` workflow path, but routing must not follow it automatically.
- Unknown valid metadata must be preserved for forward compatibility.

# Operating modes

The mode states the maximum project effect requested by the workflow. It does not grant capabilities, weaken constraints, satisfy approval requirements, or guarantee that the host agent has tools capable of the requested operation.

## `read-only`

The workflow may inspect context and report findings. It must not create, update, move, or delete project content.

## `suggestion`

The workflow may inspect context and produce a proposed change, plan, patch, or recommendation. It must not apply the proposed project mutation.

## `mutation`

The workflow may request project changes. Actual changes remain bounded by the active role, active constraints, the user's approved scope, and capabilities exposed by the host agent and its available tools.

# Prompt body

A workflow document must contain one level-one heading matching its metadata title and these non-empty level-two sections in this order:

1. `Purpose`
2. `Inputs`
3. optional `Required context`
4. `Procedure`
5. `Expected output`
6. optional `Trigger notes`

Additional sections are allowed when they refine the bounded procedure without duplicating durable role instructions.

# Inputs

Inputs remain structured Markdown rather than frontmatter or a separate machine schema.

Use `None.` when the workflow accepts no inputs. Otherwise, define each input with a level-three heading and this structure:

```markdown
### `scope`

- Required: yes
- Description: Project area or set of files to configure.
```

An optional input must declare its default:

```markdown
### `include_examples`

- Required: no
- Description: Whether the proposal should include illustrative examples.
- Default: no
```

Input rules:

- input names must be unique within the workflow
- input names must use lower snake case and match `[a-z][a-z0-9_]*`
- `Required` must be exactly `yes` or `no`
- `Description` must be non-empty
- an optional input must include `Default`; use `none` when omission has no value
- a required input must not rely on a default to become optional
- the invocation supplies values; the workflow must not silently invent missing required values

# Required context

The optional `Required context` section lists procedure-specific files that must be loaded in addition to the primary role's required reading.

Use normal Markdown links with bundle-root-relative targets:

```markdown
## Required context

- [Project terminology](/knowledge/work/project-terminology.md)
- [Writing convention](/shared/instructions/writing-convention.md)
```

Every required-context link must resolve. Context links activate only the referenced context for this workflow and must not activate another role.

# Procedure

The `Procedure` section contains the workflow-specific prompt and ordered steps. It should define what is unique to the procedure, including its scope, decisions, and completion conditions.

A workflow must not copy or redefine the primary role's durable purpose, responsibilities, capabilities, constraints, or general working method. Link to authoritative shared instructions or context instead of duplicating them.

# Expected output

The `Expected output` section describes the result the caller should receive. It must state:

- the deliverable or outcome
- whether changes are only reported, proposed, or applied, consistently with `mode`
- what completion or unresolved-decision information must be returned

The output remains human-readable Markdown. This contract does not define a JSON response schema or require a particular presentation format.

# Composition boundaries

A workflow activates exactly one role through `primary_role`.

A workflow must not:

- reference supporting workflows as active dependencies
- invoke, include, or chain another workflow
- declare supporting roles
- request delegation or transition to another role
- expand the primary role's capabilities
- weaken any active constraint

Normal links to related documentation are allowed, but they must not imply workflow or role activation.

# Trigger boundary

This contract defines no portable trigger metadata. Unknown trigger-related fields must be preserved but have no Ava execution or validation semantics yet.

A workflow may include an optional `Trigger notes` section for human-readable, advisory context. External scheduling and event configuration remain outside Ava. The dedicated trigger-portability contract will decide recognized trigger metadata and executor discovery.

# Validation

Treat these as errors:

- missing or malformed required workflow metadata
- a workflow file that is not registered through `/workflows/index.md`
- a `primary_role` that is absent, unresolved, not bundle-root-relative, deprecated, or does not identify exactly one registered `role.md`
- a missing or unsupported `mode`
- a missing, duplicate, empty, or incorrectly ordered required body section
- a level-one heading that does not match `title`
- duplicate or malformed input names
- an input missing `Required` or `Description`
- an optional input missing `Default`
- a broken required-context link
- a declared supporting workflow, supporting role, delegation, or role transition
- an explicit procedure or expected output that contradicts the declared mode
- a workflow instruction that attempts to grant capabilities or weaken constraints
- a deprecated workflow being executed or redirected automatically through `replaced_by`

Treat these as warnings or semantic findings:

- a filename and title that describe materially different procedures
- vague input descriptions or defaults
- an expected output that does not make completion reporting clear
- likely duplication of the primary role's durable instructions
- trigger-like metadata that has no recognized semantics
- a draft workflow being invoked
- a deprecated workflow without a valid replacement

Semantic ambiguity requiring authority, policy, routing, compatibility, or destructive-action judgment must block execution until the user resolves it.

# Valid example

```markdown
---
type: Workflow
title: Configure project
description: Establishes or updates project-wide purpose and shared guidance.
primary_role: /roles/project-steward/role.md
mode: mutation
status: stable
---

# Configure project

## Purpose

Configure a bounded part of the project's shared guidance from approved user decisions.

## Inputs

### `scope`

- Required: yes
- Description: Project-wide topic or set of files to configure.

### `include_examples`

- Required: no
- Description: Whether changed guidance should include illustrative examples.
- Default: no

## Required context

- [Document metadata](/shared/instructions/document-metadata.md)

## Procedure

1. Inspect the approved scope and existing authoritative project guidance.
2. Identify material ambiguity before changing policy or authority.
3. Apply the smallest coherent project-wide change.
4. Update affected discovery and scoped history when required.

## Expected output

Return the files changed, the validation performed, and any unresolved decision. Apply approved changes because this workflow uses `mutation` mode.
```

# Invalid and ambiguous examples

The following are invalid:

- `primary_role` is a list or points to a role `index.md` rather than one `role.md`
- `primary_role` points to an unregistered or deprecated role
- `mode: write` uses an unsupported mode
- a `read-only` workflow tells the agent to update files
- the workflow declares `supporting_role` or instructs the primary role to delegate
- an optional input omits `Default`
- `Procedure` is replaced by copied role instructions
- a workflow exists beneath `/workflows/` but is omitted from its registry index
- a deprecated workflow is executed or automatically redirected

The following require clarification or correction before reliable invocation:

- the title says `Review change`, but the filename is `apply-change.md`
- an input says only `scope` without defining what form the value takes
- the expected output does not say whether a suggestion should be applied
- a shorthand workflow name matches more than one registered workflow path