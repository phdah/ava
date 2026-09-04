# Release qualification state

This directory contains current qualification configuration/state plus immutable evidence from completed runs.

## Current operational state

- [Qualification configuration](config.json) - Selects the active adjacent release pair.
- [Release-pair catalog](pair-catalog.json) - Exact published/local selectors and expected release digests.
- [Current state](current-state.json) - Final qualification state and per-release acceptance ledger.
- [Schemas](schemas/) - Validation schemas for current configuration, state, pair catalog, and final run records.

## Historical evidence

- [Run records](runs/) - Committed qualification evidence from completed release candidates.

Run records are immutable historical evidence. Their field names and recorded executor provenance reflect the format used when each run was produced and are not operational instructions for new qualification runs.
