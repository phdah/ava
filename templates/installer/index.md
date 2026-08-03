# Ava Installer Sources

This directory contains authored sources for the release `ava-install.sh` entry point and its manifest-driven engine.

- [POSIX bootstrap](ava-install.sh) - Downloads or accepts verified release assets, validates SHA-256 records, and starts the packaged engine.
- [Installer engine fragments](engine/) - Concatenated bytewise by release assembly and embedded as `installer/engine.py` in `ava-base.tar.gz`.

The engine is release support code, not installed project content. Only destinations declared by `ava-release.json` are applied to the target project.
