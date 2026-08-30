---
id: ava-5614
title: "Repair Inbox Ingester project-root links"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5614
---

## Description

Fix Inbox Ingester references that incorrectly resolved the project-owned inbox beneath the managed role directory instead of the project root.

## Migrated task record

Historical metadata: phase 5 finding 14, `blocker`, blocking next prerelease, general managed Inbox Ingester behavior, completed after implementation.

### Finding and fix

During realistic recipe ingestion, required-context loading tried to read `/.ava/base/roles/inbox-ingester/inbox/index.md` and stopped. The managed role used Markdown links such as `./inbox/` and `./inbox/index.md`; although Ava prose treats `./...` as project-root-relative, normal Markdown resolution from the nested role made the host interpret them as role-relative.

The fix expresses the project-owned inbox and required convention as explicit project-root paths in prose. Required reading names `./inbox/index.md` directly and states that it must not be resolved relative to the managed role directory. Inbox ownership and ingestion semantics did not change.

### Completion and evidence

Completion required project-root resolution for inbox/convention, no managed role instruction treating inbox as a role child, assembled/installed regression coverage, failure on reintroduced nested-link shape, successful required reading in a conforming install, and aligned fixtures/tests.

The implementation replaced the broken Markdown links in `templates/base/roles/inbox-ingester/index.md`, retained document-relative links for managed role content, and extended `internal/release/tests/test_installed_paths.py` to inspect the assembled role mapping. It asserts project-root `./inbox/index.md`, rejects `](./inbox/`, confirms the project-owned `/inbox/index.md` scaffold destination, and confirms no managed nested inbox path is assembled. Existing installed-path tests run in `internal/release/test.sh`.

Published installed-project confirmation remained a release qualification gate. The historical note that Finding 15 was then the next blocker is preserved as context only; current work comes from Backlog state.