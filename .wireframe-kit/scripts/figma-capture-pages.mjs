#!/usr/bin/env node
/**
 * @deprecated Use figma-capture-one.mjs + figma-capture-all.sh instead.
 * This script awaits every capture in one browser session and often hangs.
 *
 * Capture local wireframe pages into Figma via html-to-design.
 * Usage: node figma-capture-pages.mjs <manifest.json>
 */
import { readFileSync } from 'fs';
import { chromium } from 'playwright';
import { getWireframeBase } from './figma-env.mjs';

const manifestPath = process.argv[2];
if (!manifestPath) {
  console.error('Usage: node figma-capture-pages.mjs <manifest.json>');
  process.exit(1);
}

const items = JSON.parse(readFileSync(manifestPath, 'utf8'));
const CAPTURE_JS = 'https://mcp.figma.com/mcp/html-to-design/capture.js';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();

const BASE = getWireframeBase();

for (const item of items) {
  const endpoint = `https://mcp.figma.com/mcp/capture/${item.captureId}/submit`;
  const url = item.url || `${BASE}/${item.path}`;
  console.log(`\n→ ${item.label}`);
  console.log(`  ${url}`);
  try {
    await page.goto(url, { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(1200);
    const script = await page.context().request.get(CAPTURE_JS);
    await page.evaluate((s) => {
      const el = document.createElement('script');
      el.textContent = s;
      document.head.appendChild(el);
    }, await script.text());
    await page.waitForTimeout(1500);
    const result = await page.evaluate(
      async ({ captureId, endpoint }) => {
        if (!window.figma?.captureForDesign) return 'no-api';
        const p = window.figma.captureForDesign({ captureId, endpoint, selector: 'body' });
        return p && typeof p.then === 'function' ? await p : p;
      },
      { captureId: item.captureId, endpoint }
    );
    console.log('  capture:', result ?? 'submitted');
    await page.waitForTimeout(5000);
  } catch (err) {
    console.error('  ERROR:', err.message);
  }
}

await browser.close();
console.log('\nDone. Poll each captureId with generate_figma_design.');
