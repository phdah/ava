# Ava internal release

[Release procedure](procedure.md) is the authoritative operator flow. The files below are the maintained implementation and support surface for that procedure.

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

`qualification.py` is the stable CLI facade. `qualification_engine.py` owns deterministic execution. `qualification_state.py` owns only current configuration, schema, digest, and repository-state helpers. `run-release-qualification.sh` prepares immutable source assets and repository-external fixture state before invoking the CLI; `qualification_ci.py` owns GitHub Actions orchestration and artifact handoff. These responsibilities are intentionally separate.

## Publication and recovery

- [publication state planner](publication.py)
- [publication recovery procedure](publication-recovery.md)
- [release workflow](../../.github/workflows/release-please.yml)

## Validation

- [conformance contract](conformance.md)
- [conformance validator](conformance.py)
- [repository boundary validator](validate-boundaries.sh)
- [maintained release suite](test.sh)
- [release tests](tests/)

## Historical records

- [final alpha stable-bootstrap evidence](history/final-alpha-1.0.0-alpha.19.json)

`log.md`, committed records under `qualification/runs/`, the final-alpha stable-bootstrap evidence, the repository changelog, completed roadmap task evidence, and published GitHub Release metadata are historical records. They may contain terminology from the process that produced them. They are evidence only and are not release instructions or executable alternatives.
