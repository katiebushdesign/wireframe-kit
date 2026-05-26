/**
 * Shared preview URL for Figma capture scripts.
 * Priority: WIREFRAME_BASE → http://localhost:${PORT|WIREFRAME_PORT|8765}
 */
export function getWireframeBase() {
  if (process.env.WIREFRAME_BASE) {
    return process.env.WIREFRAME_BASE.replace(/\/$/, '');
  }
  const port = process.env.PORT || process.env.WIREFRAME_PORT || '8765';
  return `http://localhost:${port}`;
}

export function getCaptureTimeoutMs() {
  const n = Number(process.env.TIMEOUT_MS || process.env.CAPTURE_TIMEOUT_MS || 12000);
  return Number.isFinite(n) && n > 0 ? n : 12000;
}
