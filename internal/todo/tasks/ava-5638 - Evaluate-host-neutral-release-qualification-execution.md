---
id: ava-5638
title: Evaluate host-neutral release qualification execution
status: In Progress
assignee: []
created_date: '2026-09-01 20:20'
labels:
  - internal
  - roadmap
  - release
  - qualification
  - portability
  - host-neutral
milestone: m-0
dependencies: []
references:
  - ava-5636
  - ava-5637
type: enhancement
ordinal: 6636
---

## Description

Evaluate whether Ava's release qualification can stop depending on OpenCode as the agent runtime and instead use a host-neutral qualification model that can be executed from other capable agent hosts, including the ChatGPT app with repository access.

Today the qualification system is coupled to OpenCode process execution, session inventory, session export, OpenCode-specific permissions/configuration, and transcript capture. The desired direction is that qualification semantics belong to Ava rather than to one agent host. OpenCode should not be required merely to exercise Ava's role, routing, ingestion, maintenance, semantic-review, and lifecycle behavior when another host can perform the same interactions and produce equivalent evidence.

This task must evaluate feasibility first. If the maintained qualification contract can be represented host-neutrally without weakening evidence or determinism, implement that path. If some checks genuinely require capabilities unavailable in the ChatGPT app or another non-local host, identify those checks precisely and preserve only the minimum host-specific execution needed.

## Evaluation questions

1. Inventory every place qualification currently depends on OpenCode-specific behavior, including process invocation, session enumeration/export, nested-session discovery, permissions, configuration, transcript format, token/session metadata, and independent audit execution.
2. Separate the qualification contract itself from the OpenCode adapter used to execute it today.
3. Determine which qualification scenarios can be driven through a host-neutral interaction protocol using repository/filesystem operations and structured prompts/responses rather than spawning `opencode run`.
4. Determine what evidence a non-OpenCode host must provide so results remain auditable, reproducible enough for release gating, and bound to the exact candidate/revision.
5. Explicitly evaluate execution from the ChatGPT app with the available GitHub/repository capabilities. Do not claim support unless the complete required workflow can actually be represented and verified there.
6. Identify any scenarios that require local process execution, temporary project roots, shell commands, mutable filesystem sandboxes, nested agent sessions, or other capabilities that cannot be reproduced through ChatGPT-connected repository operations.

## Preferred design

If feasible, define qualification as a host-neutral protocol plus deterministic validators:

- Ava owns scenario definitions, inputs, expected outcomes, evidence schema, and acceptance rules.
- An agent host receives one scenario at a time and returns structured outputs/evidence through a documented interface.
- Host-specific adapters are optional execution layers rather than the qualification contract itself.
- OpenCode may remain one adapter, but must not be the mandatory runtime when another capable host can satisfy the same contract.
- The ChatGPT app should be able to execute the qualification workflow directly when its available repository/file capabilities satisfy a scenario's requirements.
- Deterministic checks should remain scripts/tests where an LLM is unnecessary rather than being converted into agent work.

## Implementation scope

If the evaluation confirms feasibility:

- extract OpenCode-independent scenario definitions and evidence contracts from the current qualification automation
- replace direct OpenCode assumptions in the qualification core with a host-neutral execution boundary
- provide a documented manual/agent-driven qualification flow that can be followed from ChatGPT or another compatible host
- retain or simplify an OpenCode adapter only when useful as one execution option
- make final evidence validation independent of OpenCode session IDs/database representation
- preserve independent-audit semantics without requiring OpenCode specifically
- update the release procedure and qualification documentation to describe supported execution modes and their capability requirements
- add regression coverage proving equivalent accepted/rejected outcomes across the host-neutral path and the existing adapter for representative scenarios
- integrate cleanly with AVA-5636's split qualification phases

If full host-neutral execution is not feasible:

- record the exact blockers by scenario/capability rather than broadly concluding that OpenCode is required
- decouple every feasible part anyway
- keep OpenCode only for the bounded checks that actually require it
- document what additional host capability would be needed for ChatGPT execution to become complete later

## Relationship to AVA-5637

This task must be completed before AVA-5637 is considered. AVA-5637 disables MCPs for qualification-owned OpenCode sessions, but that hardening should only be implemented for whatever OpenCode execution remains after this evaluation and implementation.

If this task removes OpenCode entirely from qualification, close AVA-5637 as `Done` with the `Won't Fix` label rather than implementing it. If OpenCode remains as a fallback or is still required for bounded scenarios, AVA-5637 continues to apply only to those executions. Do not preserve OpenCode solely to justify AVA-5637.

## Completion criteria

- every OpenCode-specific dependency in current qualification is inventoried and classified as essential, replaceable, or incidental
- the qualification contract is clearly separated from any particular agent-host implementation
- ChatGPT-app feasibility is tested against the actual capability requirements rather than assumed
- when feasible, the complete release qualification can be driven without OpenCode and produces evidence accepted by the same release gate
- when full portability is not feasible, all feasible qualification work is decoupled and the remaining host-specific blockers are explicit and minimal
- release acceptance, revision binding, independent review, failure reporting, and evidence integrity are not weakened
- documentation makes clear which host capabilities are required and does not make unverified compatibility claims

## Rework note

The first implementation incorrectly treated the GitHub connector available in an ordinary Chat session as the complete ChatGPT execution surface and concluded that local execution remained required. That conclusion is rejected.

The approved target is now explicit: the complete non-CI qualification workflow must run in ChatGPT Work Cloud on OpenAI-hosted compute. It must not require OpenCode, Codex Local, Work Local, a developer workstation, or any other user-hosted process. Work Cloud shell/filesystem execution provides the isolated mutable workspace, and Work subagents provide the fresh agent interactions and independent audit.
