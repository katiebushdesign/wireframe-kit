# Copy doc format (Google Docs)

Canonical example: link in `.wireframe-kit/config/client.yaml`.

## Document structure

1. **Optional preamble** — project title, mega menu section (plain text or tables).
2. **Mega menu tables** — multi-column grids; row 0 = `SOLUTIONS MEGA MENU`, etc.
3. **Page tables** — **one table per wireframe page** (this rule stays strict).

### Multiple tabs in one Google Doc

Some copy docs use **multiple document tabs** (e.g. “Wireframes”, “Archive”, “Nav only”). Only **one tab** is the source of truth for a given run.

| Situation | Agent behavior |
|-----------|----------------|
| User or `copy_doc_tab` in `client.yaml` names the tab | Use that tab only |
| One tab clearly holds all page tables for this project | Proceed |
| Several tabs could be wireframe copy and you were **not** told which | **Stop and ask** which tab to use — do not merge tabs or guess |
| Tab looks like notes/archive only | Ignore unless the user says otherwise |

When asking, list the **tab names** you can see and ask which to parse/export.

## Page tables (flexible layout)

Writers do not need a rigid two-column grid. Tables vary: merged title rows, one cell per row, two columns (label + copy), or **extra columns that represent wireframe layout** (e.g. left column / right column on the page) rather than “section name / body.”

| Constant | Meaning |
|----------|---------|
| **One table = one page** | Page name in the top row (often merged across cells). Must match a title in `site-map.yaml`. |
| **One row ≈ one section** | Usually. Sometimes a row is **only a section heading** (next row holds the copy). Sometimes a row is **only a team note**. Use judgment when building HTML. |
| **Publishable copy vs notes** | Notes are not body copy. See [notes-and-cues.md](./notes-and-cues.md). |

### Typical patterns (not requirements)

| Pattern | How to read it |
|---------|----------------|
| Label + content (2 cells) | First cell = section intent (`Hero`, `What we build`); rest = copy, lists, CTAs. |
| Single cell | May be a **section title row**, **full section in one cell**, or a **standalone note**. |
| 3+ cells | May be **layout columns** on the wireframe; do not assume “column A / column B” semantics. Parser keeps per-cell text in JSON for the agent. |
| Split hero | Headline in one row, lead + CTAs in the next (with or without a note row between). Agent merges into one `page-hero` unless a note says otherwise. |

### Section labels and team cues

Section intent often appears in the **first cell** of a row (when present): `Hero`, `What we build`, `Key Questions`, `CTA Band`.

Team cues may appear in any cell or on their own row. Common signals (not exhaustive):

- `Note`, `Note to team:`, `Note to KBD team:`
- `(note to team, …)`
- `Kill eyebrow`, `KBD team: …`

Parser and agent treat these as **meta**, not published copy. When phrasing is ambiguous, **prefer not publishing** the line and flag it in the build summary.

### Content shape (wherever the copy lives)

- **Hero**: often headline first; body/CTAs may be on the **next row**.
- **Section heading**: a row that is only a heading, or the first paragraph before a list.
- **Repeatables**: Google Docs **bulleted lists** — card count = bullet count (do not label Card 1, Card 2).
- **Card title + body**: **bold** title, normal description (parser splits on bold runs).
- **CTAs**: short line with **hyperlink**; often ends with `→` or `»`.

### Vertical hub row (`topic-block`) — CONSIDERATIONS

Used on long-scroll verticals pages (Corporate, Hospitality, etc.). Cell content often follows:

1. **Section H2** (bold line)
2. **Intro paragraph**
3. **`CONSIDERATIONS`** (label only — not published)
4. Lines: **`Card title** card body`

Parser splits into JSON: `heading`, `sub`, `items[]` when `CONSIDERATIONS` is detected.

Agents: map to `topic-block` only. **Never** put `heading` / `sub` inside the card grid.

## Mega menu tables

Not page body. Export to `.wireframe-kit/content/nav/mega-menus.json` for `make sync` / manual nav update.

Structure: header row + grid of columns; cells contain title+description (often concatenated in export — parser uses cell boundaries).

## Export requirements

| Format | Use |
|--------|-----|
| **`.docx`** | **Required** for automation — preserves tables, `w:numPr` lists, bold, links |
| `.txt` | Human read only; **do not** use for parsing |
| PDF | Not supported |

**Restricted doc?** Agents must not guess copy — see [copy-doc-access.md](./copy-doc-access.md) (share, OAuth, or manual download).

## Writer guidelines (paste into doc intro)

1. One **table per page**; page name in the top row.
2. Each **section** is usually one table row (extra rows OK for headings-only or notes).
3. Put **features/steps/cards** as a **bullet list** (bold the card title).
4. Put **buttons** on their own line as a **link** (e.g. `Become a partner →`).
5. Mark **internal team notes** clearly (`Note:`, `Note to team:`) — we won’t publish them.
6. Don’t worry about exact column count; we map sections to the wireframe with judgment.

## Agent judgment (after `make parse-copy`)

JSON is a **best-effort structural export**, not a perfect page model. When building HTML:

- Distinguish **notes** from **copy** using cues in [notes-and-cues.md](./notes-and-cues.md) and context (adjacent rows, italics, tone).
- Treat **heading-only rows** as belonging to the following section unless a note says otherwise.
- For `multi_column` sections, decide whether cells are layout columns or label+body before choosing a block.
