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
- [Hands-off release qualification procedure](qualification-automation.md)
- [ChatGPT Work Cloud qualification execution](qualification-work.md)
- [Release qualification protocol entry point](qualify-release.sh)
- [ChatGPT Work qualification protocol driver](qualification_work.py)
- [Explicit qualification acceptance entry point](accept-release-qualification.sh)
- [Shared qualification automation compatibility helpers](qualification_automation.py)
- [Shared qualification scenario engine](qualification_runner.py)
- [Phase contract and matrix classification](qualification_phase_runner.py)
- [Historical phase orchestration compatibility module](qualification_phase_automation.py)
- [Two-phase acceptance and release-PR gate](qualification_phase_gate.py)
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

`qualify-release.sh` is the qualification execution entry point. It is a deterministic protocol for ChatGPT Work Cloud: deterministic checks run in the Work cloud shell, semantic interactions are delegated to fresh Work subagents, and a separate fresh Work subagent performs the independent audit. The supported release path has no local agent runtime and no OpenCode dependency.

`qualification_phase_automation.py` and historical qualification evidence remain available to validate and interpret previously recorded runs. They are not the canonical execution path for new release qualification.

`validate_upgrade_impact.py` and historical target-specific guidance remain available only for compatibility investigation of already published releases. They are not active release-authoring inputs.
