# Ava Internal Release Procedures

This directory contains maintainer-only release assembly, installation implementation, publication coordination, qualification, validation, fixtures, and tests. It is never distributed to Ava projects.

- [Release assembler entry point](assemble.sh)
- [Release assembler implementation](assemble.py)
- [Installer and updater shell template](ava-install.sh)
- [Embedded installer Python fragments](installer/)
- [Installer implementation guide](installer.md)
- [Release automation and Conventional Commit contract](release-please.md)
- [Pull-request title validator](validate_pr_title.py)
- [Alpha qualification policy](alpha-qualification.md)
- [Conformance validation contract](conformance.md)
- [Unified conformance validator](conformance.py)
- [Release publication procedure](procedure.md)
- [Repository boundary validator](validate-boundaries.sh)
- [Installer and conformance test runner](test.sh)
- [Validation fixtures](fixtures/) - Machine-readable contract, qualification, release-automation, and conformance cases used by release qualification.
- [Release implementation tests](tests/)
- [Release implementation log](log.md)
