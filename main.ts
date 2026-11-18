// news-image-20261117 entry (Node 22, standard library only).
// The image is entry.png beside this file: a one-page newspaper front page
// summarising the world news of Tuesday 17 November 2026, drawn locally with
// draw_news.py (PIL) from reporting of that day and shipped as a static file.
// This program copies it to /output/entry.png, byte for byte, every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

// The PNG signature every whole PNG starts with; the gate rejects anything else.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

const source = new URL('./entry.png', import.meta.url);
const target = join(outDir, 'entry.png');
copyFileSync(source, target);

// Refuse to hand the gate a truncated file: the copied bytes must open as a PNG.
const head = readFileSync(target).subarray(0, PNG_SIGNATURE.length);
if (!head.equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG file');
}
