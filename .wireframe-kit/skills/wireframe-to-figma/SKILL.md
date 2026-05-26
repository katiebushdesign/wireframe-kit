---
name: wireframe-to-figma
description: >-
  Export HTML wireframes to a Figma design file using html-to-design capture,
  shared components, and layout on a Wireframes page. Use when the user wants
  wireframes in Figma, sync HTML to Figma, or run the standard html-to-design capture workflow
  on another project.
disable-model-invocation: false
---

# Wireframe → Figma

**Guide:** [figma-html-export.md](../../figma-html-export.md)  
**Canonical:** [AI-INSTRUCTIONS.md](../../AI-INSTRUCTIONS.md) (Task: Export to Figma)

Requires **Figma MCP** (`generate_figma_design`, `use_figma`). Do not commit unless the user asks.

---

## Phase 0 — Intake

| # | Question | Maps to |
|---|----------|---------|
| 1 | Figma file URL or `file_key` | `config/figma.yaml` |
| 2 | Wireframes page node id (or create page named `Wireframes`) | `wireframes_page_id` |
| 3 | All HTML pages captured? (list or use `site-map.yaml`) | manifest |
| 4 | Preview port (8765 free?) | `PORT` / `WIREFRAME_BASE` |
| 5 | Nav/footer synced in HTML? | `make sync` before capture |
| 6 | New file or update existing captures? | merge manifest vs new UUIDs |

---

## Phase 1 — Preflight

From **repo root**:

```bash
make link-skills
cp .wireframe-kit/config/figma.yaml.example .wireframe-kit/config/figma.yaml   # if missing
make figma-install-deps
make figma-init-manifest    # or MERGE=1 when adding pages
make sync                   # if multi-page shell
make serve
make figma-check
```

Fill `figma.yaml` with `file_key`, `file_url`, `wireframes_page_id`.

---

## Phase 2 — Figma file structure

Create or confirm pages:

- `Wireframes` — destination for captures
- `— Foundations —` — tokens from `css/style.css`
- `— Components —` — primitives + site chrome

**Components page order (Y axis, no overlap):**

1. Primitives label → Button set → Card set → Section Header → **Site / Logo**
2. Site chrome label → **Site / Nav** → **Site / Footer**

**Site / Nav** (1440×60): 40px padding, 1200px inner, logo instance + links + CTA.  
**Site / Footer**: same horizontal alignment as nav.  
**Site / Logo**: master; instances in nav + footer (`mainComponent` linked).

After `combineAsVariants`: resize component set; `clipsContent = false` if clipped.

---

## Phase 3 — Capture (CLI + MCP)

```bash
make figma-capture-all
```

For each row in `config/figma-capture-manifest.json`:

1. Poll `generate_figma_design` with `captureId`, `outputMode: "existingFile"`, `fileKey`, `nodeId` = `wireframes_page_id`
2. On success: rename frame to `label`; width 1440
3. On failure: re-run `make figma-capture-one CAPTURE_ID=… PATH=…` then poll again

**Rules**

- One Playwright process per page (`figma-capture-one.mjs`) — never batch-await in one browser
- Do not unbounded-await `captureForDesign` in the browser (12s race is in the script)
- Sequential Figma MCP **writes** (`use_figma`)

---

## Phase 4 — Layout Wireframes page

- Frames in `site-map.yaml` order
- Gap `frame_gap_px` from `figma.yaml` (default 200)
- Remove empty duplicate Figma pages if capture created them

---

## Phase 5 — Chrome swap (recommended)

Per wireframe frame (`use_figma`):

1. Delete captured Navigation/Footer groups if duplicated
2. `createInstance` from **Site / Nav** / **Site / Footer** via `getNodeByIdAsync` (same file)
3. Position nav at top, footer at bottom; width 1440
4. Keep middle content from capture

---

## Phase 6 — QA

- [ ] Logo readable (HTML `<img>` + Figma **Site / Logo**)
- [ ] Nav/footer align to 1200px content
- [ ] No component overlap on `— Components —`
- [ ] Button/card variant sets not clipped
- [ ] Spot-check 2–3 wireframe frames vs `make serve`

---

## Response template

Report: figma file link, pages captured, frames laid out, components built/swapped, manifest path, port used, anything skipped or failed.
