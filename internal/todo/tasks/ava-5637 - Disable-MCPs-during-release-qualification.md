---
id: ava-5637
title: Disable MCPs during release qualification
status: To Do
assignee: []
created_date: '2026-09-01 20:15'
labels:
  - internal
  - roadmap
  - release
  - qualification
  - opencode
  - mcp
milestone: m-0
dependencies:
  - ava-5638
type: enhancement
ordinal: 6637
---

## Description

Make every OpenCode session that remains part of Ava release qualification after AVA-5638 run with MCP integrations hard-disabled. Qualification does not require MCP access, and inheriting user or global MCP configuration adds unnecessary tools, context, token consumption, latency, and environmental variability to qualification runs.

AVA-5638 must be completed first. If it removes OpenCode entirely from qualification, this task should be closed as `Done` with the `Won't Fix` label instead of implemented. Qualification must not retain OpenCode merely to satisfy this task.

Where OpenCode remains necessary, qualification must own its configuration explicitly rather than relying on the operator to disable MCPs globally or on a particular local OpenCode setup.

## Required behavior

1. Every OpenCode process still spawned by release qualification after AVA-5638 must receive qualification-owned configuration that disables all MCP servers.
2. The disablement must override or neutralize MCPs configured by user-global, repository-local, environment-specific, or inherited OpenCode configuration.
3. Qualification must not require operators to modify their normal OpenCode configuration before or after a run.
4. The rule must apply consistently to all remaining qualification-owned OpenCode sessions, including nested sessions, independent audits, retries, and any future qualification phase introduced by AVA-5636.
5. MCP disablement must not weaken the existing qualification-owned external-directory permission configuration or other required sandbox/runtime settings.

## Implementation scope

- first use AVA-5638's outcome to identify whether any OpenCode qualification path remains
- if none remains, close this task as intentionally not implemented
- otherwise identify the canonical remaining OpenCode invocation/configuration path used by qualification
- add explicit qualification-owned configuration that disables every MCP integration for those invocations
- ensure nested and independently spawned qualification sessions inherit the same MCP-disabled policy
- document the behavior in the qualification/release procedure where runtime isolation is defined
- add regression coverage using a deliberately configured MCP to prove qualification sessions cannot discover or invoke it
- preserve normal repository development behavior outside qualification

## Completion criteria

- AVA-5638 has been completed and its host-runtime decision is known
- if OpenCode is no longer used by qualification, this task is closed without implementation using `Done` plus the `Won't Fix` label
- otherwise, a qualification run started from an environment with one or more MCPs configured still exposes no MCP tools to qualification OpenCode sessions
- all remaining qualification-owned OpenCode invocations use the same enforced MCP-disabled policy
- nested sessions and the independent audit cannot access MCPs where OpenCode remains involved
- ordinary non-qualification OpenCode use remains unaffected
- tests fail if MCP inheritance is accidentally reintroduced
- qualification documentation states that MCPs are intentionally disabled for determinism and token efficiency wherever OpenCode is retained
