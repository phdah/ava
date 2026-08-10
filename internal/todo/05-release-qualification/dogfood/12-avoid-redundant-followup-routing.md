---
type: Internal Development Task
title: Avoid Redundant Routing for Conversational Follow-Ups
description: Refine Ava routing so conversational follow-ups can continue with the current role or no role, while full routing runs only when a request requires scoped work or a role change.
tags: [internal, roadmap, dogfood, routing, roles, conversations, follow-ups]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 12
classification: required-v1
blocks: release-candidate
affected_version: current prerelease dogfood behavior
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T11:29:00+02:00
---

# Avoid Redundant Routing for Conversational Follow-Ups

## Observed behavior

Ava currently treats every user request as a fresh routing event. Even when the user is asking a direct follow-up about the immediately preceding result, the managed router is expected to resolve a role again, reload its required context, and announce the role before answering.

This is correct for preventing the host agent from bypassing Ava on a new task, but it is unnecessarily heavy for conversational continuity. A follow-up may only ask for clarification of the previous result, may still belong to the role that is already active, or may not require role-scoped authority at all.

The resulting interaction repeatedly performs routing work that does not change the active instruction scope and makes ordinary follow-up conversation feel procedural rather than continuous.

## Relationship to finding 07

[Finding 07](07-enforce-role-routing-before-every-response.md) fixed a different failure: a host persona could decide that a new request did not need Ava routing and answer or refuse before evaluating Ava's role system.

This finding must not reintroduce that bypass. The distinction to define is between:

- a new request that requires scoped work or authority and therefore must enter role routing before substantive handling
- a conversational follow-up that can safely continue the already-established context without resolving the same role from scratch

The existing unconditional managed-state safety gate may remain distinct from full role resolution. The resolving design must make that distinction explicit rather than treating "routing" as one indivisible operation.

## Classification

This is `required-v1` and blocks the release candidate. Role routing is one of Ava's core interaction contracts, and the current per-turn behavior creates avoidable friction during normal multi-turn use. The v1 contract should define conversational continuity before exactly-one-role routing semantics are treated as stable.

Because this changes public routing semantics, the resolving task must present the final contract for explicit user approval before implementing it as accepted Ava behavior.

## Desired behavior

The resolving design should support these cases:

1. **Pure conversational follow-up:** when the user is asking about, clarifying, or refining the immediately preceding result and no new scoped action is required, no fresh role routing should be required. No role may be active for that turn when role-scoped authority is unnecessary.
2. **Same-role continuation:** when the follow-up requires work but the currently active role is still clearly correct, Ava should retain that role without repeating registry resolution or reloading unchanged required context. The agent should only state that the role remains active before continuing role-scoped work.
3. **Role transition:** when the request introduces a new task, changes domain or authority, explicitly invokes another role or workflow, or otherwise makes the current role insufficient, normal routing must run and select the appropriate role before substantive work.
4. **No active role to scoped work:** when a turn that currently has no active role asks Ava to perform scoped project work, normal routing must run before that work begins.
5. **Managed-state override:** maintenance, upgrade, malformed-state, or other pre-routing conditions that require a specific managed role must still take precedence over conversational continuity.

## Scope

The resolving PR must:

- define the boundary between the lightweight per-request managed-state gate and full workflow or role resolution
- define what counts as a conversational follow-up that does not require fresh routing
- define how the current active role persists within a conversation and when that continuity ends
- keep role continuity session-scoped and avoid introducing persistent runtime state as a new Ava requirement
- allow a roleless follow-up only when no role-scoped capability, constraint, project action, or new authority is needed
- retain the current role without repeated registry traversal or required-reading reload when that role remains valid and its required context is already loaded
- define the minimal announcement for same-role continuation, such as stating that the current role remains active
- enumerate the triggers that force fresh routing, including new tasks, explicit workflow or role activation, role mismatch, authority changes, and managed-state overrides
- preserve finding 07's guarantee that a host persona cannot classify a new substantive request as outside Ava before Ava determines whether routing is required
- reconcile the accepted documentation that currently states that every request performs explicit workflow or role routing and has exactly one active role
- add regression coverage for roleless clarification, same-role continuation, role transition, new scoped work after a roleless turn, and the original finding 07 bypass case

## Completion criteria

- Ava distinguishes managed-state gating from full role resolution
- a pure follow-up can be answered without resolving a role when no role-scoped authority is needed
- a same-role follow-up retains the active role without repeating unchanged routing and required-reading work
- same-role continuation states that the existing role remains active before role-scoped handling continues
- new substantive work still routes before project action or role-scoped handling
- a change in task, workflow, authority, or role fit causes fresh routing
- managed maintenance and upgrade gates still override normal conversational continuity
- the original generic host-persona bypass fixed by finding 07 remains impossible
- session continuity does not require Ava to introduce a persistent runtime or hidden mutable role state
- public routing, role, workflow, conformance, and compatibility documentation are updated consistently after the user approves the final routing contract
- repository and assembled-installation regression coverage protects all defined continuity and rerouting cases
- concrete resolution and validation evidence are recorded below

## Resolution evidence

Pending.

## Release qualification follow-up

After implementation, exercise a realistic installed project through a multi-turn session that covers an initial routed task, a pure clarification, a same-role action, a role-changing request, and a later new task after a roleless follow-up. Record that Ava performs full routing only at the defined transition points while preserving finding 07's no-bypass guarantee.
