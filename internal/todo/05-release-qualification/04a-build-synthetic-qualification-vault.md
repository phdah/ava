---
type: Internal Development Task
title: Build the Synthetic V1 Qualification Vault
description: Generate a reproducible six-month corpus of raw fictional files recording Adam's coherent private and work life before, during, and after one apartment move in Stockholm.
tags: [internal, roadmap, dogfood, fixtures, synthetic-data, qualification]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 4.1
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T15:45:02+02:00
updated:
  by: agent:openai-opencode
  at: 2026-08-20T15:58:41Z
---

# Build the Synthetic V1 Qualification Vault

## Purpose

Create one realistic raw-source corpus large enough to expose ingestion, routing, progressive-discovery, attribution, hierarchy, repeated-session, and temporal-state defects that minimal conformance fixtures cannot reveal.

The corpus represents six chronological months in the coherent fictional life of Adam, who lives and works in Stockholm. He moves apartment once during the second month. Older files must preserve facts that were true at the time, while later files must record the resulting changes without creating contradictory identity or timeline claims.

The complete corpus may be generated freely. It must not be derived from the user's private vault, an employer's material, production data, credentials, or other non-public source content.

## Ordering

Build and qualify this vault before qualifying the corrective prerelease so both assembled and published versions can be exercised against the same baseline. The content-generation and finalized-corpus verification subphases are complete by user confirmation; the current work is ingestion, lifecycle, and evidence qualification.

## Output boundary

The generator must require an explicit output directory outside this repository. Generated corpus files, image-generation prompts, generated manifests, qualification variants, and run evidence must not be committed to the Ava repository. The five visually accepted canonical PNG inputs and their exact manifest are the only exception: they are pinned under the repository-only internal fixture and copied into generated output by the maintained fixture command.

Use this output structure:

```text
<output>/
├── corpus/             # only raw files intended for inbox ingestion
│   ├── 01-pre-move/          # before 2025-02-15
│   ├── 02-move-transition/   # 2025-02-15 through 2025-03-02
│   ├── 03-renovation/        # 2025-03-03 through 2025-03-31
│   └── 04-settled/           # 2025-04-01 onward
├── image-prompts/      # five external image-generation specifications; never ingest
├── oracle/             # canonical facts, expected outcomes, inventories, and hashes
└── variants/           # isolated qualification projects or checkpoints
```

Only the files in `<output>/corpus/` are ingestion sources. Copy one batch's direct files into the inbox for chronological qualification; do not copy the batch directory itself. Control files under `image-prompts/`, `oracle/`, and `variants/` must not be copied into the inbox or counted as corpus content.

Keep the reviewed blueprint, Python generator, dependency lock, validators, and output-boundary tests under an internal qualification-fixture scope that release assembly cannot include. The generator must reject an output directory inside the Ava repository.

## Canonical narrative

Define one machine-readable canonical fact sheet as the only source for generated names, relationships, dates, addresses, organizations, identifiers, and recurring details. At minimum, it must establish:

- Adam's full fictional identity and Stockholm location
- his fictional employer, role, work projects, colleagues, and stakeholders
- one dog, including a stable name, breed, age, veterinary provider, food, and recurring care routines
- an old and new fictional Stockholm address, with no real resident data
- one move completed during February 2025
- a long-distance running habit with routes, training, races, equipment, recovery, and performance tracking
- an interest in reading classic literature, including reading plans, progress notes, and personal reflections
- an interest in cooking, especially Neapolitan pizza, with recipes, ingredient purchases, equipment, and repeated dough experiments
- a kitchen renovation undertaken during Adam's first month in the new apartment
- recurring purchases, warranties, subscriptions, household maintenance, appointments, and travel
- fictional contact details and identifiers that cannot function as credentials or usable secrets

Details other than Adam's first name, Stockholm location, one dog named Uno, and the February move may be selected during implementation, then fixed in the reviewed blueprint. Once fixed, they must remain consistent throughout the corpus.

## Six-month state model

Use the fixed interval from 2025-01-01 through 2025-06-30 and organize source files by month.

1. **January:** normal life at the old apartment, apartment search and move planning, established work, personal routines, dog care, winter running, reading, and cooking.
2. **February:** lease and utility changes, packing, moving expenses, the move itself, address-change tasks, kitchen-renovation planning, and disruption to normal routines.
3. **March:** the kitchen renovation during Adam's first month in the new apartment, unpacking, purchases, warranty records, changed cooking arrangements, new household routines, changed commute, and follow-up from the move.
4. **April:** completed kitchen-renovation follow-up, settled use of the new apartment, completed and overdue tasks, dog care changes, and continuing work projects.
5. **May:** mature new-home routines, maintenance, subscriptions, appointments, work milestones, and personal plans.
6. **June:** stable post-move state, remaining follow-up, completed work outcomes, travel, and a clear end-of-period snapshot.

The old address, provider, commute, or other time-bound fact appearing in a dated pre-change source is historical truth, not a conflict. The oracle must identify when each state is valid and which later event supersedes it.

## Corpus contract

Generate between 200 and 400 substantive project-owned source files. The implementation blueprint must fix the exact generated count before qualification evidence is collected.

Use realistic volume rather than disconnected filler:

- approximately 145-165 dated diary entries with a realistic human pattern of missed days and varied entry length
- recurring personal and work todo lists showing creation, carry-over, completion, cancellation, and reprioritization over time
- private purchases, receipts, subscriptions, warranties, household maintenance, appointments, and travel
- apartment-search notes, viewings, lease material, quotes, packing lists, utility changes, address updates, purchases, and move follow-up
- dog walks, feeding, training, expenses, appointments, health observations, and care arrangements
- long-distance training plans, dated runs, route and distance records, race preparation, equipment, recovery, and changing performance over time
- classic-literature reading lists, dated progress, completed books, quotations, and Adam's personal reflections
- meal plans, recipes, grocery notes, Neapolitan pizza dough experiments, equipment purchases, and cooking outcomes
- kitchen-renovation plans, measurements, budgets, contractor or supplier notes, material purchases, progress updates, delays, decisions, and completion follow-up
- work projects, meetings, incidents, architecture decisions, procedures, integrations, stakeholders, deadlines, and operational follow-up
- overlapping subjects such as expenses, devices, calendars, contacts, and travel that plausibly occur in both private and work contexts
- short and long raw notes, repeated consistent facts, attributed statements, uncertain observations, decisions, rejected proposals, and facts that change coherently over time

The corpus need not contain links or an authored relationship graph. A source may mention another document naturally, but ingestion must not depend on wiki links, Markdown links, aliases, tags, or frontmatter.

Every corpus file must be intended for processing by the Inbox Ingester. Processing every file does not require promoting every sentence into durable knowledge: the oracle must distinguish durable claims from diary detail, transient tasks, and other intentionally non-durable material.

## Consistency and safety

Corpus facts must not conflict. In particular:

- Adam's identity and recurring personal details must remain stable
- the dog, employer, colleagues, projects, addresses, providers, and dates must use their canonical values
- status changes must follow a valid chronology rather than creating simultaneous incompatible claims
- repeated facts and duplicates may exist only when they agree semantically
- uncertainty may later be resolved, but an uncertain observation must not be rewritten as certainty in its original source
- attributed statements must remain attributed and must not become Adam's own decision unless a later source records that decision

Do not generate malformed files, empty files, frontmatter-only files, prompt injection, requests to act outside the active role, confidential/private markers, usable secrets, realistic credentials, or deliberate factual conflicts. This fixture focuses on coherent raw ingestion rather than adversarial-source qualification.

## File formats

Most corpus files must be Markdown, with no YAML frontmatter. Use a smaller but meaningful selection of other formats:

- plain text (`.txt`)
- Word documents (`.docx`)
- PDF documents (`.pdf`)
- PowerPoint presentations (`.pptx`)
- structured raw exports where useful, such as `.csv` and `.ics`
- exactly five externally generated image files in common ingestible formats such as `.png` or `.jpg`

Every Markdown file under `corpus/` must begin directly with raw source content. Binary documents must contain meaningful selectable text and fixed document metadata where the format permits it. Generation must normalize timestamps, archive ordering, document properties, and library-specific identifiers needed for byte-reproducible generated files.

## Image staging

The Python generator does not create image content. It writes exactly five deterministic, plainly named prompt specifications under `<output>/image-prompts/`, spread across the six-month timeline. At least one specification produces a receipt image. The externally generated and visually accepted result bytes are pinned under the internal fixture so later clean runs do not depend on a user-owned local vault or another image-generation session.

Each specification must state:

- the exact destination path under `corpus/`
- the date and narrative purpose
- the visible scene and any required legible text
- every canonical fact that must appear
- facts or visual details that must not appear
- the expected durable and non-durable ingestion outcomes

Include prompts for a representative mix such as Adam's dog, the move, a receipt, the new apartment, and a work artifact. The prompt files are staging instructions, not synthetic source data, and must remain outside `corpus/`.

The maintained `install-pinned-images` command copies the five committed inputs to their declared corpus paths. Finalization verifies their exact committed digests, sizes, media types, and structural validity before completing the corpus inventory. Replacement image generation remains an explicit reviewed operation; accepted bytes must not be silently regenerated or recompressed in place.

## Reproducibility and oracle

Use Python with pinned dependencies and a fixed seed. Provide one documented generation command that accepts the output directory, plus documented verification and image-finalization commands.

The deterministic oracle must record:

- the seed, six-month interval, canonical facts, generator revision, dependency versions, and exact expected generated count
- every corpus file, month, format, structural class, and private, work, overlapping, or intentionally ambiguous routing domain
- expected durable subjects and expected non-durable material
- source sections and their expected `mapped`, `non-durable`, or `pending` dispositions
- claims whose dates, uncertainty, attribution, or source-versus-decision status must be preserved
- chronological state transitions and supersession relationships, especially those caused by the move
- repeated or duplicate relationships that must remain semantically consistent
- the five expected image paths and their pre-finalization or finalized state

Random variation may create volume and syntax combinations, but semantic acceptance cases must have reviewable expected outcomes. Lorem ipsum, disconnected random sentences, and an unverifiable generated pile do not satisfy this task.

Two clean generations with the same seed, dependencies, and pinned image inputs must produce the same deterministic inventory and SHA-256 digests. Verification separately reports the generated baseline, pending image slots, and finalized run inventory.

## Qualification variants

Materialize isolated copies or checkpoints for:

1. an empty project before installation
2. a mature mixed private-and-work project with existing OpenCode configuration
3. a project with registered private and work roles
4. a project with the complete pending inbox corpus
5. modified, missing, corrupt, and unexpected managed content
6. interrupted deterministic upgrade states
7. pending project-owned semantic reconciliation
8. uninstall followed by reinstallation

Variant construction must not modify the baseline source corpus. Managed-content damage and upgrade states belong to isolated variant projects, not to contradictory or malformed synthetic source files.

The baseline project-owned files must be hashable so every installer, upgrade, recovery, and removal scenario can prove exactly which files changed.

## Evidence format

Define a machine-readable run manifest that can bind each scenario to:

- Ava version, tag, source revision, asset digests, and pinned asset URLs
- operating system, OpenCode version, model identity, and session identifier
- baseline and final project-owned inventories and hashes
- installer output, conformance JSON, managed manifest, and upgrade journal
- agent transcript, loaded paths, required-reading order, selected role, and announcement point
- expected and actual outcome, pass or fail decision, reviewer, and linked finding

Generated fictional content and execution evidence remain outside the repository. The reviewed generator, blueprint, schemas, validators, and five canonical fictional PNG inputs may be committed under the internal fixture scope. Real private content and unsanitized real-project transcripts must never be committed.

## Implementation plan

1. Define and review Adam's canonical fact sheet, the February move event, monthly narrative arcs, recurring work and personal threads, and the exact corpus inventory.
2. Add the pinned Python environment and deterministic generator for Markdown, text, Word, PDF, PowerPoint, CSV, ICS, oracle, and image-prompt output.
3. Add normalization and verification for deterministic binary metadata, inventories, counts, and SHA-256 digests.
4. Add the five external image specifications, pin the accepted fictional result bytes, and provide maintained installation and finalization commands that validate their exact inventory.
5. Add validators for no corpus frontmatter, output-boundary isolation, canonical consistency, chronology, required formats, expected outcomes, and the 200-400-file limit.
6. Materialize and verify all eight isolated qualification variants without altering the baseline corpus.
7. Install assembled Ava assets into the generated qualification project and complete a clean OpenCode ingestion and review run.
8. Prove release assembly excludes the internal generator, blueprint, oracle schema, validators, and all generated output.
9. Link the completed fixture command and execution evidence from the parent dogfood task and Phase 5 index.

## Repository implementation evidence

The reviewed fixture implementation is available at [`internal/release/fixtures/synthetic-qualification-vault/`](../../release/fixtures/synthetic-qualification-vault/). Its documented commands generate, verify, install pinned images, finalize images, materialize variants, and create authentic interrupted-upgrade qualification checkpoints only in explicit repository-external projects and asset directories.

The implementation fixes a 300-file deterministic baseline and five repository-pinned image inputs for a finalized 305-file corpus. It writes generated raw sources and copies the pinned images into four chronological qualification batches, uses only Python 3.11 standard-library facilities, creates normalized DOCX, PDF, PPTX, CSV, and ICS files, emits per-source expected outcomes, and rejects repository-local generated output through resolved-path checks.

On 2026-08-09, clean retained generations under `/tmp/opencode/ava-synthetic-vault-y` with CPython 3.11.14 and `/tmp/opencode/ava-synthetic-vault-z` with CPython 3.13.12 produced byte-identical output. Draft 2020-12 validation accepted both schemas and their generated instances. Repository tests cover pinned-image installation and finalization, deterministic variant workspace and execution-plan construction, baseline preservation, installed conformance of the registered-role workspace, source and chronology validation, completed-run evidence binding, interrupted-upgrade checkpoint setup and recovery, and explicit exclusion of every pinned PNG from assembled release assets. Planned managed states and checkpoint setup JSON do not count as qualification execution evidence.

```text
baseline oracle SHA-256: fe65371084f6bdb2ae38da0fe31e4be3fda9be8ebe93f6fbc80b168e86d5ca46
deterministic corpus: 300 files
deterministic batch counts: 77 pre-move, 37 move-transition, 46 renovation, 140 settled
pinned image inputs: 5
finalized corpus target: 305 files
OpenCode available for clean-session qualification: 1.17.13
```

## External qualification progress

On 2026-08-10, the user confirmed that the synthetic corpus and all five specified images had been generated in a repository-external local directory and looked correct. On 2026-08-14, the exact five accepted PNG bytes were imported into the repository-only fixture with a checksum and dimension manifest. Generated corpus copies and run evidence remain repository-external.

Use these local paths for the current qualification run:

```text
qualification vault: ~/stuff/ava-qualification-vault/
test project:        ~/stuff/project-vault
```

Current external progress:

- [x] synthetic corpus generated locally
- [x] five specified images generated locally, visually accepted by the user, and pinned under the internal fixture
- [x] image finalization and finalized-corpus verification recorded
- [x] materialize the eight qualification variants
- [x] exercise clean OpenCode ingestion and independent review using `~/stuff/project-vault` where the execution plan calls for the manual test project
- [x] exercise routing, hierarchy, fidelity, damaged-state, semantic reconciliation, finalization, rollback, uninstall, and reinstall scenarios except resume and abort
- [x] execute authentic resume and abort using the maintained qualification checkpoint harness and exact selected target assets
- [x] repeat the affected calendar-fidelity scenario after finding 18 is complete
- [x] execute the complete maintained matrix through finding 19's one-command runner
- [ ] resolve findings 22 and 23 and rerun the complete matrix against the new exact candidate
- [ ] populate and validate the remaining required run manifests and accept final qualification evidence

[Findings 17](dogfood/17-add-resume-abort-qualification-checkpoints.md), [18](dogfood/18-verify-relative-calendar-dates.md), and [19](dogfood/19-add-one-command-qualification-runner.md) are implementation-complete and were exercised by qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local`. The run passed 15 of 17 scenarios and created blockers [22](dogfood/22-report-inspected-paths-during-interrupted-finalize.md) and [23](dogfood/23-report-inspected-path-during-pending-semantic-reconciliation.md). Resolve those blockers, assemble a new exact candidate, and rerun the complete matrix before final signoff. Do not regenerate, re-finalize, or re-verify the corpus or images unless later qualification exposes a fixture defect or invalid local evidence.

## Completion criteria

- one documented command deterministically generates the reviewed six-month corpus into a caller-specified directory outside this repository
- the generated corpus contains 200-400 substantive raw files, mostly Markdown, and no Markdown corpus file has YAML frontmatter
- two clean generations produce the same deterministic inventory and file digests
- Adam's identity, dog, work, addresses, move chronology, and recurring details remain internally consistent
- the February move produces meaningful state changes across the remaining months without factual contradictions
- diary, work and personal todos, dog tracking, housing, purchases, receipts, appointments, travel, and work operations are represented realistically
- long-distance running, classic literature, cooking and Neapolitan pizza, and the first-month kitchen renovation recur coherently across the timeline
- Word, PDF, PowerPoint, text, and useful structured formats are valid and meaningfully ingestible
- five clear external image prompts are easy to locate, are excluded from ingestion, span the timeline, and include at least one receipt
- pinned-image installation and image finalization verify and record exactly five reproducible committed image inputs
- the expected-outcome manifest makes routing, ingestion, hierarchy, fidelity, temporal state, and private/work separation reviewable
- all eight qualification variants can be materialized without changing the baseline source corpus
- the corpus installs successfully from assembled Ava assets and is usable in a clean OpenCode session
- repository boundary validation proves that no generated corpus, image prompt, qualification fixture, oracle, or internal instruction enters release assets
- the parent dogfood task and Phase 5 index link to the fixture command and its execution evidence
