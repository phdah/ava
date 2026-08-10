---
type: Internal Development Task
title: Avoid Redundant Routing for Conversational Follow-Ups
description: Refine Ava routing so conversational follow-ups can continue with the current role or no role, while full routing runs only when a request requires scoped work or a role change.
tags: [internal, roadmap, dogfood, routing, roles, conversations, follow-ups]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 12
classification: required-v1
blocks: release-candidate
affected_version: current prerelease dogfood behavior
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T11:29:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T11:49:00+02:00
---

# Avoid Redundant Routing for Conversational Follow-Ups

## Observed behavior

Ava previously treated every user request as a fresh routing event. Even when the user was asking a direct follow-up about the immediately preceding result, the managed router was expected to resolve a role again, reload its required context, and announce the role before answering.

This was correct for preventing the host agent from bypassing Ava on a new task, but unnecessarily heavy for conversational continuity. A follow-up may only ask for clarification of the previous result, may still belong to the role that is already active, or may not require role-scoped authority at all.

The resulting interaction repeatedly performed routing work that did not change the active instruction scope and made ordinary follow-up conversation feel procedural rather than continuous.

## Relationship to finding 07

[Finding 07](07-enforce-role-routing-before-every-response.md) fixed a different failure: a host persona could decide that a new request did not need Ava routing and answer or refuse before evaluating Ava's role system.

This finding preserves that guarantee by separating two decisions:

- every request still enters the managed-state gate and Ava's own turn classification before substantive handling
- full workflow or role resolution runs only when the classified turn requires fresh scoped routing

The host persona therefore cannot use apparent subject matter to bypass Ava, while Ava itself can recognize bounded conversational continuity after the unconditional safety gate.

## Classification

This is `required-v1` and blocks the release candidate. Role routing is one of Ava's core interaction contracts, and the previous per-turn behavior created avoidable friction during normal multi-turn use. The v1 contract now defines conversational continuity before exactly-one-role routing semantics are treated as stable.

The user explicitly approved implementation of this refined routing contract by asking the Ava Internal Maintainer to implement the current next to-do after the complete finding and approval requirement were already recorded in the roadmap.

## Resolved behavior

Ava now supports these cases:

1. **Pure conversational follow-up:** when the user is asking about, clarifying, or refining the immediately preceding result and no new scoped action or authority is required, no fresh role routing is required and no role is active for that turn.
2. **Same-role continuation:** when the follow-up continues the same active objective, requires role-scoped work, and the currently active role is still clearly correct with its required context already loaded, Ava retains that role without repeated registry resolution or unchanged required-reading reload. It states `Active role remains: <role title>` before continuing role-scoped work.
3. **Role transition or new task:** when the request introduces a new task, changes domain or authority, explicitly invokes another role or workflow, or otherwise makes the current role insufficient, normal routing runs before substantive work.
4. **No active role to scoped work:** a roleless turn clears role continuity. Later scoped work therefore uses normal routing rather than reusing a role that was active before the roleless turn.
5. **Managed-state override:** maintenance, upgrade, malformed-state, or other managed pre-routing conditions always take precedence over conversational continuity.

Role continuity exists only in the host's current conversation context. Ava introduces no persistent runtime state, manifest field, project metadata, or hidden mutable role record for continuation.

## Scope

The resolving PR:

- separates the lightweight per-request managed-state gate from full workflow or role resolution
- defines the exact boundary for roleless conversational follow-ups
- defines same-role continuation for the same active objective only
- clears role continuity after a roleless turn
- keeps role continuity session-scoped without introducing persistent runtime state
- permits roleless handling only when no role-scoped capability, constraint, project action, workflow procedure, or new authority is needed
- retains a role without repeated registry traversal or required-reading reload only when the role remains valid and its complete required context is already loaded
- standardizes `Active role remains: <role title>` as the same-role continuation announcement
- forces fresh routing for new tasks, explicit workflow or role activation, role mismatch, authority or domain changes, missing role context, scoped work after roleless handling, and managed-state overrides
- preserves finding 07's guarantee that a host persona cannot classify a new substantive request as outside Ava before Ava determines the routing mode
- reconciles the public router, role catalog, workflow routing, compatibility, and overview documentation with zero-or-one role turn semantics
- adds regression coverage for roleless clarification, same-role continuation, role transition, scoped work after a roleless turn, unresolved routing, and the original finding 07 bypass case

## Completion criteria

- [x] Ava distinguishes managed-state gating from full role resolution.
- [x] A pure follow-up can be answered without resolving a role when no role-scoped authority is needed.
- [x] A same-role follow-up retains the active role without repeating unchanged routing and required-reading work.
- [x] Same-role continuation states that the existing role remains active before role-scoped handling continues.
- [x] New substantive work still routes before project action or role-scoped handling.
- [x] A change in task, workflow, authority, or role fit causes fresh routing.
- [x] Managed maintenance and upgrade gates still override normal conversational continuity.
- [x] The original generic host-persona bypass fixed by finding 07 remains impossible under the contract and maintained fixture.
- [x] Session continuity does not require Ava to introduce a persistent runtime or hidden mutable role state.
- [x] Public routing, role, workflow, conformance, and compatibility documentation are updated consistently.
- [x] Repository and assembled-installation regression coverage protects the defined continuity and rerouting cases.
- [x] Concrete resolution and validation evidence are recorded below.

## Resolution evidence

`templates/base/AGENTS.md` now performs the managed-state gate on every request and only then classifies normal-operation turns as roleless conversational follow-up, same-role continuation, or fresh routing. The router defines conservative fallback to fresh routing, session-only role continuity, roleless continuity clearing, same-role announcement, and all required rerouting triggers while retaining the generic-host no-bypass rule from finding 07.

`templates/base/shared/instructions/instruction-resolution.md` defines the activation, authority, context-loading, conflict, workflow-continuity, and validation consequences of the three routing modes. `templates/base/shared/instructions/workflow-routing.md` makes every explicit workflow invocation a fresh-routing event and prevents workflow-specific procedure or mode from persisting implicitly across later turns. The managed role catalog now states that registry traversal is for fresh routing and that valid continuation may reuse the active role.

`internal/release/fixtures/root-routing.json` freezes six scenarios: the original warranty bypass, a roleless clarification, same-role mutation continuation, role transition to independent review, scoped work after a roleless turn, and unresolved fresh routing. `internal/release/tests/test_root_routing.py` validates the source router and shared continuity contracts, rejects the legacy unconditional full-routing shape, verifies assembly preserves the router bytes at `/AGENTS.md`, and exercises the installed OpenCode conformance model.

The README and public versioning contract now treat turn-level routing classification, active-role continuity, required-reading reuse, and continuation announcements as supported compatibility behavior. Internal conformance documentation and fixture discovery describe the maintained regression boundary.

The finding, dogfood backlog, Phase 5 indexes, and stable roadmap are advanced together. Immutable multi-turn release evidence remains a release qualification gate rather than pending implementation work.

## Release qualification follow-up

Exercise a realistic installed project through a multi-turn session that covers an initial routed task, a pure clarification, a same-role action, a role-changing request, and a later new task after a roleless follow-up. Record that Ava performs full routing only at the defined transition points while preserving finding 07's no-bypass guarantee.
