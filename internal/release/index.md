# Ava Internal Release Procedures

This directory contains maintainer-only release assembly, installation implementation, publication coordination, qualification, validation, fixtures, and tests. It is never distributed to Ava projects.

- [Release assembler entry point](assemble.sh)
- [Release assembler implementation](assemble.py)
- [Installer and updater shell template](ava-install.sh)
- [Embedded installer Python fragments](installer/)
- [Installer implementation guide](installer.md)
- [Adjacent edge catalog model](adjacent_edges.py) - Validates immutable edge identity, unique paths, supported-source retention, separate managed and semantic resolution, and guidance supersession for the proposed catalog contract.
- [Adjacent catalog composer](compose_adjacent_catalog.py) - Appends one reviewed edge and optional guidance to an inherited immutable catalog.
- [Adjacent catalog validator](validate_adjacent_catalog.py) - Proves graph safety, inherited identity, explicit retirement, and representative managed and semantic path resolution.
- [Release automation and Conventional Commit contract](release-please.md)
- [Release pull-request policy validator](validate_release_pr.py)
- [Pull-request title validator](validate_pr_title.py)
- [Alpha qualification policy](alpha-qualification.md)
- [Conformance validation contract](conformance.md)
- [Unified conformance validator](conformance.py)
- [Release publication procedure](procedure.md)
- [Release guidance sources](guidance/) - Version-scoped reviewed semantic-upgrade guidance included in release assets when an edge requires project-owned reconciliation.
- [Repository boundary validator](validate-boundaries.sh)
- [Installer and conformance test runner](test.sh)
- [Validation fixtures](fixtures/) - Machine-readable contract, qualification, release-automation, and conformance cases used by release qualification.
- [Release implementation tests](tests/)
- [Release implementation log](log.md)
