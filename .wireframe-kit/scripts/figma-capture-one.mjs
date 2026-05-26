#!/usr/bin/env node
/**
 * Fire-and-forget single-page Figma html-to-design capture.
 * Usage: node figma-capture-one.mjs <captureId> <path>
 * Example: node figma-capture-one.mjs 839770de-... index.html
 *
 * Env: WIREFRAME_BASE, PORT / WIREFRAME_PORT (default 8765), TIMEOUT_MS
 * See: .wireframe-kit/figma-html-export.md
 */
import { chromium } from 'playwright';
import { getWireframeBase, getCaptureTimeoutMs } from './figma-env.mjs';

const captureId = process.argv[2];
const pagePath = process.argv[3];
if (!captureId || !pagePath) {
  console.error('Usage: node figma-capture-one.mjs <captureId> <path>');
  process.exit(1);
}

const BASE = getWireframeBase();
const TIMEOUT_MS = getCaptureTimeoutMs();
const url = `${BASE}/${pagePath.replace(/^\//, '')}`;
const endpoint = `https://mcp.figma.com/mcp/capture/${captureId}/submit`;
const CAPTURE_JS = 'https://mcp.figma.com/mcp/html-to-design/capture.js';
const browser = await chromium.launch({ headless: true });
const page = await browser.newContext({ viewport: { width: 1440, height: 900 } }).then((c) => c.newPage());

try {
  console.log(`URL: ${url}`);
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(1200);

  const script = await page.context().request.get(CAPTURE_JS);
  await page.evaluate((s) => {
    const el = document.createElement('script');
    el.textContent = s;
    document.head.appendChild(el);
  }, await script.text());
  await page.waitForTimeout(1500);

  const result = await page.evaluate(
    async ({ captureId, endpoint, timeoutMs }) => {
      if (!window.figma?.captureForDesign) return { ok: false, reason: 'no-api' };
      const capturePromise = Promise.resolve(
        window.figma.captureForDesign({ captureId, endpoint, selector: 'body' })
      );
      const timeoutPromise = new Promise((resolve) =>
        setTimeout(() => resolve({ timedOut: true }), timeoutMs)
      );
      const outcome = await Promise.race([capturePromise, timeoutPromise]);
      if (outcome?.timedOut) return { ok: true, fired: true, timedOut: true };
      return { ok: true, fired: true, outcome: String(outcome) };
    },
    { captureId, endpoint, timeoutMs: TIMEOUT_MS }
  );

  console.log('submit:', JSON.stringify(result));
  console.log('Poll with: generate_figma_design captureId', captureId);
} catch (err) {
  console.error('ERROR:', err.message);
  process.exit(1);
} finally {
  await browser.close();
}
