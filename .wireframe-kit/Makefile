# Wireframe kit commands (run from repo root via top-level Makefile, or here)

KIT_ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
REPO_ROOT := $(abspath $(KIT_ROOT)/..)
DOCX ?= $(KIT_ROOT)content/source/copy.docx

PORT ?= 8765

.PHONY: help parse-copy sync link-skills validate-blocks setup-github clean-content serve serve-stop serve-status \
	figma-install-deps figma-check figma-init-manifest figma-capture-all figma-capture-one figma-list-captures

help:
	@echo ".wireframe-kit targets:"
	@echo "  make parse-copy        — docx → content/pages/*.json"
	@echo "  make sync              — sync nav + footer HTML"
	@echo "  make link-skills       — symlink skills for Cursor / Claude / OpenClaw"
	@echo "  make validate-blocks   — block classes exist in css/style.css"
	@echo "  make setup-github      — create katiebushdesign/{SLUG}-wireframes + Pages (SLUG= client name, e.g. 212-visual)"
	@echo "  make clean-content     — remove generated pages/nav JSON and source docx"
	@echo "  make serve             — local preview at http://localhost:$(PORT)/ (background)"
	@echo "  make serve-stop        — stop local preview server"
	@echo "  make figma-install-deps — npm ci + Playwright Chromium (for HTML → Figma)"
	@echo "  make figma-check         — preflight: node, playwright, preview, manifest"
	@echo "  make figma-init-manifest — site-map.yaml → config/figma-capture-manifest.json"
	@echo "  make figma-capture-all   — submit all pages to Figma capture API"
	@echo "  make figma-list-captures — print captureIds for MCP poll"

parse-copy:
	python3 $(KIT_ROOT)scripts/parse-copy-docx.py $(DOCX)

sync:
	python3 $(KIT_ROOT)scripts/sync-nav.py
	python3 $(KIT_ROOT)scripts/sync-footer.py

link-skills:
	$(KIT_ROOT)scripts/link-agent-skills.sh

validate-blocks:
	python3 $(KIT_ROOT)scripts/validate-block-classes.py

setup-github:
	@test -n "$(SLUG)" || (echo "Usage: make setup-github SLUG=clientname [NAME='Client Name'] [YES=1]" >&2; exit 1)
	$(KIT_ROOT)scripts/setup-github-repo.sh --slug "$(SLUG)" $(if $(NAME),--name "$(NAME)",) $(if $(YES),--yes,)

clean-content:
	rm -f $(KIT_ROOT)content/pages/*.json $(KIT_ROOT)content/nav/*.json
	rm -f $(KIT_ROOT)content/source/*.docx $(KIT_ROOT)content/source/*.doc
	@echo "Cleared generated content under .wireframe-kit/content/"

serve:
	PORT=$(PORT) $(KIT_ROOT)scripts/serve-local.sh start

serve-stop:
	$(KIT_ROOT)scripts/serve-local.sh stop

serve-status:
	PORT=$(PORT) $(KIT_ROOT)scripts/serve-local.sh status

figma-install-deps:
	cd $(KIT_ROOT) && npm ci && npx playwright install chromium

figma-check:
	PORT=$(PORT) WIREFRAME_BASE="$(WIREFRAME_BASE)" FIGMA_MANIFEST="$(FIGMA_MANIFEST)" $(KIT_ROOT)scripts/figma-check-deps.sh

figma-init-manifest:
	MERGE=$(MERGE) node $(KIT_ROOT)scripts/figma-init-manifest.mjs

figma-capture-all:
	PORT=$(PORT) WIREFRAME_BASE="$(WIREFRAME_BASE)" FIGMA_MANIFEST="$(FIGMA_MANIFEST)" SKIP_PATH="$(SKIP_PATH)" $(KIT_ROOT)scripts/figma-capture-all.sh

figma-capture-one:
	@test -n "$(CAPTURE_ID)" && test -n "$(PATH)" || (echo "Usage: make figma-capture-one CAPTURE_ID=<uuid> PATH=index.html" >&2; exit 1)
	PORT=$(PORT) WIREFRAME_BASE="$(WIREFRAME_BASE)" node $(KIT_ROOT)scripts/figma-capture-one.mjs "$(CAPTURE_ID)" "$(PATH)"

figma-list-captures:
	node $(KIT_ROOT)scripts/figma-poll-captures.mjs $(FIGMA_MANIFEST)
