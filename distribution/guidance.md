---
type: Distribution Contract
title: Ava Release Guidance
description: Defines installed semantic-upgrade guidance, its release metadata, discovery, composition, and completion contract.
tags: [ava, distribution, releases, guidance, upgrades, migration]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Ava Release Guidance

This contract defines the Ava-managed guidance used by the Upgrade Role to reconcile project-owned context after deterministic installation of a new Ava base. It implements the semantic state defined by [Ava Versioning and Compatibility](versioning.md) and the transaction boundary defined by [Ava Upgrade and Migration Protocol](upgrades.md).

Release guidance is explicit migration input. Scoped `log.md` files and release notes may explain history, but agents and tooling must not infer migration obligations from arbitrary historical prose.

# Installed location and identity

Each supported source-to-target edge installs one canonical guidance document at:

```text
/.ava/guidance/<from_version>-to-<to_version>/UPGRADE.md
```

The containing release manifest lists the relative path and SHA-256 value in `guidance.entries`. Every applicable upgrade edge lists the same path in `guidance_paths`. The updater copies the resolved relative paths into `/.ava/state/upgrade.json` before managed mutation. The managed router resolves each recorded path beneath `/.ava/guidance/`.

The canonical guidance identity is the installed path. `guidance_id` is a stable release-local identifier used for validation, composition, and reporting.

# Required metadata

Every `UPGRADE.md` begins with YAML frontmatter equivalent to the object validated by [`guidance.schema.json`](schemas/guidance.schema.json):

```yaml
---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.4.2 to 2.0.0
description: Reconciles project-owned Ava context with the 2.0.0 managed base.
guidance_schema: 1
guidance_id: 1.4.2-to-2.0.0
from_version: 1.4.2
to_version: 2.0.0
semantic_review_required: true
migration_ids:
  - manifest-v1-to-v2
supersedes: []
generated:
  by: agent:ava-release
  at: 2026-07-31T15:35:00+02:00
---
```

Rules:

- `from_version` and `to_version` must match the release edge that references the document.
- `guidance_id` must be unique within the release guidance archive.
- Every `migration_ids` entry must be declared by the referencing upgrade edge. The field lists the deterministic migrations whose project-facing semantic effects this document explains.
- `semantic_review_required` must agree with the containing release declaration and the edge's guidance requirements.
- `supersedes` may name earlier guidance IDs only when every superseded obligation is restated or explicitly declared no longer applicable.
- Unknown valid metadata must be preserved for forward compatibility.

# Required sections

The guidance body contains these non-empty level-two sections in this order:

1. `Summary`
2. `Changed managed contracts`
3. `Affected project-owned concepts`
4. `Required decisions`
5. `Semantic migration procedure`
6. `Validation and completion criteria`
7. `Rollback implications`

Use `None.` when a section has no entries. Do not omit the section.

## Summary

State the behavioral reason for the upgrade, the source and target versions, and whether project-owned semantic work is required.

## Changed managed contracts

For each relevant managed change, state:

- the exact managed path or contract identity
- the previous and target behavior
- the compatibility impact
- the related deterministic migration ID when present

This section describes impact. It must not instruct the Upgrade Role to customize managed payload files.

## Affected project-owned concepts

Identify every project-owned concept class that may require inspection or change, including roles, workflows, registries, shared instructions, knowledge, indexes, logs, metadata, links, filenames, and structural conventions.

Each entry must state:

- the concept or path scope
- the condition that makes it affected
- the required semantic outcome
- how completion is validated

A blanket instruction to scan or rewrite the entire project is invalid. Guidance must provide bounded discovery conditions while still covering every affected relationship.

## Required decisions

Each decision uses a stable lowercase identifier and states:

- the decision needed
- why existing project intent and release guidance are insufficient
- which files or completion criteria are blocked
- the allowed choices when they are known

A decision is blocking unless the guidance explicitly marks it advisory. Blocking decisions must be copied into `semantic_compatibility.unresolved_decisions` before the Upgrade Role reports `blocked`.

## Semantic migration procedure

Define the ordered semantic operations unique to this release edge. Reference authoritative managed contracts rather than duplicating their durable instructions.

The procedure must distinguish:

- required edits
- optional recommendations
- user decisions
- deterministic work already completed by the updater

## Validation and completion criteria

List explicit criteria that must all pass before semantic compatibility advances to the target version. Criteria must cover every affected project-owned registry, index, reference, metadata field, structural convention, and unresolved decision.

A successful structural parse is insufficient when the release changes meaning, authority, routing, or behavior.

## Rollback implications

Explain whether project-owned edits remain compatible with the source release and which paths require explicit reconciliation before rollback can reach a safe terminal state.

# Multi-version composition

For a chained upgrade, the Upgrade Role loads guidance in the exact order recorded by the transaction path.

- Every non-superseded obligation remains cumulative.
- A later document may supersede an earlier guidance ID only through explicit `supersedes` metadata.
- Supersession never hides unresolved user decisions or removes required source compatibility work unless the later document states the replacement obligation and completion test.
- If complete composition cannot be proven, the updater must reject the chained path during preflight.

# Role activation boundary

Guidance does not activate a workflow or role by itself.

The root managed router checks `upgrade.json` and manifest semantic state before ordinary routing. When upgrade mode is required, it activates `/.ava/base/roles/upgrade-role/role.md` directly, then the Upgrade Role resolves the recorded relative guidance paths beneath `/.ava/guidance/` and loads only those documents.

Project-owned role and workflow registries are migration inputs after activation. They are never required to discover or authorize the Upgrade Role.

# Canonical user request

The supported one-prompt semantic migration request is:

```text
Reconcile this project's project-owned Ava context with the installed Ava version. Apply the installed upgrade guidance, explain material semantic changes, and report unresolved decisions before marking semantic migration complete.
```

The request authorizes changes required by the installed source-to-target guidance. It does not authorize unrelated project maintenance or invention of project-specific semantics.

# Logs and release notes

Scoped `log.md` files may supply historical rationale to release authors. Release notes may summarize user-visible changes. Neither is the migration protocol.

No additional `log.md` metadata is required. Upgrade obligations, affected concepts, decisions, procedures, and completion criteria must be written explicitly in `UPGRADE.md` and validated against this contract.

# Validation

Treat these as errors:

- a referenced guidance path is absent from the guidance archive or its SHA-256 inventory
- guidance metadata fails `guidance.schema.json`
- source or target version disagrees with the referencing edge
- `semantic_review_required` or `migration_ids` disagree with release metadata
- required sections are missing, empty, duplicated, or out of order
- an affected concept lacks a discovery condition, required outcome, or completion test
- a blocking decision lacks a stable identifier
- a completion criterion depends on arbitrary log interpretation
- guidance instructs deterministic tooling to modify project-owned content
- guidance instructs the Upgrade Role to customize managed payload
- a chained path contains guidance that cannot be composed safely

Treat vague impact descriptions, unbounded scanning, missing rollback implications, and optional recommendations presented as mandatory as blocking semantic findings.
