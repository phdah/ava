---
type: Internal Development Task
title: Clarify release semantic-impact assessment
description: Make release completion distinguish managed behavior changes from project-owned semantic incompatibility before deciding semantic_review_required.
tags: [internal, roadmap, dogfood, releases, upgrades, semantic-compatibility, guidance]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 13
classification: blocker
blocks: next-prerelease
affected_version: general release process, exposed by 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T12:48:00+02:00
---

# Clarify Release Semantic-Impact Assessment

## Finding

While completing the `1.0.0-alpha.14` release PR, the first release-edge assessment set `semantic_review_required: false` because the implementation changed only Ava-managed routing contracts and did not directly require a deterministic project-file transformation.

That reasoning was incomplete. The managed delta changed normal-turn routing semantics from unconditional fresh routing to roleless clarification, same-role continuation, or fresh routing. Existing project-owned authoritative instructions can remain structurally valid and untouched while still encoding the previous global routing behavior. In that case, mechanically advancing semantic compatibility would be incorrect even though the updater has no deterministic project-owned edit to perform.

The release decision was corrected before publication, but the internal release instructions do not currently make the distinction explicit enough to prevent the same false-negative assessment in a future release.

## Required clarification

Release completion must distinguish three separate questions:

1. **Managed delta:** What Ava-managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed between the immediately previous release and the target?
2. **Project-owned compatibility:** Could any valid project-owned context from the previous release remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible under the target managed contracts?
3. **Required reconciliation:** If yes, what bounded project-owned concepts must the Upgrade Role inspect or change before semantic compatibility may advance?

A managed behavior change alone must not imply `semantic_review_required: true`. Conversely, the absence of a deterministic project-file migration must not imply `false`.

The decisive test should be whether project-owned context may require semantic inspection or reconciliation because of the managed delta.

## False-positive and false-negative boundaries

The release procedure should make both failure modes explicit:

- **False positive:** marking semantic review required merely because the Ava-managed agent behavior changed, even though no supported project-owned context can conflict with or depend on that change.
- **False negative:** marking semantic review unnecessary because only managed files changed, even though project-owned roles, workflows, shared instructions, indexes, host entrypoints, metadata, links, or other active context may encode assumptions that become incompatible.

For a `false` decision, the maintainer should be able to explain why project-owned context cannot require reconciliation for the reviewed delta. For a `true` decision, guidance must identify bounded discovery conditions and completion criteria rather than requiring a blanket project scan.

## Alpha.14 evidence

The alpha.14 routing change exposed the gap:

- managed `/AGENTS.md` and instruction-resolution behavior changed substantially
- project-owned files do not need deterministic rewriting merely because the managed router changed
- however, project-owned authoritative instructions can duplicate the old exact-one-role, fresh-routing, required-reading reload, or implicit workflow-persistence assumptions
- those files can remain structurally valid while conflicting with the new managed contract
- therefore semantic compatibility must not advance mechanically until the bounded project-owned routing assumptions have been inspected

This is the kind of second-order compatibility question that release completion must force the maintainer to answer before authoring the adjacent edge.

## Expected implementation scope

The implementation task should update the internal release-authoring instructions and supporting validation or fixtures where useful so that every release PR completion explicitly performs this semantic-impact reasoning.

At minimum, consider:

- `internal/release/procedure.md`
- `internal/release/release-please.md`
- Ava Internal Maintainer release instructions where the release-PR workflow is described
- release-policy tests or fixtures that can enforce the presence and consistency of the decision without pretending deterministic validation can replace semantic judgment

Do not change the public semantic-compatibility model merely to solve an internal release-authoring clarity problem unless a separate architectural need is demonstrated.

## Completion criteria

- [ ] release instructions explicitly separate managed behavior change from project-owned semantic impact
- [ ] `semantic_review_required` is defined by whether project-owned context may require semantic inspection or reconciliation, not by whether managed files changed
- [ ] instructions explicitly reject the inference that no deterministic project-file migration means no semantic review
- [ ] instructions explicitly reject automatically requiring semantic review for every managed behavioral change
- [ ] release completion requires an explicit reviewed rationale for both `true` and `false` decisions
- [ ] `true` decisions require bounded affected project-owned concepts, discovery conditions, and completion criteria in upgrade guidance
- [ ] `false` decisions require enough evidence to justify mechanically advancing semantic compatibility when the previous semantic state is complete
- [ ] release assessment considers project-owned active instruction relationships, including roles, workflows, shared instructions, indexes, and host entrypoints, without defaulting to blanket scans of unrelated project content
- [ ] semantic judgment remains a maintainer responsibility; deterministic validation checks representation and consistency rather than guessing migration need
- [ ] regression coverage represents at least one managed-only change that correctly yields `false` and one managed-contract change with possible project-owned dependency that correctly yields `true`
- [ ] affected internal release documentation, indexes, fixtures, and tests are aligned

## Release gate

This finding blocks the next prerelease after `1.0.0-alpha.14`. Alpha.14 itself may proceed with the corrected reviewed semantic decision and guidance. The process clarification must be implemented before another release PR is completed so the next adjacent edge cannot repeat the same reasoning failure.
