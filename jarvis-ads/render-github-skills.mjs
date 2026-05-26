import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import path from "path";
import { mkdir } from "fs/promises";

const OUT_DIR = "/Users/passionchu/claude/jarvis-ads/output";
const OUT_FILE = path.join(OUT_DIR, "GithubSkills.mp4");

async function main() {
  await mkdir(OUT_DIR, { recursive: true });

  console.log("▶ Bundling...");
  const bundled = await bundle({
    entryPoint: path.resolve("src/remotion/index.js"),
    webpackOverride: (config) => config,
  });

  console.log("▶ Selecting composition GithubSkills...");
  const composition = await selectComposition({
    serveUrl: bundled,
    id: "GithubSkills",
    inputProps: {},
  });

  console.log("▶ Rendering 15s × 1080×1920...");
  await renderMedia({
    composition,
    serveUrl: bundled,
    codec: "h264",
    outputLocation: OUT_FILE,
    inputProps: {},
    onProgress: ({ progress }) =>
      process.stdout.write(`\r  ${Math.round(progress * 100)}%   `),
  });

  console.log(`\n✓ Done → ${OUT_FILE}`);
}

main().catch(console.error);
