# Ava Internal Release Procedures

This directory contains maintainer-only release assembly, publication, qualification, validation, fixtures, and tests. It is never distributed to Ava projects.

- [Release assembler entry point](assemble.sh)
- [Release assembler implementation](assemble.py)
- [Reviewed adjacent-catalog assembler](assemble_reviewed.py)
- [Canonical release catalogs](catalogs/)
- [Adjacent edge model](adjacent_edges.py)
- [Strict release catalog policy](release_catalog.py)
- [Adjacent catalog composer](compose_adjacent_catalog.py)
- [Adjacent catalog validator](validate_adjacent_catalog.py)
- [Installer and updater shell template](ava-install.sh)
- [Embedded installer Python fragments](installer/)
- [Release automation and Conventional Commit contract](release-please.md)
- [Release pull-request policy validator](validate_release_pr.py)
- [Pull-request title validator](validate_pr_title.py)
- [Alpha qualification policy](alpha-qualification.md)
- [Conformance validation contract](conformance.md)
- [Unified conformance validator](conformance.py)
- [Release publication procedure](procedure.md)
- [Release guidance sources](guidance/)
- [Repository boundary validator](validate-boundaries.sh)
- [Installer and conformance test runner](test.sh)
- [Validation fixtures](fixtures/)
- [Release implementation tests](tests/)
- [Release implementation log](log.md)

`validate_upgrade_impact.py` and historical target-specific guidance remain available only for compatibility investigation of already published releases. They are not active release-authoring inputs.
