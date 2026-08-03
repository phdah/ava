# OpenCode release validation

OpenCode is the first named host in Ava's supported host matrix. The public behavior contract is [OpenCode host support](../../distribution/opencode.md).

## Release policy

A release does not contain or generate `opencode.json`, `opencode.jsonc`, or `.opencode/` content. OpenCode uses the installed root `AGENTS.md` natively, and required managed files remain direct project-local reads under `./.ava/`.

The installer must preserve existing project OpenCode configuration and every global configuration path because those files are outside the Ava-managed release set.

## Maintained checks

Run the complete release suite:

```sh
sh internal/release/test.sh
```

The OpenCode fixture verifies fresh installation, project and global configuration preservation, upgrades, managed-path resolution, and host-neutral router portability.

A CI job additionally installs the pinned supported OpenCode version and runs:

```sh
AVA_OPENCODE_LIVE=1 python -m unittest -v internal.release.tests.test_opencode
```

The live check starts `opencode debug config` from an installed fixture with isolated user data. It must succeed without creating project configuration or requesting access to an external directory.

## Version policy

The pinned CI version is evidence for the currently validated host contract, not a permanent support ceiling. Updating the pin requires the same fixture to pass. A later OpenCode release that changes `AGENTS.md` discovery, workspace boundaries, permission defaults, or configuration precedence requires an explicit compatibility review.
