import { fal } from "@fal-ai/client";
import { writeFile } from "fs/promises";
import { createWriteStream } from "fs";
import https from "https";
import http from "http";
import path from "path";

fal.config({ credentials: process.env.FAL_KEY });

const BASE = "/Users/passionchu/jarvis-ads/creatives-v3";

const BATCHES = [
  // C1 — Time Prison — 10x square
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c1-time-prison-${String(i + 1).padStart(2, "0")}`,
    dir: "c1-time-prison",
    image_size: "square_hd",
    prompt: `Cinematic photo, miniature tiny businessman figure trapped inside a giant hourglass filled with emails and spreadsheets, dark moody lighting, neon yellow glow from inside the glass, photorealistic, ultra sharp, studio quality, no text, dramatic shadows, 8K resolution, advertising photography, seed variant ${i + 1}`,
  })),

  // C2 — $10/hr Trap — 10x square
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c2-10hr-trap-${String(i + 1).padStart(2, "0")}`,
    dir: "c2-10hr-trap",
    image_size: "square_hd",
    prompt: `Cinematic photo, tiny miniature person drowning in giant pile of dollar coins all labeled $10, dark background, neon yellow light casting dramatic shadows, photorealistic, ultra sharp, no text overlay, advertising quality, bird's eye view angle, seed variant ${i + 1}`,
  })),

  // C3 — VA of the Week — 10x vertical 9:16
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c3-va-week-${String(i + 1).padStart(2, "0")}`,
    dir: "c3-va-week",
    image_size: "portrait_4_3",
    prompt: `Split screen cinematic photo, left side: stressed founder buried under giant pile of paperwork at dark desk, right side: same person relaxed on rooftop at sunset, city view, clean desk, neon yellow dividing line, photorealistic, ultra sharp, no text, 9:16 vertical, seed variant ${i + 1}`,
  })),

  // C4 — Guarantee — 10x square
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c4-guarantee-${String(i + 1).padStart(2, "0")}`,
    dir: "c4-guarantee",
    image_size: "square_hd",
    prompt: `Cinematic photo, two hands doing a firm handshake, one hand wearing a business suit, dramatic dark background, neon yellow #D4FF00 spotlight from above, photorealistic, ultra sharp, no text, advertising quality, trust and confidence feel, seed variant ${i + 1}`,
  })),
];

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const proto = url.startsWith("https") ? https : http;
    const file = createWriteStream(dest);
    proto.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        return downloadFile(res.headers.location, dest).then(resolve).catch(reject);
      }
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(dest); });
      file.on("error", reject);
    }).on("error", (err) => { file.close(); reject(err); });
  });
}

async function generateOne(batch) {
  const { id, dir, prompt, image_size } = batch;
  const dest = path.join(BASE, dir, `${id}.jpg`);
  try {
    const result = await fal.subscribe("fal-ai/flux-pro/v1.1", {
      input: { prompt, image_size, num_images: 1, safety_tolerance: "5" },
    });
    const url = result?.data?.images?.[0]?.url || result?.images?.[0]?.url;
    if (!url) throw new Error(`No URL: ${JSON.stringify(result).slice(0, 150)}`);
    await downloadFile(url, dest);
    return { id, dest, status: "done", url };
  } catch (err) {
    return { id, dest, status: "error", error: err.message };
  }
}

async function main() {
  console.log("\n╔═══════════════════════════════════════════════════╗");
  console.log("║  JARVIS — 30 Visuals-Only Creatives (flux-pro)    ║");
  console.log("╚═══════════════════════════════════════════════════╝\n");
  console.log("  C1 Time Prison      10x 1080×1080  (hourglass)");
  console.log("  C2 $10/hr Trap      10x 1080×1080  (coin pile)");
  console.log("  C3 VA of the Week   10x 1080×1920  (split screen)");
  console.log("  C4 Guarantee        10x 1080×1080  (handshake)");
  console.log("\n  Generating in batches of 5...\n");

  const results = [];
  const total = BATCHES.length;
  let done = 0, errors = 0;

  const CONCURRENCY = 5;
  for (let i = 0; i < BATCHES.length; i += CONCURRENCY) {
    const chunk = BATCHES.slice(i, i + CONCURRENCY);
    const chunkResults = await Promise.all(
      chunk.map(async (b) => {
        const r = await generateOne(b);
        if (r.status === "done") {
          done++;
          console.log(`  ✓ [${done + errors}/${total}] ${r.id}`);
        } else {
          errors++;
          console.error(`  ✗ [${done + errors}/${total}] ${r.id}: ${r.error}`);
        }
        return r;
      })
    );
    results.push(...chunkResults);
  }

  await writeFile(
    "/Users/passionchu/jarvis-ads/manifest-v4.json",
    JSON.stringify({
      version: "v4",
      generated: new Date().toISOString(),
      model: "fal-ai/flux-pro/v1.1",
      note: "Visuals only — no text. Text to be added in Canva.",
      summary: { total, done, errors },
      assets: results,
    }, null, 2)
  );

  console.log(`\n╔══════════════════════════════════════╗`);
  console.log(`║  Done: ${done}/${total} — ${errors} errors                 ║`);
  console.log(`╚══════════════════════════════════════╝\n`);
  console.log("  creatives-v3/c1-time-prison/   (10 files)");
  console.log("  creatives-v3/c2-10hr-trap/     (10 files)");
  console.log("  creatives-v3/c3-va-week/       (10 files)");
  console.log("  creatives-v3/c4-guarantee/     (10 files)");
  console.log("  manifest-v4.json\n");
}

main().catch(console.error);
