# Alpha Dogfood Findings

This index is the mutable backlog for findings discovered while exercising published Ava prereleases. The parent task remains [Dogfood the Alpha and Track Findings](../04-dogfood-alpha-and-track-findings.md).

## Control rule

Dogfooding remains active until the user explicitly declares it complete. An empty findings list, a passing test suite, or publication of another prerelease does not automatically complete the parent task or advance the roadmap to the release candidate.

## Current next finding

[Repair installed context link resolution](02-repair-installed-context-link-resolution.md).

## Backlog status

- 3 pending findings
- 1 pending blocker
- 2 pending required-v1 findings
- 1 completed finding

## Findings

| ID | Status | Classification | Blocks | Finding |
|---|---|---|---|---|
| 01 | completed | blocker | next prerelease | [Restore supported prerelease upgrade paths](01-restore-prerelease-upgrade-paths.md) |
| 02 | pending | blocker | next prerelease | [Repair installed context link resolution](02-repair-installed-context-link-resolution.md) |
| 03 | pending | required-v1 | release candidate | [Make knowledge hierarchy promotion predictable](03-make-knowledge-hierarchy-promotion-predictable.md) |
| 04 | pending | required-v1 | release candidate | [Enforce faithful inbox ingestion completion](04-enforce-faithful-inbox-ingestion-completion.md) |

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
2. add concrete resolution and validation evidence
3. update its row in this index
4. select the next actionable pending finding, when one exists
5. leave the parent dogfood task pending unless the user explicitly closes dogfooding

Completed findings remain in the index as durable prerelease evidence. Do not delete or renumber them.

## Shared prerelease validation

Implement findings in dependency order. When several findings require the same published-asset validation, a finding whose repository implementation is complete may remain pending while work proceeds to the next finding. Publish one corrective prerelease when practical, record its evidence in every finding it validates, and complete only the findings whose criteria pass.

This batching rule does not permit publication while a pending blocker is absent from the release or otherwise unresolved.

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
