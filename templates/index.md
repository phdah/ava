# Ava Release Sources

This directory contains only authored release payload, installer, and project-scaffold source material.

Repository location does not determine installed ownership. Release assembly must map every installed source file to an explicit destination, ownership class, role, checksum, and operation.

- [Base and scaffold sources](base/)
- [Installer sources](installer/)

Public distribution contracts and schemas live under [`/distribution/`](../distribution/). Maintainer-only publication procedures live under [`/internal/release/`](../internal/release/). Neither is copied into a distributed project unless an explicit release manifest entry declares otherwise, and internal content must never be declared.
