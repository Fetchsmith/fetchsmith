// Integration test: runs the SHIPPED countDiffRegions (extracted from src/main.js, not a copy)
// against REAL pixelmatch output, and reproduces the two scenarios the dev.to reader described.
import fs from 'fs';
import pngjs from './node_modules/pngjs/lib/png.js';
import pixelmatch from './node_modules/pixelmatch/index.js';
const { PNG } = pngjs;

const src = fs.readFileSync('./src/main.js', 'utf8');
const start = src.indexOf('function countDiffRegions');
const end = src.indexOf('\n}', src.indexOf('return { regions,', start)) + 2;
const cap = src.match(/const REGION_PIXEL_CAP = ([\d_]+)/)[1].replace(/_/g, '');
const fn = new Function('REGION_PIXEL_CAP', `${src.slice(start, end)}; return countDiffRegions;`)(Number(cap));
console.log(`extracted countDiffRegions from src/main.js (${end - start} chars), REGION_PIXEL_CAP=${cap}\n`);

const W = 1200, H = 800;
// A page-like baseline: white background, a dark header bar, and grey "text" rows with a
// horizontal gradient so there are genuine intermediate/antialiased tones for pixelmatch to chew on.
function baseline() {
  const png = new PNG({ width: W, height: H });
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const p = (y * W + x) * 4;
      let v = 255;
      if (y < 60) v = 32;
      else if (y % 24 < 10 && x > 40 && x < 1100) v = 90 + ((x * 37) % 120);
      png.data[p] = png.data[p + 1] = png.data[p + 2] = v;
      png.data[p + 3] = 255;
    }
  }
  return png;
}

function mutate(png, fn2) {
  const out = new PNG({ width: W, height: H });
  png.data.copy(out.data);
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const p = (y * W + x) * 4;
      const nv = fn2(x, y, out.data[p]);
      if (nv != null) { out.data[p] = nv[0]; out.data[p + 1] = nv[1]; out.data[p + 2] = nv[2]; }
    }
  }
  return out;
}

const base = baseline();
const TARGET = Math.round(W * H * 0.04); // ~4% of pixels in both scenarios
// A: one contiguous block changed (a swapped hero image / moved card)
const blockW = 240, blockH = Math.round(TARGET / 240);
const caseA = mutate(base, (x, y) => (x >= 100 && x < 100 + blockW && y >= 200 && y < 200 + blockH) ? [220, 40, 40] : null);
// B: the SAME number of pixels, scattered one at a time (antialiasing / font-rendering speckle)
// Only pick pixels on one colour of a checkerboard, so no two chosen pixels are ever 4-adjacent
// and every one stays a genuinely isolated 1 px speck. Seeded LCG so the set is reproducible.
const candidates = [];
for (let y = 2; y < H - 2; y++) for (let x = 2 + ((y + 1) % 2); x < W - 2; x += 2) candidates.push(y * W + x);
let seed = 12345;
for (let i = candidates.length - 1; i > 0; i--) {
  seed = (seed * 1103515245 + 12345) & 0x7fffffff;
  const j = seed % (i + 1);
  [candidates[i], candidates[j]] = [candidates[j], candidates[i]];
}
const speck = new Set(candidates.slice(0, TARGET));
if (speck.size !== TARGET) throw new Error(`speck setup: wanted ${TARGET} isolated pixels, got ${speck.size}`);
const caseB = mutate(base, (x, y, v) => speck.has(y * W + x) ? [Math.max(0, v - 160), Math.max(0, v - 160), Math.max(0, v - 160)] : null);

function run(label, cmp, threshold, minRegionPixels = 4) {
  const diffPng = new PNG({ width: W, height: H });
  const diffPixels = pixelmatch(base.data, cmp.data, diffPng.data, W, H, { threshold, includeAA: true });
  const t0 = process.hrtime.bigint();
  const r = fn(diffPng.data, W, H, minRegionPixels);
  const ms = Number(process.hrtime.bigint() - t0) / 1e6;
  const pct = Number(((diffPixels / (W * H)) * 100).toFixed(4));
  const ok = r.changedPixels === diffPixels;
  console.log(`${ok ? 'INVARIANT OK ' : 'INVARIANT FAIL'}  ${label} thr=${threshold} floor=${minRegionPixels}
    diffPixels=${diffPixels} (derived ${r.changedPixels})  diffPercent=${pct}%
    diffRegions=${r.regions}  largest=${r.largestRegionPixels}px  diffSpecks=${r.specks}  [${ms.toFixed(0)} ms]`);
  return { ok, pct, r, diffPixels };
}

console.log('=== the reader\'s scenario: same diffPercent, structurally different change ===');
let fails = 0;
const a = run('A one contiguous block ', caseA, 0.1);
const b = run('B scattered 1px speckle', caseB, 0.1);
if (!a.ok) fails++;
if (!b.ok) fails++;
console.log(`
  -> diffPercent ${a.pct}% vs ${b.pct}% (within ${Math.abs(a.pct - b.pct).toFixed(4)} pp -- indistinguishable)
  -> diffRegions ${a.r.regions} vs ${b.r.regions}, specks ${a.r.specks} vs ${b.r.specks} (clearly distinguishable)\n`);

console.log('=== invariant across thresholds and floors (real pixelmatch output each time) ===');
for (const thr of [0, 0.02, 0.05, 0.1, 0.3, 1]) {
  for (const cmp of [['A', caseA], ['B', caseB]]) {
    const res = run(`${cmp[0]} sweep`, cmp[1], thr);
    if (!res.ok) fails++;
  }
}
for (const floor of [1, 2, 10, 500, 10000]) {
  const res = run('A floor sweep', caseA, 0.1, floor);
  if (!res.ok) fails++;
}
// identical images: pixelmatch takes its fast path and writes only gray pixels
const res0 = run('identical images', base, 0.1);
if (!res0.ok || res0.r.regions !== 0 || res0.diffPixels !== 0) { fails++; console.log('  FAIL: identical images should be 0/0'); }

console.log(`\n${fails} failure(s)`);
process.exit(fails ? 1 : 0);
