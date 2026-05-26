#!/usr/bin/env bash
# Capture all pages from manifest (one process per page, fire-and-forget).
# See: .wireframe-kit/figma-html-export.md
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$DIR/.." && pwd)"
DEFAULT_MANIFEST="$KIT/config/figma-capture-manifest.json"
LEGACY_MANIFEST="$DIR/figma-capture-manifest.json"
MANIFEST="${1:-${FIGMA_MANIFEST:-}}"
if [[ -z "$MANIFEST" ]]; then
  if [[ -f "$DEFAULT_MANIFEST" ]]; then
    MANIFEST="$DEFAULT_MANIFEST"
  else
    MANIFEST="$LEGACY_MANIFEST"
  fi
fi
MANIFEST="$(cd "$(dirname "$MANIFEST")" && pwd)/$(basename "$MANIFEST")"

if [[ -n "${WIREFRAME_BASE:-}" ]]; then
  BASE="${WIREFRAME_BASE%/}"
else
  P="${PORT:-${WIREFRAME_PORT:-8765}}"
  BASE="http://localhost:${P}"
fi

if ! curl -sf "$BASE/index.html" -o /dev/null; then
  echo "Preview not reachable at $BASE — start with: make serve (or PORT=8890 make serve)" >&2
  exit 1
fi

SKIP_PATH="${SKIP_PATH:-}"
node -e "
const items = require(process.argv[1]);
const skip = (process.env.SKIP_PATH || '').split(',').filter(Boolean);
for (const i of items) {
  if (skip.includes(i.path)) continue;
  console.log([i.captureId, i.path, i.label].join('\t'));
}
" "$MANIFEST" | while IFS=$'\t' read -r captureId path label; do
  echo ""
  echo "=== $label ==="
  node "$DIR/figma-capture-one.mjs" "$captureId" "$path" || echo "WARN: capture command failed for $label"
  sleep 3
done

echo ""
echo "All submits fired. Poll captureIds via Figma MCP generate_figma_design."
