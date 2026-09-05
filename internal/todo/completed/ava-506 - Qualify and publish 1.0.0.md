---
id: ava-506
title: Qualify and publish 1.0.0
status: Done
assignee: []
created_date: ''
updated_date: '2026-09-01 19:54'
labels:
  - internal
  - roadmap
  - phase-05
  - release
  - stable
  - v1
  - "Won't Fix"
dependencies: []
ordinal: 506
---

## Description

Apply the stable acceptance gate, verify upgrade from the release candidate, and publish Ava's first supported stable distribution. This task also owns the migrated Phase 5 roadmap and V1 release-operator context that previously lived in separate todo files. Release progression is intentionally parked. The material below is historical planning state only and does not authorize publication or destructive release maintenance.

## Migrated task record

Historical metadata: Internal Development Task; phase 5 order 6; previous status pending; generated 2026-08-03 and updated 2026-08-10. Original tags were internal, roadmap, releases, stable, v1, and publishing.

### Stable acceptance gate

Stable publication was defined to require no unresolved blocker or required-v1 task; completion of AVA-551 release-candidate stabilization; no known corruption, project-owned overwrite, path escape, authority bypass, or unrecoverable transaction defect; frozen and aligned public contracts; all maintained validators and conformance fixtures passing; OpenCode fresh-install, repeated-session, upgrade, recovery, and uninstall evidence; Ava Maintenance and Upgrade Role authority evidence across state transitions; an explicitly declared and tested latest-RC-to-stable path; complete user-facing installation, verified-bootstrap, OpenCode, maintenance, recovery, upgrade, semantic-reconciliation, and removal documentation; reproducible assembly; release automation using the same validated assets and paths; a revision-bound machine-readable stable qualification result tied to the generated-vault and release evidence; and documented post-v1 work that does not weaken v1 guarantees.

### Preparation requirements

The historical plan included the approved cleanup of old immutable alpha release history associated with redacted content before stable publication, under the release procedure and exact user authorization. It also required two byte-identical builds of the exact seven stable assets, fresh installation and RC-to-stable verification from assembled assets, semantic compatibility validation independent of installed `ava_version`, stable-convenience and pinned-authenticated installation verification, release-immutability verification, complete final release notes, and README/public-status updates that state the stable support boundary.

### Publication requirements

Publication remained separately approval-gated for exact version `1.0.0` and exact source revision. The plan required the maintained automation to prepare the immutable stable release identity, attach exactly the required assets, publish as stable and `latest` only after all checks succeeded, verify immutability, attestation, tag target, asset inventory, checksums and published download paths, then perform fresh installation and latest-RC upgrade from published assets and update repository documentation to identify `1.0.0` as the first supported stable distribution.

### Support boundary

Stable support guarantees begin at `1.0.0`. Historical unversioned Ava installations do not become supported merely because stable is published. Future changes remain governed by Ava SemVer, deprecation, support-window, release-guidance, and upgrade contracts.

### Completion criteria

Completion required an immutable approved `1.0.0` release, working stable convenience and pinned verified installation flows, successful latest-RC upgrade, documented and tested OpenCode support, separately observable installed-base and project semantic compatibility, recovery/finalization/role-led uninstall against published stable assets, complete stable acceptance evidence, and no remaining required-v1 work.

## Migrated Phase 5 roadmap context

Phase 5 turns Ava's format, roles, release tooling, OpenCode support, and conformance suite into tested prereleases and the first stable distribution.

Core release gates at migration:

1. AVA-501 alpha acceptance and prerelease policy: Done.
2. AVA-502 release-please integration: Done.
3. AVA-503 first alpha publication: Done.
4. AVA-504 dogfood umbrella: Parked, still requiring explicit user closure when resumed.
5. AVA-505 release candidate: Parked.
6. AVA-506 stable qualification/publication: Parked.

Supporting qualification tasks:

- AVA-541 synthetic qualification vault: Parked.
- AVA-542 corrective alpha qualification/publication: Parked.
- AVA-543 automated qualification/evidence state: Done.
- AVA-544 qualification OpenCode permission hardening: Done.
- AVA-545 qualification session-inventory isolation: Done.
- AVA-551 published RC stabilization: Parked.

Both qualification-infrastructure defects exposed by `v1.0.0-alpha.15` are implementation-complete. Further alpha dogfooding and immediate V1 progression remain parked by explicit user decision. Current roadmap execution moves through Backlog.md integration and durable interaction evidence before reassessment with the user.

The qualification-hardening rationale remains that temporary-root OpenCode permission had to become qualification-owned rather than depend on user-global state, and session inventory had to be bounded to sessions created by the exact current operation rather than admit historical sessions. These are infrastructure corrections, not exceptional qualification acceptance mechanisms.

Completed dogfood findings remain durable evidence. The dogfood umbrella cannot be inferred complete from a passing suite, empty blocker list, or completed infrastructure work.

## Migrated V1 release operator path

The canonical release path is parked and must be resumed only by explicit user direction. When resumed, the conceptual order remains:

1. finish the synthetic qualification/evidence obligations needed for a trustworthy full run
2. complete remaining corrective-alpha evidence obligations
3. obtain explicit user closure of alpha dogfooding
4. prepare, qualify, accept, and publish the release candidate
5. stabilize the published release candidate
6. prepare, qualify, accept, and publish stable `1.0.0`

A new blocker preempts the next prerelease. A `required-v1` finding preempts the release gate named by its blocking metadata.

For each future release edge, the maintained release procedure remains authoritative: release-please determines the release identity; the semantic-impact assessment and adjacent edge are completed; deterministic validation/tests and exact candidate assembly run; the published-source/local-target qualification pair is configured; full qualification is run and genuine failures corrected; explicit user approval is obtained for an `awaiting-user-signoff` result; accepted qualification state is recorded; the Release PR policy must pass; and only then may the separately authorized release process advance.

Qualification must run without hidden host permission state, historical-session contamination, or manual qualification-state rewriting. Existing historical acceptance entries remain governed by the release-quality ledger and release procedure and are not reinterpreted during resumption.

When asked what work is next, use the native Backlog.md task state rather than the removed `/internal/todo.md`. Use this parked operator context only when the user explicitly asks to inspect or resume V1 release progression.
