---
id: ava-505
title: Publish the 1.0.0 release candidate
status: Won't Fix
assignee: []
created_date: ''
updated_date: '2026-08-30 18:27'
labels:
  - internal
  - roadmap
  - phase-05
  - release
  - rc
dependencies: []
ordinal: 505
---

## Description

Freeze the intended v1 public behavior and publish an immutable release candidate after alpha findings and required fixes are resolved. This release-progression task is closed as Won't Fix after being converted into the `v1.0.0` milestone. Next-up roadmap tasks are tracked toward that milestone. The migrated material below is historical planning state only and does not authorize release activity.

## Migrated task record

Historical metadata: Internal Development Task; phase 5 order 5; previous status pending; generated 2026-08-03 and updated 2026-08-10. Original tags were internal, roadmap, releases, rc, publishing, and compatibility.

### Entry gate

Release-candidate work was defined to begin only after explicit user closure of alpha dogfooding, no remaining blocker, completion of required-v1 findings affecting public behavior, freezing of intended v1 contracts, no planned incompatible public-contract change, a declared and tested latest-alpha-to-RC path, and a stable synthetic qualification-vault baseline plus complete expected-outcome manifest.

### Preparation requirements

The task recorded `1.0.0-rc.1` as the default RC identifier unless an approved sequence requires another canonical RC. It required two identical builds from one clean source revision, the complete conformance matrix against fresh installation and supported prerelease sources, the complete OpenCode fixture, the complete synthetic qualification-vault matrix, Ava Maintenance and Upgrade Role lifecycle verification, machine-readable transition evidence from the actual latest supported alpha, a revision-bound RC qualification result, complete release notes, and documentation that presents the RC as a compatibility candidate rather than stable support.

### Publication requirements

Publication remained separately approval-gated for the exact RC version and source revision. The planned release automation was to create the immutable tag and draft GitHub Release, keep it a prerelease rather than `latest`, attach and verify the required asset set, publish only after local and draft checks agreed, verify immutability, attestation, source revision, asset digests and pinned URLs, and then verify installation and upgrade behavior from published assets.

### RC policy

After RC publication, only release-blocking fixes, documentation corrections, or compatibility-preserving repairs required for stable qualification were to be accepted. An incompatible public contract or behavior change required another RC and repeated qualification. Every resulting repository fix was to receive a bounded roadmap task. Stable `1.0.0` required a tested direct or declared chained path from the latest RC.

### Completion criteria

Completion required an immutable approved RC, successful fresh installation and all declared prerelease upgrades using published assets, complete OpenCode supported-host evidence, no known planned incompatible public change, stable-safe disposition for remaining known issues, and readiness for AVA-551 release-candidate stabilization.

The V1 release operator sequence formerly stored in a separate todo file is preserved in AVA-506. This task is closed as Won't Fix; the `v1.0.0` milestone carries release progression.

## Comments

<!-- COMMENTS:BEGIN -->
author: Philip
created: 2026-08-30 18:17
---
Convert this to a milestone, and place all next up tasks towards this milestone. Then move this task to won't fix.
---
<!-- COMMENTS:END -->
