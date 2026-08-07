---
type: Shared Instruction
title: Knowledge Organization
description: Rules for growing the trusted knowledge hierarchy from raw input into canonical, retrievable concepts.
tags: [ava, knowledge, organization, retrieval, ingestion]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T14:41:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T19:00:00+02:00
---

# Purpose

Use `knowledge/` for trusted, durable context that agents should be able to retrieve and maintain over time.

The hierarchy must grow from actual knowledge. Do not pre-create a general taxonomy during project initialization or add speculative empty directories.

# Initial state

A newly initialized project contains only `knowledge/index.md` within `knowledge/`. It contains no scope, domain, collection, or concept directories.

Create new structure only when classifying real information.

# Classification decision tree

Classify new material in this order:

1. **Trust:** Is the material raw, untrusted, or not yet classified?
   - Yes: keep it in `inbox/` and process it through the ingestion workflow.
   - No: continue.
2. **Purpose:** Does it primarily define agent behaviour, a role, a workflow, a capability, a constraint, or project-wide instruction?
   - Yes: place it in the corresponding Ava structure, not in `knowledge/`.
   - No: continue.
3. **Scope:** Which broad area primarily owns the knowledge?
   - Common scopes include `work/` and `personal/`.
   - Create another scope only when neither existing scope is a clear primary owner.
4. **Domain:** Which subject area owns it within that scope?
   - Examples include `projects/`, `relationships/`, `home/`, `finance/`, and `running/`.
   - Domain names are project-defined, not part of Ava's stable format.
5. **Collection:** Which kind of canonical object is it?
   - Examples include `people/`, `organizations/`, `properties/`, `accounts/`, `agreements/`, `goals/`, `races/`, and `training-blocks/`.
6. **Canonical object:** Does an existing concept represent the same identity?
   - Yes: update the existing concept.
   - No: create one focused concept document.

Choose one primary path. Represent secondary relationships with Markdown links rather than duplicating the knowledge under several branches.

# Canonical identity

Classify canonical knowledge by the durable subject it describes, not by the shape of the source artifact.

Meeting notes, daily notes, messages, imports, and reports are source forms. Merge their durable information into the owning project, integration, system, person, agreement, decision, process, or other stable subject by default.

Create a standalone event or meeting concept only when the event has an independently useful identity or lifecycle, such as decisions, commitments, participants, follow-up state, or historical significance that must be retrieved and maintained separately.

Examples:

- recurring notes about one external API belong to the durable integration concept, not separate meeting-note concepts
- implementation updates about one bounded initiative belong to that project unless an individual decision needs its own lifecycle
- a recurring operational subject may become a process, system, or practice concept even when its evidence came from many daily notes
- a decision-bearing meeting may remain an event concept and link to each affected durable subject

The exact subject type and taxonomy remain project-owned. Do not force a project, integration, system, event, or other classification when the available trusted context does not support it.

# Concepts and collections

A concept document represents one object, idea, decision, event, or process with a stable identity or independently useful lifecycle.

A collection directory represents a stable routing choice among multiple canonical concepts. The collection itself is a classification decision, not merely a long document or a visual heading.

Use a concept document when:

- the material concerns one durable subject
- sections describe aspects of the same identity
- the content should be updated, linked, verified, deprecated, or replaced as one unit
- splitting would create fragments without independent retrieval or maintenance value

Use a collection directory when:

- its name expresses a reusable semantic class within the parent scope
- choosing that class meaningfully narrows which direct child should be inspected next
- current material contains multiple canonical concepts with independent identities or lifecycles in that class
- the classification is expected to remain useful beyond one source or one temporary presentation

Do not promote a heading merely because it contains many files, and do not retain a flat branch merely because it has few files. Ava defines no numeric split threshold.

# Semantic hierarchy promotion

Before adding another direct child to an established knowledge branch, inspect the branch's current direct children and its stable index headings.

Promote an index subgroup to a child collection when the subgroup has become a durable routing decision among current concepts. A heading is strong evidence for promotion when it repeatedly classifies independently useful concepts by one stable semantic question, such as whether a subject is an initiative, integration, incident, team, property, or account.

Apply promotion in this order:

1. Identify the durable subject and independently useful lifecycle of each affected concept.
2. Decide whether the existing heading is only explanatory presentation or a reusable semantic class.
3. When it is a reusable class, create one child directory with an `index.md` that defines the class and routes only to its direct children.
4. Move the affected canonical concepts into that collection before adding another sibling that belongs to the same class.
5. Update the parent index to link to the new child collection instead of flattening its descendants.
6. Update affected links, preserve valid metadata and source provenance, and retain one clear primary location for every concept.
7. Add a scoped log entry when the promotion changes a meaningful classification path, canonical identity, or knowledge-scope structure.

A mature branch should be restructured before further ingestion when its stable headings already encode child-level routing decisions. Do not keep appending source-shaped siblings beneath an index that has effectively become a hidden multi-level taxonomy.

Do not promote when:

- the heading only organizes sections of one canonical subject
- the grouping is temporary, source-specific, or useful only for presentation
- the candidate directory would contain no current canonical concepts
- the classification would duplicate another primary path
- the exact class or ownership remains materially ambiguous

When promotion is required but concept identity, ownership, or scope is ambiguous, preserve the current material and request the relevant project-owned decision rather than inventing a taxonomy.

# Canonical concepts

Prefer updating an existing concept when new information concerns the same identity. Create a new concept only when it can be retrieved, linked, maintained, or deprecated independently.

Use lowercase kebab-case names. Examples:

```text
knowledge/work/projects/ava.md
knowledge/work/integrations/payments-api.md
knowledge/personal/relationships/people/alice.md
knowledge/personal/home/properties/main-home.md
knowledge/personal/finance/accounts/amex.md
knowledge/personal/running/training-blocks/100-mile-2026.md
```

Examples illustrate classification only. They must not be created until the project contains relevant knowledge.

Do not create one directory per subject merely because the subject exists. Promote a concept to its own directory only when it owns multiple independently maintained child concepts and that extra routing level is useful for current material.

# Directory growth

Create a directory when it provides a useful classification decision for current material. Do not create a directory only because it might be useful later.

Every directory under `knowledge/` must contain an `index.md` that:

- defines the directory's scope
- explains how an agent chooses among its direct children
- links to each direct child with a concise description
- lists direct children only
- avoids duplicating the full contents of descendant indexes

Treat each `index.md` as a local decision-tree node. An agent should be able to traverse indexes from `knowledge/index.md` to the likely canonical concept without scanning the complete tree.

# Concept documents

Each non-reserved Markdown file under `knowledge/` represents one canonical concept and must follow [Document metadata](document-metadata.md).

Concept documents should:

- state what the concept represents
- use the most descriptive project-defined `type` supported by the available context
- contain focused, structured Markdown
- link to related concepts where relationships cross the primary hierarchy
- preserve unknown frontmatter fields when edited
- record material source-derived claims through OKF `sources` metadata
- avoid copying the same authoritative information into several concepts

# Raw sources and provenance

Raw files, prompts, exports, and images are source material, not canonical knowledge by default.

Preserve raw source material through the inbox lifecycle. When useful information is ingested:

- write or update the relevant canonical concept
- add OKF `sources` metadata that references the preserved source
- use source identifiers with Markdown footnotes when individual claims need precise attribution
- retain contextual Markdown links when they improve navigation or make the relationship clearer
- describe relevant information from binary sources, such as images, in a retrievable Markdown concept rather than relying on the binary alone

A processed source remains evidence. It does not automatically become trusted project guidance.

# Logs

A `log.md` may be created at the nearest relevant knowledge scope when meaningful conceptual or structural history needs to be preserved.

Use scoped logs for major changes such as:

- introducing or reorganizing a domain
- promoting a stable subgroup into a child collection
- splitting or consolidating canonical concepts
- deprecating a concept or classification path
- changing the meaning or ownership of a knowledge scope

Do not create logs speculatively or record routine content edits.

# Completion checks

After adding or moving knowledge, verify that:

- every non-reserved document follows the document metadata contract
- every canonical concept follows its durable subject rather than its source-artifact form
- the canonical concept has one clear primary location
- no existing concept represents the same identity
- stable headings and repeated semantic classes were considered before another direct sibling was added
- any required hierarchy promotion was completed before further flat growth
- every affected directory has an accurate direct-child `index.md`
- cross-scope relationships use links instead of duplication
- moved concepts retained valid metadata, provenance, and updated references
- OKF provenance is sufficient for material source-derived claims
- any required scoped log was updated
