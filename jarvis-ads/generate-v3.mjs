import { fal } from "@fal-ai/client";
import { writeFile } from "fs/promises";
import { createWriteStream } from "fs";
import https from "https";
import http from "http";
import path from "path";

fal.config({ credentials: process.env.FAL_KEY });

const BASE = "/Users/passionchu/jarvis-ads/creatives-v2";

// ─── Exact prompts as specified ───────────────────────────────────────────────

const BATCHES = [
  // AD 1 — The Bottleneck Confession — 10x 1080x1080 square
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `ad1-bottleneck-${String(i + 1).padStart(2, "0")}`,
    dir: "ad1-bottleneck",
    prompt: `Premium Meta ad creative, pure black background, bold neon yellow #D4FF00 Barlow Condensed font, large text overlay reading "I BUILT A BUSINESS I CAN'T LEAVE FOR A SINGLE DAY", small subtext "The Bottleneck Confession", bottom corner small text "gojarvis.ai", sharp crisp edges, no blur, professional advertising quality, high contrast, seed ${i + 1}`,
    image_size: "square_hd",
  })),

  // AD 2 — The $10/hr Brain Problem — 10x 1080x1080 square
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `ad2-10hr-brain-${String(i + 1).padStart(2, "0")}`,
    dir: "ad2-10hr-brain",
    prompt: `Premium Meta ad creative, pure black background, massive neon yellow #D4FF00 bold condensed text "$300K BUSINESS. $10/HR TO-DO LIST.", supporting text in white "Stop doing work that's keeping you small", bottom "gojarvis.ai", stark minimalist design, sharp text, no blur, scroll-stopping, seed ${i + 1}`,
    image_size: "square_hd",
  })),

  // AD 3 — The Identity Reframe — 10x 1080x1920 vertical
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `ad3-identity-reframe-${String(i + 1).padStart(2, "0")}`,
    dir: "ad3-identity-reframe",
    prompt: `Premium Instagram Reel ad, black background, bold white text at top "THERE ARE TWO TYPES OF BUSINESS OWNERS.", neon yellow #D4FF00 accent line divider, bottom text "WHICH ONE ARE YOU?", Jarvis yellow circle logo bottom center, 9:16 vertical format, sharp, professional, high contrast, seed ${i + 1}`,
    image_size: "portrait_4_3",
  })),
];

// ─── Helpers ──────────────────────────────────────────────────────────────────

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
      input: {
        prompt,
        image_size,
        num_images: 1,
        safety_tolerance: "5",
      },
    });

    const url = result?.data?.images?.[0]?.url || result?.images?.[0]?.url;
    if (!url) throw new Error(`No URL: ${JSON.stringify(result).slice(0, 150)}`);

    await downloadFile(url, dest);
    return { id, dest, status: "done", url };
  } catch (err) {
    return { id, dest, status: "error", error: err.message };
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log("\n╔══════════════════════════════════════════════╗");
  console.log("║  JARVIS AD STACK — 30 Creatives (flux-pro)   ║");
  console.log("╚══════════════════════════════════════════════╝\n");
  console.log("  AD 1 — Bottleneck Confession    10x 1080×1080");
  console.log("  AD 2 — $10/hr Brain Problem     10x 1080×1080");
  console.log("  AD 3 — Identity Reframe         10x 1080×1920");
  console.log("\n  Generating...\n");

  const results = [];
  const total = BATCHES.length;
  let done = 0, errors = 0;

  // 5 concurrent requests
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

  // Save manifest
  const manifest = {
    version: "v3",
    generated: new Date().toISOString(),
    model: "fal-ai/flux-pro/v1.1",
    summary: { total, done, errors },
    assets: results,
  };
  await writeFile(
    "/Users/passionchu/jarvis-ads/manifest-v3.json",
    JSON.stringify(manifest, null, 2)
  );

  console.log("\n╔══════════════════════════════════════════╗");
  console.log(`║  Done: ${done}/${total} creatives generated             ║`);
  console.log("╚══════════════════════════════════════════╝\n");
  console.log("  Output:");
  console.log("  creatives-v2/ad1-bottleneck/        (10 files)");
  console.log("  creatives-v2/ad2-10hr-brain/        (10 files)");
  console.log("  creatives-v2/ad3-identity-reframe/  (10 files)");
  console.log("  manifest-v3.json\n");

  if (errors > 0) {
    console.log(`  ⚠ ${errors} failed. Re-run to retry failed items.`);
  }
}

main().catch(console.error);
