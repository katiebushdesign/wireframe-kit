---
name: wireframe-from-copy-doc
description: >-
  Applies Google Docs copy (one table per page; flexible row/column layout) to HTML
  wireframes via docx export and JSON. Use when updating copy from the client copy
  doc, parsing docx, building pages from copy tables, or wireframe copy workflow.
---

# Wireframe from copy doc

**Follow:** [`AI-INSTRUCTIONS.md`](../AI-INSTRUCTIONS.md) — Task: **Apply copy from doc**.

**Also read:** [`copy-doc-access.md`](../copy-doc-access.md) (if URL blocked), [`assembling-pages.md`](../assembling-pages.md), [`notes-and-cues.md`](../notes-and-cues.md), [`block-mapping.md`](../block-mapping.md), `../config/client.yaml`, `../config/site-map.yaml`.

**If the Google Doc is not readable:** stop per `copy-doc-access.md` — ask for permissions, OAuth, or `.docx` export. Do not web-search or search the user’s computer.

**Multiple tabs:** If unsure which tab holds wireframe copy, ask before parsing (use `copy_doc_tab` in `client.yaml` when set).

**JSON examples:** [reference.md](reference.md)

**Command:** `make parse-copy` (from repo root)

Edit procedures in `AI-INSTRUCTIONS.md` only.
