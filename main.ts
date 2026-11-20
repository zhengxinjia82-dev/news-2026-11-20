// news-image-20261120 entry (Node 22, standard library only).
// The image is entry.png beside this file; the program copies it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR when set, for local runs).
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
