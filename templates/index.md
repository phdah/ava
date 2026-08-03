# Ava Release Sources

This directory contains only authored managed release payload and project-scaffold source material.

Repository location does not determine installed ownership. Release assembly maps every distributed source file to an explicit destination, ownership class, role, checksum, and operation.

- [Managed base and format-reference sources](base/)
- [Project-owned create-if-absent scaffolds](project-scaffolds/)

Host-specific instruction files are supplied by adopting projects. They are not Ava release templates or payload sources.

Public distribution contracts and schemas live under [`/distribution/`](../distribution/). Maintainer-only publication and assembly procedures live under [`/internal/release/`](../internal/release/). Neither is copied into a distributed project unless an explicit release manifest entry declares public content, and internal content must never be declared.
