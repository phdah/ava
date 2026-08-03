---
type: Shared Instruction
title: Workflow Lifecycle
description: Defines ownership, lifecycle procedures, approval boundaries, migration behavior, and completion checks for project-owned workflows.
tags: [ava, workflows, lifecycle, ownership, migration]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T13:52:00+02:00
---

# Purpose

This instruction defines who maintains workflows and how project-owned workflows are created, updated, repaired, reorganized, renamed, deprecated, replaced, removed, and migrated.

It applies the durable contracts in [Workflow format](workflow-format.md), [Workflow registry and routing](workflow-routing.md), [Workflow triggers](workflow-triggers.md), [Document metadata](document-metadata.md), [Ownership and mutation authority](ownership-and-mutation.md), and [Scoped history](scoped-history.md). It does not restate their schemas or routing algorithms.

# Lifecycle ownership

The Project Steward owns the lifecycle of project-owned workflows under `/workflows/`.

A dedicated Workflow Manager role is not justified because workflow lifecycle work uses the same project-wide authority, trusted context, discovery structures, and policy boundary already assigned to the Project Steward. A separate role would overlap rather than establish a distinct trust or separation-of-duty boundary.

Adjacent responsibilities remain separate:

- the Role Manager owns role definitions and role lifecycle, including changes to a workflow's primary role when that role itself must change
- the Change Reviewer provides independent semantic review and must remain separate from authoring or remediation
- the Upgrade Role applies release-specific semantic changes to project-owned workflows during active upgrade mode and exclusively updates semantic compatibility state
- deterministic installers and updaters replace Ava-managed workflows and run mechanical migrations
- deterministic validators check structure, metadata, links, registries, and references without deciding semantic purpose or authority

Routine workflow lifecycle work is free-form Project Steward work. Ava does not add a workflow-maintenance workflow because that would duplicate the role's durable procedure. Semantic Ava version reconciliation also remains direct Upgrade Role activation rather than a workflow.

# Ownership boundary

Before changing a workflow, classify it by installed path and manifest state.

- workflows under `/.ava/base/workflows/` are Ava-managed and must not be customized by the Project Steward
- workflows under `/workflows/` are project-owned and may be maintained within the current user-approved scope
- a writable file does not imply mutation authority
- a local edit to an Ava-managed workflow is a managed-file conflict, not project-owned customization

Changes to managed workflow payloads belong to Ava release development and deterministic release installation. Project-specific behavior belongs in a project-owned workflow or ordinary project guidance.

# Required inspection

Before applying a lifecycle change, inspect only the relevant scope:

1. Read the managed and project-owned workflow registries to establish canonical identity, ambiguity, and discovery.
2. Read the target workflow, its nearest index, and its nearest scoped log when present.
3. Resolve the workflow's `primary_role` through the role registry. Read that role's index and complete required instruction set when assessing authority, mode, procedure, or expected output.
4. Inspect workflows with the same filename stem, materially overlapping purpose, the same primary role, or known cross-references.
5. Resolve every required-context link and inspect context whose meaning or path is affected.
6. Find known references to the canonical workflow path, invocation name, old path, or `replaced_by` relationship.
7. Read installed release guidance when the change is part of an active semantic migration.
8. Identify portable trigger declarations and any known external binding owner that may require a coordinated configuration change.

Do not scan the complete project when indexes, references, and targeted search define a sufficient scope.

# Lifecycle procedure

For every workflow lifecycle request:

1. Classify the operation as creation, update, repair, reorganization, rename, deprecation, replacement, removal, or migration.
2. Confirm that the target is project-owned and that Project Steward authority applies.
3. Inspect the required lifecycle context above.
4. Confirm that the workflow satisfies the workflow admission criteria and adds reusable procedural value beyond ordinary role work.
5. Determine the intended identity, primary role, operating mode, inputs, required context, procedure, expected output, triggers, lifecycle status, and compatibility impact.
6. Identify ambiguity or conflict affecting authority, destructive behavior, routing, trigger behavior, compatibility, ownership, or removal.
7. Obtain a user decision when the approval boundaries below require one.
8. Apply the smallest coherent change while preserving unknown valid metadata and existing decisions outside the approved scope.
9. Synchronize the workflow registry, nearest indexes, canonical links, affected references, deprecation metadata, and scoped history.
10. Use deterministic validation when available and perform direct structural checks until such tooling exists.
11. Report the lifecycle operation, behavior or compatibility impact, validation result, external follow-up, and unresolved decisions.

# Operation rules

## Creation

Create a project-owned workflow only when it satisfies every workflow admission criterion.

- choose one canonical path beneath `/workflows/`
- use exactly one registered, non-deprecated ordinary primary role
- define the narrowest mode consistent with the intended effect
- keep role authority and safeguards in the role rather than duplicating them in the workflow
- register the workflow through the nearest direct-child index
- check shorthand-name ambiguity across managed and project-owned registries
- add portable trigger metadata only when the trigger intent is useful outside one executor configuration

When ordinary free-form role work already represents the request, do not create a workflow merely to provide a command-like name.

## Update and repair

An update changes intended workflow behavior. A repair restores an already established contract without changing intended behavior.

For both operations:

- preserve canonical identity unless rename or replacement is explicitly intended
- preserve unknown valid metadata
- repair broken registry, role, context, input, trigger, and reference relationships together
- reassess admission criteria when procedure or expected output has become equivalent to ordinary role work
- classify behavior and compatibility impact rather than treating every structurally valid edit as safe

## Reorganization

Reorganize workflow directories only when the new structure improves current discovery or ownership.

- update each affected direct-child index
- keep canonical path changes subject to rename and compatibility rules
- do not move workflows only to create a speculative taxonomy
- preserve cross-references, scoped history, and project-owned status

## Rename, deprecation, and replacement

A workflow path is its stable identity.

When a published or referenced workflow identity changes:

1. create the workflow at the new canonical path
2. keep the old workflow as deprecated while supported references may remain
3. set `replaced_by` to the new canonical workflow path when a direct replacement exists
4. update affected indexes and known references
5. record the identity change in the nearest scoped log
6. report that routing must not automatically follow `replaced_by`

A replacement may change primary role, mode, inputs, context, triggers, procedure, or expected output. It therefore requires explicit invocation and normal validation.

## Removal

Remove a project-owned workflow only when:

- the user has explicitly approved removal or requested an unambiguous removal operation
- no unresolved authority, compatibility, history, or ownership question remains
- retained references have been migrated or intentionally preserved
- the nearest registry and indexes are updated
- unique rationale or history remains available where required

Prefer deprecation before removal when callers, external bindings, documentation, or unknown references may still depend on the old identity.

Managed workflow removal follows the Ava SemVer and deprecation contract and is performed through a release, not by the Project Steward.

## Migration

A workflow migration may be mechanical, semantic, or both.

- deterministic tooling owns managed-file replacement, fixed path transforms, schema-state transitions, and structural validation
- semantic changes to project-owned workflow purpose, role resolution, mode, inputs, triggers, authority implications, and intended behavior require an active role
- during active Ava upgrade mode, the Upgrade Role follows installed release guidance and owns the project-owned semantic migration
- the Project Steward must not update `semantic_compatibility` or claim release migration completion
- outside active upgrade mode, the Project Steward may perform user-requested project-owned workflow migration under this lifecycle procedure

Release guidance must identify affected project-owned workflows, discovery conditions, required outcomes, decisions, and completion checks. The Project Steward must not infer release obligations from arbitrary logs or release history.

# Approval boundaries

An explicit user request counts as approval only when it unambiguously authorizes the specific change.

Stop and obtain a user decision before:

- changing `primary_role` in a way that changes the workflow's authority boundary
- changing `mode`, especially into or out of `mutation`
- adding, broadening, or obscuring destructive behavior
- adding or changing schedule or event trigger intent that may cause new automatic invocation
- removing a trigger when an external executor may still depend on it
- changing required inputs, defaults, procedure, or expected output in a compatibility-sensitive way
- resolving ambiguous workflow purpose, ownership, routing, or overlap
- renaming, replacing, deprecating, or removing a workflow when the requested lifecycle outcome is uncertain
- discarding unique history or unresolved references
- applying an incompatible migration not already authorized by the current request or active release guidance

Structural repair that preserves established behavior does not require a new decision when the intended result is clear.

# Records and references

Keep these relationships synchronized when affected:

- project-owned workflow registry entries and direct-child indexes
- canonical workflow paths and shorthand-name ambiguity
- `primary_role` and required-context links
- related workflow documentation and known invocation examples
- portable trigger declarations and known external binding documentation
- lifecycle metadata, including `status`, `replaced_by`, and release-bound deprecation fields when applicable
- nearest scoped `log.md` for identity, authority, routing, lifecycle, or stable structural changes
- release guidance completion evidence during Upgrade Role work

Only the Upgrade Role may update semantic compatibility state. Only deterministic tooling may update installed release identity and managed-file state.

# Compatibility

Workflow changes follow [Ava Versioning and Compatibility](../../../../distribution/versioning.md) and [Ava Release Guidance](../../../../distribution/guidance.md).

For managed workflows after `1.0.0`:

- behavior-preserving corrections may be PATCH
- backward-compatible additions require proof that supported routing, authority, validation, and behavior remain unchanged or explicitly opt-in
- changes to identity, primary role, mode, required inputs, routing, trigger discovery, intended behavior, removal, or replacement behavior are generally MAJOR
- deprecation may be introduced compatibly, but removal waits for the permitted later MAJOR version

Project-owned workflows are not independently assigned Ava release versions. They must still be reconciled when a release changes the contracts or role paths they rely on.

# Completion checks

Before completing workflow lifecycle work, verify that:

- every changed workflow remains in the correct ownership class
- the workflow still satisfies the admission criteria or has been intentionally deprecated or removed
- exactly one registered, non-deprecated ordinary primary role resolves
- mode, procedure, expected output, and actual requested effect agree
- required inputs and required-context links are complete and valid
- trigger metadata remains portable and does not embed executor configuration
- managed and project-owned workflow registries remain separate and accurate
- canonical paths, indexes, references, and `replaced_by` relationships are consistent
- no deprecated workflow is automatically redirected or executed
- approval-sensitive changes were explicitly authorized
- deterministic tooling responsibilities were not reproduced as semantic workflow steps
- active upgrade work remained with the Upgrade Role and semantic state was updated only by that role
- independent review was not implied by the Project Steward's own maintenance pass
- unresolved decisions and external binding follow-up are reported
