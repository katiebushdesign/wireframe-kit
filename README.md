# Wireframe kit

Build client wireframe previews from a Google Docs copy doc. **You don’t clone or run commands** — your agent does.

---

## Get started

Paste this into Cursor, Claude Code, or any coding agent (swap in your client and copy doc):

```
Create a new wireframe using https://github.com/katiebushdesign/wireframe-kit for client 212 Visual using this copy doc: https://docs.google.com/document/d/YOUR_DOC_ID/edit
```

The agent sets up the project, builds the pages, and gives you a local preview link (usually http://localhost:8765/).

---

## When it’s ready for the client

Ask the agent:

```
Set up GitHub Pages for this client (slug: 212-visual) and push when I approve.
```

Preview URL: `https://katiebushdesign.github.io/212-visual-wireframes/`

---

## Export to Figma

```
/wireframe-to-figma — export this site to https://www.figma.com/design/YOUR_FILE_KEY/Client-Wireframes
```

---

## Copy updates

Edit the Google Doc, then:

```
Apply the latest copy doc to the wireframes.
```

---

## More detail

- [Copy doc access](.wireframe-kit/copy-doc-access.md) — if the agent can’t open the Google Doc, it should ask you for permissions or a `.docx` export (not search the web or your computer)
- [Copy doc format](.wireframe-kit/copy-doc-format.md)
- [Kit docs](.wireframe-kit/README.md) · [Agent instructions](.wireframe-kit/AI-INSTRUCTIONS.md) · [Figma export](.wireframe-kit/figma-html-export.md)

**Optional (terminal):** `make serve` for local preview · `make link-skills` after cloning yourself
