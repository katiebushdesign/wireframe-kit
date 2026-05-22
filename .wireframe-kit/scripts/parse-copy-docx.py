#!/usr/bin/env python3
"""Parse KBD copy doc .docx export into content/pages/*.json and content/nav/."""
from __future__ import annotations

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = KIT_ROOT.parent
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
NOTE_RE = re.compile(
    r"^\s*("
    r"note\b|note\s*:|note\s+to\b|note\s+to\s+team\b|"
    r"\(note\b|kill\b|kbd\s+team\b|team:\s|"
    r"do\s+not\s+fold\b|net\s+new\b"
    r")",
    re.I,
)
HEADING_ONLY_MAX = 120
MEGA_RE = re.compile(r"MEGA\s*MENU", re.I)
CONSIDERATIONS_SPLIT = re.compile(r"\*\*CONSIDERATIONS\*\*|\bCONSIDERATIONS\b", re.I)
WHOLE_PAREN_RE = re.compile(r"^\s*\((.+)\)\s*\.?\s*$", re.S)
PAREN_SEGMENT_RE = re.compile(r"\(([^)]+)\)")
PAREN_NOTE_INSIDE_RE = re.compile(
    r"(?i)\b("
    r"note\s+to|scrollable|wireframe|layout|placeholder|kill\s|kbd\s+team|"
    r"do\s+not\s+fold|net\s+new|leads\s+—|for\s+team|designer|not\s+published|"
    r"internal|should\s+be\s+photos?|photos?\s+not|cards?\s+only|section\s+only|"
    r"carousel|slider|component|block\s+only"
    r")\b",
)


def cell_text(cell: ET.Element) -> str:
    parts: list[str] = []
    for p in cell.findall(".//w:p", NS):
        runs = []
        for r in p.findall(".//w:r", NS):
            t = "".join(x.text or "" for x in r.findall("w:t", NS))
            if not t:
                continue
            if r.find("w:rPr/w:b", NS) is not None:
                runs.append(f"**{t}**")
            else:
                runs.append(t)
        line = "".join(runs).strip()
        if line:
            parts.append(line)
    return "\n".join(parts)


def cell_paragraphs(cell: ET.Element) -> list[dict]:
    """Paragraphs and list items with optional bold title prefix."""
    out: list[dict] = []
    for p in cell.findall(".//w:p", NS):
        is_list = p.find(".//w:numPr", NS) is not None
        title_parts: list[str] = []
        body_parts: list[str] = []
        after_bold = False
        for r in p.findall(".//w:r", NS):
            t = "".join(x.text or "" for x in r.findall("w:t", NS))
            if not t:
                continue
            bold = r.find("w:rPr/w:b", NS) is not None
            if bold and not after_bold:
                title_parts.append(t)
            else:
                after_bold = True
                body_parts.append(t)
        title = "".join(title_parts).strip()
        body = "".join(body_parts).strip()
        text = (title + " " + body).strip() if title and not body else title or body
        if not text:
            continue
        if is_list and title:
            out.append({"type": "item", "title": title, "body": body})
        else:
            out.append({"type": "p", "text": text, "is_list": is_list})
    return out


def clean_title(title: str) -> str:
    return re.sub(r"\*+", "", title).strip()


def slugify(title: str) -> str:
    s = clean_title(title).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80] or "page"


def load_site_map() -> dict[str, str]:
    path = KIT_ROOT / "config" / "site-map.yaml"
    if not path.exists():
        return {}
    mapping: dict[str, str] = {}
    text = path.read_text()
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
        for entry in data.get("pages", []):
            mapping[entry["title"].lower()] = entry["path"]
        return mapping
    except ImportError:
        pass
    # Fallback: `- title: Foo` / `path: bar.html` pairs without PyYAML
    titles: list[str] = []
    for line in text.splitlines():
        m = re.match(r'\s*-\s*title:\s*(.+)$', line)
        if m:
            titles.append(m.group(1).strip().strip('"').lower())
            continue
        m = re.match(r"\s*path:\s*(.+)$", line)
        if m and titles:
            mapping[titles.pop(0)] = m.group(1).strip()
    return mapping


def match_path(title: str, site_map: dict[str, str]) -> str | None:
    key = title.strip().lower()
    if key in site_map:
        return site_map[key]
    for t, p in site_map.items():
        if key in t or t in key:
            return p
    return None


def parse_consideration_items_from_text(text: str) -> list[dict]:
    """Vertical hub rows: lines after CONSIDERATIONS → **title** body."""
    if not CONSIDERATIONS_SPLIT.search(text):
        return []
    _, tail = CONSIDERATIONS_SPLIT.split(text, maxsplit=1)
    items: list[dict] = []
    for line in tail.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"\*\*([^*]+)\*\*\s*(.+)", line)
        if not m:
            continue
        title, body = m.group(1).strip(), m.group(2).strip()
        if title.upper() in {"CONSIDERATIONS", "ANCHORED NAV", "PARTNER TIERS"}:
            continue
        items.append({"title": title, "body": body})
    return items


def parse_heading_sub_before_considerations(text: str) -> tuple[str, str, list[str]]:
    """H2 + intro paragraph before CONSIDERATIONS (not card copy)."""
    if not CONSIDERATIONS_SPLIT.search(text):
        return "", "", []
    before = CONSIDERATIONS_SPLIT.split(text, maxsplit=1)[0]
    lines = [ln.strip() for ln in before.splitlines() if ln.strip()]
    heading = ""
    sub = ""
    extra: list[str] = []
    for line in lines:
        m = re.match(r"\*\*([^*]+)\*\*\s*(.*)", line)
        if m and not heading:
            heading = m.group(1).strip()
            rest = m.group(2).strip()
            if rest:
                sub = rest
            continue
        if not heading:
            heading = re.sub(r"\*+", "", line).strip()
            continue
        if not sub and len(line) > 40:
            sub = re.sub(r"\*+", "", line).strip()
        else:
            extra.append(re.sub(r"\*+", "", line).strip())
    return heading, sub, extra


def is_note_text(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    if NOTE_RE.search(text):
        return True
    m = WHOLE_PAREN_RE.match(text)
    if m and not looks_like_publishable_paren(m.group(1).strip()):
        return True
    return False


def is_paren_note_content(inner: str) -> bool:
    inner = inner.strip()
    if not inner:
        return False
    if NOTE_RE.search(inner):
        return True
    if PAREN_NOTE_INSIDE_RE.search(inner):
        return True
    if re.search(r"[—–]", inner) and len(inner) < 160:
        return True
    if re.search(
        r"(?i)\b(scrollable|carousel|slider|grid|wireframe|placeholder)\b", inner
    ):
        return True
    return False


def looks_like_publishable_paren(inner: str) -> bool:
    """Rare in KBD copy docs: parenthetical text that stays in published copy."""
    inner = inner.strip()
    if not inner or is_paren_note_content(inner):
        return False
    if len(inner) <= 40 and re.match(
        r"^(optional|required|US|UK|CA|Inc\.?|LLC|™|®|\d{4}|[A-Z]{2,5})$",
        inner,
        re.I,
    ):
        return True
    return False


def process_text_field(text: str) -> tuple[str, list[str]]:
    """Split publishable copy from parenthetical notes."""
    stripped = text.strip()
    if not stripped:
        return "", []

    notes: list[str] = []
    m = WHOLE_PAREN_RE.match(stripped)
    if m:
        inner = m.group(1).strip()
        notes.append(stripped)
        if looks_like_publishable_paren(inner):
            return stripped, notes
        return "", notes

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        if is_paren_note_content(inner):
            notes.append(match.group(0))
            return ""
        return match.group(0)

    cleaned = PAREN_SEGMENT_RE.sub(repl, stripped)
    cleaned = re.sub(r"  +", " ", cleaned)
    cleaned = re.sub(r"\s+([,.;:])", r"\1", cleaned).strip()
    return cleaned, notes


def collect_paren_notes_from_lines(text: str) -> list[str]:
    found: list[str] = []
    for line in text.splitlines():
        _, notes = process_text_field(line.strip())
        for n in notes:
            if n not in found:
                found.append(n)
    return found


def sanitize_publishable_fields(data: dict) -> dict:
    """Remove parenthetical notes from fields agents map to HTML."""
    content_notes = list(data.get("content_notes") or [])

    for field in ("heading", "sub"):
        val = (data.get(field) or "").strip()
        if not val:
            continue
        cleaned, notes = process_text_field(val)
        content_notes.extend(n for n in notes if n not in content_notes)
        data[field] = cleaned

    paras: list[str] = []
    for p in data.get("paragraphs") or []:
        cleaned, notes = process_text_field(p)
        content_notes.extend(n for n in notes if n not in content_notes)
        if cleaned:
            paras.append(cleaned)
    data["paragraphs"] = paras

    for item in data.get("items") or []:
        if not isinstance(item, dict):
            continue
        for key in ("title", "body"):
            val = (item.get(key) or "").strip()
            if not val:
                continue
            cleaned, notes = process_text_field(val)
            content_notes.extend(n for n in notes if n not in content_notes)
            item[key] = cleaned

    content_notes.extend(
        n for n in collect_paren_notes_from_lines(data.get("raw") or "") if n not in content_notes
    )
    data["content_notes"] = content_notes
    return data


def section_has_publishable_copy(content: dict) -> bool:
    if (content.get("heading") or "").strip():
        return True
    if (content.get("sub") or "").strip():
        return True
    if content.get("paragraphs") or content.get("items"):
        return True
    return False


def is_heading_only_row(label: str, content: dict) -> bool:
    """Row that is only a section title — copy often follows on the next row."""
    if not label or is_note_text(label):
        return False
    if content.get("items") or content.get("content_notes"):
        return False
    paras = content.get("paragraphs") or []
    heading = (content.get("heading") or "").strip()
    if len(label) > HEADING_ONLY_MAX:
        return False
    if paras or heading:
        return False
    return True


def parse_section_cell(text: str, paragraphs: list[dict]) -> dict:
    items = [x for x in paragraphs if x["type"] == "item"]
    plain: list[str] = []
    for x in paragraphs:
        if x["type"] != "p" or x.get("is_list"):
            continue
        cleaned, _ = process_text_field(x["text"])
        if cleaned:
            plain.append(cleaned)
    content_notes = [
        m.group(0)
        for line in text.splitlines()
        for m in [
            re.search(
                r"(?i)(note\s*:|note\s+to\b.*?$|kill eyebrow.*?$|\(note to team[^)]*\))",
                line,
            )
        ]
        if m
    ]
    content_notes.extend(collect_paren_notes_from_lines(text))
    consideration_items = parse_consideration_items_from_text(text)
    if consideration_items:
        heading, sub, extra_paras = parse_heading_sub_before_considerations(text)
        data = {
            "heading": heading or (plain[0] if plain else ""),
            "sub": sub,
            "paragraphs": extra_paras,
            "items": consideration_items,
            "content_notes": content_notes,
            "raw": text,
        }
        return sanitize_publishable_fields(data)
    heading = plain[0] if plain else ""
    body_paras = plain[1:] if len(plain) > 1 else []
    data = {
        "heading": heading,
        "sub": "",
        "paragraphs": body_paras,
        "items": items,
        "content_notes": content_notes,
        "raw": text,
    }
    return sanitize_publishable_fields(data)


def page_title_from_row(cells: list[ET.Element]) -> str:
    """Best-effort page title from row 0 (merged or multi-cell)."""
    parts = [clean_title(cell_text(c).strip()) for c in cells]
    parts = [p for p in parts if p]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return parts[0]


def parse_section_row(cells: list[ET.Element]) -> dict | None:
    """One table row → section JSON (flexible cell count)."""
    if not cells:
        return None

    n = len(cells)
    texts = [cell_text(c).strip() for c in cells]

    if n == 1:
        label = ""
        body_text = texts[0]
        paras = cell_paragraphs(cells[0])
        if is_note_text(body_text):
            return {
                "label": "",
                "meta_row": True,
                "instruction": body_text,
                "heading": "",
                "sub": "",
                "paragraphs": [],
                "items": [],
                "content_notes": [],
                "raw": body_text,
            }
        content = parse_section_cell(body_text, paras)
        if not section_has_publishable_copy(content) and content.get("content_notes"):
            return {
                "label": "",
                "meta_row": True,
                "instruction": content["content_notes"][0],
                "heading": "",
                "sub": "",
                "paragraphs": [],
                "items": [],
                "content_notes": content["content_notes"],
                "raw": body_text,
            }
        if is_heading_only_row(body_text, content):
            return {
                "label": body_text,
                "heading_only": True,
                "meta_row": False,
                "instruction": None,
                "heading": "",
                "sub": "",
                "paragraphs": [],
                "items": [],
                "content_notes": [],
                "raw": body_text,
            }
        return {
            "label": label,
            "meta_row": False,
            "instruction": None,
            **content,
        }

    label = texts[0]
    body_cells = cells[1:]
    body_texts = texts[1:]
    joined_body = "\n\n".join(t for t in body_texts if t)
    paras: list[dict] = []
    for c in body_cells:
        paras.extend(cell_paragraphs(c))
    content = parse_section_cell(joined_body, paras)

    meta = is_note_text(label) and len(label) < 160
    if not meta and not joined_body.strip() and is_note_text(label):
        meta = True

    section: dict = {
        "label": label,
        "meta_row": meta
        and not content["items"]
        and not content.get("heading"),
        "instruction": label if meta else None,
        **content,
    }

    if n >= 3:
        section["multi_column"] = True
        section["cell_texts"] = texts

    if is_heading_only_row(label, content):
        section["heading_only"] = True

    return section


def parse_table(tbl: ET.Element, site_map: dict[str, str]) -> dict | None:
    rows = tbl.findall("w:tr", NS)
    if not rows:
        return None
    r0_cells = rows[0].findall("w:tc", NS)
    title = page_title_from_row(r0_cells)
    if not title:
        return None
    if MEGA_RE.search(title):
        return {"type": "mega_menu", "title": title, "rows": len(rows)}

    sections = []
    for row in rows[1:]:
        cells = row.findall("w:tc", NS)
        parsed = parse_section_row(cells)
        if parsed:
            sections.append(parsed)

    path = match_path(title, site_map)
    return {
        "type": "page",
        "title": title,
        "slug": slugify(title),
        "path": path,
        "sections": sections,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: parse-copy-docx.py <path-to.docx>", file=sys.stderr)
        sys.exit(1)

    docx = Path(sys.argv[1])
    if not docx.is_file():
        print(f"File not found: {docx}", file=sys.stderr)
        sys.exit(1)

    site_map = load_site_map()
    pages_dir = KIT_ROOT / "content" / "pages"
    nav_dir = KIT_ROOT / "content" / "nav"
    pages_dir.mkdir(parents=True, exist_ok=True)
    nav_dir.mkdir(parents=True, exist_ok=True)

    z = zipfile.ZipFile(docx)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(".//w:body", NS)
    if body is None:
        sys.exit("No document body")

    pages: list[dict] = []
    megas: list[dict] = []
    for tbl in body.findall("w:tbl", NS):
        parsed = parse_table(tbl, site_map)
        if not parsed:
            continue
        if parsed["type"] == "mega_menu":
            megas.append(parsed)
        else:
            pages.append(parsed)

    for page in pages:
        out = pages_dir / f"{page['slug']}.json"
        out.write_text(json.dumps(page, indent=2) + "\n")
        print(f"page: {page['title']} -> {out.relative_to(KIT_ROOT)}")

    mega_path = nav_dir / "mega-menus.json"
    mega_path.write_text(json.dumps({"menus": megas}, indent=2) + "\n")
    print(f"nav: {len(megas)} mega menu tables -> {mega_path.relative_to(KIT_ROOT)}")


if __name__ == "__main__":
    main()
