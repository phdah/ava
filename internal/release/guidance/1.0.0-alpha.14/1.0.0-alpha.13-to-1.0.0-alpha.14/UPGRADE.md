---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.0.0-alpha.13 to 1.0.0-alpha.14
description: Reconciles project-owned routing assumptions with Ava 1.0.0-alpha.14 conversation-aware routing.
guidance_schema: 1
guidance_id: 1.0.0-alpha.13-to-1.0.0-alpha.14
from_version: "1.0.0-alpha.13"
to_version: "1.0.0-alpha.14"
semantic_review_required: true
migration_ids: []
supersedes: []
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T12:36:00+02:00
---

# Upgrade Ava project context from 1.0.0-alpha.13 to 1.0.0-alpha.14

## Summary

Ava 1.0.0-alpha.14 changes normal-turn routing from unconditional fresh role resolution to an explicit three-way classification: roleless conversational follow-up, same-role continuation, or fresh routing. Project-owned roles, workflows, shared instructions, or host entrypoints may contain alpha.13 assumptions that every turn selects exactly one role, reloads required reading, or keeps an invoked workflow procedurally active across follow-ups. Semantic review is therefore required. The updater replaces managed files only and must not infer or rewrite project-owned routing intent.

## Changed managed contracts

- `/AGENTS.md` now performs the managed-state gate on every request and then classifies normal turns as roleless conversational follow-up, same-role continuation, or fresh routing.
- `/.ava/base/shared/instructions/instruction-resolution.md` now permits zero active roles only for bounded conversational follow-ups, permits retained role scope only for the same active objective with already-loaded required context, and requires fresh routing whenever continuity is uncertain or scope changes.
- `/.ava/base/shared/instructions/workflow-routing.md` and the managed router now make explicit that workflow procedural scope does not persist implicitly across later turns. A later turn may retain the workflow's primary role only as ordinary same-role work when workflow-specific procedure, inputs, mode, or context are no longer required.
- Managed role-routing documentation now distinguishes role activation from role continuation and no longer requires registry traversal or unchanged required-reading reloads for valid same-role continuation.

No deterministic migration is declared for this edge.

## Affected project-owned concepts

Inspect only project-owned files that encode routing or continuation behavior:

- `/roles/index.md` and `/roles/**/*.md` when they state or imply that every user turn must freshly select or activate a role, that exactly one role must be active for conversational clarification, or that unchanged required reading must be reloaded on every continuation. The required outcome is compatibility with managed roleless and same-role continuation while preserving the role's own authority and safeguards.
- `/workflows/index.md` and `/workflows/**/*.md` when they state or imply that an invoked workflow remains procedurally active across later turns without explicit invocation, or that every follow-up must rerun workflow resolution. The required outcome is explicit workflow invocation with later eligible follow-ups handled only as ordinary same-role continuation.
- `/shared/**/*.md`, `/index.md`, and the project-owned host integration entrypoint recorded in the manifest when they duplicate or restate the alpha.13 global routing model. The required outcome is removal or reconciliation of project-owned global rules that conflict with the managed conversation-aware router. Pure project documentation that does not participate in active instruction resolution does not require modification.

For each candidate, completion is validated by confirming that new tasks, authority changes, explicit workflows or roles, scoped work after a roleless turn, and uncertain continuity still require fresh routing, while bounded clarification can be roleless and same-objective scoped work can retain the current role only under the managed continuation conditions.

## Required decisions

### `project-routing-intent`

A user decision is required only when a project-owned instruction intentionally requires fresh routing or persistent workflow procedure in a scope where the new managed contract would instead permit roleless or same-role continuation, and the project context does not establish whether that rule is an intentional narrower safeguard or a stale copy of the former global behavior. The affected instruction remains unresolved until its intended authority and scope are decided.

## Semantic migration procedure

1. Do not edit managed files. Record every project-owned file inspected or changed.
2. Search only the bounded project-owned scopes above for semantic statements about per-turn role activation, exact-one-role behavior, required-reading reloads, conversational follow-ups, role continuity, or implicit workflow persistence.
3. For each match, determine whether it is a stale restatement of the former global router, an intentional narrower safeguard, or unrelated descriptive text.
4. Update stale authoritative instructions so they defer to the managed three-way routing classification. Preserve narrower project safeguards only when they remain compatible with the managed activation chain and do not claim global routing authority.
5. Reconcile project-owned workflow instructions so workflow procedure remains active only for explicit invocation. Later turns may retain the workflow's primary role only when they satisfy ordinary same-role continuation and no workflow-specific procedure, inputs, mode, or required context are needed.
6. Update affected project-owned indexes, links, or explanatory text only when necessary to keep the resulting instruction structure coherent.
7. If `project-routing-intent` is triggered, record the unresolved decision and stop compatibility completion until the user resolves it.
8. Run independent semantic review of the changed project-owned instructions. Structural validation supports the review but does not prove routing compatibility.

## Validation and completion criteria

- no project-owned authoritative instruction globally requires fresh role selection, activation, announcement, or unchanged required-reading reload for every normal turn
- no project-owned authoritative instruction requires a role for a bounded conversational follow-up unless that narrower scope genuinely requires role authority
- no project-owned workflow relies on implicit procedural persistence across later turns
- project-owned narrower safeguards do not weaken the managed-state gate, fresh-routing triggers, role authority, workflow resolution, or roleless-turn continuity reset
- every inspected or changed project-owned file is recorded in the migration result
- `project-routing-intent` is resolved when triggered
- independent semantic review reports no unresolved routing, authority, workflow-continuity, or instruction-scope finding

Only then may semantic compatibility advance to `1.0.0-alpha.14`.

## Rollback implications

Project-owned edits made for conversation-aware routing may not remain semantically compatible with 1.0.0-alpha.13, whose managed router performs fresh role resolution for normal follow-ups. Before rollback completes, re-evaluate any project-owned instruction changed by this guidance against the source release's routing contract. Do not silently preserve alpha.14 continuation semantics under an alpha.13 managed router when that would create conflicting active instructions.
