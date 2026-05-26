import { fal } from "@fal-ai/client";
import { writeFile, mkdir } from "fs/promises";
import { createWriteStream } from "fs";
import https from "https";
import path from "path";

fal.config({ credentials: process.env.FAL_KEY });

const BASE = "/Users/passionchu/jarvis-ads";

// ─── Ad Concepts ────────────────────────────────────────────────────────────
const CONCEPTS = [
  {
    id: "C1",
    funnel: "funnel-1",
    name: "Time Prison",
    hook: "Most founders hired themselves into a prison",
    visual: "A dark prison cell with neon yellow bars, a founder trapped behind them staring at a laptop, cinematic lighting",
  },
  {
    id: "C2",
    funnel: "funnel-2",
    name: "$10/hr Trap",
    hook: "What's 3 hours of your time worth?",
    visual: "A clock melting on a desk covered in dollar bills, dark moody background, neon yellow highlights",
  },
  {
    id: "C3",
    funnel: "funnel-3",
    name: "VA of the Week",
    hook: "He got back 15 hours — here's what changed",
    visual: "Split screen: exhausted founder before vs. relaxed founder with family after, cinematic dark tones",
  },
  {
    id: "C4",
    funnel: "funnel-4",
    name: "The Guarantee",
    hook: "You're not taking a risk. We are.",
    visual: "A contract being signed in neon yellow light, bold guarantee seal, dark dramatic background",
  },
  {
    id: "C5",
    funnel: "funnel-5",
    name: "Freedom",
    hook: "Your business should work for you. Not the other way around.",
    visual: "Founder walking away from a glowing laptop toward an open horizon, neon yellow sunset, cinematic",
  },
];

const STYLE_SUFFIX =
  "cinematic photography, dark background, bold white text overlay space, punk rock energy, high contrast, neon yellow #D4FF00 accents, Barlow Condensed typography style, Meta ad creative, 8K";

// ─── Helpers ─────────────────────────────────────────────────────────────────
async function download(url, dest) {
  await mkdir(path.dirname(dest), { recursive: true });
  return new Promise((resolve, reject) => {
    const file = createWriteStream(dest);
    https.get(url, (res) => {
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(dest); });
    }).on("error", reject);
  });
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// ─── Static Images via Flux Pro ──────────────────────────────────────────────
async function generateImage(concept, index, ratio) {
  const aspectRatio = ratio === "1:1" ? "square_hd" : "portrait_4_3";
  const prompt = `${concept.visual}, ${STYLE_SUFFIX}`;
  console.log(`  [IMG] ${concept.id} #${index} (${ratio})...`);

  try {
    const result = await fal.subscribe("fal-ai/flux-pro/v1.1", {
      input: {
        prompt,
        image_size: aspectRatio,
        num_images: 1,
        safety_tolerance: "5",
      },
    });
    const url = result.data?.images?.[0]?.url;
    if (!url) throw new Error("No image URL returned");

    const filename = `${concept.id}-${index}-${ratio.replace(":", "x")}.jpg`;
    const dest = path.join(BASE, "creatives", concept.funnel, filename);
    await download(url, dest);
    console.log(`  ✓ Saved: ${dest}`);
    return { concept: concept.id, index, ratio, url, dest, status: "done" };
  } catch (err) {
    console.error(`  ✗ ${concept.id} #${index}: ${err.message}`);
    return { concept: concept.id, index, ratio, status: "error", error: err.message };
  }
}

// ─── Video Clips via Kling ───────────────────────────────────────────────────
async function generateVideo(concept, index) {
  const prompt = `${concept.hook}. ${concept.visual}. ${STYLE_SUFFIX}. Vertical 9:16 short ad clip, 5 seconds, cinematic motion`;
  console.log(`  [VID] ${concept.id} #${index}...`);

  try {
    const result = await fal.subscribe("fal-ai/kling-video/v1.6/standard/text-to-video", {
      input: {
        prompt,
        duration: "5",
        aspect_ratio: "9:16",
      },
      pollInterval: 5000,
    });
    const url = result.data?.video?.url;
    if (!url) throw new Error("No video URL returned");

    const filename = `${concept.id}-video-${index}.mp4`;
    const dest = path.join(BASE, "video", filename);
    await download(url, dest);
    console.log(`  ✓ Saved: ${dest}`);
    return { concept: concept.id, index, url, dest, status: "done" };
  } catch (err) {
    console.error(`  ✗ ${concept.id} video #${index}: ${err.message}`);
    return { concept: concept.id, index, status: "error", error: err.message };
  }
}

// ─── Main ────────────────────────────────────────────────────────────────────
async function main() {
  const results = { images: [], videos: [] };

  console.log("\n=== JARVIS AD STACK — Creative Generation ===\n");

  // 30 static images: 6 per concept (3×1:1 + 3×9:16)
  console.log("▶ Generating 30 static images (Flux Pro)...\n");
  for (const concept of CONCEPTS) {
    for (let i = 1; i <= 3; i++) {
      results.images.push(await generateImage(concept, i, "1:1"));
      await sleep(500);
    }
    for (let i = 1; i <= 3; i++) {
      results.images.push(await generateImage(concept, i, "9:16"));
      await sleep(500);
    }
  }

  // 20 video clips: 4 per concept
  console.log("\n▶ Generating 20 video clips (Kling)...\n");
  for (const concept of CONCEPTS) {
    for (let i = 1; i <= 4; i++) {
      results.videos.push(await generateVideo(concept, i));
      await sleep(1000);
    }
  }

  // Save manifest
  const manifest = {
    generated: new Date().toISOString(),
    images: results.images,
    videos: results.videos,
    summary: {
      images_total: results.images.length,
      images_done: results.images.filter((r) => r.status === "done").length,
      videos_total: results.videos.length,
      videos_done: results.videos.filter((r) => r.status === "done").length,
    },
  };
  await writeFile(
    path.join(BASE, "manifest.json"),
    JSON.stringify(manifest, null, 2)
  );

  console.log("\n=== DONE ===");
  console.log(`Images: ${manifest.summary.images_done}/${manifest.summary.images_total}`);
  console.log(`Videos: ${manifest.summary.videos_done}/${manifest.summary.videos_total}`);
  console.log(`Manifest: ${BASE}/manifest.json`);
}

main().catch(console.error);
