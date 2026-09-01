---
type: Shared Instruction
title: Interaction Evidence
description: Captures minimal conversational source evidence when a semantic mutation materially depends on a user-supplied fact or authority.
tags: [ava, provenance, interaction, evidence, privacy, mutation]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-31T08:19:00+02:00
---

# Purpose

Use interaction evidence to preserve the smallest safe user statement that materially supplies a fact, correction, approval, conflict resolution, retirement decision, exceptional task-state decision, or other authority for a semantic project mutation.

Interaction evidence is source provenance. It is not a transcript archive, a task database, a scoped history mechanism, an identity system, or a new authority class.

# Capture threshold

Interaction evidence is required only when all of these are true:

1. the operation is a meaningful semantic mutation rather than a trivial edit;
2. the mutation materially depends on information or authority supplied in the current conversation;
3. no existing durable project source already fully supports that same information or authority;
4. the relevant statement can be preserved safely under the privacy rules below; and
5. the active role independently has authority to perform the target mutation.

Capture qualifying new facts, corrections, approvals required by an existing gate, explicit conflict resolutions, retirement or supersession decisions, and exceptional task-state decisions whose authority comes from the current conversation.

Do not capture formatting-only work, deterministic operations already authorized by an established protocol, normal task completion after accepted implementation, conclusions fully supported by existing durable sources, routine restatements, brainstorming, or generic conversation that does not supply evidence or authority for a semantic mutation.

The test is the source of authority for the mutation, not merely whether a human participated in the conversation.

# Ancillary evidence authority

A mutating role that lists this instruction as required reading may create the interaction evidence required for its own already-authorized semantic mutation.

This is a narrow ancillary capability only. It does not grant:

- authority to perform a semantic mutation the role could not otherwise perform;
- general authority to classify, ingest, reorganize, or delete inbox sources;
- authority to modify Ava-managed files or state;
- authority to create evidence for unrelated work.

The read-only Change Reviewer may inspect interaction evidence but must not create or modify it.

# Storage and source lifecycle

Store each record directly with ordinary processed inbox sources:

```text
./inbox/processed/interaction-<interaction-id>.md
```

Do not create an interaction-specific directory, monthly hierarchy, secondary index, or other source-form taxonomy. `./inbox/processed/` already represents preserved successfully handled source material.

The identifier must be opaque, collision-resistant, and must not encode a person's name, secret material, or substantive prompt text. Existing evidence files must never be overwritten on collision.

The conversational source is considered successfully processed only when the evidence record, target mutation, and required provenance reference all succeed as one logical operation. Do not create a pending duplicate merely to move it immediately. If the operation cannot complete, do not report the source as processed.

Storage under `./inbox/processed/` does not make a statement authoritative. It remains source evidence and follows the same trust boundary as other processed inbox material.

# Record format

A record is an ordinary non-reserved Markdown document:

```yaml
---
type: Interaction Evidence
title: <short non-sensitive description>
generated:
  by: agent:<recording-role-or-agent>
  at: <ISO-8601 timestamp with offset>
interaction_id: <opaque collision-resistant id>
evidence_kind: <fact|authorization|correction|conflict-resolution|retirement|task-state|mixed>
supplier:
  kind: human
  identity: unverified
  actor: <optional established human:... identifier>
targets:
  - ./path/to/project-owned-target.md
supersedes: []
redactions: []
---

# Statement

> <smallest complete exact statement or ordered exact excerpts>

# Context

<only context required to avoid misleading interpretation>
```

Rules:

- `generated.by` identifies the agent or deterministic tool that recorded the source. It does not identify the human supplier.
- `supplier.kind` is `human` for conversational evidence.
- `supplier.identity` is `unverified` unless an independent trusted project mechanism establishes identity.
- `supplier.actor` is optional and may use an existing stable `human:...` identifier only when trusted project context already establishes it.
- `targets` lists the project-owned semantic records whose mutation depends on the evidence. It does not grant mutation authority.
- `supersedes` contains earlier interaction evidence paths only when the new statement actually corrects, resolves, retires, or replaces them.
- `redactions` contains only non-sensitive reasons such as `secret omitted`; it must never contain the removed value.
- preserve exact relevant wording when safely possible. For multi-turn evidence, keep only the smallest ordered excerpts needed to preserve the decision.

# Factual and authorization evidence

`fact`, `correction`, `conflict-resolution`, and factual portions of `mixed` evidence support claims about project state. `authorization` supports permission to apply a proposal or another gated mutation. Approval is not factual proof of the proposal's claims.

When a mutation needs both factual support and approval, preserve those sources distinctly.

For ordinary non-task Markdown targets, add the evidence through the existing `sources` metadata using the exact processed-source path. Use a Markdown footnote when only a specific claim or decision needs precise attribution.

For a native Backlog.md task, keep Backlog.md as the sole task-state model. When interaction evidence is required, add a normal Markdown link in the task notes or final-summary area instead of adding Ava-specific task frontmatter.

# Corrections and supersession

Interaction evidence is append-only in meaning.

- A correction creates a new `correction` record and updates the canonical target to the corrected state.
- A conflict resolution creates a new `conflict-resolution` record preserving the exact user decision.
- A retirement creates a new `retirement` record before normal target lifecycle rules are applied.
- Later evidence points backward through `supersedes`; earlier evidence is not rewritten solely to add a forward pointer.

If the recorder captured the wrong excerpt or unsafe content before completion, repair the working-tree record before success is reported. If unsafe or incorrect content was already committed, create corrected evidence as needed and explicitly report that deleting the current file does not guarantee removal from Git history.

# Privacy and safety

Capture is minimization-first.

Never preserve passwords, API keys, access tokens, private keys, session cookies, recovery codes, or equivalent secrets. Do not store hashes of omitted secrets.

When a prompt mixes relevant evidence with an irrelevant secret, preserve only the safe relevant excerpt and record a generic redaction reason. When the secret itself is necessary to understand the mutation, do not persist interaction evidence or complete a mutation whose required provenance cannot be recorded safely. Request a sanitized restatement or an appropriate durable secure source.

For personal, regulated, or otherwise highly sensitive information, persist only the minimum necessary statement. When preserving the evidence would materially increase exposure compared with the target fact itself, require explicit confirmation or use a safer durable source.

Do not infer verified human identity from display names, usernames, email metadata, account metadata, or host UI labels alone.

Do not embed large transcripts or binary attachments. Preserve a material attachment through the ordinary source lifecycle and capture only the minimal conversational decision about it.

There is no default time-based retention. Keep evidence while a live or historical semantic interpretation or review obligation depends on it. Current-tree deletion follows ordinary project-owned deletion rules and does not imply Git-history erasure.

# Atomicity and recovery

Treat required evidence and the semantic mutation as one logical transaction:

1. determine the qualifying statement and safe minimal excerpt;
2. prepare the processed evidence record and target mutation together;
3. add the target's `sources` entry or Backlog Markdown link;
4. validate evidence shape, target existence, reverse references, and supersession paths;
5. run the target's ordinary metadata, index, link, and scoped-history checks;
6. report success only when every required side is complete.

If execution stops after only one side is written, the state is incomplete. Recovery must either finish the missing side while the original authority remains clear or roll back the orphan evidence or semantic mutation. Do not silently accept a partial transaction.

Concurrent evidence uses distinct collision-resistant IDs. Concurrent changes to the same semantic target still follow normal repository conflict handling; evidence does not create last-writer-wins semantics.

# Role-specific application

Project Steward and Role Manager apply this threshold to their semantic project changes. Inbox Ingester applies it when a new conversational decision, rather than the selected source itself, supplies material authority for ingestion. Project Task Manager applies it only to exceptional conversational task-state decisions, not ordinary execution progress. Upgrade Role applies it only when a new user decision supplies authority for a project-owned semantic migration change beyond the installed guidance; guidance-driven deterministic or semantic work does not create evidence merely because the user invoked the upgrade.

Change Reviewer inspects available linked interaction evidence when authority for a manual semantic mutation is material. It must distinguish factual evidence from authorization and must not infer a defect merely because interaction evidence is absent when another durable source fully supports the mutation.

# Scoped history boundary

Interaction evidence and scoped `log.md` history are independent.

Interaction evidence records the user-supplied source or authority for a mutation. Scoped history records major conceptual or structural consequences that future readers need to understand. Creating interaction evidence neither raises nor lowers the existing scoped-history threshold. A change may require both.

# Validation

Deterministic validation may check structure and integrity but must not decide what the user meant or whether a role has semantic mutation authority.

Stable diagnostics are:

- `AVA-INTERACTION-PATH`: evidence is outside the accepted processed-source location.
- `AVA-INTERACTION-SHAPE`: required metadata is missing or malformed.
- `AVA-INTERACTION-ID`: identifier or filename binding is invalid.
- `AVA-INTERACTION-DUPLICATE-ID`: more than one record declares the same interaction identifier.
- `AVA-INTERACTION-KIND`: evidence kind is unsupported.
- `AVA-INTERACTION-SUPPLIER`: supplier metadata is invalid or claims unsupported identity.
- `AVA-INTERACTION-TARGET`: a target path is unsafe, managed, missing, or otherwise invalid.
- `AVA-INTERACTION-REVERSE-REF`: a target does not reference the evidence record.
- `AVA-INTERACTION-SUPERSEDES`: a superseded evidence path is unsafe, missing, or not interaction evidence.
- `AVA-INTERACTION-STATEMENT`: the exact-statement body is absent.

Validation does not scan conversations or infer that an uncaptured conversation should have produced evidence.

# Upgrade behavior

This contract applies prospectively after the installed Ava version introducing it becomes active. Do not synthesize historical interaction evidence for earlier project mutations.

Release guidance must identify this as compatibility-sensitive when the new mandatory capture obligation affects project-owned mutation or review behavior.