---
id: ava-5638
title: Evaluate host-neutral release qualification execution
status: Done
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

## Resolution

The qualification contract is now host-neutral while OpenCode remains the configured local adapter.

Dependency classification:

- **Local process execution** is essential to the maintained qualification semantics. Install, upgrade, conformance, checkpoint, fixture-verification, git, and deterministic validation commands must execute against exact local state. The OpenCode command syntax used for agent work is replaceable and is now behind the host adapter.
- **Mutable temporary project roots** are essential. All 17 scenarios exercise isolated repository-external project state; interruption scenarios additionally depend on persisted transaction/checkpoint state across commands. The specific OpenCode external-directory permission mechanism is incidental and remains adapter-local.
- **Exact local source/target release assets** are essential inputs. How an agent runtime is given permission to read them is adapter-specific.
- **Session enumeration and export** are replaceable. OpenCode still uses its database/session APIs internally to discover top-level and nested current-run work, but those IDs and rows are normalized before compact evidence is produced.
- **Nested-session discovery** is not a core contract requirement. The generic evidence model represents parent/child interaction lineage with opaque interaction IDs. An adapter may obtain that lineage however its host exposes it.
- **OpenCode permissions and configuration** are incidental adapter transport. They are not part of scenario definitions, evidence validation, audit semantics, or release acceptance.
- **Provider-specific transcript format** is replaceable. The active contract requires a materialized complete transcript path plus a SHA-256 digest and does not prescribe the transcript's internal serialization.
- **Token counters and OpenCode session metadata** are not required release evidence and are absent from the host-neutral schema.
- **Independent semantic audit** remains essential, while OpenCode as the audit runtime is replaceable. The audit consumes host-neutral interaction evidence and materialized transcripts and does not require OpenCode IDs, database state, or export commands.

Implementation evidence:

- `qualification_host.py` defines capability profiles, the adapter protocol, host-neutral interaction evidence, OpenCode normalization, transcript materialization, and the independent-audit boundary.
- `qualification_host_runner.py` injects agent execution into the existing deterministic scenario engine through the host protocol.
- `qualification_host_automation.py` is the active two-phase orchestration path and writes host-neutral run records and interaction inventories.
- `qualify-release.sh` routes the canonical release qualification entry point through that host-neutral orchestration while selecting OpenCode as the current local adapter.
- compact host-neutral run schemas no longer require `opencode_version` or `session_inventory_file`; OpenCode-native session evidence remains external adapter-private raw evidence only.
- `audit-prompt.md` now audits opaque interactions and materialized transcript digests rather than OpenCode sessions.
- regression coverage checks capability assessment, interaction normalization, adapter-independent audit inputs, active entrypoint routing, and absence of OpenCode state from the new evidence schemas.

ChatGPT app feasibility was evaluated against the actual GitHub-connected capabilities used for this task. The complete workflow is not currently executable there: every maintained scenario requires local process execution, mutable repository-external workspaces, and exact local release assets, and each phase audit requires access to the raw external evidence tree. The GitHub connector can reason about and mutate repository content but does not expose those qualification sandbox/process/evidence capabilities. A future ChatGPT host that adds them can implement the same protocol without changing the release gate.

OpenCode therefore remains required only as the currently available local agent adapter, not as qualification semantics. AVA-5637 remains applicable to those remaining OpenCode executions and stays `To Do`.
