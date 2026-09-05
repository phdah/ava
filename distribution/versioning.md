---
type: Distribution Contract
title: Ava Versioning and Compatibility
description: Defines Ava SemVer, installed manifest state, semantic compatibility, upgrade-path compatibility, deprecation, and support guarantees.
tags: [ava, distribution, semver, compatibility, manifest, upgrades]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T11:49:00+02:00
---

# Ava Versioning and Compatibility

This document defines how Ava versions its managed distribution, records installed state, classifies compatible and incompatible changes, and distinguishes a successful base upgrade from completed migration of project-owned context.

The distribution and ownership paths are defined by [Ava Distribution and Ownership Boundary](ownership.md). Release assets and bootstrap trust are defined by [Ava GitHub Release Assets](releases.md). Upgrade transaction mechanics are defined by [Ava Upgrade and Migration Protocol](upgrades.md), and semantic guidance is defined by [Ava Release Guidance](guidance.md). Those contracts must preserve the state and authority rules established here.

# Version identities

Ava uses three separate version identities.

## Ava version

`ava_version` is a Semantic Versioning value that identifies the installed Ava-managed base distribution.

It covers the mutually compatible managed router, base roles, workflows, shared instructions, guidance, state schema, migrations, and other managed release content. It does not describe whether project-owned context has completed semantic migration.

`ava_version` changes only after deterministic installation or base-upgrade work succeeds.

## Semantic compatibility

Semantic compatibility describes how far the project-owned roles, workflows, shared instructions, knowledge, and other context have been reconciled with the installed Ava contracts.

A project may therefore validly report:

```text
Installed Ava base: 2.0.0
Project context compatible through: 1.4.2
Semantic migration: pending for 2.0.0
```

This state must never be reported as fully migrated.

## OKF version

`okf_version` identifies the Open Knowledge Format compatibility level used by the installed Ava base. It is independent from `ava_version`.

An Ava release may change `okf_version` only under the SemVer classification rules in this contract. The installed OKF value is recorded in the managed manifest and declared by the managed base index.

# Installed manifest

The canonical installed state file is:

```text
/.ava/state/manifest.json
```

It is Ava-managed and conforms to [`distribution/schemas/manifest.schema.json`](schemas/manifest.schema.json) in the source repository.

The manifest is both:

- the ownership inventory for installed Ava-managed files
- the authoritative installed-base and semantic-compatibility state

The manifest must not contain project-specific configuration other than the bounded semantic compatibility state and optional project-owned host integration metadata defined by the public schemas.

## Manifest fields

The manifest contains:

- `manifest_schema`: integer schema revision for this JSON document
- `ava_version`: installed Ava-managed base version
- `okf_version`: installed OKF compatibility version
- `installed_at`: timestamp of the completed install or base upgrade
- `release`: immutable identity of the installed release
- `managed_files`: complete installed Ava-managed file inventory
- `host_integration`: optional metadata for one existing project-owned host entrypoint, or `null`
- `semantic_compatibility`: separate project-context compatibility state

Published `ava_version` values use canonical SemVer without build metadata. Git tags use the same version prefixed by `v`.

## Release identity

`release` contains:

- `tag`: canonical Git tag such as `v1.2.0` or `v2.0.0-rc.1`
- `channel`: `stable`, `rc`, `beta`, or `alpha`
- `source_revision`: full Git commit SHA used to build the release
- `release_manifest_sha256`: SHA-256 of the release manifest asset

The release-assets contract defines how this identity is authenticated and how assets prove they came from the same source revision.

## Managed file entries

Each `managed_files` entry contains:

- `path`: canonical project-root-relative absolute path
- `role`: semantic release role such as `router`, `base`, `guidance`, `migration`, or `state`
- `kind`: `payload` or `state`
- `sha256`: required only for `payload`

`payload` identifies release content that must remain byte-for-byte equal to the installed release baseline. The updater uses its SHA-256 checksum to detect local modification, deletion, or corruption before replacement.

`state` identifies Ava-managed mutable state whose validity depends on schema, authority, and allowed transitions rather than byte equality to an immutable release copy.

`/.ava/state/manifest.json` and `/.ava/state/upgrade.json` are recorded as `state`. They must not contain their own checksums. A self-checksum cannot stabilize because writing the checksum changes the file and therefore changes the checksum again.

All other managed files are `payload` unless another public contract explicitly defines a mutable state file.

## Host integration metadata

`host_integration` is either `null` or a bounded reference to one project-owned host instruction file:

- `entrypoint`: normalized project-root-relative absolute path
- `ownership`: always `project-owned`
- `discovery`: always `project-provided`

The entrypoint is not part of `managed_files`, carries no Ava checksum, and is never created, modified, migrated, backed up, restored, or rolled back by deterministic Ava tooling.

## Example manifest

```json
{
  "manifest_schema": 1,
  "ava_version": "2.0.0",
  "okf_version": "0.2",
  "installed_at": "2026-07-31T12:08:00+02:00",
  "release": {
    "tag": "v2.0.0",
    "channel": "stable",
    "source_revision": "0123456789abcdef0123456789abcdef01234567",
    "release_manifest_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
  },
  "managed_files": [
    {
      "path": "/AGENTS.md",
      "role": "router",
      "kind": "payload",
      "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    },
    {
      "path": "/.ava/state/manifest.json",
      "role": "state",
      "kind": "state"
    },
    {
      "path": "/.ava/state/upgrade.json",
      "role": "state",
      "kind": "state"
    }
  ],
  "host_integration": {
    "entrypoint": "/CODEX.md",
    "ownership": "project-owned",
    "discovery": "project-provided"
  },
  "semantic_compatibility": {
    "compatible_through": "1.4.2",
    "target_version": "2.0.0",
    "status": "pending",
    "unresolved_decisions": []
  }
}
```

# Semantic compatibility state

`semantic_compatibility` contains:

- `compatible_through`: highest Ava version whose semantic contracts the project-owned context has completed
- `target_version`: installed version currently requiring semantic reconciliation, or `null`
- `status`: `complete`, `pending`, `partial`, or `blocked`
- `unresolved_decisions`: explicit user decisions or external conditions preventing completion

## State invariants

### Complete

When `status` is `complete`:

- `compatible_through` equals `ava_version`
- `target_version` is `null`
- `unresolved_decisions` is empty

### Pending

`pending` means required semantic review has not started.

- `compatible_through` is lower than `ava_version`
- `target_version` equals `ava_version`
- `unresolved_decisions` is empty

### Partial

`partial` means some required project-owned changes have been applied, but completion criteria are not yet satisfied.

- `compatible_through` remains the last fully completed version
- `target_version` equals `ava_version`
- unresolved work is reported in the migration result and may also appear in `unresolved_decisions`

### Blocked

`blocked` means migration cannot continue safely without a user decision, missing prerequisite, unsupported host behavior, or another explicit condition.

- `compatible_through` remains unchanged
- `target_version` equals `ava_version`
- `unresolved_decisions` is non-empty

The state must not use `ava_version` to imply semantic completion.

# Manifest update authority

The manifest is not a normal project document. Manual editing is unsupported.

## Deterministic installer and updater

Deterministic tooling exclusively controls:

- `manifest_schema`
- `ava_version`
- `okf_version`
- `installed_at`
- `release`
- `managed_files`
- `host_integration`

`host_integration` records only validated metadata for a project-owned entrypoint. Control of that metadata does not grant Ava authority over the referenced project file.

During a completed base upgrade it may also perform only these mechanical semantic transitions:

1. When the target release declares no project-owned semantic review and the prior state was `complete`, set `compatible_through` to the target `ava_version` and retain `complete`.
2. When semantic review is required, preserve `compatible_through`, set `target_version` to the installed target, set `status` to `pending`, and initialize `unresolved_decisions` as empty.
3. When an upgrade transaction fails, leave the previously completed manifest authoritative. Temporary transaction state belongs in `upgrade.json`.

The updater must not mark user-dependent semantic work `partial`, `blocked`, or `complete` based on filesystem replacement alone.

## Upgrade Role

The explicit Upgrade Role is the only agent role allowed to update `semantic_compatibility`.

Within the installed source-to-target guidance it may:

- move `pending` to `partial`, `blocked`, or `complete`
- move `partial` to `blocked` or `complete`
- move `blocked` to `partial` or `complete` after its blocking decisions are resolved
- update `unresolved_decisions`
- advance `compatible_through` only when every completion criterion for the target is satisfied
- clear `target_version` only when marking the installed `ava_version` complete

It must not:

- change release identity, installed-base fields, managed paths, checksums, or host integration metadata
- reduce `compatible_through`
- mark a version complete while unresolved decisions remain
- claim compatibility beyond the installed `ava_version`

The Upgrade Role definition and exact reconciliation procedure belong to the release-guidance contract. They must implement, not redefine, this authority.

# Semantic Versioning policy

Ava follows Semantic Versioning after `1.0.0`. Classification is based on supported behavior, not only whether old files remain parseable.

## PATCH

A PATCH release preserves every supported structure and intended behavior outcome.

PATCH examples include:

- correcting spelling or broken links without changing instruction meaning
- fixing validation that previously rejected an already-valid supported structure
- repairing release tooling without changing accepted inputs, state meaning, or guarantees
- clarifying text where all supported interpretations already produce the same behavior

A change is not PATCH when it changes routing, resolution, authority, ownership, required reading, validation acceptance, migration state, or intended agent behavior for a supported project.

## MINOR

A MINOR release adds backward-compatible capability.

An addition is MINOR only when at least one condition is proven:

1. It is unreachable until an explicit opt-in action enables it, and the default installed registries and instruction-loading closure remain unchanged.
2. The compatibility test proves that every supported existing project retains identical routing, workflow resolution, role selection, authority, validation, and intended behavior outcomes.

Examples may include:

- an optional metadata field that old agents preserve and ignore, with no changed default behavior when absent
- an unreferenced shared reference document that is not part of required reading
- an optional release component that is not installed or registered without explicit selection
- new tooling diagnostics that are non-blocking and do not alter accepted state or mutation authority

Calling something optional in prose is insufficient. The release must show how the opt-in is represented and why the concept is unreachable through default role selection, workflow invocation, name resolution, or required-reading traversal.

## MAJOR

A MAJOR release contains any incompatible format, routing, ownership, authority, resolution, validation, or behavioral change.

MAJOR examples include:

- moving or repurposing a managed or project-owned public path
- changing the meaning of an existing manifest field or semantic state
- adding a required metadata field that makes an existing supported project invalid
- changing whether a supported turn is roleless, retains an active role, or requires fresh workflow or role resolution
- changing when active-role continuity is cleared, when required reading is reused, or when a role announcement is required
- changing a workflow's primary role, mode, required inputs, invocation identity, or intended outcome
- removing a registered workflow or changing its replacement behavior
- changing a role's authority, capabilities, constraints, or activation outcomes
- adding a registered role that changes free-form role selection or introduces ambiguity
- adding a registered workflow whose name makes an existing invocation ambiguous
- adding required reading that changes effective authority or behavior
- automatically following a deprecation replacement where previous versions only reported it

A structurally readable file can still require MAJOR classification when its interpretation changes.

# Workflow catalog compatibility

Managed workflows are versioned Ava-managed payloads. The deterministic updater installs the target managed catalog and records it in the managed-file inventory.

Project-owned workflows remain outside managed replacement. When a new Ava release changes workflow format, routing, role paths, invocation identity, or required behavior in a way that affects project-owned workflows or references, release guidance must identify the affected concepts and the managed Upgrade Role must reconcile them before semantic compatibility is complete.

Ava does not migrate workflows through a persistent execution service. Deterministic tooling replaces managed payloads and runs mechanical migrations; the Upgrade Role applies release-specific semantic changes to project-owned workflow definitions, indexes, links, and references.

Before `1.0.0`, repository workflow files are unversioned development material and may be removed directly. After publication, deprecation and removal follow the compatibility and lifecycle rules below.

# Compatibility proof for MINOR releases

Every proposed MINOR release must produce a repeatable compatibility report against the immediately previous stable release in the same MAJOR line.

The report runs the previous and candidate managed bases against maintained fixtures representing all supported project shapes and routing boundaries.

For each fixture and request or explicit workflow invocation, compare at least:

- validation success, errors, and blocking warnings
- managed versus project-owned path classification
- conversational routing classification: `roleless`, `same-role`, or `fresh-routing`
- whether active-role continuity is retained or cleared
- resolved workflow identity
- resolved primary role
- free-form selected role when fresh routing applies
- ambiguity and failure outcomes
- workflow mode
- complete required-reading closure, including whether unchanged role reading is validly reused
- role activation or continuation announcement behavior
- effective capabilities and constraints
- mutation authority and prohibited operations
- semantic migration requirement

A candidate qualifies as MINOR only when:

- every baseline outcome is identical for existing supported behavior
- every new behavior is unreachable without explicit opt-in, or separately proven behavior-preserving
- unknown fields and project extensions remain preserved
- fixture coverage includes every changed registry, role, workflow, instruction, metadata rule, and authority boundary

If the repository cannot produce sufficient evidence, classify the release as MAJOR or expand the fixtures before release. Absence of a failing test is not by itself proof of compatibility.

# Prerelease policy

Ava's supported public lineage begins at stable `1.0.0`. No prerelease is a predecessor of that root release.

SemVer prerelease identifiers remain valid syntax for future release channels when Ava intentionally uses them. Neutral examples are:

- `2.0.0-alpha.1`
- `2.0.0-beta.1`
- `2.0.0-rc.1`

Prereleases may change incompatibly between identifiers. A target prerelease must explicitly declare whether direct upgrade from an earlier prerelease is supported.

Channel representation is derived from the SemVer prerelease identifier:

| Version | Channel |
|---|---|
| `1.2.3` | `stable` |
| `2.0.0-rc.1` | `rc` |
| `2.0.0-beta.1` | `beta` |
| `2.0.0-alpha.1` | `alpha` |

Stable installers must not select prereleases automatically. Exact asset names, URLs, development snapshots, and channel publication rules belong to the GitHub release-assets contract.

# Direct and chained upgrades

Semantic version precedence alone does not prove that a version can be skipped.

A direct upgrade from version A to version B is supported only when release metadata for B:

- explicitly includes A in its supported source range
- provides every deterministic migration required across the interval
- provides complete semantic guidance for the source-to-target transition
- identifies no mandatory intermediate waypoint

When these conditions are not met, the updater must construct a declared chained path through supported intermediate releases or abort with the missing path.

A release may require an intermediate waypoint when a migration must establish state that later migrations assume, when guidance is not composable, or when a schema transition cannot be safely collapsed.

Base upgrade while semantic migration is `partial` or `blocked` is allowed only when every traversed release explicitly declares that unresolved state can be carried forward and provides composed guidance. Otherwise semantic migration must be completed or resolved before the next base upgrade.

The upgrade protocol defines the machine-readable path representation and transaction order.

# Deprecation and removal

Deprecated files, metadata, roles, and workflows remain valid until removal.

A deprecated managed document, role, or workflow must communicate through frontmatter and its body:

- `status: deprecated`
- `deprecated_since`: first stable Ava version that declared the deprecation
- `removal_not_before`: earliest MAJOR Ava version in which removal is allowed
- `replaced_by`: canonical path when a direct replacement exists
- a body explanation of migration impact

A deprecated metadata field cannot carry its own frontmatter. Its authoritative contract, release notes, and upgrade guidance must communicate the same `deprecated_since`, `removal_not_before`, replacement, and migration information.

Deprecation does not authorize automatic redirection or ownership transfer.

After `1.0.0`:

- deprecation may be introduced in MINOR when existing behavior remains available
- removal or behavior-changing replacement requires MAJOR
- `removal_not_before` must name a later MAJOR than `deprecated_since`
- release notes and upgrade guidance must list newly deprecated and removed concepts

The [document metadata contract](../templates/base/shared/instructions/document-metadata.md) defines field shape and validation. Release guidance defines project-specific migration actions.

# Host conformance and compatibility claims

Ava compatibility assumes the host loads the complete managed router, required instructions for freshly selected roles, retained required instructions for valid same-role continuations, and workflow context for explicit workflow invocations according to the installed contracts.

When a host agent skips the managed-state gate, bypasses fresh routing, applies incompatible precedence, cannot preserve unknown metadata, cannot reliably retain required context for claimed same-role continuation, or cannot perform required file operations, Ava must not report the project as fully compatible merely because the files parse.

Host discovery is reported separately as `native`, `project-provided`, `explicit-only`, or `unsupported`. Unsupported or unverified host behavior may block semantic migration and must be recorded as an unresolved decision when it prevents completion.

A `project-provided` result means only that an existing project-owned entrypoint has been recorded. It is not a native-support or content-conformance claim.

# Reporting requirements

Human and machine-readable reports must distinguish:

```text
Installed Ava base: 2.0.0
Installed release channel: stable
Project context compatible through: 1.4.2
Semantic migration target: 2.0.0
Semantic migration status: blocked
Unresolved decisions: 2
```

Reports must not collapse these fields into a single "Ava version" or "up to date" result.

# Support windows

For stable releases after `1.0.0`:

- all releases in the current MAJOR line remain supported upgrade sources while that MAJOR is current
- only the latest MINOR in the current MAJOR is guaranteed to receive new PATCH fixes
- the immediately previous MAJOR remains a supported upgrade source for at least twelve months after the next MAJOR becomes stable
- older release assets remain immutable and downloadable according to the release-retention contract, but no maintenance guarantee is implied
- prereleases receive no support window beyond their explicit test programme

A future release may extend support but must not shorten an already published window retroactively.

# Release and validation alignment

Every release must state:

- SemVer classification and rationale
- source and target compatibility
- whether project-owned semantic review is required
- supported direct and chained upgrade paths
- manifest schema impact
- newly deprecated and removed concepts
- host-conformance assumptions
- MINOR compatibility evidence when applicable

Validation must reject:

- manifest fields with invalid shapes or versions
- duplicate managed-file paths
- payload entries without checksums
- state entries with checksums
- manifest or upgrade state omitted from the managed inventory
- invalid or managed-path host integration metadata
- inconsistent release tag, channel, and `ava_version`
- impossible semantic state combinations, including pending state with unresolved decisions or blocked state without them
- unauthorized or regressive semantic transitions
- a `complete` state that does not match the installed `ava_version`
- a release classified below the compatibility impact demonstrated by its fixtures
