---
type: Shared Instruction
title: Workflow Registry and Routing
description: Deterministic managed and project-owned workflow registration, explicit invocation, external trigger discovery, role resolution, routing precedence, validation, and deprecation rules.
tags: [ava, workflows, registry, routing, validation]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T14:10:00+02:00
---

# Purpose

This instruction defines how managed and project-owned workflows become registered, how a request or external executor explicitly invokes one workflow, how the router resolves its primary role, and when routing must stop instead of guessing.

Workflow routing is deterministic. Ava does not infer a workflow from semantic similarity to an ordinary request.

Portable trigger discovery and executor ownership follow [Workflow triggers](workflow-triggers.md).

# Workflow registries

The managed workflow registry begins at:

```text
/.ava/base/workflows/index.md
```

The project-owned workflow registry begins at `/workflows/index.md` when present.

A managed workflow is registered only when all of these conditions hold:

- it is a non-reserved Markdown document with `type: Workflow` beneath `/.ava/base/workflows/`
- it is reachable by following workflow discovery links from `/.ava/base/workflows/index.md`
- every traversed `index.md` lists only its direct child files and directories
- the workflow follows the shared [Workflow format](workflow-format.md)
- its path is unique within the managed registry

A project-owned workflow is registered only when the equivalent conditions hold beneath `/workflows/` and it is reachable from `/workflows/index.md`.

A workflow file that exists beneath either workflow root but is not reachable from its corresponding registry is unregistered and must not be invoked.

The workflow file path is its stable identity. Do not add a separate registry file, identifier field, numeric priority, or routing-rule language.

Managed and project-owned registries remain separate ownership scopes. Registration and name resolution inspect both registries without giving either ownership class precedence.

# Registry structure

Each registry root may link directly to workflow files and to workflow-owning subdirectories.

Each workflow-owning subdirectory must contain an `index.md` that:

- explains the subdirectory's scope
- links to every direct child workflow and child directory
- lists direct children only
- leaves discovery of deeper descendants to their nearest index

A validator must detect broken index links, duplicate links to the same workflow identity, workflow files omitted from their nearest owning index, and entries that escape the registry's workflow root.

# Explicit invocation

A request explicitly invokes a workflow only when it supplies one of these identifiers as the workflow to run:

1. a canonical bundle-root-relative workflow path, such as `/.ava/base/workflows/review-change.md` or `/workflows/review-deployment.md`
2. a lowercase kebab-case workflow name matching the workflow filename stem, such as `review-change`

A canonical path always identifies at most one workflow.

A filename-stem invocation is valid only when exactly one registered, non-deprecated workflow across both registries has that stem. If no workflow or more than one workflow matches, routing must stop and report the valid canonical paths.

Workflow titles and descriptions are for humans and semantic discovery. They are not stable invocation identifiers because titles need not be globally unique.

A client may provide a dedicated workflow selector or structured invocation field. The resulting value must still resolve by canonical path or unambiguous filename stem according to this contract.

# External trigger discovery and invocation

An external executor may inspect registered workflows for portable `triggers` metadata according to [Workflow triggers](workflow-triggers.md).

Discovery does not invoke a workflow. A matching trigger declaration only states that the workflow is suitable for that trigger kind.

When an external executor invokes a discovered workflow, it must:

1. retain and submit the canonical workflow path
2. provide every required workflow input
3. identify the invocation as explicit rather than free-form role work
4. allow the normal managed upgrade-state, registration, validation, routing, role, authority, approval, and capability checks to run

An executor must not use trigger metadata to bypass routing or execute an unregistered, invalid, deprecated, or blocked workflow.

Ava does not validate or operate the external scheduler or event binding. It validates only the portable workflow declaration and the resulting explicit workflow invocation.

# Routing precedence

The managed upgrade-state check runs before ordinary workflow or role routing. When the upgrade protocol does not permit normal operation, workflow discovery and invocation remain blocked and the managed Upgrade Role is selected directly.

When normal operation is permitted, an explicitly invoked registered workflow takes precedence over free-form role selection.

The router must not ignore an explicit workflow invocation and select a role directly from the request. It must first resolve and validate the workflow, then activate the workflow's declared `primary_role`.

When no workflow is explicitly invoked, the router must not guess a workflow. It uses semantic free-form role selection across the managed and project-owned role registries.

# Workflow-driven routing

After the root router has loaded the instruction-resolution and workflow-routing contracts, an explicitly invoked workflow must be processed in this order:

1. Confirm that managed upgrade state permits normal routing.
2. Resolve the invocation through the managed and project-owned workflow registries.
3. Confirm that the workflow is registered and not deprecated.
4. Validate the workflow metadata and body against the workflow-format and workflow-trigger contracts.
5. Resolve `primary_role` to exactly one registered, non-deprecated ordinary `role.md` document.
6. Reject a role whose activation contract reserves managed pre-routing.
7. Read the selected role's `index.md` and every document it marks as required.
8. Announce `Active role: <role title>` after the role's complete required reading has been loaded.
9. Load the workflow document and every valid link in its optional `Required context` section.
10. Resolve the workflow inputs supplied by the invocation.
11. Execute the workflow within its declared mode, the active role's authority, cumulative constraints, the user's approved scope, and capabilities exposed by the host agent and its available tools.

The workflow remains the active procedural scope for the duration of the invocation. It does not replace the role as the authority boundary.

# Interactive free-form routing

For a request without an explicit workflow invocation, the router must:

1. read the managed role registry at `/.ava/base/roles/index.md`
2. read the project-owned role registry at `/roles/index.md` when present
3. exclude roles whose activation contract reserves direct managed activation
4. semantically compare the request with the registered ordinary roles' stated purposes and activation conditions
5. resolve exactly one active role or ask the user when the choice is materially ambiguous
6. load and announce that role before acting

A free-form request may have the same intent as a known workflow without invoking it. In that case the role may perform ordinary work within its durable instructions, but the workflow's procedure, inputs, mode, required context, triggers, and expected output are not active.

# Registered role resolution

A managed role is registered when its direct child directory is linked from `/.ava/base/roles/index.md` and its role index exposes the required role documents.

A project-owned role is registered when the equivalent conditions hold beneath `/roles/` and it is linked from `/roles/index.md`.

A workflow `primary_role` must:

- be one bundle-root-relative path
- point directly to a `role.md` document
- remain beneath `/.ava/base/roles/` or `/roles/`
- resolve to a role registered through the corresponding role registry
- resolve to a role whose status is not `deprecated`
- resolve to an ordinary role whose activation is valid during normal routing

The router must not use a workflow title, role title, directory-name guess, ownership precedence, `replaced_by` value, or semantic similarity to repair an invalid `primary_role` reference.

# Input resolution

The invocation must provide every required workflow input.

The router may apply declared defaults for omitted optional inputs. It must not invent a value for a missing required input or reinterpret an invalid value without user confirmation.

Input values refine the workflow's bounded procedure. They must not change the active role, expand capabilities, weaken constraints, or change the workflow mode.

# Failure behavior

Routing must stop before execution when:

- managed upgrade state blocks normal routing
- the workflow invocation is unresolved or ambiguous
- the resolved file is not registered
- the workflow is deprecated
- required workflow metadata, trigger metadata, or body structure is invalid
- `primary_role` is missing, malformed, unresolved, unregistered, deprecated, or reserved for managed pre-routing
- a required-context link is broken
- a required input is missing
- the procedure contradicts the declared mode
- the workflow attempts role composition, delegation, or a role transition
- an external executor attempts to bypass normal invocation checks
- an active authority or instruction conflict remains unresolved

A failed explicit workflow invocation must not fall back to free-form role selection. The router must report the blocking reason and the user decision or correction required.

# Deprecation and replacement

A deprecated workflow remains registered and discoverable for history and existing references, but it must not execute.

When a direct replacement exists, the deprecated workflow may declare:

```yaml
status: deprecated
replaced_by: /.ava/base/workflows/new-workflow.md
```

`replaced_by` must resolve to one registered workflow whose status is not `deprecated`.

The router must report the replacement but must not redirect automatically. The replacement may have different inputs, mode, required context, procedure, primary role, triggers, or expected output, so invoking it requires an explicit new selection.

A workflow whose `primary_role` is deprecated or reserved for managed pre-routing is invalid. The router must not automatically follow the role's `replaced_by` value. The workflow must be explicitly migrated to a valid registered ordinary role and reviewed as a workflow contract change.

When a workflow is renamed or moved after publication:

1. create the replacement at its new canonical path
2. keep the old workflow as deprecated when existing references may remain
3. set `replaced_by` on the old workflow
4. update affected workflow indexes and known references
5. record the lifecycle change in the nearest relevant scoped log
6. provide release notes and upgrade guidance when managed or project-owned references may require migration

Removing a deprecated workflow is an explicit compatibility decision. Do not remove it merely because a replacement exists. Remove it only after the versioning and migration scope permits removal and retained references and history no longer require the old path.

# Validation

Treat these as errors or blocking findings:

- missing `/.ava/base/workflows/index.md`
- a workflow path that is not reachable through its corresponding workflow registry
- a workflow registry link that is broken, duplicated, escapes its workflow root, or bypasses direct-child indexing
- an explicit workflow name resolving to zero or multiple registered workflows
- invocation of a deprecated workflow
- malformed workflow metadata, trigger metadata, or body structure
- a `primary_role` that does not resolve to exactly one registered, non-deprecated ordinary `role.md`
- a workflow referencing a role reserved for managed pre-routing
- a broken required-context link
- a missing required input
- automatic fallback from a failed workflow invocation to role selection
- automatic redirection through `replaced_by`
- an external executor invoking an inferred workflow rather than an explicit canonical path

Treat these as warnings or semantic findings:

- a draft workflow being invoked
- multiple registered workflows sharing a filename stem, because shorthand invocation becomes unavailable
- workflow titles, descriptions, or trigger descriptions that make discovery unclear
- a deprecated workflow without a replacement
- references to a deprecated workflow outside the known migration scope
- a registered workflow that appears to duplicate ordinary role work rather than satisfy the workflow admission criteria
- an external binding that cannot be verified from portable Ava context

Semantic ambiguity involving authority, policy, destructive action, or compatibility must remain blocking until the user resolves it.

# Examples

Given these registered workflows:

```text
/.ava/base/workflows/review-change.md
/workflows/review-deployment.md
```

These invocations are valid:

```text
/.ava/base/workflows/review-change.md
review-change
/workflows/review-deployment.md
review-deployment
```

An external executor that discovers a matching trigger should retain and invoke the canonical path:

```text
/.ava/base/workflows/review-change.md
```

It must not infer another workflow from the event payload or invoke a title.

If both of these exist:

```text
/.ava/base/workflows/review-change.md
/workflows/review-change.md
```

then `review-change` is ambiguous. The caller must use one canonical path.

If `/.ava/base/workflows/old-audit.md` is deprecated and replaced by `/.ava/base/workflows/audit-project-context.md`, the router reports the replacement and stops. It does not invoke the replacement automatically.
