#!/usr/bin/env python3
"""Sync site nav from index.html to all pages (desktop + mobile + mega backdrop)."""
from pathlib import Path
import re

KIT_ROOT = Path(__file__).resolve().parent.parent
root = KIT_ROOT.parent  # repo root (HTML pages)
index = (root / "index.html").read_text()
nav_pattern = re.compile(
    r"(?:<!-- NAV[^\n]*\n)?"
    r"<nav class=\"navbar\">.*?</nav>\n"
    r"<div class=\"nav-mobile\" id=\"nav-mobile\">.*?</div>\n"
    r"<div class=\"mega-backdrop\" id=\"mega-backdrop\"></div>",
    re.DOTALL,
)

m = nav_pattern.search(index)
if not m:
    raise SystemExit(
        "nav block not found in index.html "
        "(expected navbar + nav-mobile + mega-backdrop; see blocks/nav-shell.html)"
    )
nav_root = m.group(0)
nav_sub = re.sub(r'href="', 'href="../', nav_root)

ROOT_FILES = {"index.html", "become-a-partner.html"}
SKIP = {"nav.html", "footer.html"}

updated = []
skipped = []
for path in sorted(root.rglob("*.html")):
    if ".wireframe-kit" in path.parts or path.name in SKIP:
        continue
    text = path.read_text()
    if 'class="navbar"' not in text:
        continue
    rel = path.relative_to(root).as_posix()
    use_sub = "/" in rel and rel not in ROOT_FILES
    new_nav = nav_sub if use_sub else nav_root
    new_text, n = nav_pattern.subn(new_nav, text, count=1)
    if n == 0:
        skipped.append(rel)
        continue
    if new_text != text:
        path.write_text(new_text)
        updated.append(rel)

print(f"Updated {len(updated)} files")
for f in updated:
    print(f"  {f}")
if skipped:
    print(f"Skipped {len(skipped)}:", ", ".join(skipped))

(root / "nav.html").write_text(
    "<!-- SHARED NAV - subpages (one level deep) -->\n" + nav_sub + "\n"
)
print("nav.html template updated")
