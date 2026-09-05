# Ava Release Implementation Log

This log records major conceptual and structural changes to the maintained stable release implementation. Detailed pre-stable development history remains available in task records and Git history rather than in the operational release surface.

## 2026-09-05

- **Stable root release**: Established `1.0.0` as the first supported release and the root of the permanent upgrade ledger. The root release has no previous supported release, no upgrade edge, and no source-to-target semantic transition.
- **Target-only first-release qualification**: The mandatory deterministic qualification gate can qualify the root release without fabricating a source release. It verifies applicable installation, mature-project preservation, managed-damage, conformance, reproducibility, attestation, publication, and immutable-release guarantees.
- **Stable adjacent history**: Permanent release-to-release history begins with `1.0.0 -> 1.0.1`. Later releases use exact previous-release assets, reviewed adjacent edges, deterministic lifecycle qualification, explicit user acceptance, merge-commit publication, and durable recovery.
- **Release PR merge safety**: Ordinary implementation PRs may be squash merged. Release Please PRs must use merge commits so the accepted qualified revision remains in publication ancestry.
- **Durable recoverable publication**: Publication resolves exact tag, revision, accepted qualification, release metadata, and asset digests from durable state. Compatible partial drafts can be resumed without moving tags or clobbering assets, and exact immutable published state is treated as success.
