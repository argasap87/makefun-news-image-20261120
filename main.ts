// make.fun news-image-20261120 entry program.
// The infographic is drawn ahead of time by draw.py and stored here as
// entry.png; this program just places those exact bytes at the output
// path the grader expects. Node 22, standard library only, no network.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");

if (!existsSync(source)) {
  throw new Error(`missing entry image: ${source}`);
}
const bytes = readFileSync(source);
if (bytes.length === 0) {
  throw new Error(`entry image is empty: ${source}`);
}
mkdirSync(dirname(target), { recursive: true });
writeFileSync(target, bytes);
const written = readFileSync(target);
if (!written.equals(bytes)) {
  throw new Error(`output differs from source: ${target}`);
}
console.log(`wrote ${target} (${bytes.length} bytes)`);
