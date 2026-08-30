---
id: ava-5605
title: "Restore complete prerelease upgrade coverage"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5605
---

## Description

Prevent release preparation from stranding supported installations and require reviewed per-source managed, migration, guidance, semantic, and cumulative-note assessments. This native task preserves the finding and resolution evidence.

## Migrated task record

Historical metadata: phase 5 finding 5, `blocker`, blocking next prerelease, affected versions alpha.6 through alpha.7, completed after implementation.

### Observed behavior and root cause

Published alpha.6 omitted alpha.5 as a source and alpha.7 declared only alpha.6, leaving alpha.5 unable to reach a newer release through the published graph. The release process also treated a source list as sufficient without explicit source-to-target assessment of managed changes, migrations, semantic guidance, and cumulative release notes.

Preparation validated release-specific declarations copied across fixtures rather than inheriting direct source commitments from the previous immutable release, protecting known sources, and binding edges to one reviewed source assessment. Generic machinery was mixed with presumed-next-version data, making it unsuitable as a reusable RC/stable flow.

### Corrective design

The approved generic flow was: implementation PR merges; release-please creates/updates release PR; incomplete release PR initially fails; an agent completes reviewed `internal/release/upgrade-impact.json` on that branch; qualification derives required sources from previous version/history/protected-source policy; actual tagged deltas, cumulative changelog, migrations, guidance, and semantics are validated; release PR can merge only after checks pass; exact tagged revision is then requalified/assembled/attested/published. Current edges came only from `upgrade-impact.json`; historical tags predating it used immutable legacy source declarations.

### Scope and completion criteria

The task required version-independent tooling across alpha/beta/RC/stable, target-derived channel validation, inherited direct sources, explicit protected-source retirement, per-source payload/migration/guidance/semantic/cumulative-note assessment, exact generated edge metadata, no next-version hardcoding, representative regression coverage, and aligned roadmap evidence. Incomplete release PRs had to fail while representative alpha/RC/stable/patch flows passed.

### Resolution evidence

Merged PR #60 implemented generic release-PR completion: target-derived identity/channel validation, direct-source inheritance from immutable release history, `upgrade-impact.json` as the sole then-current edge declaration, reviewed assembly derived from it, and tests for alpha/RC/stable/patch, inheritance, retirement, cumulative notes, managed deltas, and edge assembly. Future-version fixtures and release-specific impact data were removed from implementation branches. Repository implementation, regression coverage, docs, and roadmap evidence were complete.

The next corrective immutable release still had a release-gate follow-up to exercise the real required source edges and prove project-owned byte preservation. That evidence was explicitly separate from reopening the completed implementation task.