---
id: ava-5612
title: "Avoid redundant routing for conversational follow-ups"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5612
---

## Description

Refine Ava routing so conversational follow-ups can continue with the current role or no role, while full routing runs only when a request requires scoped work or a role change.

## Migrated task record

Historical metadata: phase 5 finding 12, `required-v1`, blocking release candidate, current prerelease dogfood behavior, completed after user-approved implementation.

### Observed behavior and relationship to AVA-5607

Ava previously treated every turn as a fresh full-routing event, even direct clarification of the immediately preceding result. This prevented host bypass but made ordinary conversation repeatedly resolve registries, reload unchanged context, and announce roles. AVA-5607 solved host-persona bypass; this finding preserved its unconditional managed-state/Ava classification gate while allowing Ava itself to recognize bounded conversational continuity.

### Resolved behavior

After the managed-state gate, normal turns are one of: (1) pure conversational follow-up requiring no role-scoped authority, with no active role for that turn; (2) same-role continuation of the same objective when the active role and complete loaded context remain valid, announced as `Active role remains: <role title>` without redundant registry/read reload; (3) new task/role transition/explicit workflow/authority or domain change, which uses fresh routing; (4) scoped work after a roleless turn, which uses fresh routing because role continuity was cleared; or (5) managed maintenance/upgrade/malformed-state override, which always wins. Continuity is only current-conversation state and introduces no persistent runtime or hidden project role record.

### Scope and completion criteria

The fix separated lightweight per-request state gating from full routing, defined roleless and same-role boundaries, cleared continuity after roleless handling, restricted roleless turns to cases needing no role capability/constraint/action/workflow/authority, required fresh routing on every relevant transition, preserved AVA-5607 no-bypass behavior, aligned public routing/workflow/compatibility docs with zero-or-one-role turns, and added regression cases for clarification, continuation, transition, post-roleless work, unresolved routing, and warranty bypass.

### Resolution evidence

`templates/base/AGENTS.md` now gates every request then classifies normal turns as roleless follow-up, same-role continuation, or fresh routing, with conservative fallback to fresh routing and all required transition triggers. `instruction-resolution.md` defines activation/authority/context/conflict consequences; `workflow-routing.md` makes explicit workflow invocation fresh routing and prevents implicit persistence of workflow mode/procedure; the role catalog confines traversal to fresh routing while valid continuation reuses the active role.

`internal/release/fixtures/root-routing.json` freezes six scenarios and `test_root_routing.py` validates source/shared contracts, rejects legacy full-routing behavior, verifies assembled `/AGENTS.md`, and exercises installed OpenCode conformance. README/versioning now treat turn classification, role continuity, required-reading reuse and continuation announcements as compatibility behavior.

Release follow-up required a realistic multi-turn installed session covering initial routed task, pure clarification, same-role action, role change, and new work after roleless follow-up, proving full routing occurs only at defined transitions while AVA-5607 no-bypass remains intact.