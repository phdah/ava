---
type: Internal Development Task
title: Add a Sanctioned Deterministic Office-Document Reader Tool for Inbox Ingestion
description: Replace the ad hoc script that used to extract text from .docx/.pptx sources with a sanctioned, deterministic, read-only extraction tool so inbox batches containing Office-format sources can complete without ad hoc code or fabricated content.
tags: [internal, roadmap, dogfood, inbox, tooling, qualification]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 34
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-25T17:13:00+02:00
---

# Add a Sanctioned Deterministic Office-Document Reader Tool for Inbox Ingestion

## Observed behavior

Removing the ability to write and execute ad hoc scripts during ingestion (finding 27) also removed the only mechanism Inbox Ingester had for extracting text from binary Office formats (`.docx`/`.pptx`). On the 2026-08-25 run, the session correctly refused to guess at 9 Office-format sources and stopped with a "User Decision Required" report rather than fabricate content, which is the right behavior given no alternative exists.

Finding 33 subsequently retained `complete-pending-inbox` but shrank its live qualification fixture to the exact seven-source format lower bound. That minimum intentionally retains one `.docx` and one `.pptx`, so the blocker remains: any maintained inbox batch containing either format still lacks a sanctioned way to read its content.

## Reproduction and evidence

Run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local` demonstrated the original failure against 7 `.docx` and 2 `.pptx` sources generated as real, minimal OOXML zip archives by `docx_bytes`/`pptx_bytes` in the synthetic fixture. Finding 33 now reduces the normal live qualification workload to one representative source of each Office format, but does not remove either format. The next generated qualification fixture records the exact seven-source selection in `variants/04-complete-pending-inbox/selection.json`.

This is therefore still both a real-world dogfooding limitation and a maintained qualification blocker: Inbox Ingester cannot safely complete the selected `.docx` and `.pptx` sources until a deterministic sanctioned reader exists.

## Classification

`blocker` for the next prerelease: the maintained synthetic qualification matrix cannot mechanically pass `complete-pending-inbox` while it retains representative `.docx` and `.pptx` sources that Inbox Ingester has no sanctioned way to read.

Finding 33 is resolved and confirms the exact dependency: Office coverage is intentionally retained, so this finding is required rather than conditional on the keep/shrink/remove decision.

## Root cause

Finding 27 correctly banned ad hoc script creation and execution as a bulk-content-transformation mechanism, but the pre-existing (now banned) script was also the only mechanism ever available for extracting text from binary `.docx`/`.pptx` containers. No deterministic, sanctioned Ava tool for that extraction exists. The role constraint and the missing capability were never reconciled: `templates/base/roles/inbox-ingester/capabilities.md` grants no read-office-document capability, and no repository or distributed tool provides one.

## Scope

- add a small, deterministic, sanctioned document-reader tool (for example a repository-provided or Ava-distributed helper that unzips `word/document.xml` / `ppt/slides/slide*.xml` and strips markup to plain text, mirroring the read-only structural check `qualification_runner.py` already performs for verification) that Inbox Ingester may invoke to read, not transform or route, a single Office-format source's text content
- explicitly scope the exception in `inbox-ingester/constraints.md` and `capabilities.md`: this tool may only extract readable text for the role's own direct reasoning; it must not classify, route, merge, or write destination content, preserving finding 27's prohibition on programmatic bulk-content transformation
- decide whether the tool ships as a distributed Ava-managed tool available in real installed projects or as a repository/qualification-only helper; because the retained scenario represents real inbox behavior, the preferred outcome must support installed projects rather than merely teach the fixture runner to bypass the role limitation
- add regression coverage proving the tool extracts the known fixture text from representative `.docx`/`.pptx` sources and that Inbox Ingester's role documents scope its use correctly

## Completion criteria

- [ ] a sanctioned, deterministic tool exists that extracts plain text from `.docx`/`.pptx` sources without ad hoc code execution by the ingesting session
- [ ] `inbox-ingester/capabilities.md` and `constraints.md` explicitly scope the tool to read-only text extraction, preserving finding 27's ban on programmatic bulk transformation
- [ ] the maintained `complete-pending-inbox` synthetic scenario can complete for its representative Office-format sources
- [ ] regression coverage exercises the tool against the vault's `.docx`/`.pptx` fixtures
- [ ] repository test suite passes

## Resolution evidence

_Complete in the resolving implementation PR._
