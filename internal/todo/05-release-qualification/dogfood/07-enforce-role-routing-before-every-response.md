---
type: Internal Development Task
title: Enforce Role Routing Before Every Response
description: Ensure the managed root router cannot treat an apparently out-of-domain request as exempt from mandatory state checks and role routing.
tags: [internal, roadmap, dogfood, routing, roles, instructions, opencode, blocker]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 7
classification: blocker
blocks: next-prerelease
affected_version: unknown installed prerelease in the user's test project
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T13:31:46+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-08T18:06:00+02:00
---

# Enforce Role Routing Before Every Response

## Observed behavior

In an Ava test project, the user asked an agent:

```text
Has my warranty run out on my glasses?
```

The agent did not perform the Ava-managed pre-routing check, inspect the role registries, select a role, load its required context, or announce an active role. It instead classified the request through a generic coding-assistant identity, said the question was outside its scope, and suggested checking receipts or contacting the retailer or manufacturer.

This bypassed the installed project's `AGENTS.md` routing contract. Whether the request ultimately matches a registered role or requires routing clarification, that determination belongs to Ava's routing procedure rather than an unscoped host persona.

## Reproduction and evidence

The failure was observed in the user's test project by asking the exact request above in an agent session where the project's `AGENTS.md` instructions were present in context.

When later asked why it failed, the agent reported that it interpreted this root-router preamble as conditional:

```text
Before reading any project-owned registry or performing ordinary routing:
```

It reasoned that an apparently simple knowledge question did not feel like a routing decision, so the pre-routing protocol never activated. It suggested making role routing an explicit blocking gate before any response or action and optionally reinforcing root-router loading through project-owned host instructions.

The exact installed prerelease, router bytes, and session configuration from the original failure were not retained. Repository investigation confirmed that the same conditional sentence existed in the managed router source and therefore in its assembled installed destination. The maintained OpenCode configuration only grants access to `./.ava/**`; it does not activate the router or duplicate routing instructions, so permission configuration was not the source of this conditional contract.

## Classification

This was a `blocker` for the next prerelease. Ava's managed root router is the canonical entry point for state gating, workflow resolution, role selection, required-context loading, and authority. If an agent can bypass that entry point based on its own perception of the request's domain, exactly-one-role routing and every role-scoped capability and constraint become optional in practice.

## Root cause

The managed root router introduced its state gate with:

```text
Before reading any project-owned registry or performing ordinary routing:
```

That wording made the gate a prerequisite of an already-selected routing activity rather than an unconditional prerequisite of handling every request. A host could therefore apply its generic persona first, decide that a request was not a coding or project-routing request, and never enter Ava routing.

The router also lacked an explicit prohibition on substantive answers and refusals before role activation. Its unresolved-routing rule required asking the user when no role matched, but did not state that this was the only permitted pre-activation response. Together, those gaps allowed the observed generic coding-assistant refusal.

OpenCode host support was not the root cause. Its project-owned configuration correctly grants read access to managed Ava content and requires confirmation for edits, while `AGENTS.md` remains the canonical routing contract.

## Scope

- reproduce the failure against an assembled installation using the maintained OpenCode path and record the installed Ava version, router content, discovery mode, and host configuration
- make the managed-state pre-routing check and normal-operation workflow or role routing an explicit prerequisite for handling every user request, regardless of apparent domain or the host agent's default persona
- prohibit substantive answers, refusals, and project actions before the routing procedure has either activated and announced one role or reached its explicit unresolved-routing behavior
- ensure an apparently non-coding request cannot be rejected as outside a generic coding-assistant scope before managed and project-owned registries have been evaluated
- preserve direct Ava Maintenance and Upgrade Role activation, operation allowlists, explicit workflow behavior, exactly-one-role semantics, required-reading order, and unresolved-routing safeguards
- determine whether maintained host discovery needs correction while keeping `AGENTS.md` canonical and avoiding duplicated routing contracts in host-specific bootstrap files
- add regression coverage that detects conditional or bypassable root-routing language and exercises the failure shape through the maintained installed-project and OpenCode conformance model
- update affected router, host-support, conformance, release, and upgrade-guidance documentation when their behavior or compatibility obligations change

## Completion criteria

- every request first enters the managed maintenance and upgrade state gate, without an apparent-domain exception
- when normal operation is permitted, every request completes explicit workflow resolution or ordinary role routing before any substantive answer, refusal, or project action
- the exact warranty question cannot trigger a generic coding-assistant scope refusal before the installed role registries and their routing conditions are evaluated
- a selected role is announced only after its complete required-reading chain has loaded and before role-scoped handling begins
- requests with no clear role follow the router's explicit ambiguity behavior without inventing permissions, authority, or a host-persona fallback
- regression coverage protects the unconditional gate, normal routing sequence, role announcement ordering, and maintained OpenCode discovery path
- conformance validation passes against both repository sources and assembled installed paths
- compatibility impact and any required release guidance are recorded before publication
- the finding task, backlog index, phase index, and stable roadmap entry remain aligned

## Resolution evidence

The managed `templates/base/AGENTS.md` router now states that every user request must enter Ava routing before any substantive answer, refusal, tool call, or project action. Apparent simplicity, subject matter, and the host's generic persona are explicitly non-exempt. Normal routing remains blocked until managed-state checks complete, workflow or role resolution completes, the selected role's required-reading chain loads, and the role is announced.

When no role clearly matches, the router permits only the minimum routing clarification required from the user. It explicitly prohibits generic host-persona answers, scope disclaimers, and refusals as fallbacks.

`internal/release/fixtures/root-routing.json` freezes the exact warranty prompt, the required routing sequence, the observed generic coding-assistant refusal, and the explicit no-clear-role outcome. `internal/release/tests/test_root_routing.py` rejects the legacy conditional sentence, verifies prerequisite ordering, checks that assembly preserves the exact router bytes at `/AGENTS.md`, and validates a healthy installed project with the maintained OpenCode permission model.

The regression suite is included by `internal/release/test.sh`, the fixture is indexed, and the conformance procedure documents the root-router guarantee. The dogfood backlog and Phase 5 roadmap now make synthetic-vault qualification the next task while keeping the parent dogfood task pending.

## Release qualification follow-up

The corrective immutable prerelease must be installed in a realistic test project with the relevant project-owned role catalog. In a fresh agent session, repeat the exact warranty question and record evidence that the agent performs the managed state gate, evaluates routing, loads the selected role's required context, announces it, and only then handles the request. Repeat a no-clear-match request to verify the explicit unresolved-routing behavior without a generic host-persona refusal.
