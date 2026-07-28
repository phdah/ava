---
type: Shared Instruction
title: Workflow Registry and Routing
description: Deterministic workflow registration, explicit invocation, role resolution, routing precedence, validation, and deprecation rules.
tags: [ava, workflows, registry, routing, validation]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T10:32:00Z
---

# Purpose

This instruction defines how workflows become registered, how a request explicitly invokes one workflow, how the router resolves its primary role, and when routing must stop instead of guessing.

Workflow routing is deterministic. Ava does not infer a workflow from semantic similarity to an ordinary request.

# Workflow registry

The canonical workflow registry begins at `/workflows/index.md`.

A workflow is registered only when all of these conditions hold:

- it is a Markdown file beneath `/workflows/`
- it is reachable by following workflow discovery links from `/workflows/index.md`
- every traversed `index.md` lists only its direct child files and directories
- the workflow follows the shared [workflow format](workflow-format.md)
- its path is unique within the project

A workflow file that exists beneath `/workflows/` but is not reachable from the registry is unregistered and must not be invoked.

The workflow file path is its stable identity. Do not add a separate registry file, identifier field, numeric priority, or routing-rule language.

# Registry structure

The root workflow index may link directly to workflow files and to workflow-owning subdirectories.

Each workflow-owning subdirectory must contain an `index.md` that:

- explains the subdirectory's scope
- links to every direct child workflow and child directory
- lists direct children only
- leaves discovery of deeper descendants to their nearest index

A validator must detect broken index links, duplicate links to the same workflow identity, workflow files omitted from their nearest owning index, and index entries that escape `/workflows/`.

# Explicit invocation

A request explicitly invokes a workflow only when it supplies one of these identifiers as the workflow to run:

1. the canonical bundle-root-relative workflow path, such as `/workflows/configure-project.md`
2. a lowercase kebab-case workflow name matching the workflow filename stem, such as `configure-project`

The canonical path always identifies one workflow.

A filename-stem invocation is valid only when exactly one registered, non-deprecated workflow has that stem. If no workflow or more than one workflow matches, routing must stop and report the valid canonical paths.

Workflow titles and descriptions are for humans and semantic discovery. They are not stable invocation identifiers because titles need not be globally unique.

A client may provide a dedicated workflow selector or structured invocation field. The resulting value must still resolve by canonical path or unambiguous filename stem according to this contract.

# Routing precedence

An explicitly invoked registered workflow takes precedence over free-form role selection.

The router must not ignore an explicit workflow invocation and select a role directly from the request. It must first resolve and validate the workflow, then activate the workflow's declared `primary_role`.

When no workflow is explicitly invoked, the router must not guess a workflow. It uses semantic free-form role selection through `/roles/index.md`.

# Workflow-driven routing

For an explicitly invoked workflow, the router must perform these steps in order:

1. Resolve the invocation through the workflow registry.
2. Confirm that the workflow is registered and not deprecated.
3. Validate the workflow metadata and body against the workflow-format contract.
4. Resolve `primary_role` to exactly one registered, non-deprecated `role.md` document.
5. Load the shared instruction-resolution contract.
6. Read the selected role's `index.md` and every document it marks as required.
7. Announce `Active role: <role title>` after the role's complete required reading has been loaded.
8. Load the workflow document and every valid link in its optional `Required context` section.
9. Resolve the workflow inputs supplied by the invocation.
10. Execute the workflow within its declared mode, the active role's authority, cumulative constraints, the user's approved scope, and available workspace capabilities.

The workflow remains the active procedural scope for the duration of the invocation. It does not replace the role as the authority boundary.

# Interactive free-form routing

For a request without an explicit workflow invocation, the router must:

1. read `/roles/index.md`
2. semantically compare the request with the registered roles' stated purposes and activation conditions
3. resolve exactly one active role or ask the user when the choice is materially ambiguous
4. load and announce that role before acting

A free-form request may have the same intent as a known workflow without invoking it. In that case the role may perform ordinary work within its durable instructions, but the workflow's procedure, inputs, mode, required context, and expected output are not active.

# Registered role resolution

A role is registered when its direct child directory is linked from `/roles/index.md` and its role index exposes the required role documents.

A workflow `primary_role` must:

- be one bundle-root-relative path
- point directly to a `role.md` document
- remain beneath `/roles/`
- resolve to a role registered through `/roles/index.md`
- resolve to a role whose status is not `deprecated`

The router must not use a workflow title, role title, directory-name guess, `replaced_by` value, or semantic similarity to repair an invalid `primary_role` reference.

# Input resolution

The invocation must provide every required workflow input.

The router may apply declared defaults for omitted optional inputs. It must not invent a value for a missing required input or reinterpret an invalid value without user confirmation.

Input values refine the workflow's bounded procedure. They must not change the active role, expand capabilities, weaken constraints, or change the workflow mode.

# Failure behavior

Routing must stop before execution when:

- the workflow invocation is unresolved or ambiguous
- the resolved file is not registered
- the workflow is deprecated
- required workflow metadata or body structure is invalid
- `primary_role` is missing, malformed, unresolved, unregistered, or deprecated
- a required-context link is broken
- a required input is missing
- the procedure contradicts the declared mode
- the workflow attempts role composition, delegation, or a role transition
- an active authority or instruction conflict remains unresolved

A failed explicit workflow invocation must not fall back to free-form role selection. The router must report the blocking reason and the user decision or correction required.

# Deprecation and replacement

A deprecated workflow remains registered and discoverable for history and existing references, but it must not execute.

When a direct replacement exists, the deprecated workflow may declare:

```yaml
status: deprecated
replaced_by: /workflows/new-workflow.md
```

`replaced_by` must resolve to one registered workflow whose status is not `deprecated`.

The router must report the replacement but must not redirect automatically. The replacement may have different inputs, mode, required context, procedure, primary role, or expected output, so invoking it requires an explicit new selection.

A workflow whose `primary_role` is deprecated is invalid. The router must not automatically follow the role's `replaced_by` value. The workflow must be explicitly migrated to a valid registered role and reviewed as a workflow contract change.

When a workflow is renamed or moved:

1. create the replacement at its new canonical path
2. keep the old workflow as deprecated when existing references may remain
3. set `replaced_by` on the old workflow
4. update affected workflow indexes and known references
5. record the lifecycle change in the nearest relevant scoped log

Removing a deprecated workflow is an explicit compatibility decision. Do not remove it merely because a replacement exists. Remove it only after the approved migration scope confirms that retained references and history no longer require the old path.

# Validation

Treat these as errors or blocking findings:

- missing `/workflows/index.md`
- a workflow path that is not reachable through the workflow registry
- a workflow registry link that is broken, duplicated, escapes `/workflows/`, or bypasses direct-child indexing
- an explicit workflow name resolving to zero or multiple registered workflows
- invocation of a deprecated workflow
- malformed workflow metadata or body structure
- a `primary_role` that does not resolve to exactly one registered, non-deprecated `role.md`
- a broken required-context link
- a missing required input
- automatic fallback from a failed workflow invocation to role selection
- automatic redirection through `replaced_by`

Treat these as warnings or semantic findings:

- a draft workflow being invoked
- multiple registered workflows sharing a filename stem, because shorthand invocation becomes unavailable
- workflow titles or descriptions that make discovery unclear
- a deprecated workflow without a replacement
- references to a deprecated workflow outside the known migration scope

Semantic ambiguity involving authority, policy, destructive action, or compatibility must remain blocking until the user resolves it.

# Examples

Given these registered workflows:

```text
/workflows/configure-project.md
/workflows/reviews/review-change.md
```

These invocations are valid:

```text
/workflows/configure-project.md
configure-project
/workflows/reviews/review-change.md
review-change
```

If both of these exist:

```text
/workflows/project/review-change.md
/workflows/roles/review-change.md
```

then `review-change` is ambiguous. The caller must use one canonical path.

If `/workflows/configure-project.md` is deprecated and replaced by `/workflows/configure-shared-guidance.md`, the router reports the replacement and stops. It does not invoke the replacement automatically.
