---
id: ava-5624
title: "Fix OpenCode session-export pipe truncation in qualification evidence capture"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5624
---

## Description

Remove the 65,536-byte pipe truncation limitation affecting qualification session-inventory evidence capture.

## Migrated task record

Historical metadata: phase 5 finding 24, `required-v1`, blocking release candidate, affected version `1.0.0-alpha.15`, completed before the corrective-alpha rerun.

### Observed behavior and root cause

Qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local` found OpenCode JSON output truncated at exactly 65,536 bytes when stdout was a pipe, while the same commands wrote complete JSON to regular files. An external `/tmp` wrapper proved the data itself was valid. The maintained `qualification-opencode.sh` adapter inherited qualification automation's stdout pipe for session-list database and `opencode export`, exposing both large JSON paths to the host limitation.

### Resolution evidence

The adapter now writes each real OpenCode JSON command to a `mktemp` regular file and only then re-emits the complete bytes to qualification automation, preserving command arguments and Python-side JSON parsing as the validation boundary. `test_qualification_opencode_adapter.py` includes a pipe-sensitive fake whose valid JSON exceeds 65,536 bytes and truncates only on FIFO stdout; tests prove both session list and export remain complete and parseable.

Completion covered locating both paths, buffering both through regular files, oversized regression coverage and documentation that normal qualification no longer needs the external shim.

Release follow-up required the next fresh full qualification run to use the normal repository command path without `AVA_QUALIFICATION_OPENCODE` pointing at the old shim, with complete inventory and audit as immutable release evidence.