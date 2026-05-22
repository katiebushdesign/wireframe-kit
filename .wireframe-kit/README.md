# Wireframe kit

Everything for **copy doc → HTML wireframe → deploy** lives in this directory. The rest of the repo is the client site (HTML, CSS, assets).

## Layout

```
.wireframe-kit/
  AI-INSTRUCTIONS.md    ← agents: canonical procedures
  README.md             ← you are here
  workflow.md  assembling-pages.md  github-setup.md  copy-doc-format.md  copy-doc-access.md  block-mapping.md  notes-and-cues.md
  agent-integrations.md
  config/               client.yaml, site-map.yaml
  skills/               create-wireframe, wireframe-from-copy-doc, wireframe-html-blocks
  scripts/              parse-copy-docx, setup-github-repo, sync-nav, sync-footer, link-agent-skills
  blocks/               section HTML templates (placeholders)
  content/              parser output (pages/*.json, nav/, source/*.docx)
  Makefile
```

## Repo root (minimal)

| File | Purpose |
|------|---------|
| `AGENTS.md` | Pointer for Cursor / generic agents |
| `CLAUDE.md` | Pointer for Claude Code |
| `.github/copilot-instructions.md` | Pointer for Copilot |
| `Makefile` | Delegates to `.wireframe-kit/Makefile` |
| `.cursor/skills` etc. | Symlinks → `.wireframe-kit/skills` |

## Commands (from repo root)

```bash
make link-skills   # once after clone
make parse-copy    # docx → .wireframe-kit/content/pages/
make sync          # nav + footer across site HTML
```

## New client

**Humans:** see [repo root README](../README.md) — one prompt with the kit repo URL, client name, and copy doc link.

**Agents:** load `/create-wireframe` — intake, then config → parse → build → `make validate-blocks` → `make serve`.

Legacy manual bootstrap (without the full repo): copy `.wireframe-kit/` + root stubs (`AGENTS.md`, `Makefile`, …), `make link-skills`, fill `config/`, add HTML at repo root.

## Agents

Read **`AI-INSTRUCTIONS.md`** first. Tool-specific discovery: [agent-integrations.md](./agent-integrations.md).
