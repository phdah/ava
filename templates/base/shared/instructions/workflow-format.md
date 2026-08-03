---
type: Shared Instruction
title: Workflow Format
description: Portable structure, admission criteria, operating modes, inputs, outputs, context links, and validation rules for Ava workflows.
tags: [ava, workflows, format, validation]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Purpose

A workflow is an optional reusable predefined prompt for one bounded procedure or outcome. It activates exactly one primary role and supplies procedure-specific scope, inputs, operating mode, required context, steps, and expected output.

A workflow must remain readable as ordinary Markdown while exposing enough stable structure for host agents and available validation tools to validate and invoke it consistently.

Workflow registration, invocation identity, routing precedence, role resolution, and deprecation follow [Workflow registry and routing](workflow-routing.md).

# Workflow admission criteria

Add or retain a workflow only when all of these conditions hold:

- the procedure or outcome is expected to recur across more than one instance
- the scope is bounded enough to execute and report without an unrestricted project scan
- the inputs define meaningful variation, or the workflow has a clear fixed batch scope
- the operating mode materially constrains whether the workflow reports, proposes, or applies changes
- the procedure adds ordering, isolation, batch semantics, audit criteria, review criteria, or another useful constraint beyond the primary role's durable instructions
- the expected output standardizes evidence, completion, unresolved decisions, or another result that ordinary role work does not already guarantee
- required context can be identified without activating another role or loading unrelated project content
- exactly one registered role owns the complete authority boundary
- the procedure is semantic agent work rather than deterministic installation, replacement, migration, integrity, or validation mechanics

Useful workflow categories include bounded audits, standardized semantic reviews, batch processing, recurring maintenance scopes, and migration preparation that does not perform deterministic upgrade mechanics.

# Free-form role boundary

An ordinary request within a role's durable responsibilities selects that role directly. A workflow must not be required merely to create, update, repair, configure, curate, tighten, or otherwise perform routine work already defined by the role.

A free-form request may have the same broad intent as a workflow. The workflow's inputs, mode, required context, procedure, and expected output become active only through explicit invocation.

A workflow is not justified only because a command-like name is convenient.

# Deterministic tooling boundary

The following belong to deterministic release or validation tooling rather than workflows:

- installation and adoption transactions
- managed-file replacement or restoration
- checksum and provenance verification
- deterministic migration execution and journaling
- manifest and state-schema validation
- structural, metadata, required-path, and link validation

A workflow may request or consume deterministic validation results, but it must not reproduce those mechanics as semantic prose.

Semantic Ava version reconciliation is also not a workflow. Active upgrade state directly selects the managed Upgrade Role under the upgrade-routing contract.

# Warning signs

A proposed workflow likely belongs in role instructions or deterministic tooling when:

- its name is only a verb-and-object alias for routine role work
- its procedure mostly repeats the primary role's general working method
- its only result is a generic list of changed files
- it wraps one-off work without a reusable scope or outcome
- it performs fixed filesystem, checksum, manifest, migration, or validation operations
- it exists only to select a role that free-form routing already selects unambiguously
- removing the workflow would not remove any meaningful inputs, mode boundary, procedure, or output contract

# Versioning boundary

Managed workflows are Ava-managed release payloads and are installed or replaced deterministically with the rest of the managed base. Project-owned workflows remain project-owned and must not be overwritten by an Ava release.

Adding, removing, renaming, or changing a workflow can affect invocation identity, ambiguity, primary-role resolution, required inputs, operating mode, and intended behavior. These changes follow the [versioning and compatibility contract](../../../versioning-and-compatibility.md), release notes, and upgrade guidance.

Ava defines and validates workflow documents. It does not provide a persistent workflow execution runtime, scheduler, or workflow state service.

# Identity and naming

The workflow file path is its stable identity. Do not add a separate `workflow_id` field.

Workflow filenames must use lowercase kebab-case and describe the procedure as an action, such as:

```text
audit-project-context.md
ingest-inbox.md
review-change.md
```

The metadata `title` is the human-readable name. It must be non-empty and should describe the same action as the filename. Titles do not need to be globally unique because identity comes from the path.

A workflow becomes invokable only when it is registered through the managed or project-owned workflow registry. A canonical path identifies one registered workflow; a filename stem may be used only when it resolves unambiguously under the workflow-routing contract.

# Required metadata

Every workflow must follow [Document metadata](document-metadata.md) and include:

```yaml
---
type: Workflow
title: Audit project context
description: Audits a bounded project-context scope.
primary_role: /.ava/base/roles/project-steward/role.md
mode: suggestion
status: stable
---
```

Rules:

- `type` must be `Workflow`.
- `title` and `description` must be non-empty strings.
- `primary_role` must be a bundle-root-relative path to exactly one registered, non-deprecated ordinary `role.md` document.
- A role using `activation_mode: managed-pre-routing` is invalid as a workflow `primary_role`.
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
- Description: Project area or set of files to inspect.
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
- a workflow file that is not registered through the correct managed or project-owned workflow registry
- a `primary_role` that is absent, unresolved, not bundle-root-relative, deprecated, reserved for managed pre-routing, or does not identify exactly one registered `role.md`
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
- failure to satisfy the workflow admission criteria
- trigger-like metadata that has no recognized semantics
- a draft workflow being invoked
- a deprecated workflow without a valid replacement

Semantic ambiguity requiring authority, policy, routing, compatibility, or destructive-action judgment must block execution until the user resolves it.

# Valid example

```markdown
---
type: Workflow
title: Audit project context
description: Audits a bounded project-context scope.
primary_role: /.ava/base/roles/project-steward/role.md
mode: suggestion
status: stable
---

# Audit project context

## Purpose

Audit a bounded project-context scope and propose prioritized maintenance.

## Inputs

### `scope`

- Required: yes
- Description: Project-wide files, directories, indexes, or concern to inspect.

## Procedure

1. Inspect only the approved scope and its nearest discovery context.
2. Record evidence for supported maintenance findings.
3. Rank proposed actions without modifying project files.

## Expected output

Return prioritized findings, evidence, responsible owners, and unresolved decisions. Do not apply changes because this workflow uses `suggestion` mode.
```

# Invalid and ambiguous examples

The following are invalid:

- `primary_role` is a list or points to a role `index.md` rather than one `role.md`
- `primary_role` points to an unregistered, deprecated, or managed pre-routing role
- `mode: write` uses an unsupported mode
- a `read-only` workflow tells the agent to update files
- the workflow declares `supporting_role` or instructs the primary role to delegate
- an optional input omits `Default`
- `Procedure` is replaced by copied role instructions
- a workflow exists beneath a managed or project-owned workflow root but is omitted from its registry index
- a deprecated workflow is executed or automatically redirected
- a workflow only renames ordinary role work without adding a reusable procedure or outcome

The following require clarification or correction before reliable invocation:

- the title says `Review change`, but the filename is `apply-change.md`
- an input says only `scope` without defining what form the value takes
- the expected output does not say whether a suggestion should be applied
- a shorthand workflow name matches more than one registered workflow path
