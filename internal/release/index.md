# Ava internal release

[Release procedure](procedure.md) is the authoritative operator flow. Stable `1.0.0` is the root of the maintained release lineage. There is no supported release before it and no upgrade edge into it. Adjacent immutable upgrade history begins with `1.0.0 -> 1.0.1`.

## Release identity and policy

- [release-please policy](release-please.md)
- [release PR validator](validate_release_pr.py)
- [PR title validator](validate_pr_title.py)
- [release-please workflow](../../.github/workflows/release-please.yml)
- [release qualification workflow](../../.github/workflows/release-qualification.yml)
- [Python release test workflow](../../.github/workflows/python-tests.yml)

## Assembly and compatibility

- [release assembler](assemble.sh)
- [release assembler implementation](assemble.py)
- [reviewed catalog assembler](assemble_reviewed.py)
- [qualification candidate assembler](assemble-candidate.sh)
- [adjacent edge model](adjacent_edges.py)
- [release catalog model](release_catalog.py)
- [adjacent catalog composer](compose_adjacent_catalog.py)
- [adjacent catalog validator](validate_adjacent_catalog.py)
- [immutable release catalogs](catalogs/)
- [release guidance](guidance/)

`1.0.0` has no release-local catalog record. Every later supported release adds exactly one record for the immediately previous stable release.

## Qualification

- [qualification contract](qualification-automation.md)
- [qualification execution](qualification-execution.md)
- [qualification CLI](qualification.py)
- [deterministic qualification engine](qualification_engine.py)
- [qualification state helpers](qualification_state.py)
- [GitHub Actions qualification driver](qualification_ci.py)
- [qualification setup runner](run-release-qualification.sh)
- [qualification shell entry point](qualify-release.sh)
- [qualification scenario engine](qualification_runner.py)
- [qualification acceptance](qualification_acceptance.py)
- [qualification acceptance shell entry point](accept-release-qualification.sh)
- [qualification state and evidence](qualification/)
- [synthetic qualification fixture](fixtures/synthetic-qualification-vault/)

The first-release qualification for `1.0.0` is target-only because no source release exists. It proves the candidate can be installed and validated as a root release. Starting with `1.0.1`, qualification binds the exact previous published release and exercises the complete adjacent upgrade lifecycle.

## Publication and recovery

- [publication state planner](publication.py)
- [publication recovery procedure](publication-recovery.md)
- [release workflow](../../.github/workflows/release-please.yml)

Publication is always derived from the exact tagged source revision and durable GitHub Release state. Recovery never moves or recreates an existing correct release tag.

## Validation

- [conformance contract](conformance.md)
- [conformance validator](conformance.py)
- [repository boundary validator](validate-boundaries.sh)
- [maintained release suite](test.sh)
- [release tests](tests/)

Checked-in release state describes only the supported stable lineage. Historical development details remain in task records and Git history, not in the operational release ledger.
