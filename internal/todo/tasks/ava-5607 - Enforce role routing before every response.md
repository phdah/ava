---
id: ava-5607
title: "Enforce role routing before every response"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5607
---

## Description

Ensure the managed root router cannot treat an apparently out-of-domain request as exempt from mandatory state checks and role routing. This task preserves the observed warranty-question failure, routing contract change, regression evidence, and release follow-up.

## Migrated task record

Historical metadata: phase 5 finding 7, `blocker`, blocking next prerelease, affected installed prerelease unknown, completed after implementation.

### Observed behavior

For the request `Has my warranty run out on my glasses?`, an Ava project agent skipped the managed pre-routing check, role registries, role selection, required context and role announcement. It instead used a generic coding-assistant identity, declared the request out of scope and suggested external checks. That bypassed `AGENTS.md`, even though no-match handling itself belongs to Ava routing.

The installed exact prerelease/session was not retained, but repository investigation confirmed the managed router contained the conditional preamble `Before reading any project-owned registry or performing ordinary routing:`. The agent later explained that it treated the request as too simple/non-project-like to enter routing. OpenCode permissions only governed access to `./.ava/**` and were not the cause.

### Classification and root cause

This was a `blocker`: if the host can decide a request is outside Ava before entering the root router, state gating, exactly-one-role routing, and role-scoped authority become optional. The router made state gating conditional on already performing routing and lacked an explicit prohibition on substantive answers/refusals before activation. Its no-match rule did not state that minimal routing clarification was the only permitted pre-activation response.

### Scope and completion criteria

The task required every request to enter managed state gating and normal workflow/role routing before substantive handling, no apparent-domain or host-persona exception, no pre-routing substantive answer/refusal/action, preserved maintenance/upgrade pre-routing and exactly-one-role semantics, maintained OpenCode discovery verification, regression coverage for the exact warranty failure, no-clear-match behavior, activation ordering and assembled router bytes, conformance across source/installed paths, compatibility guidance, and aligned roadmap evidence.

### Resolution evidence

The managed `templates/base/AGENTS.md` now states every user request enters Ava routing before any substantive answer, refusal, execution, or project action. Apparent simplicity, subject matter, and host persona are non-exempt. Routing-only reads/checks remain allowed to complete activation. Normal work remains blocked until state checks, routing, complete required reading, and role announcement finish. With no clear role, only the minimum routing clarification is permitted, explicitly excluding generic host-persona answers, scope disclaimers, or refusals.

`internal/release/fixtures/root-routing.json` freezes the warranty prompt, required sequence, observed bad refusal, and no-clear-role outcome. `internal/release/tests/test_root_routing.py` rejects the legacy conditional wording, verifies prerequisite ordering, checks assembled `/AGENTS.md` bytes, and validates a healthy installed project under maintained OpenCode permission behavior. The test is in `internal/release/test.sh`, the fixture is indexed, and conformance documentation records the guarantee.

### Release qualification follow-up

The corrective immutable prerelease still had to be installed in a realistic project. A fresh agent session was to repeat the warranty question and prove state gating, registry evaluation, required-reading load, role announcement, then handling. A no-clear-match request was also required to demonstrate explicit unresolved routing without host-persona fallback. This remained release evidence rather than reopening the implementation task.