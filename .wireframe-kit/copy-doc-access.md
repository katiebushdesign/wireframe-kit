# Copy doc access (agents — read first)

When the copy doc is a **Google Doc URL** and you **cannot read it** (403, “request access”, sign-in wall, empty body, “you need permission”, fetch error), **stop the workflow** and ask the human. Do not improvise.

## Required behavior

1. **Tell the user access failed** — quote or summarize the error if you have one.
2. **Offer exactly these fixes** (pick what fits their environment):
   - **Share the doc** — add the user’s Google account (or the service account your integration uses) as **Viewer** (or Editor).
   - **Relax link sharing** — in Google Docs: Share → General access → “Anyone with the link” → **Viewer** (or their org policy equivalent).
   - **Manual export** — user downloads **File → Download → Microsoft Word (.docx)** and places it at `copy_docx_path` in `client.yaml` (default `.wireframe-kit/content/source/copy.docx`), then you run `make parse-copy`.
   - **OAuth / Google sign-in** — if the IDE or MCP provides Google Drive/Docs access, ask the user to **complete OAuth** or connect Google; do not proceed until authenticated access works.
3. **Wait** for one of the above before building copy from the doc.
4. If they have **no copy doc yet**, say so and continue only with placeholders they approve — do not fabricate client copy.

## Multiple tabs (which content to use)

Google Docs may have **more than one tab** in the same file. Before `make parse-copy` or building HTML from the doc:

1. Check `copy_doc_tab` in `client.yaml` if set — use that tab.
2. If the user already said which tab in the prompt, use it.
3. If **multiple tabs look like wireframe copy** (page tables, mega menu, etc.) and you are **not sure** which is canonical → **ask** which tab to use. List tab names; wait for an answer.
4. Do **not** combine tabs, pick the first tab, or assume “the leftmost tab” without confirmation.

See [copy-doc-format.md](./copy-doc-format.md) for structure; optional config: `copy_doc_tab` in `client.yaml.example`.

## Forbidden when access fails

Do **not**:

- **Web search** for the doc, client copy, or “212 Visual copy doc” to substitute content.
- **Search the user’s computer** outside this repo (`~/Desktop`, `~/Downloads`, `~/Documents`, Spotlight, broad `find`/`grep` for `.docx` / “copy”) looking for the file.
- **Guess or invent** marketing copy because the doc is locked.
- **Scrape** the public marketing site and treat it as the copy doc unless the user explicitly says that is the source of truth.
- **Loop** on failed URL fetches — one clear failure → ask for access.

Allowed without the Google Doc:

- Read **`copy_docx_path`** if the file exists in the workspace.
- Read **`.wireframe-kit/content/pages/*.json`** from a prior `make parse-copy`.
- Read **repo-root HTML** for revision mode.

## Quick decision tree

```
copy_doc_url or docx needed?
  ├─ .docx at copy_docx_path exists → make parse-copy
  ├─ pages/*.json already present → use JSON (note if stale)
  └─ neither → need access
        ├─ Google URL not readable → ASK USER (share / link / OAuth / manual docx)
        └─ never web-search or scan ~/ for the doc
```

## Message template (paste to user)

> I can’t read the copy Google Doc (permission denied / sign-in required). To continue, please do **one** of the following:
> 1. Share the doc with [my account / your agent’s Google account] as Viewer, or set link sharing to “Anyone with the link can view”.
> 2. Export **.docx** (File → Download → Word) and save it to `.wireframe-kit/content/source/copy.docx`, then tell me to run `make parse-copy`.
> 3. If your editor supports Google Drive, sign in via OAuth so I can access the doc.
>
> I won’t search the web or your computer for the document — I need explicit access or the export file.
