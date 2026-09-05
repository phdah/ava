---
id: ava-5611
title: "Normalize and enforce adjacent-edge release authoring"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5611
---

## Description

Store one immutable previous-to-target edge per release and recursively compose the records required for an upgrade.

## Migrated task record

Historical metadata: phase 5 finding 11, `blocker`, blocking next prerelease, general release process exposed by `1.0.0-alpha.12`, completed after implementation.

### Resolution and contract

The repository normalized upgrade history into a continuous immutable linked ledger with exactly one release file and one adjacent edge per published release, from the `0.0.0 -> 1.0.0-alpha.1` bootstrap sentinel through each successive alpha. Alpha.1 retires the non-installable bootstrap sentinel; alpha.9-to-alpha.10 owns the knowledge-hierarchy/inbox-fidelity guidance. No target file repeats historical edges or guidance.

Active `internal/release/upgrade-impact.json` authoring was removed. Historical target-specific guidance became read-only evidence, and assembly stages only artifacts referenced by owning edge records.

Every prerelease/stable release must leave historical records unchanged, create only `internal/release/catalogs/<target>.json`, author exactly one `previous_release -> target` edge, assess only that managed delta, add only transition-local migrations/guidance/retirement, and resolve older sources recursively. There is no first-release exception: missing bootstrap or intermediate records invalidate the ledger.

The release-PR validator rejects missing target/predecessor, skipped/wrong predecessor, cumulative guidance, invalid retirement, guidance digest changes, historical catalog changes, and legacy impact authoring. The assembler composes selected records in memory and mechanically derives installer-compatible source-to-target projections as generated output.

### Regression and completion evidence

Tests cover the complete alpha ledger, exactly-one-edge invariant, mandatory bootstrap edge, recursive composition, missing/skipped/wrong records, transition-local guidance, artifact digest mutation, source retirement, explicit no-impact edges, retained historical sources, semantic lag with exact-once guidance, and prerelease/stable SemVer. Both release-PR policy and `internal/release/test.sh` run strict chain tests.

Completion established normalized immutable per-release records, explicit reconstructed early-alpha records, no cumulative snapshots, immutable published assets, one-new-target authoring, recursive validation, rejection of invalid/cyclic/non-adjacent chains, immutable historical edge/guidance/artifact/migration identity, unique retained-source composition, release-local source retirement, explicit false semantic decisions on no-impact edges, alpha.12 regression coverage, exact-once semantic lag, channel neutrality, and aligned docs/tooling/fixtures/history.

Release follow-up required the next exact tagged release to prove all older records unchanged, only the target record added, full bootstrap-to-target resolution, and exact-once outstanding semantic guidance.