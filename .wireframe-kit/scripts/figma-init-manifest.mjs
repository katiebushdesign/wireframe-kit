#!/usr/bin/env node
/**
 * Build figma-capture-manifest.json from site-map.yaml.
 * Usage: node figma-init-manifest.mjs [site-map.yaml] [output.json]
 * Env: MERGE=1 — keep existing captureIds for matching paths
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { randomUUID } from 'crypto';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const kitRoot = join(__dir, '..');
const siteMapPath = process.argv[2] || join(kitRoot, 'config/site-map.yaml');
const outPath =
  process.argv[3] || join(kitRoot, 'config/figma-capture-manifest.json');
const merge = process.env.MERGE === '1' || process.env.MERGE === 'true';

function parseSiteMap(yaml) {
  const pages = [];
  const re = /-\s*title:\s*(.+)\n\s*path:\s*(.+)/g;
  let m;
  while ((m = re.exec(yaml))) {
    pages.push({ label: m[1].trim(), path: m[2].trim() });
  }
  if (!pages.length) {
    throw new Error(`No pages found in ${siteMapPath} (expected "  - title:" / "    path:")`);
  }
  return pages;
}

function loadExisting(path) {
  if (!existsSync(path)) return [];
  return JSON.parse(readFileSync(path, 'utf8'));
}

const yaml = readFileSync(siteMapPath, 'utf8');
const pages = parseSiteMap(yaml);
const existing = merge ? loadExisting(outPath) : [];
const byPath = new Map(existing.map((e) => [e.path, e]));

const manifest = pages.map(({ label, path }) => {
  const prev = byPath.get(path);
  return {
    label,
    path,
    captureId: prev?.captureId || randomUUID(),
  };
});

writeFileSync(outPath, JSON.stringify(manifest, null, 2) + '\n');
console.log(`Wrote ${manifest.length} entries → ${outPath}`);
if (merge) {
  const added = manifest.filter((e) => !byPath.has(e.path)).length;
  const kept = manifest.length - added;
  console.log(`MERGE: ${kept} kept, ${added} new`);
}
