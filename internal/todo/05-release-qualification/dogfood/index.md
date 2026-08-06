# Alpha Dogfood Findings

This index is the mutable backlog for findings discovered while exercising published Ava prereleases. The parent task remains [Dogfood the Alpha and Track Findings](../04-dogfood-alpha-and-track-findings.md).

## Control rule

Dogfooding remains active until the user explicitly declares it complete. An empty findings list, a passing test suite, or publication of another prerelease does not automatically complete the parent task or advance the roadmap to the release candidate.

## Current next finding

[Make knowledge hierarchy promotion predictable](03-make-knowledge-hierarchy-promotion-predictable.md).

Findings 05 and 06 are completed by merged PR #60 and PR #62. Their corrective immutable-release checks remain explicit release qualification follow-up, not pending implementation work.

## Backlog status

- 2 pending findings
- 0 pending blockers
- 2 pending required-v1 findings
- 4 completed findings

## Findings

| ID | Status | Classification | Blocks | Finding |
|---|---|---|---|---|
| 01 | completed | blocker | next prerelease | [Restore supported prerelease upgrade paths](01-restore-prerelease-upgrade-paths.md) |
| 02 | completed | blocker | next prerelease | [Repair installed context link resolution](02-repair-installed-context-link-resolution.md) |
| 03 | pending | required-v1 | release candidate | [Make knowledge hierarchy promotion predictable](03-make-knowledge-hierarchy-promotion-predictable.md) |
| 04 | pending | required-v1 | release candidate | [Enforce faithful inbox ingestion completion](04-enforce-faithful-inbox-ingestion-completion.md) |
| 05 | completed | blocker | next prerelease | [Restore complete prerelease upgrade coverage](05-restore-complete-prerelease-upgrade-coverage.md) |
| 06 | completed | blocker | next prerelease | [Remove empty upgrade transaction containers](06-remove-empty-upgrade-transaction-containers.md) |

## Adding a finding

1. Assign the next unused two-digit ID.
2. Copy the structure from [the finding template](finding-template.md) into a new file named `NN-short-description.md`.
3. Record the affected published version or source revision, observed behavior, reproduction evidence, classification, blocked gate, and completion criteria.
4. Add the finding to this table and make the first actionable pending finding the current next finding.
5. Keep the parent dogfood task pending.

A finding that requires repository work must not remain only in a conversation, CI log, release comment, or informal checklist.

## Resolving a finding

The implementation PR that resolves a finding must:

1. change its task status from `pending` to `completed`
2. add concrete resolution and repository-validation evidence
3. update its row in this index
4. select the next actionable pending finding, when one exists
5. leave the parent dogfood task pending unless the user explicitly closes dogfooding

A finding is completed when its bounded repository change, regression coverage, documentation, indexes, and resolution evidence are implemented in the resolving PR. Published-asset or realistic-project checks that can only happen after merge are appended later as release qualification evidence. They do not keep or return the finding to `pending`.

Completed findings remain in the index as durable prerelease evidence. Do not delete or renumber them.

## Release qualification evidence

When several completed findings require validation through the same published assets, validate them through one corrective prerelease when practical and append the resulting evidence to every relevant finding.

Missing immutable-release evidence can still prevent the next release from qualifying. It is represented as an unmet release gate, not as unfinished implementation-task status.

Finding 02 is complete. PR [#53](https://github.com/phdah/ava/pull/53) supplied the repository implementation and local qualification, and immutable `1.0.0-alpha.7` validation on 2026-08-06 proved that the Inbox Ingester loaded its complete required-reading chain from exact installed-project paths without substitution or mutation.

Finding 05 is complete through merged PR [#60](https://github.com/phdah/ava/pull/60). Its generic release-PR completion machinery prevents future releases from silently omitting inherited or protected direct sources. The next corrective immutable release must still declare the required real edges and validate the affected source installations before that release qualifies.

Finding 06 is complete through PR [#62](https://github.com/phdah/ava/pull/62). Terminal transaction cleanup now removes an empty parent after its final workspace is deleted while preserving active, blocked, or non-empty transaction state. The next corrective immutable release must still prove the behavior through real supported-source upgrades and a healthy Ava Maintenance inspection before that release qualifies.

Finding 03 is the current actionable implementation task. It defines semantic hierarchy-promotion guidance so repeated ingestion routes durable subjects predictably without imposing a fixed project taxonomy or numeric split threshold.

## Classification

- `blocker`: prevents the next prerelease and every later release gate until resolved
- `required-v1`: must be completed before the release candidate or stable release gate named by the finding
- `post-v1`: an explicit accepted deferral that does not weaken a v1 contract or safety property

A post-v1 decision is recorded as a completed finding with the deferral rationale and approving user decision. It is not represented as unresolved work in this backlog.

## Dogfood completion

The parent task may be completed only after the user explicitly says dogfooding is complete and all of the following are true:

- no blocker remains pending
- every required-v1 finding is completed or placed before the release gate it blocks
- the latest supported prerelease has a tested upgrade path to the next planned release stage
- the required realistic installation, routing, recovery, upgrade, uninstall, and reinstall scenarios have been exercised
- this index and the phase roadmap accurately reflect every finding and disposition
