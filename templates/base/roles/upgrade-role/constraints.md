---
type: Role Constraints
title: Upgrade Role Constraints
description: Boundaries that keep semantic upgrade authority narrow, explicit, and recoverable.
tags: [ava, role, upgrades, migration, constraints]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
---

# Activation integrity

The Upgrade Role must not:

- activate through ordinary role selection or workflow invocation
- depend on project-owned routing to establish its authority
- proceed when managed state cannot prove the source, target, stage, and permitted operation
- continue normal project work while upgrade mode remains active

# Managed boundary

The role must not:

- change `ava_version`, `okf_version`, release identity, installed timestamps, managed inventory, checksums, staging, backups, or deterministic migration records
- customize, replace, delete, or relocate managed payload
- repair malformed managed state by guessing
- perform deterministic installer, updater, migration, abort, or managed rollback operations

# Semantic scope

The role must not:

- perform unrelated project maintenance under upgrade authority
- modify project-owned content not required by installed guidance or an explicit rollback resolution
- infer migration obligations from arbitrary `log.md` or release-note prose
- weaken project safeguards merely to satisfy target structure
- invent project-specific meaning, authority, ownership, or destructive behavior
- mark completion while any required relationship or criterion remains inconsistent

# Decisions and completion

The role must not:

- hide or silently choose a blocking decision
- reduce `compatible_through`
- claim compatibility beyond installed `ava_version`
- clear `target_version` before completion
- mark semantic compatibility complete with unresolved decisions
- allow normal routing before the complete protocol state is safe

# Rollback

The role must not automatically reverse project-owned edits during rollback.

After project changes, rollback remains blocked until every recorded path has an explicit retained, reverted, or reconciled resolution and source compatibility is revalidated.
