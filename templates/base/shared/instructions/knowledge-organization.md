---
type: Shared Instruction
title: Knowledge Organization
description: Rules for growing the trusted knowledge hierarchy from raw input into canonical, retrievable concepts.
tags: [ava, knowledge, organization, retrieval, ingestion]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-26T14:41:00Z
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

# Canonical concepts

A concept document should represent one object, idea, decision, or process with a stable identity or independently useful lifecycle.

Prefer updating an existing concept when new information concerns the same identity. Create a new concept only when it can be retrieved, linked, maintained, or deprecated independently.

Use lowercase kebab-case names. Examples:

```text
knowledge/work/projects/ava.md
knowledge/personal/relationships/people/alice.md
knowledge/personal/home/properties/main-home.md
knowledge/personal/finance/accounts/amex.md
knowledge/personal/running/training-blocks/100-mile-2026.md
```

Examples illustrate classification only. They must not be created until the project contains relevant knowledge.

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
- splitting or consolidating canonical concepts
- deprecating a concept or classification path
- changing the meaning or ownership of a knowledge scope

Do not create logs speculatively or record routine content edits.

# Completion checks

After adding or moving knowledge, verify that:

- every non-reserved document follows the document metadata contract
- the canonical concept has one clear primary location
- no existing concept represents the same identity
- every affected directory has an accurate `index.md`
- cross-scope relationships use links instead of duplication
- OKF provenance is sufficient for material source-derived claims
- any required scoped log was updated
