#!/usr/bin/env node
/**
 * List captureIds from manifest (for Figma MCP generate_figma_design polling).
 * Usage: node figma-poll-captures.mjs [manifest.json]
 */
import { readFileSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const kitRoot = join(__dir, '..');
const defaultManifest = join(kitRoot, 'config/figma-capture-manifest.json');
const legacyManifest = join(__dir, 'figma-capture-manifest.json');

let manifestPath = process.argv[2];
if (!manifestPath) {
  manifestPath = existsSync(defaultManifest) ? defaultManifest : legacyManifest;
}

const items = JSON.parse(readFileSync(manifestPath, 'utf8'));
for (const i of items) {
  console.log([i.captureId, i.path, i.label].join('\t'));
}
