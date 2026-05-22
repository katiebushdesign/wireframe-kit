# Copy pipeline output

This folder holds **parser output** from `make parse-copy`.

## Starter template (wireframe-kit repo)

Keep `pages/` and `nav/` empty except `.gitkeep` — no client copy in the kit repo.

## Client wireframe repos (e.g. `leotech-wireframes`)

**Commit** `pages/*.json` and `nav/*.json` after `make parse-copy` so collaborators get the same structured copy without re-exporting the Google Doc.

| Path | Git in client repos |
|------|---------------------|
| `source/*.docx` | Ignored — export from Google Doc locally when refreshing copy |
| `pages/*.json` | **Tracked** — one JSON file per copy-doc page table |
| `nav/*.json` | **Tracked** — mega menu tables from the doc (if any) |

Workflow when copy changes: export `.docx` to `source/` → `make parse-copy` → commit JSON → update HTML → push.
