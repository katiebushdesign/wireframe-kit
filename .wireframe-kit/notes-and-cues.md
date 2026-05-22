# Team notes and agent cues

Notes in the copy doc are **first-class**. They are not published HTML; they steer the agent.

There is **no fixed column layout** in every doc. Use **best-effort judgment** to separate notes from publishable copy — the parser helps but does not replace reading the row in context.

## Recognizing notes (heuristics, not exhaustive)

Treat a line or row as a **note / instruction** when it matches patterns like:

| Signal | Examples |
|--------|----------|
| Starts with note language | `Note`, `Note:`, `Note to team:`, `Note to KBD team:` |
| **Whole line in parentheses** | `(Success stories leads — scrollable cards.)` | **Note** — do not put in `sec-sub`, cards, or body |
| Parenthetical team cue | `(note to team, kill eyebrow)` |
| Parenthetical layout / UI | `(scrollable cards)`, `(photos not boxes)` |
| KBD / team prefix | `KBD team:`, `Team:` (when clearly editorial, not a nav label) |
| Kill / remove editorial | `Kill eyebrow`, `kill the pills` |
| Structural instruction | `Do not fold into hero`, `net new`, `replaces content samples` |
| Whole row is meta | Short row with no list bullets and no CTA links, only instruction text |

**Not notes:** section labels (`Hero`, `What we build`), industry names on verticals hubs, mega menu labels, normal marketing copy even if informal.

When unsure: **do not publish** the text; mention it in the build summary.

## Parentheses — note vs published copy

In KBD copy docs, **text wrapped in parentheses is usually a team or layout note**, not visitor-facing copy.

| Pattern | Usually | Agent / parser |
|---------|--------|----------------|
| Entire line/cell is `(…)` | Note | Strip; store in `content_notes`; never render in HTML |
| `(note to team, …)` inline | Note | Strip segment |
| `(scrollable cards)`, `leads —`, wireframe/layout words inside `()` | Note | Strip |
| `(optional)`, `(US)`, `(2024)`, short legal/product clarifier | Copy | May keep when clearly supplemental |

**Example (do not publish):** Section H2 = `Real Impact, Real Results` and sub = `(Success stories leads — scrollable cards.)` → only the H2 is copy; the parenthetical is a build cue for cards below.

After `make parse-copy`, check JSON: `sub` / `paragraphs` should be empty when the doc only had a parenthetical note. If you are patching HTML by hand, remove any `sec-sub` that matches a stripped `content_notes` entry.

## Note locations

| Where | Example | Handling |
|-------|---------|----------|
| First cell / label position | `Hero` + `Kill eyebrow` jammed together | Normalize label to `Hero`; strip cue from label; record note |
| Whole row (any cell count) | `Note, do not fold this into the hero…` | Meta row: apply to **previous** or **next** section |
| Inline in copy | `(note to team, kill eyebrow)` | Strip from HTML; keep in build log |
| Whole line in parentheses | `(Success stories leads — scrollable cards.)` | Strip; use for block choice only (e.g. scrollable card row) |
| Own paragraph in body | `Note to KBD team: this section is net new` | Strip; may trigger **greenfield section** or **replace** |

## Heading-only rows

Sometimes a row is **only** a section title (e.g. `What we build`) and the next row holds bullets or prose.

- Attach the heading to the **following** section’s block (`sec-h2` / `sec-eyebrow`) unless a note says otherwise.
- Do not render an empty section for the heading row alone.

## Multi-column rows (layout vs label)

Three or more cells may mean **wireframe columns** (left/right content), not “label | body.”

- Read all cell texts in `section.cell_texts` (when present).
- If cells read as parallel content columns → pick `split-content`, side-by-side blocks, or custom layout — do not flatten into one prose block without intent.
- If the first cell is clearly a section name and the rest are one narrative → treat like classic label + body.

## Note types

### Structural

- “Do not fold into hero” → two rows become one `page-hero` **or** hero + following `section-prose` — follow literal instruction.
- “New section” / “net new” / “replaces content samples” → don’t assume old HTML; build or replace block.
- “4 cards” / “photos not boxes” → pick block variant + wireframe placeholders; optional comment in HTML.

### Editorial (revision)

- “Kill eyebrow” / “kill the pills” → remove `.hero-tag`, pills, eyebrow elements on that page.
- “combining team & careers” → IA change; update nav + `site-map.yaml`, not copy only.

### Nav / IA

- “Remove this from the mega menu” → update nav config, not page body.
- Mega menu tables → always nav pipeline.

### Design (wireframe stage)

- “should be photos” → keep `img-placeholder` or similar; don’t swap in stock images unless asked.
- “Pair with large image” → use block variant with media column.

## Greenfield vs revision

Same note text can mean different things:

| Note | Greenfield (new page) | Revision (existing HTML) |
|------|------------------------|---------------------------|
| `Kill eyebrow` | Never add eyebrow | Remove eyebrow from DOM |
| `net new` | Add section from blocks | Replace or insert section; flag if block missing |
| `note to team, this is the headline` | Use body text as `h2`, no eyebrow | Change heading level/class; remove eyebrow |
| `do not fold into hero` | Merge rows when assembling | Split/merge DOM to match |

When unsure, prefer **literal reading of the note** over guessing from old HTML.

## Agent output

After a copy pass, briefly list:

- Sections updated
- Notes applied (stripped)
- Ambiguous notes or rows flagged for human review

Optional: write stripped notes to `.wireframe-kit/content/notes/<slug>.md` for audit trail.
