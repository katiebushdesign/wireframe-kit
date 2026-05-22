# Parsed page JSON shape (from parse-copy-docx.py)

Best-effort export — table layouts vary. Agents apply judgment for notes, heading-only rows, and `multi_column` rows ([copy-doc-format.md](../../copy-doc-format.md)).

## Page file: `content/pages/solutions-high-impact.json`

```json
{
  "title": "SOLUTIONS: High Impact Installations",
  "slug": "solutions/high-impact",
  "path": "solutions/high-impact.html",
  "sections": [
    {
      "label": "Hero",
      "label_notes": [],
      "meta_row": false,
      "heading": "LED projects that define the space they live in",
      "paragraphs": [],
      "items": [],
      "ctas": []
    },
    {
      "label": "Note, do not fold this into the hero",
      "meta_row": true,
      "instruction": "do not fold into hero",
      "paragraphs": ["Some installations call for more than..."],
      "ctas": [{ "label": "Talk to our team →", "href": "../company/contact.html" }]
    },
    {
      "label": "What we build",
      "heading_only": false,
      "heading": "Every environment, every form factor.",
      "items": [
        { "title": "Curved and architectural LED", "body": "Curved, wrapped..." }
      ],
      "content_notes": ["these should be photos, not just boxes with copy"]
    },
    {
      "label": "**Corporate**",
      "heading": "LED for the environments that represent the business.",
      "sub": "Boardrooms, conference rooms…",
      "items": [
        { "title": "Conferencing system integration", "body": "LED systems specified…" },
        { "title": "Content for the corporate audience", "body": "Brand-led motion design…" },
        { "title": "Quiet, continuous operation", "body": "Hardware engineered…" }
      ],
      "paragraphs": []
    }
  ]
}
```

## Vertical hub row (`topic-block`)

After `make parse-copy`, rows with **CONSIDERATIONS** in the doc have `heading`, `sub`, and `items` — not card copy in `paragraphs`.

| JSON field | Block field |
|------------|-------------|
| `heading` | `{{heading}}` in `sec-h2` only |
| `sub` | `{{sub}}` in `sec-sub` only |
| `items[]` | `<!-- repeat:cards -->` only |

Never copy `heading` / `sub` into the first card. See [assembling-pages.md](../../assembling-pages.md).

**Parenthetical notes:** Parser moves `(…)` layout/team lines into `content_notes` and clears `sub` / `paragraphs`. Do not reintroduce them in HTML (e.g. a `sec-sub` that only restates “scrollable cards”).

## Section list item (from docx bullet + bold)

```json
{ "title": "Define the vision", "body": "212Visual works with the lead firm..." }
```

## CTA (from hyperlink in cell)

```json
{ "label": "Start a conversation →", "href": "../become-a-partner.html" }
```

## Multi-column row (layout or extra cells)

```json
{
  "label": "Hero",
  "multi_column": true,
  "cell_texts": ["Hero", "Headline copy…", "Sidebar note…"],
  "heading": "…",
  "paragraphs": []
}
```

Decide whether `cell_texts` are wireframe columns or label + body before mapping to a block.

## Heading-only row

```json
{
  "label": "What we build",
  "heading_only": true,
  "paragraphs": [],
  "items": []
}
```

Attach label/heading to the **next** section when assembling HTML.

## Nav: `content/nav/mega-menus.json`

Mega menu tables only — structure varies; used for manual or future nav sync. Do not merge into page body JSON.
