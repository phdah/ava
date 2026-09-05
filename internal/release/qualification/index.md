# Release qualification state

This directory contains current qualification configuration/state and evidence for the supported stable release lineage.

## Current operational state

- [Qualification configuration](config.json) selects the active qualification operation.
- [Qualification catalog](pair-catalog.json) binds the exact target and, after the root release, the exact previous published source.
- [Current state](current-state.json) records final qualification state and the supported release acceptance ledger.
- [Schemas](schemas/) validate current configuration, state, catalog, and final run records.

The initial `bootstrap-to-1.0.0` operation is target-only because stable `1.0.0` has no supported predecessor. After `1.0.0` is published, normal qualification operations bind adjacent stable releases beginning with `1.0.0 -> 1.0.1`.

## Evidence

Final qualification writes exact run records under `runs/` when a release candidate reaches the user-signoff gate. Those records are immutable evidence for supported stable releases and are not alternate release instructions.
