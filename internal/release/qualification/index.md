# Release Qualification State

This directory is the repository-owned control and compact-evidence scope for mandatory release qualification. It is internal maintainer state and is never distributed to Ava projects.

- [Qualification configuration](config.json) - Active release pair plus fixed qualification and audit models.
- [Release-pair catalog](pair-catalog.json) - Reviewed exact published or local selectors used to execute qualification.
- [Current state](current-state.json) - Pair execution state plus the durable per-release acceptance ledger.
- [Independent audit prompt](audit-prompt.md) - Prompt/contract used by the fresh independent audit session.
- [Schemas](schemas/) - Validation contracts for control state and compact evidence.
- [Run evidence](runs/) - Compact run records, session inventories, audit reports, and issue inventories.

Historical releases are distinguished with `basis: historical-backfill`. New releases may satisfy the merge gate only with `basis: qualified-run` and explicit user signoff.

Raw release assets, generated qualification vaults, isolated projects, command logs, and full transcripts remain repository-external. Qualification and acceptance update compact state here but never create Git commits automatically.
