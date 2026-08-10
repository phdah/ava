---
type: Internal Development Task
title: Clarify release semantic-impact assessment
description: Make release completion distinguish managed behavior changes from project-owned semantic incompatibility before deciding semantic_review_required.
tags: [internal, roadmap, dogfood, releases, upgrades, semantic-compatibility, guidance]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 13
classification: blocker
blocks: next-prerelease
affected_version: general release process, exposed by 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T12:48:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T13:34:00+02:00
---

# Clarify Release Semantic-Impact Assessment

## Finding

While completing the `1.0.0-alpha.14` release PR, the first release-edge assessment set `semantic_review_required: false` because the implementation changed only Ava-managed routing contracts and did not directly require a deterministic project-file transformation.

That reasoning was incomplete. The managed delta changed normal-turn routing semantics from unconditional fresh routing to roleless clarification, same-role continuation, or fresh routing. Existing project-owned authoritative instructions can remain structurally valid and untouched while still encoding the previous global routing behavior. In that case, mechanically advancing semantic compatibility would be incorrect even though the updater has no deterministic project-owned edit to perform.

The release decision was corrected before publication, but the internal release instructions did not make the distinction explicit enough to prevent the same false-negative assessment in a future release.

## Required clarification

Release completion distinguishes three separate questions:

1. **Managed delta:** What Ava-managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed between the immediately previous release and the target?
2. **Project-owned compatibility:** Could any valid project-owned context from the previous release remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible under the target managed contracts?
3. **Required reconciliation:** If yes, what bounded project-owned concepts must the Upgrade Role inspect or change before semantic compatibility may advance?

A managed behavior change alone does not imply `semantic_review_required: true`. Conversely, the absence of a deterministic project-file migration does not imply `false`.

The decisive test is whether project-owned context may require semantic inspection or reconciliation because of the managed delta.

## False-positive and false-negative boundaries

The release procedure makes both failure modes explicit:

- **False positive:** marking semantic review required merely because the Ava-managed agent behavior changed, even though no supported project-owned context can conflict with or depend on that change.
- **False negative:** marking semantic review unnecessary because only managed files changed, even though project-owned roles, workflows, shared instructions, indexes, host entrypoints, metadata, links, or other active context may encode assumptions that become incompatible.

For a `false` decision, the maintainer explains why project-owned context cannot require reconciliation for the reviewed delta. For a `true` decision, guidance identifies bounded discovery conditions and completion criteria rather than requiring a blanket project scan.

## Alpha.14 evidence

The alpha.14 routing change exposed the gap:

- managed `/AGENTS.md` and instruction-resolution behavior changed substantially
- project-owned files do not need deterministic rewriting merely because the managed router changed
- however, project-owned authoritative instructions can duplicate the old exact-one-role, fresh-routing, required-reading reload, or implicit workflow-persistence assumptions
- those files can remain structurally valid while conflicting with the new managed contract
- therefore semantic compatibility must not advance mechanically until the bounded project-owned routing assumptions have been inspected

This is the kind of second-order compatibility question that release completion now forces the maintainer to answer before authoring the adjacent edge.

## Implemented scope

The implementation updates:

- `internal/release/procedure.md` with the authoritative project-owned semantic-impact assessment, `true` and `false` boundaries, author/reviewer ownership, bounded discovery, and deterministic validation boundary
- `internal/release/release-please.md` with the same release-PR authoring contract
- `internal/roles/ava-internal/instructions.md` so release completion explicitly loads and applies the semantic-impact assessment rather than inferring from managed change or deterministic migration presence
- `internal/release/fixtures/semantic-impact-assessment.json` with maintained `false` and `true` regression examples
- `internal/release/tests/test_semantic_impact_assessment.py` and `internal/release/test.sh` to keep both examples and the documentation boundary covered

The public semantic-compatibility model is unchanged. Deterministic release validation continues to enforce representation consistency, such as guidance being present only for semantic edges, without attempting to infer the semantic decision.

## Completion criteria

- [x] release instructions explicitly separate managed behavior change from project-owned semantic impact
- [x] `semantic_review_required` is defined by whether project-owned context may require semantic inspection or reconciliation, not by whether managed files changed
- [x] instructions explicitly reject the inference that no deterministic project-file migration means no semantic review
- [x] instructions explicitly reject automatically requiring semantic review for every managed behavioral change
- [x] release completion requires an explicit reviewed rationale for both `true` and `false` decisions
- [x] `true` decisions require bounded affected project-owned concepts, discovery conditions, and completion criteria in upgrade guidance
- [x] `false` decisions require enough evidence to justify mechanically advancing semantic compatibility when the previous semantic state is complete
- [x] release assessment considers project-owned active instruction relationships, including roles, workflows, shared instructions, indexes, and host entrypoints, without defaulting to blanket scans of unrelated project content
- [x] semantic judgment remains a maintainer responsibility; deterministic validation checks representation and consistency rather than guessing migration need
- [x] regression coverage represents at least one managed-only change that correctly yields `false` and one managed-contract change with possible project-owned dependency that correctly yields `true`
- [x] affected internal release documentation, indexes, fixtures, and tests are aligned

## Resolution evidence

The maintained fixture freezes both sides of the decision boundary. Its `false` case is a managed installer behavior fix with no supported project-owned semantic dependency. Its `true` case is the alpha.14-style routing-contract change where active project-owned instructions may encode previous routing assumptions. The regression test requires both outcomes, explicit rationales, bounded reconciliation guidance for `true`, and the documented rule that deterministic tooling does not make the semantic decision.

## Release gate

This finding no longer blocks the next prerelease. Release completion now requires the explicit reviewed semantic-impact assessment before an adjacent edge is accepted.
