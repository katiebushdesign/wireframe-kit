#!/usr/bin/env bash
# Preflight for HTML → Figma capture.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$DIR/.." && pwd)"
REPO="$(cd "$KIT/.." && pwd)"
MANIFEST="${FIGMA_MANIFEST:-$KIT/config/figma-capture-manifest.json}"
LEGACY_MANIFEST="$DIR/figma-capture-manifest.json"

source_port() {
  if [[ -n "${WIREFRAME_BASE:-}" ]]; then
    echo "${WIREFRAME_BASE%/}"
    return
  fi
  local p="${PORT:-${WIREFRAME_PORT:-8765}}"
  echo "http://localhost:${p}"
}

BASE="$(source_port)"
FAIL=0

echo "== Figma capture preflight =="
echo "Preview base: $BASE"

if ! command -v node >/dev/null; then
  echo "FAIL: node not found" >&2
  FAIL=1
else
  echo "OK: node $(node -v)"
fi

if [[ ! -f "$KIT/package.json" ]]; then
  echo "WARN: $KIT/package.json missing — run from kit with npm ci"
else
  if [[ ! -d "$KIT/node_modules/playwright" ]]; then
    echo "FAIL: Playwright not installed — run: make figma-install-deps" >&2
    FAIL=1
  else
    echo "OK: playwright package present"
  fi
fi

if [[ ! -f "$MANIFEST ]]; then
  if [[ -f "$LEGACY_MANIFEST" ]]; then
    MANIFEST="$LEGACY_MANIFEST"
    echo "OK: using legacy manifest $MANIFEST"
  else
    echo "FAIL: no manifest — run: make figma-init-manifest" >&2
    FAIL=1
  fi
else
  echo "OK: manifest $MANIFEST"
fi

if ! curl -sf "${BASE}/index.html" -o /dev/null; then
  echo "FAIL: preview not reachable at ${BASE}/index.html — run: make serve" >&2
  FAIL=1
else
  echo "OK: preview reachable"
fi

if [[ -f "$KIT/config/figma.yaml" ]]; then
  echo "OK: figma.yaml present"
else
  echo "WARN: copy config/figma.yaml.example → config/figma.yaml"
fi

exit "$FAIL"
