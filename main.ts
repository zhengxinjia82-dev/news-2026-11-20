// news-image-20261120 entry (Node 22, standard library only).
// The image is entry.png beside this file; the program copies it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR when set, for local runs).
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
// Verify the copy landed intact: same size as the source image.
const srcSize = statSync(src).size;
const destSize = statSync(dest).size;
if (srcSize !== destSize) {
  throw new Error(`entry.png copy mismatch: source ${srcSize} bytes, output ${destSize} bytes`);
}
console.log(`entry.png copied to ${dest} (${destSize} bytes)`);
