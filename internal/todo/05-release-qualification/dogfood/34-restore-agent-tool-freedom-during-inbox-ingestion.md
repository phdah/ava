---
type: Internal Development Task
title: Restore Agent Tool Freedom During Inbox Ingestion
description: Revert Finding 27's mechanism-level ban so Inbox Ingester may use available tools, scripts, temporary helpers, and other execution mechanisms as needed while remaining accountable for trusted boundaries, semantic fidelity, provenance, and the final project state.
tags: [internal, roadmap, dogfood, inbox, tools, agents, qualification]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 34
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:openai-chatgpt
  at: 2026-08-29T11:50:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-29T12:56:00+02:00
---

# Restore Agent Tool Freedom During Inbox Ingestion

## Decision

Finding 27 introduced an explicit prohibition on creating or executing scripts, programs, temporary implementation files, and other programmatic transformation mechanisms during inbox ingestion. That restriction is not aligned with Ava's intended responsibility.

Ava should define the role's authority, trust boundaries, required outcomes, and semantic correctness. It should not prescribe which tools or execution mechanisms the host agent may use to accomplish the work. An agent may therefore use its available tools, scripts, code execution, document readers, or temporary helpers when they are useful.

The resulting ingestion must still satisfy all applicable role constraints and output requirements. Tool use does not permit fabricated content, unsafe instruction following, incorrect disposition, missing provenance, unrelated permanent project mutations, or any other behavior prohibited independently of the execution mechanism.

## Motivation

The mechanism-level ban introduced by Finding 27 created a concrete problem: Inbox Ingester could no longer use available tooling to read formats such as `.docx` and `.pptx`, which then produced Finding 34's proposal for a special sanctioned Office reader. Adding format-specific exceptions or Ava-owned reader tooling is the wrong abstraction. The agent should be free to use the tools available in its host environment.

Findings 28 and 29 remain the semantic safeguards. They require correct per-passage disposition, rendered-output reconciliation, bounded structural evidence, and independent semantic audit. Those requirements should judge the result rather than the implementation technique used to produce it.

## Scope

- remove the Inbox Ingester instruction and constraint language added by Finding 27 that prohibits scripts, generated code, temporary helper artifacts, code execution, or programmatic transformation as an ingestion mechanism
- make it explicit, where useful, that Inbox Ingester may use the host agent's available tools and execution capabilities within its existing authority and trust boundaries
- remove qualification checks and regression coverage whose only purpose is to fail ingestion because a temporary helper, script, or other tool-driven mechanism was used
- preserve the semantic fidelity, disposition, provenance, source-preservation, trust, and final-state requirements established independently of Finding 27, especially Findings 28 and 29
- keep permanent project mutations bounded to the role's declared destination and maintenance authority; allowing tools does not make unrelated helper artifacts valid final project content
- record that this finding supersedes only Finding 27's execution-mechanism restriction, not the semantic defects that originally motivated Findings 28 and 29

## Completion criteria

- [x] Inbox Ingester no longer prohibits scripts, code execution, temporary helpers, or other available agent tools merely because of the mechanism used
- [x] role instructions continue to constrain authority, trust, fidelity, provenance, source handling, and final project state rather than implementation technique
- [x] qualification no longer fails solely because the agent used a helper script or tool during ingestion
- [x] Findings 28 and 29 semantic protections remain intact
- [x] affected role documentation, qualification coverage, and indexes are aligned
- [x] repository test suite passes

## Resolution evidence

- `templates/base/roles/inbox-ingester/{instructions,capabilities,constraints}.md` now explicitly permits host-agent tools, document readers, scripts, code execution, and temporary helpers while keeping permanent project mutations and final-state cleanup bounded by the existing role authority.
- `templates/base/roles/inbox-ingester/log.md` records that this reverses only Finding 27's mechanism restriction. The rendered disposition-reconciliation requirement introduced by Finding 28 remains unchanged.
- `internal/release/qualification_runner.py` removes the transient direct-project-root watcher and the inbox-specific `guard_project_root` path. Complete inbox qualification still requires processed-source preservation, provenance, structural fidelity, installed conformance, and audit-gated `structural-pass` semantics.
- `internal/release/tests/test_qualification_runner.py` replaces the former transient-helper rejection regression with a regression proving that an OpenCode session may create and remove a temporary project-root helper without failing qualification, and pins the complete-inbox scenario's independent semantic-audit requirement.
- `internal/release/qualification-runner.md` and the release implementation log now describe outcome-based inbox qualification rather than tool-mechanism policing.
- The dogfood backlog and V1 release roadmap advance to assembling a new exact corrective-alpha candidate and rerunning the complete qualification flow. Finding 25 remains post-v1 and non-blocking.
- The repository test suite passes with these changes before the implementation PR is considered complete.
