---
type: Internal Release Procedure
title: Ava Conformance Validation
description: Defines the stable machine-readable finding contract and validation modes used to qualify repository sources, installed projects, and release assets.
tags: [internal, release, validation, conformance, fixtures]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T22:30:00+02:00
updated:
  by: agent:openai-opencode
  at: 2026-08-20T15:36:31Z
---

# Purpose

`conformance.py` is the internal validator used by release tests and qualification. It does not add a user-facing Ava command surface. Ava Maintenance interprets installed-state findings and invokes existing deterministic installer operations when recovery is authorized.

# Validation modes

- `repository` validates public contracts, release sources, metadata, source and installed-destination inline links, indexes, role and workflow discovery, routing references, deprecated paths, and internal-content leakage.
- `installed` validates the managed router, manifest, journal, managed payload integrity, semantic compatibility, routing gates, host metadata, and OpenCode access.
- `release` validates the exact release asset inventory, checksums, release identity, channel consistency, and optional immutable-publication evidence.
- `auto` selects a mode from the target root without mutating it.

# Finding contract

Every finding has these stable fields:

```json
{
  "rule_id": "AVA-MANAGED-CHECKSUM",
  "severity": "error",
  "path": "AGENTS.md",
  "message": "managed payload checksum does not match the manifest",
  "fix_available": false,
  "decision_required": true,
  "category": "deterministic",
  "related": {"role": "Ava Maintenance"}
}
```

`rule_id` is stable and begins with `AVA-`. `severity` is one of:

- `error`: the claimed structure, integrity, routing, release, or compatibility state is invalid and qualification fails.
- `warning`: the installation or project remains inspectable, but an unsafe, incomplete, or degraded state requires attention.
- `recommendation`: optional context or publication evidence is absent without invalidating the current validation mode.

`fix_available` is true only when an unambiguous deterministic correction exists. `decision_required` is true when a user or semantic role must decide how to proceed. The validator never applies fixes.

# Routing gate

Installed validation reports `normal_routing_permitted` separately from overall finding validity. Normal routing is permitted only when:

- the journal is in a safe terminal state with `allowed_operations: [normal]`
- semantic compatibility is complete for the installed `ava_version`
- `/.ava/state/transactions/` is absent
- no blocking deterministic, semantic, or routing finding exists

`normal_routing_permitted` means the managed-state gate allows ordinary conversation-aware routing. It does not mean every turn must traverse workflow and role registries.

Host-access findings do not silently mutate project-owned configuration. Ava Maintenance reports the required OpenCode merge or host correction.

Root-router regression coverage separately freezes unconditional router entry and the managed-state gate on every turn, then the normal-operation continuity decision between roleless conversational handling, same-role continuation, and fresh routing. It verifies that roleless clarification performs no project action, same-role continuation retains an already-loaded role without registry traversal or required-reading reload, explicit workflows and routing transitions force fresh resolution, a roleless turn clears stale role continuity, and the original warranty request still cannot be answered or refused by a generic host persona before Ava decides routing. The coverage validates both the repository source and assembled installed `/AGENTS.md` bytes against the maintained OpenCode access model.

# Semantic review sufficiency

Change Reviewer regression coverage freezes the default bounded `acceptance` standard, explicit `audit` standard, evidence-consequence-confidence-threshold finding admission test, optional-observation boundary, and terminal conclusions.

Re-review coverage requires prior findings and remediation to be evaluated first. It permits a new or reopened finding only from changed evidence, changed scope, changed authority, or a genuine regression that independently passes the admission test. The maintained fixture covers a clean first review, satisfied remediation and re-review, a remediation regression, and an explicitly exhaustive audit.

These semantic fixtures validate the managed review contract. They do not turn deterministic conformance into semantic approval or replace installed-release dogfood qualification.

# Publication evidence

Before publication, missing `publication.json` is a recommendation. Release qualification uses `--require-publication-evidence`, which requires evidence that immutable releases are enabled, the release is immutable, and attestation verification succeeded.

# Alpha qualification

The [alpha qualification policy](alpha-qualification.md) composes repository, installed, and release conformance with roadmap completion, reproducible assembly, prerelease support declarations, defect classification, and exact publication approval.

[alpha-qualification.json](fixtures/alpha-qualification.json) freezes the required gates and their conformance evidence. [test_alpha_qualification.py](tests/test_alpha_qualification.py) proves that:

- every evidence reference resolves
- Phase 1 through Phase 4 tasks are complete
- the first alpha assembles reproducibly
- `1.0.0-alpha.1` declares no supported source release
- later intended prerelease transitions are represented as release-manifest upgrade edges
- historical unversioned sources are rejected
- publication approval is bound to both version and source revision

Passing individual conformance modes is necessary but not sufficient for alpha publication. Every alpha gate must pass and the exact publication transaction must be approved.

# Fixture matrix

`fixtures/conformance-matrix.json` freezes required structural, installation, recovery, removal, host, semantic, upgrade, trust, and publication scenarios. Every matrix case names executable evidence in the test suite. New supported behavior must add or update a case before publication.

Release-source link validation uses the assembler's complete source-to-installed payload mapping. It accepts local inline links only when their target is present in the assembled managed payload or create-if-absent project scaffold, so repository-only source paths cannot mask a broken installed role or context chain. Project-root and document-relative links that escape the selected project are rejected.
