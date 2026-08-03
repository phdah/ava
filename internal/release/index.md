# Ava Internal Release Procedures

This directory contains maintainer-only release assembly, installation implementation, publication coordination, validation, fixtures, and tests. It is never distributed to Ava projects.

- [Release assembler entry point](assemble.sh)
- [Release assembler implementation](assemble.py)
- [Installer and updater shell template](ava-install.sh)
- [Embedded installer Python fragments](installer/)
- [Installer implementation guide](installer.md)
- [Release publication procedure](procedure.md)
- [Repository boundary validator](validate-boundaries.sh)
- [Installer test runner](test.sh)
- [Validation fixtures](fixtures/) - Machine-readable contract cases used by release and conformance tests.
- [Release implementation tests](tests/)
- [Release implementation log](log.md)
