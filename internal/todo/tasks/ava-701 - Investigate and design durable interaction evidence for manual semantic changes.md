---
id: ava-701
title: >-
  Investigate and design durable interaction evidence for manual semantic
  changes
status: Done
assignee: []
created_date: ''
updated_date: '2026-08-30 22:30'
labels:
  - internal
  - roadmap
  - phase-07
  - provenance
  - interaction-evidence
  - metadata
milestone: m-0
dependencies:
  - ava-602
ordinal: 701
---

## Description

Define a privacy-aware provenance mechanism for semantic mutations supported or authorized directly by a user's conversational prompt. This is a proposal/design task and must not record or implement a new public format or role-authority architecture without explicit user approval.

## Purpose

A mutation role may change trusted context from facts, corrections, approvals, conflict resolutions, task-state changes, or retirement decisions supplied directly in conversation. Existing `updated` metadata identifies the recording agent and Git records the mutation, but neither necessarily preserves the human statement that supplied the fact or authority. Commit messages are not canonical evidence, and scoped `log.md` must remain reserved for meaningful conceptual/structural history rather than routine prompt provenance.

Investigate a durable, minimal evidence model, potentially using narrowly scoped project-owned processed evidence referenced from canonical destinations through `sources` metadata and precise Markdown attribution where useful. The exact path, representation, and authority model remain undecided until user approval.

## Required design decisions

### Capture boundary

Define deterministic inclusion/exclusion rules. Capture only material user-supplied facts, task-state changes, corrections, conflict resolutions, approvals, retirement decisions, or other authority necessary to understand a semantic mutation. Exclude formatting, mechanical repairs, already-authorized deterministic operations, and changes fully supported by an existing durable source.

Do not create a transcript archive. Preserve the smallest complete exact user statement needed for the mutation, with only enough surrounding context to avoid misleading evidence.

### Evidence and authority semantics

Distinguish the human supplier/approver from the role or tool that records the evidence. Separate factual evidence from approval evidence. Approval may authorize mutation while a proposal or existing source remains factual evidence. Storage location must not itself make content authoritative.

Define correction, conflict-resolution, retirement, and later supersession semantics without rewriting original evidence.

### Record/reference model

Evaluate canonical path, filename, Markdown structure, metadata, lifecycle, ownership, indexing, provenance fields, `sources` references, precise footnotes, attachment handling, and whether mutation roles may create evidence directly or must invoke a bounded deterministic capture mechanism.

Do not infer verified human identity from display names or host metadata.

### Privacy and safety

Define minimization, secret/token handling, personal or regulated data behavior, user-visible disclosure/confirmation, redaction boundaries, attachment/repository-size handling, unsafe-capture fallback, deletion/correction/retention, and Git-history limitations.

### Mutation integrity

Define atomic evidence creation plus semantic mutation, rollback/interruption recovery, concurrent edits, validation, and completion checks. A successful operation must not leave a semantic mutation without required evidence, an orphan evidence record, a broken link, or inconsistent provenance.

Interaction evidence does not replace scoped conceptual history when the same mutation independently crosses the `log.md` threshold.

### Contract integration

If approved, identify required changes to project-owned path/ownership rules, inbox/processed lifecycle, document metadata and `sources`, mutation-role capabilities/constraints, mutation completion, change review, installation/upgrade/validation, and compatibility contracts.

Reviewers should inspect available linked interaction evidence before concluding a manual semantic mutation lacks authority, while still recognizing that not every manual change requires captured prompt evidence.

### Backlog.md compatibility

Use the accepted Backlog.md model from AVA-601/602. Interaction evidence may support a task-state mutation but must not duplicate task history, become a second backlog, or introduce competing task lifecycle/approval semantics.

## Evaluation scenarios

Cover at least: direct new fact, correction of sourced context, approval of a proposal, conflict resolution, trusted-context retirement, conversational completion of a Backlog task, already-authorized deterministic operation, formatting-only repair, mixed relevant/secret prompt, attachment or multi-turn evidence, either-side atomic failure, and a mutation that also meets the scoped-history threshold.

## Constraints

- Git commit messages are not canonical interaction evidence
- do not persist full transcripts by default
- preserve exact relevant wording when safely possible rather than paraphrasing
- do not infer verified human identity
- do not require interaction evidence when an existing durable source fully supports the mutation
- do not weaken scoped-history thresholds
- do not grant new mutation-role write authority before the ownership/safety model is approved
- do not adopt a mandatory public path/format/authority change without explicit user approval

## Completion criteria

- deterministic capture/exclusion thresholds
- distinct factual versus approval evidence models
- minimal exact-statement representation and separate human/agent provenance
- complete privacy, secrets, attachment, minimization, retention, and unsafe-capture rules
- explicit path, ownership, metadata, lifecycle, links, supersession, and authority semantics
- atomic mutation/evidence behavior and recovery/validation model
- evaluated direct-role versus deterministic-capture alternatives with recommendation
- independent scoped-history and review semantics
- Backlog.md remains the sole task-state model
- affected public contracts/roles/fixtures/upgrade impacts are identified
- design is presented for explicit user approval before architecture is recorded or implemented

This follows AVA-602 and is tracked toward the `v1.0.0` milestone rather than resuming the former parked V1 release-task path.

## Design result

**State:** complete design proposal for review. Nothing in this task makes the proposal an accepted Ava public contract. Public format, role-authority, compatibility, installer, or release behavior must not change until the user explicitly approves this design or a revised form of it.

### Recommended model

Use a lazily created project-owned interaction-evidence collection below the existing preserved-source boundary:

```text
./inbox/processed/interactions/
  index.md
  YYYY-MM/
    index.md
    <interaction-id>.md
```

Do not scaffold this collection during installation. Create it only when the first qualifying interaction must be preserved. Keeping the records below `./inbox/processed/` preserves the existing ownership and trust model: the record is durable source evidence, not authoritative project knowledge merely because it exists or has been processed.

Authorized mutation roles should be allowed to create these records directly as part of the same semantic change. Ava should not require a persistent service, transcript store, or mandatory capture CLI. A bounded deterministic validator/helper may later validate record shape, links, target symmetry, uniqueness, and transaction completeness, but it must not decide which user words are material, whether a statement is factual authority, or whether the role has semantic mutation authority.

### Deterministic capture boundary

Interaction evidence is required only when all of the following are true:

1. the requested operation is a meaningful semantic mutation rather than a trivial edit;
2. the mutation materially depends on a fact, correction, approval, conflict resolution, retirement decision, exceptional task-state decision, or other authority supplied in the current conversation;
3. an existing durable project source does not already fully support that same fact or authority;
4. preserving the relevant statement is safe under the privacy rules below; and
5. the active role independently has authority to perform the target mutation.

Capture examples:

- a new durable fact supplied directly by the user and written into trusted context;
- a user correction that changes or supersedes previously sourced trusted context;
- explicit approval needed before a proposal or compatibility-sensitive change may be applied;
- a user decision resolving a material contradiction between otherwise plausible sources;
- explicit retirement or supersession of trusted context when no durable decision source already records it;
- a Backlog task-state change whose authority comes from a new user decision rather than normal completion of already-authorized implementation work.

Do not capture:

- formatting, spelling, wrapping, or other trivial edits;
- deterministic installation, validation, migration, assembly, or release operations already authorized by an established protocol;
- a normal task transition to `Done` after the requested implementation and acceptance criteria are satisfied;
- an agent conclusion fully supported by existing durable project sources;
- routine restatement of already-recorded facts or decisions;
- generic conversation, brainstorming, questions, or instructions that do not supply evidence or authority for a semantic mutation.

The capture test is about the source of authority for the mutation, not whether a human happened to be present in the conversation.

### Minimal record and metadata

Each record should be one ordinary project-owned Markdown source document with a collision-resistant opaque interaction identifier. The identifier must not encode the user's name, secret material, or substantive prompt text.

Proposed shape:

```yaml
---
type: Interaction Evidence
title: <short non-sensitive description>
generated:
  by: agent:<recording-role-or-agent>
  at: <ISO-8601 timestamp with offset>
interaction_id: <opaque id>
evidence_kind: <fact|authorization|correction|conflict-resolution|retirement|task-state|mixed>
supplier:
  kind: human
  identity: unverified
  actor: <optional established human:... identifier>
targets:
  - ./path/to/canonical-target.md
supersedes: []
redactions: []
---
```

Rules:

- `generated.by` records the agent or deterministic tool that created the evidence file; it must never be used to imply that agent supplied the human fact or approval.
- `supplier.kind: human` records only that the statement came from the conversational user.
- `supplier.identity` remains `unverified` unless a project-owned trusted mechanism establishes identity independently of display name or host metadata.
- `supplier.actor` is optional and may be written only when an existing stable `human:...` identity is already established by trusted project context.
- `targets` identifies the semantic records whose mutation depends on this evidence. It does not grant mutation authority.
- `supersedes` points from a later evidence record to earlier evidence when the user corrects, resolves, retires, or replaces prior interaction evidence. Earlier records remain unchanged.
- `redactions` records only non-sensitive reasons or categories, never the removed secret value.

The Markdown body should contain:

```markdown
# Statement

> <smallest complete exact statement or ordered exact excerpts>

# Context

<only the minimum context required to explain what the statement authorizes or supports>
```

For multi-turn evidence, use the smallest ordered set of exact excerpts required to preserve the decision. Do not copy surrounding turns merely for convenience.

### Factual versus approval evidence

`fact`, `correction`, `conflict-resolution`, and factual portions of `mixed` evidence support claims about project state. `authorization` supports permission to apply a proposal or otherwise gated mutation. Approval is not itself factual proof of the proposal's claims.

When a change requires both factual support and approval, retain both sources distinctly. For example, a design document may remain the factual/proposal source while a later interaction record proves that the user approved applying it.

Canonical non-task documents should reference qualifying interaction evidence through the existing `sources` mechanism. The evidence record's `evidence_kind` determines how reviewers interpret that source. Use a precise Markdown footnote when only a specific claim or decision is supported by the interaction evidence.

Storage below `inbox/processed/` and presence in `sources` do not make the interaction record authoritative by themselves. Authority still comes from the active role, user-approved task, applicable project instructions, and the semantics of the statement.

### Corrections, conflicts, retirement, and supersession

Evidence is append-only in meaning. Do not rewrite an earlier statement because a later statement changes the project decision.

- **Correction:** create new `correction` evidence with `supersedes` referencing the earlier interaction evidence when applicable. Update the canonical destination to the corrected state and current supporting sources.
- **Conflict resolution:** create `conflict-resolution` evidence that records the exact user choice and identifies the affected target. Preserve the conflicting source material unless its own lifecycle independently allows removal.
- **Retirement:** create `retirement` evidence for the user decision, then apply the normal lifecycle/deprecation/removal rules to the canonical target. Do not delete earlier evidence as part of retirement.
- **Later supersession:** create a new record pointing backward. Never mutate old evidence solely to add a forward pointer.

A correction to the evidence record itself is different from a correction of the project fact. If the recorder captured the wrong excerpt or unsafe material, replace the working-tree record before completion when possible. If it was already committed, add a corrected evidence record, remove the unsafe/incorrect working-tree record when appropriate, and explicitly acknowledge that Git history may retain the earlier bytes.

### Privacy, secrets, and retention

Interaction capture must be minimization-first.

- Never preserve passwords, API keys, access tokens, private keys, session cookies, recovery codes, or equivalent secrets.
- When a prompt mixes relevant evidence with an irrelevant secret, preserve only the safe relevant excerpt and record a generic redaction reason such as `secret omitted`.
- When the secret itself is necessary to understand or perform the semantic mutation, do not create interaction evidence and do not complete a mutation whose required provenance cannot be recorded safely. Ask for a sanitized restatement or an appropriate durable secure source.
- For personal, regulated, or highly sensitive information, capture only the minimum necessary statement. If the evidence would materially increase exposure compared with the target fact itself, require explicit confirmation or a safer durable source before persisting it.
- Do not infer or persist a verified human identity from account display names, usernames, email metadata, or host UI labels alone.
- Do not embed binary attachments or large transcripts in interaction evidence. A material attachment should use the ordinary source/inbox lifecycle when it must be preserved. The interaction record may reference that stable project-local source and retain only the minimal conversational decision about it.
- Do not store hashes of removed secrets as a substitute for redaction.

Successful capture should be disclosed in the mutation completion report by naming the created evidence path. Separate pre-write confirmation is not required for ordinary non-sensitive capture because the user has already requested the semantic mutation. Confirmation is required when sensitive-data minimization, ambiguous excerpt selection, or unusual retention materially changes what would be persisted.

Deletion removes the current project file only. Because Git history may retain prior content, any deletion or correction report must state that repository-history erasure is a separate repository-administration concern and is not guaranteed by deleting the file.

No general time-based retention policy is proposed. Evidence should remain as long as a surviving semantic mutation, historical interpretation, or review obligation depends on it. Once no live or historical target depends on the record, ordinary project-owned deletion rules may remove it from the current tree.

### Atomic mutation and recovery

Treat required interaction evidence and the semantic mutation as one logical transaction.

Before completion:

1. determine the exact qualifying statement and safe evidence record;
2. prepare the evidence file and target mutation together;
3. add the target's `sources` or explicit Backlog evidence link when required;
4. validate that every evidence `target` exists and every required target reference resolves back to the record;
5. apply ordinary metadata, index, link, and scoped-history checks;
6. report success only when the evidence and mutation are both complete.

If execution stops after only one side is written, the next maintenance pass must treat the state as incomplete rather than accepted. Recovery may either finish the missing side when the original authority remains clear or roll back the orphan mutation/evidence. It must not silently bless an orphan because Git contains a partial change.

Use opaque collision-resistant interaction IDs so concurrent captures cannot overwrite one another. Existing evidence files must never be overwritten on ID collision. Concurrent semantic edits to the same canonical target still follow the host/repository's normal conflict handling; evidence does not provide last-writer-wins semantics.

A future validator may expose errors such as missing target, missing reverse reference, orphan evidence, duplicate interaction ID, unsafe absolute path, malformed evidence metadata, or a required evidence link that resolves outside project-owned content.

### Direct role capture versus deterministic helper

Three models were evaluated:

1. **Mandatory deterministic capture tool:** strongest structural consistency, but it would need semantic inputs selected by an agent and risks becoming a new runtime/CLI responsibility that Ava otherwise avoids.
2. **Unrestricted role-written evidence:** fits Ava's file-based model, but without a shared contract it can drift in shape and leave partial transactions unnoticed.
3. **Role-owned semantic capture plus deterministic validation:** preserves Ava's architecture while separating semantic authority from mechanical checks.

Recommendation: **model 3**. The authorized mutation role chooses whether capture is required, selects the minimal exact statement, applies privacy rules, and creates the record. Deterministic tooling validates structure and integrity when available. The helper must not expand role authority or decide what the user meant.

### Backlog.md compatibility

Backlog.md remains the sole task-state model.

Interaction evidence is required for a task-state mutation only when a new conversational statement is itself the material authority, for example an explicit decision to mark work `Won't Fix`, accept a materially reduced outcome, or close/reopen a task contrary to what existing durable task state and acceptance criteria would otherwise imply.

Normal task execution does not need evidence merely because the maintainer updates `To Do -> In Progress -> Done` while fulfilling an already-authorized task.

Do not add an Ava task schema, duplicate status field, or evidence lifecycle to Backlog frontmatter. When evidence is required, keep the Backlog task native and add a normal Markdown reference in its notes/final-summary area to the interaction evidence record. The evidence record may list the task path in `targets`.

### Scoped history and review

Interaction evidence and scoped history solve different problems.

- Interaction evidence answers: "what user-supplied statement or approval supported this semantic mutation?"
- `log.md` answers: "what major conceptual or structural change must future readers understand?"

A qualifying mutation may require both. Creating interaction evidence never lowers or raises the existing scoped-history threshold.

Independent Change Reviewer behavior should be extended, if this proposal is approved, to inspect linked interaction evidence when authority for a manual semantic mutation is material. Review must still distinguish factual evidence from authorization, recognize that missing interaction evidence can be valid when a durable source already supports the change, and never treat an evidence record as proof that the mutation itself was semantically correct.

### Evaluation scenarios

- **Direct new fact:** capture the exact fact, link it through `sources`, and update the canonical target.
- **Correction of sourced context:** capture the correction, preserve the old external/source evidence, update canonical truth, and use `supersedes` only for earlier interaction evidence that is actually superseded.
- **Approval of a proposal:** capture approval as `authorization`; the proposal remains the factual/design source.
- **Conflict resolution:** capture the exact selected resolution and preserve both conflicting source records unless their independent lifecycle permits removal.
- **Trusted-context retirement:** capture the retirement decision and apply normal target lifecycle/history rules.
- **Conversational Backlog completion:** no capture for normal accepted implementation completion; capture only when a new user decision materially changes the expected completion/state semantics.
- **Already-authorized deterministic operation:** no capture.
- **Formatting-only repair:** no capture.
- **Mixed relevant/secret prompt:** keep only the safe relevant excerpt; if the secret is itself required context, stop and request a sanitized source.
- **Attachment or multi-turn evidence:** preserve the attachment through normal source handling when needed and capture only the minimum ordered user excerpts that establish the semantic decision.
- **Evidence write succeeds, target fails:** transaction is incomplete; remove the orphan or finish the target before success is reported.
- **Target succeeds, evidence fails:** transaction is incomplete; roll back or finish evidence before success is reported.
- **Mutation also crosses scoped-history threshold:** create required interaction evidence and the independently required nearest `log.md` entry.

### Contract integration if approved

Implementation should be a separate approved task and should identify exact release impact before changing stable contracts. Expected touch points are:

- **Ownership and mutation authority:** explicitly recognize interaction evidence below `./inbox/processed/interactions/` as project-owned preserved source material and separate storage from authority.
- **Inbox lifecycle:** reserve the `interactions/` child from pending Inbox Ingester discovery and allow authorized mutation roles to create already-processed interaction evidence there without pretending it passed through normal inbox ingestion.
- **Document metadata:** define the interaction-evidence shape, actor separation, target/supersession fields, privacy constraints, and how canonical `sources` entries reference evidence.
- **Knowledge organization:** state that interaction records are source artifacts and must not become canonical knowledge objects merely because they describe durable facts.
- **Mutation roles:** update only roles that can perform semantic project-owned mutations so they apply the capture threshold and transaction checks without broadening their existing write authority.
- **Project Task Manager / task-board contract:** permit a normal Markdown evidence link when a conversational decision materially supplies task-state authority, while keeping native Backlog state canonical.
- **Change Reviewer:** require review of available linked evidence when manual authority is in question, while preserving read-only independence.
- **Scoped history:** explicitly preserve the independent history threshold.
- **Installation:** do not eagerly scaffold interaction evidence directories; creation is lazy and project-owned.
- **Upgrade:** do not retrofit or synthesize historical prompt evidence for existing project content. Any release introducing the behavior should explain that capture applies prospectively after the new contract becomes active.
- **Validation/fixtures:** cover safe record parsing, source/target links, orphan detection, supersession, secrets/redaction boundaries, task links, concurrent IDs, and interrupted transactions.
- **Compatibility/versioning:** treat the eventual mandatory capture behavior as compatibility-sensitive because it changes mutation obligations and review semantics. The exact SemVer classification belongs to the release/versioning assessment once the user approves the public behavior; this design does not pre-approve that classification.

No new managed state, ownership class, task database, transcript service, identity system, or runtime component is required by the recommendation.

## Completion evidence

The design above resolves every required AVA-701 decision and evaluation scenario while keeping the result proposal-only. It recommends direct semantic capture by already-authorized mutation roles, project-owned storage under the existing processed-source boundary, existing `sources` provenance for canonical documents, native Backlog.md task state, append-only supersession, minimization-first privacy rules, and deterministic validation rather than deterministic semantic authority.

No public contract, managed template, role capability, installer behavior, compatibility state, or release asset has been changed. Explicit user approval is still required before the proposed architecture may be recorded as accepted or implemented.