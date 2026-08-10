---
type: Internal Development Task
title: Stabilize the Published Release Candidate
description: Exercise the immutable release candidate as the final compatibility input and resolve or classify every result before stable qualification.
tags: [internal, roadmap, release-candidate, stabilization, qualification, dogfood]
status: pending
phase: 5
parent: 05-publish-release-candidate
order: 5.1
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T15:45:02+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T16:23:00+02:00
---

# Stabilize the Published Release Candidate

Use [Step 5 of the V1 Release Operator Path](v1-release-operator-path.md#step-5-stabilize-the-published-rc) as the canonical operator entry point.

## Entry gate

Begin only after an immutable release candidate has passed [release-candidate publication](05-publish-release-candidate.md).

## Scope

- regenerate the synthetic qualification vault from its fixed specification and verify the baseline digest
- repeat fresh installation, mature-project installation, repeated OpenCode sessions, every role-routing class, and every managed workflow
- repeat inbox ingestion, project-context maintenance, role creation, and isolated semantic review
- exercise modified, missing, corrupt, and unexpected managed content
- exercise resume, abort, rollback, and finalize from their maintained fault-injection states
- complete semantic reconciliation through Upgrade Role and verify normal routing remains blocked until finalization
- upgrade every source declared by the RC, then uninstall and reinstall while preserving project-owned content
- record context-loading failures, semantic regressions, performance problems, host-persona bypasses, and private-to-work leakage as release findings

## Change policy

After RC publication, accept only release-blocking fixes, documentation corrections, or compatibility-preserving repairs required for stable qualification.

An incompatible public contract or behavior change requires another release candidate and a complete repeat of this task. Every discovered defect requiring repository work must receive a bounded roadmap finding before correction.

## Executable evidence

Produce a revision-bound, machine-readable RC qualification result that references the release assets, conformance output, qualification-vault run manifest, upgrade edges, transcripts, retained project-owned hashes, findings, and final disposition.

## Completion criteria

- the complete generated-vault matrix passes against immutable RC assets
- every declared RC source upgrade and terminal lifecycle state has executable evidence
- no blocker or required-v1 finding remains open
- no incompatible public change is planned
- every known limitation has an approved stable-safe disposition
- the RC qualification result is complete and identifies the exact RC version and source revision
- the RC is accepted as the final input to stable qualification
