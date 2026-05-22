# Blocks

Reusable section HTML for wireframes. **Generic IDs** — same blocks across clients; only CSS at repo root changes per brand.

## Styling contract

Every published page must include:

```html
<link rel="stylesheet" href="css/style.css">
```

(or `../css/style.css` one level down). Blocks use **only** classes defined in `css/style.css` — not `shared.css`.

Before deploy or after editing blocks, run from repo root:

```bash
make validate-blocks
```

Agents must **resolve** template tokens before writing HTML:

| Token | Use real classes |
|-------|------------------|
| `section-{{tone}}` | `section-white` or `section-grey` |
| `grid-{{columns}}` | `grid-3` or `grid-4` |
| `{{card_class}}` | `card` or `card-grey` |
| `{{btn_class}}` | `btn-red`, `btn-outline-white`, `btn-outline-dark`, or `btn-white` |

Never leave `{{…}}` or `<!-- repeat -->` comments in client-facing HTML.

## Site chrome (not in registry)

[`nav-shell.html`](nav-shell.html) — sticky header, mobile menu, mega menu backdrop. Not copy-doc driven.

## Registry

[`registry.json`](registry.json) — block `id`, fields, copy-doc label hints.

## Placeholders

| Syntax | Meaning |
|--------|---------|
| `{{field}}` | Replace with copy |
| `{{#if field}}…{{/if}}` | Omit block if empty |
| `<!-- repeat:cards -->` … `<!-- /repeat:cards -->` | Duplicate inner markup per list item |

Agent fills templates; no build step required. Remove HTML comments when rendering final page.

## Blocks

| ID | Use when |
|----|----------|
| `hero-landing` | Homepage hero + optional stats |
| `hero-page` | Inner page hero |
| `breadcrumb` | Below nav on inner pages |
| `section-qa` | Dark Q&A grid |
| `section-header` | Eyebrow + H2 + sub only |
| `cards-grid` | H2 (+ optional sub) + 3/4 plain or grey cards |
| `cards-grid-media` | Cards with image placeholders |
| `cards-grid-linked` | Linked tiles + optional inline CTA row |
| `inline-cta` | Catchall row inside a section |
| `topic-block` | Stacked hub section (H2, sub, 3 cards) |
| `feature-band` | Full-width dark feature (portal-style) |
| `tiers` | Tier/pricing cards |
| `prose-band` | Dark centered statement |
| `split-content` | Two columns (form + sidebar) |
| `cta-band` | Pre-footer CTA strip |

## Page recipes (212 Visual examples)

| Page type | Typical stack |
|-----------|----------------|
| Homepage | `hero-landing` → `section-qa` → `cards-grid-linked` → `cards-grid` → `section-header` + `cards-grid` → `feature-band` → `cards-grid` → `cta-band` |
| Solution detail | `breadcrumb` → `hero-page` → `cards-grid-media` → `cards-grid` × n → `cta-band` |
| Audience detail | `breadcrumb` → `hero-page` → `cards-grid` (grey, 4) → `cta-band` |
| Partner program | `breadcrumb` → `hero-page` → `cards-grid` (grey, 6) → `tiers` → `prose-band` → `cta-band` |
| Contact | `breadcrumb` → `hero-page` → `split-content` → `cta-band` |
| Verticals hub | `breadcrumb` → `hero-page` → `topic-block` × n → `cta-band` |

## Shell (not blocks)

Nav (`sync-nav.py`), site footer (`sync-footer.py`), `js/marker.js`, mega menu script — live at repo root.
