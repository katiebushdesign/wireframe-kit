---
name: create-wireframe
description: >-
  Onboard and run a full wireframe project from scratch. Use when the user asks
  to create wireframes, start a new wireframe preview, onboard a client, set up
  the kit, or says onboard / create-wireframe. Walk through required inputs first,
  then configure, parse copy, build HTML, and validate.
disable-model-invocation: false
---

# Create wireframe (onboard + execute)

**Canonical procedures:** [`.wireframe-kit/AI-INSTRUCTIONS.md`](../AI-INSTRUCTIONS.md)

**Delegate detail to:** `/wireframe-from-copy-doc`, `/wireframe-html-blocks`

Do not commit unless the user asks.

---

## Phase 0 — Intake (do this first)

Ask the user for anything missing. Use structured questions when the tool is available; otherwise ask in one short message.

| # | Question | Why |
|---|----------|-----|
| 1 | **Client / project name** | `config/client.yaml` |
| 2 | **Copy doc URL** (Google Doc) or **no copy doc yet** | Source of truth; can skip parse until doc exists |
| 2b | **Which doc tab?** (if the file has multiple tabs) | Set `copy_doc_tab` in `client.yaml` or answer when agent asks — do not guess |
| 3 | **Greenfield or revision?** | Greenfield = assemble from `blocks/`; revision = patch existing repo-root HTML |
| 4 | **Pages to build** (titles + URL paths) or **derive from doc after export** | `config/site-map.yaml` |
| 5 | **Client name** for repo (e.g. `212-visual`, `acme-health`) | Repo: `katiebushdesign/{clientname}-wireframes` |
| 6 | **New GitHub repo?** or existing `origin` | Run [github-setup.md](../github-setup.md) vs verify Pages only |
| 7 | **`.docx` ready?** Path under `.wireframe-kit/content/source/` or wait for export | `make parse-copy` needs docx, not txt |
| 8 | **Nav/footer** — single demo page or full site shell? | `make sync` only when multi-page nav exists in `index.html` |

Derive **preview URL** (do not ask separately unless overriding):

`https://katiebushdesign.github.io/{clientname}-wireframes/`

**Stop and confirm** plan: `config` → `github` (if new) → `parse` → `build` → `validate` → `make serve` → `push`.

Do not `git push` or create the GitHub repo until the user approves.

---

## Phase 1 — Kit setup

From **repo root**:

```bash
make link-skills
```

1. Copy `.wireframe-kit/config/client.yaml.example` → `client.yaml` if missing; fill `client_name`, `github_org`, `github_repo`, `preview_base_url`, `copy_doc_url`, `copy_docx_path`.
2. Set `github_repo` to `{clientname}-wireframes` and `preview_base_url` to the KBD Pages URL above.
3. Edit `.wireframe-kit/config/site-map.yaml` — map each copy-doc **table title** (row 0) → repo-root HTML `path`.
4. Read [copy-doc-format.md](../copy-doc-format.md) and [notes-and-cues.md](../notes-and-cues.md) if the user has a copy doc.

---

## Phase 1b — GitHub repository + Pages

**Standard:** org `katiebushdesign`, repo `{clientname}-wireframes`, Pages from `main` at `/`.

Full reference: [github-setup.md](../github-setup.md)

**Greenfield (no remote yet):**

1. Ensure local work is committed on `main` (ask before `git commit`).
2. Dry-run, then run (user approved):

```bash
.wireframe-kit/scripts/setup-github-repo.sh --slug <slug> --name "<Client Name>" --dry-run
.wireframe-kit/scripts/setup-github-repo.sh --slug <slug> --name "<Client Name>" --yes
# or: make setup-github SLUG=<slug> NAME="<Client Name>" YES=1
```

Creates the public repo, sets `origin`, pushes `main`, enables GitHub Pages, patches `client.yaml`.

**Existing repo:** If `origin` is already `katiebushdesign/{clientname}-wireframes`, skip create; verify Pages (`gh api repos/katiebushdesign/<repo>/pages`) and align `client.yaml`.

**After HTML changes:** push again (`git push origin main`). Pages rebuild in 1–3 minutes.

Requires `gh` CLI authenticated for `katiebushdesign`.

---

## Phase 2 — Copy → JSON (if docx exists)

**Before parse:** If `copy_doc_url` is unreachable (permissions / sign-in), **stop** — do not web-search or search the user’s machine. Follow [copy-doc-access.md](../copy-doc-access.md) and ask for share, link access, OAuth, or manual `.docx` at `copy_docx_path`. If the doc has **multiple tabs** and `copy_doc_tab` is unset, **ask which tab** before exporting/parsing.

```bash
make parse-copy
# or: python3 .wireframe-kit/scripts/parse-copy-docx.py .wireframe-kit/content/source/<file>.docx
```

Inspect `.wireframe-kit/content/pages/*.json`. Fix `site-map.yaml` if any table titles fail to map.

If **no copy doc yet**: skip to Phase 3 with placeholder copy or block shells only; remind user to re-run parse when docx is ready.

---

## Phase 3 — Build HTML

Follow **AI-INSTRUCTIONS.md** tasks:

| Mode | Action |
|------|--------|
| **Greenfield** | For each page in `site-map.yaml`: shell ([`nav-shell.html`](../blocks/nav-shell.html) + `js/nav.js` → breadcrumb → sections → `cta-band` → footer), fill from `blocks/*.html` + parsed JSON |
| **Revision** | Patch existing repo-root HTML; same block mapping |

Rules:

- Assemble from [assembling-pages.md](../assembling-pages.md) — **no** new `build-pages.py` at repo root.
- Map sections via [block-mapping.md](../block-mapping.md) and [registry.json](../blocks/registry.json).
- **`topic-block`:** use JSON `heading`, `sub`, `items` only — never duplicate heading/sub in cards.
- Resolve all `{{placeholders}}` to real classes in `css/style.css`.
- Strip team notes per [notes-and-cues.md](../notes-and-cues.md).
- Use `../` for assets one level below repo root.

```bash
make sync          # only if nav/footer IA changed and shell supports it
make validate-blocks
make serve         # start local preview (background, default http://localhost:8765/)
```

**Always run `make serve` at the end of onboard** (after HTML exists — starter `index.html` is enough). Report the printed local URL to the user. Use `PORT=8080 make serve` if 8765 is taken. Stop with `make serve-stop`.

---

## Phase 4 — Handoff

Report to the user:

- Pages created/updated (paths)
- Section → block map per page
- Scripts run (`parse-copy`, `sync`, `validate-blocks`, `serve`)
- **Local preview URL** from `make serve` (e.g. `http://localhost:8765/index.html`)
- Copy doc / site-map gaps or notes you could not auto-apply
- GitHub repo URL and Pages preview (`preview_base_url` + paths)
- Whether initial push / Pages setup ran
- Reminder: export doc as **.docx** when copy changes; re-run `make parse-copy`

---

## If blocked

| Blocker | Next step |
|---------|-----------|
| No `site-map` match for a table title | Add row to `site-map.yaml` or rename doc table |
| Missing block layout | Add `blocks/<id>.html` + registry entry; do not invent DOM in page HTML |
| Class validation fails | Add classes to `css/style.css` or fix placeholders |
| `make sync` fails | Starter may only have minimal `index.html` — build nav in shell first or skip sync |
| No commits yet | Commit locally before `setup-github-repo.sh` |
| `gh` auth / org permission | User runs `gh auth login`; needs create-repo on `katiebushdesign` |
| Repo name taken | Pick a different slug or use existing repo + verify Pages |
| Copy doc 403 / no access | [copy-doc-access.md](../copy-doc-access.md) — share doc, link viewer, OAuth, or manual `.docx`; **never** web-search or `~/` file hunt |
| Multiple doc tabs, unclear which | Ask user; set `copy_doc_tab` — do not merge tabs or pick one silently |
