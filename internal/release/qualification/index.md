# Release Qualification State

This directory is the repository-owned control and compact-evidence scope for hands-off release qualification. It is internal maintainer state and is never distributed to Ava projects.

- [Qualification configuration](config.json) - Active release pair plus fixed qualification and audit models.
- [Release-pair catalog](pair-catalog.json) - Reviewed exact published or local release selectors and historical pair ledger.
- [Current pair state](current-state.json) - Latest automated state and later explicit user signoff per pair.
- [Independent audit prompt](audit-prompt.md) - Read-only semantic audit contract applied in a fresh OpenCode session.
- [Schemas](schemas/) - Validation contracts for checked-in control state and generated compact evidence.
- [Run evidence](runs/) - Generated compact run records, session inventories, audit reports, and issue inventories.

Raw release assets, generated qualification vaults, isolated projects, command logs, and full transcripts remain repository-external. The hands-off operation writes compact evidence here but never commits it.
