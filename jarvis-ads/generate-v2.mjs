import { fal } from "@fal-ai/client";
import { writeFile, mkdir } from "fs/promises";
import { createWriteStream } from "fs";
import https from "https";
import http from "http";
import path from "path";

fal.config({ credentials: process.env.FAL_KEY });

const BASE = "/Users/passionchu/jarvis-ads/creatives";

// ─── Prompts ─────────────────────────────────────────────────────────────────

const BATCHES = [
  // C1: Time Prison — 10x square via flux/dev
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c1-time-prison-${String(i + 1).padStart(2, "0")}`,
    dir: "c1-time-prison",
    model: "fal-ai/flux/dev",
    prompt: `Ultra-minimal ad creative. Pure black background. A lone founder slumped at a desk, 11:07 PM on clock, harsh cold blue monitor glow. Neon yellow (#D4FF00) bold condensed sans-serif text overlay: "YOU HIRED YOURSELF INTO A PRISON." — stark, confrontational, punk energy. No decoration. No gradients. Just black, white, and neon yellow. High contrast editorial photography style. Seed variant ${i + 1}.`,
    image_size: "square_hd",
  })),

  // C2: $10/hr Trap — 10x square via flux/dev
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c2-10hr-trap-${String(i + 1).padStart(2, "0")}`,
    dir: "c2-10hr-trap",
    model: "fal-ai/flux/dev",
    prompt: `Stark ad creative. Pure black background. Giant neon yellow (#D4FF00) text dominates frame: "$500/DAY LOST". Below in smaller bold white text: "You spend 3 hrs/day on $10/hr tasks." Brutal simple math layout. No people. Pure typographic visual. Barlow Condensed style bold typography. Aggressive, confrontational, direct. Minimal. Seed variant ${i + 1}.`,
    image_size: "square_hd",
  })),

  // C4: Guarantee — 10x square via flux/dev
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c4-guarantee-${String(i + 1).padStart(2, "0")}`,
    dir: "c4-guarantee",
    model: "fal-ai/flux/dev",
    prompt: `Bold ad creative. Pure black background. Centered neon yellow (#D4FF00) geometric circle badge with bold text "JARVIS" inside. Below the badge, large white bold condensed text: "YOU'RE NOT TAKING A RISK. WE ARE." Below that, smaller white text: "No payment before your VA starts." Clean, confident, premium. Nike-level visual authority. Seed variant ${i + 1}.`,
    image_size: "square_hd",
  })),

  // C3: VA of the Week — 10x vertical via fast-sdxl
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c3-va-week-${String(i + 1).padStart(2, "0")}`,
    dir: "c3-va-week",
    model: "fal-ai/fast-sdxl",
    prompt: `Vertical ad creative 9:16. Split screen layout: LEFT side dark moody — exhausted founder overwhelmed at messy desk, stressed face, harsh cold light. RIGHT side warm golden light — same founder relaxed, smiling, outdoors or with family. Bold white text overlay top: "15 HOURS BACK EVERY WEEK." Neon yellow (#D4FF00) divider line between halves. Bottom: "Real founder. Real result." — Jarvis VA Service. Cinematic, results-focused, emotional. Seed variant ${i + 1}.`,
    image_size: "portrait_4_3",
  })),

  // C1: Time Prison vertical — 10x vertical via fast-sdxl
  ...Array.from({ length: 10 }, (_, i) => ({
    id: `c1-time-prison-v-${String(i + 1).padStart(2, "0")}`,
    dir: "c1-time-prison",
    model: "fal-ai/fast-sdxl",
    prompt: `Vertical cinematic ad 9:16. Extreme close-up of an old analogue wall clock showing 11:47 PM, ticking. Deep black background with moody shadows. Neon yellow (#D4FF00) glow emanating from clock face. Bold condensed white text overlay: "MOST FOUNDERS HIRED THEMSELVES INTO A PRISON." Underneath in neon yellow: "Sound like you?" Dark, dramatic, punk energy. High contrast. Cinematic grain. Seed variant ${i + 1}.`,
    image_size: "portrait_4_3",
  })),
];

// ─── Helpers ─────────────────────────────────────────────────────────────────

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
  const { id, dir, model, prompt, image_size } = batch;
  const dest = path.join(BASE, dir, `${id}.jpg`);

  try {
    const result = await fal.subscribe(model, {
      input: { prompt, image_size, num_images: 1, num_inference_steps: 28, guidance_scale: 3.5 },
    });

    const url = result?.data?.images?.[0]?.url || result?.images?.[0]?.url;
    if (!url) throw new Error(`No URL in response: ${JSON.stringify(result).slice(0, 200)}`);

    await downloadFile(url, dest);
    return { id, dest, status: "done", url };
  } catch (err) {
    return { id, dest, status: "error", error: err.message };
  }
}

// ─── Notion Tracking ─────────────────────────────────────────────────────────

async function trackInNotion(results, dbId) {
  if (!process.env.NOTION_API_KEY || !dbId) return;

  for (const r of results.filter((x) => x.status === "done")) {
    const concept = r.id.startsWith("c1") ? "C1 Time Prison"
      : r.id.startsWith("c2") ? "C2 $10/hr Trap"
      : r.id.startsWith("c3") ? "C3 VA of the Week"
      : "C4 The Guarantee";

    await fetch("https://api.notion.com/v1/pages", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.NOTION_API_KEY}`,
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        parent: { database_id: dbId },
        properties: {
          Creative: { title: [{ text: { content: r.id } }] },
          Funnel: { select: { name: concept } },
          Status: { select: { name: "Generated" } },
          Platform: { select: { name: "Meta" } },
        },
      }),
    });
  }
  console.log(`\n  ✓ Tracked ${results.filter((x) => x.status === "done").length} assets in Notion`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log("\n╔══════════════════════════════════════════╗");
  console.log("║  JARVIS AD STACK — 50 Creative Generator  ║");
  console.log("╚══════════════════════════════════════════╝\n");

  const results = [];
  const total = BATCHES.length;
  let done = 0, errors = 0;

  // Process in parallel batches of 5 to avoid rate limits
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
    generated: new Date().toISOString(),
    summary: { total, done, errors },
    assets: results,
  };
  await writeFile(
    path.join("/Users/passionchu/jarvis-ads", "manifest.json"),
    JSON.stringify(manifest, null, 2)
  );

  // Notion tracking (set NOTION_DB_ID env var to enable)
  if (process.env.NOTION_DB_ID) {
    console.log("\n  Syncing to Notion...");
    await trackInNotion(results, process.env.NOTION_DB_ID);
  } else {
    console.log("\n  (Notion sync skipped — set NOTION_DB_ID to enable)");
  }

  console.log("\n╔══════════════════════════════╗");
  console.log(`║  Done: ${done}/${total} assets generated  ║`);
  console.log("╚══════════════════════════════╝");
  console.log("\nOutput:");
  console.log("  /jarvis-ads/creatives/c1-time-prison/  (20 files: 10 square + 10 vertical)");
  console.log("  /jarvis-ads/creatives/c2-10hr-trap/    (10 files: square)");
  console.log("  /jarvis-ads/creatives/c3-va-week/      (10 files: vertical)");
  console.log("  /jarvis-ads/creatives/c4-guarantee/    (10 files: square)");
  console.log("  /jarvis-ads/manifest.json");
}

main().catch(console.error);
