# Host Bootstrap Sources

This directory contains optional thin host-specific instruction files that may be selected explicitly during release assembly.

A bootstrap source:

- only directs the host to load and follow the project-root `/AGENTS.md`
- contains no routing, role, workflow, ownership, or upgrade semantics of its own
- is included only through an explicit `SOURCE=DESTINATION` release-assembly mapping
- becomes Ava-managed and is recorded in the installed manifest when selected at installation
- must not be presented as native host support until maintained conformance evidence exists

No host bootstrap implementation is registered yet.
