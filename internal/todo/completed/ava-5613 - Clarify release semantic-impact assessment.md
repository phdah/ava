---
id: ava-5613
title: "Clarify release semantic-impact assessment"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5613
---

## Description

Make release completion distinguish managed behavior changes from project-owned semantic incompatibility before deciding `semantic_review_required`.

## Migrated task record

Historical metadata: phase 5 finding 13, `blocker`, originally blocking next prerelease, general release process exposed by `1.0.0-alpha.14`, completed after implementation.

### Finding and required clarification

During alpha.14 release-PR completion, the first edge assessment set semantic review false because the implementation changed only managed routing and required no deterministic project-file transformation. That was incomplete: structurally unchanged project-owned instructions could still encode the previous routing assumptions and become semantically incompatible.

Release completion now separates: (1) the immediately previous-to-target managed delta; (2) whether valid project-owned context can remain structurally unchanged yet become conflicting/misleading/invalid/incompatible; and (3) what bounded project-owned concepts require Upgrade Role inspection/reconciliation if so. Managed behavior change alone does not imply true, and absence of deterministic project-file migration does not imply false. The decisive test is possible project-owned semantic dependency.

Both false-positive and false-negative boundaries are explicit. A false result requires rationale showing supported project-owned context cannot require reconciliation. A true result requires bounded discovery and completion criteria rather than a blanket scan. Alpha.14 demonstrated the true case because project-owned roles/workflows/shared instructions could duplicate old exactly-one-role/fresh-routing/reload/workflow-persistence assumptions.

### Implementation and evidence

`internal/release/procedure.md` and `release-please.md` define the authoritative semantic-impact assessment, decision boundaries, reviewer ownership, bounded discovery, and deterministic-validation boundary. Ava Internal Maintainer release instructions require applying that assessment rather than inferring from managed changes or migration presence. `internal/release/fixtures/semantic-impact-assessment.json`, `test_semantic_impact_assessment.py`, and the release test runner cover maintained true/false examples.

The public compatibility model did not change. Deterministic tooling validates representation consistency, such as guidance presence for semantic edges, but does not infer the semantic decision.

Completion required explicit separation of managed change/project semantic impact, rejected bad inferences in both directions, reviewed rationale for true and false, bounded guidance for true, sufficient evidence for false, consideration of active project-owned instruction relationships without unrelated scans, semantic judgment owned by the maintainer, and regression examples for both outcomes. The maintained false case is a managed installer fix with no project-owned semantic dependency; the true case is the alpha.14 routing-contract shape. This finding therefore no longer blocks the next prerelease.