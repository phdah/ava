# Ava Internal Release Procedures

This directory contains maintainer-only release assembly, publication, qualification, validation, fixtures, and tests. It is never distributed to Ava projects.

- [Release assembler entry point](assemble.sh)
- [One-command qualification candidate assembler](assemble-candidate.sh)
- [Release assembler implementation](assemble.py)
- [Reviewed recursive-edge assembler](assemble_reviewed.py)
- [Immutable release edge records](catalogs/)
- [Adjacent edge model](adjacent_edges.py)
- [Release-record and recursive composition policy](release_catalog.py)
- [Release-local edge composer](compose_adjacent_catalog.py)
- [Recursive edge-chain validator](validate_adjacent_catalog.py)
- [Installer and updater shell template](ava-install.sh)
- [Embedded installer Python fragments](installer/)
- [Release automation and Conventional Commit contract](release-please.md)
- [Release pull-request policy validator](validate_release_pr.py)
- [Pull-request title validator](validate_pr_title.py)
- [Alpha qualification policy](alpha-qualification.md)
- [Deterministic release qualification procedure](qualification-automation.md)
- [Session-neutral deterministic qualification execution](qualification-execution.md)
- [Release qualification execution entry point](qualify-release.sh)
- [Canonical session-neutral qualification driver](qualification.py)
- [Host-neutral qualification setup runner](run-release-qualification.sh)
- [Deterministic qualification implementation compatibility module](qualification_work.py)
- [Explicit qualification acceptance entry point](accept-release-qualification.sh)
- [Shared qualification automation helpers](qualification_automation.py)
- [Shared qualification scenario engine](qualification_runner.py)
- [Historical phase contract and matrix runner](qualification_phase_runner.py)
- [Historical phase orchestration compatibility module](qualification_phase_automation.py)
- [Historical two-phase gate](qualification_phase_gate.py)
- [Qualification acceptance and release-PR state implementation](qualification_acceptance.py)
- [Qualification configuration and compact evidence state](qualification/)
- [Deterministic inbox qualification checks](qualification_inbox.py)
- [Conformance validation contract](conformance.md)
- [Unified conformance validator](conformance.py)
- [Interaction evidence validator](interaction_evidence.py)
- [Release publication procedure](procedure.md)
- [Release guidance sources](guidance/)
- [Repository boundary validator](validate-boundaries.sh)
- [Installer and conformance test runner](test.sh)
- [Validation fixtures](fixtures/)
- [Release implementation tests](tests/)
- [Release implementation log](log.md)

`qualify-release.sh` is the qualification execution entry point. It routes through the session-neutral deterministic driver and does not select a ChatGPT mode or agent runtime.

The canonical release flow is orchestrated from whichever repository-capable maintainer session is active. GitHub Actions executes the mandatory deterministic pre-edge/final checks, so normal ChatGPT chat does not need Work or shell access.

The normal flow has an ephemeral `pre-edge` fail-fast stage and one authoritative `final` deterministic run. Optional agent-behavior scenarios remain in the synthetic fixture for targeted QA and future host-protocol work, but they are not publication gates.

`qualification_work.py` is retained as the current deterministic implementation module while `qualification.py` provides the canonical host-neutral interface. Its historical name does not imply a Work requirement.

`qualification_phase_runner.py`, `qualification_phase_automation.py`, `qualification_phase_gate.py`, and historical qualification evidence remain available to interpret earlier runs. They are not the canonical execution or acceptance path for new releases.

`validate_upgrade_impact.py` and historical target-specific guidance remain available only for compatibility investigation of already published releases. They are not active release-authoring inputs.
