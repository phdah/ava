# Canonical Adjacent Release Catalogs

Each file is the complete immutable adjacent-edge history through its target version.

- [1.0.0-alpha.12](1.0.0-alpha.12.json) normalizes retained support from alpha.5 through alpha.11.

For a new release:

1. inherit the previous target catalog unchanged
2. add exactly one edge from the previous release to the proposed target
3. add only guidance and migrations introduced by that edge
4. update `../catalog-retirements.json`
5. validate the inherited-versus-proposed delta

Published direct source-to-target representations are compatibility inputs, not catalog-authoring templates.
