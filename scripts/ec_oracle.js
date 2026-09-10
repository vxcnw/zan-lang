#!/usr/bin/env node
/**
 * Numeric oracle: run the REAL ECharts engine headless and dump exact geometry.
 *
 * Why this exists
 * ---------------
 * Chart correctness cannot be judged from screenshots: a screenshot cannot tell
 * you that the bar width formula is wrong if the picture "looks like a bar
 * chart". The only trustworthy reference is the engine that defines the
 * semantics, producing numbers for the same input. This script is that
 * reference: give it an official option file, get the exact layout ECharts
 * computes (bar rects, symbol positions, axis ticks, plot rect), so a Zan port
 * can be diffed against it numerically.
 *
 * Pinned reference: echarts 6.1.0, git 33ec5201159fe84f1317e4a7b00d63a73e095703.
 * The reference checkout lives outside version control (see
 * docs/CHART_CODE_GAP_LEDGER.md); this script only needs `dist/echarts.js`.
 *
 * Resolving the engine (first hit wins):
 *   1. --echarts=<path/to/dist/echarts.js>
 *   2. $ZAN_ECHARTS_DIST
 *   3. _scratch/echarts-master/dist/echarts.js   (local keeper, README-marked)
 * Re-acquire: git clone https://github.com/apache/echarts && git checkout 33ec5201
 *
 * Usage
 * -----
 *   node scripts/ec_oracle.js --option examples/gui_charts/options/bar-simple.json
 *   node scripts/ec_oracle.js --option <f> --width 1200 --height 780
 *   node scripts/ec_oracle.js --option <f> --golden      # rounded, for diffing
 *   node scripts/ec_oracle.js --option <f> --svg         # raw SVG
 *
 * Exit codes: 0 ok, 2 engine not found, 3 bad option.
 * Dev tool only -- not part of the build or the ctest tiers.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const PINNED = '6.1.0';
const ROOT = path.resolve(__dirname, '..');

function argOf(name, dflt) {
  const eq = process.argv.find((a) => a.startsWith('--' + name + '='));
  if (eq) { return eq.slice(name.length + 3); }
  const i = process.argv.indexOf('--' + name);
  if (i >= 0 && i + 1 < process.argv.length && !process.argv[i + 1].startsWith('--')) {
    return process.argv[i + 1];
  }
  return dflt;
}
const hasFlag = (name) => process.argv.includes('--' + name);

function resolveEngine() {
  const candidates = [
    argOf('echarts', null),
    process.env.ZAN_ECHARTS_DIST,
    path.join(ROOT, '_scratch', 'echarts-master', 'dist', 'echarts.js'),
  ].filter(Boolean);
  for (const c of candidates) {
    if (fs.existsSync(c)) { return c; }
  }
  console.error('ECharts dist not found. Tried:\n  ' + candidates.join('\n  '));
  console.error('Pass --echarts=<path>, set ZAN_ECHARTS_DIST, or clone the pinned');
  console.error('reference (see docs/CHART_CODE_GAP_LEDGER.md).');
  process.exit(2);
}

const optionPath = argOf('option', null);
if (!optionPath) {
  console.error('usage: node scripts/ec_oracle.js --option <option.json> [--width W] [--height H] [--golden] [--svg]');
  process.exit(3);
}

let option;
try {
  const raw = fs.readFileSync(optionPath, 'utf8');
  // Corpus options are single-line compact JSON; `__grad` marks are Zan-side
  // gradient hints that ECharts does not know about. Drop them so the oracle
  // sees exactly the official option.
  option = JSON.parse(raw, (k, v) => (k === '__grad' ? undefined : v));
} catch (err) {
  console.error('cannot parse option %s: %s', optionPath, err.message);
  process.exit(3);
}

const echarts = require(resolveEngine());
if (echarts.version !== PINNED) {
  console.error('warning: engine is %s, ledger is pinned to %s', echarts.version, PINNED);
}

const W = parseInt(argOf('width', '1200'), 10);
const H = parseInt(argOf('height', '780'), 10);

// SSR + no animation: layout is computed synchronously and nothing runs on
// timers, so the process exits deterministically.
const chart = echarts.init(null, null, {
  renderer: 'svg', ssr: true, width: W, height: H,
});
const ssrOption = Object.assign({}, option, { animation: false });
chart.setOption(ssrOption);

if (hasFlag('svg')) {
  process.stdout.write(chart.renderToSVGString());
  process.exit(0);
}

const list = chart.getZr().storage.getDisplayList(true);
const r3 = (n) => Math.round(n * 1000) / 1000;

const shapes = [];
const texts = [];
for (const el of list) {
  const s = el.shape || {};
  if (el.type === 'rect') {
    shapes.push({ t: 'rect', x: r3(s.x), y: r3(s.y), w: r3(s.width), h: r3(s.height) });
  } else if (el.type === 'circle') {
    shapes.push({ t: 'circle', cx: r3(s.cx), cy: r3(s.cy), r: r3(s.r) });
  } else if (el.type === 'line') {
    shapes.push({ t: 'line', x1: r3(s.x1), y1: r3(s.y1), x2: r3(s.x2), y2: r3(s.y2) });
  } else if (s.x != null && s.y != null && s.width != null) {   // polyline / bezier-ish
    shapes.push({ t: el.type, x: r3(s.x), y: r3(s.y), w: r3(s.width), h: r3(s.height) });
  }
  const txt = (el.style && el.style.text) || (el.type === 'tspan' && el.style && el.style.text);
  if (typeof txt === 'string' && txt.length) { texts.push(txt); }
}

// The plot rect is the bounding box of the axis lines, which ECharts emits as
// `line` shapes spanning the grid. Consumers mostly want the bar/symbol shapes,
// so it is a convenience field, not a gate.
const axisLines = shapes.filter((s) => s.t === 'line');
let plot = null;
if (axisLines.length) {
  plot = {
    x0: Math.min(...axisLines.map((s) => Math.min(s.x1, s.x2))),
    x1: Math.max(...axisLines.map((s) => Math.max(s.x1, s.x2))),
    y0: Math.min(...axisLines.map((s) => Math.min(s.y1, s.y2))),
    y1: Math.max(...axisLines.map((s) => Math.max(s.y1, s.y2))),
  };
}

const out = {
  engine: echarts.version,
  source: path.relative(ROOT, optionPath).replace(/\\/g, '/'),
  width: W, height: H,
  plot,
  texts,
  shapes,
};
process.stdout.write(JSON.stringify(out, null, hasFlag('golden') ? 0 : 1) + '\n');
