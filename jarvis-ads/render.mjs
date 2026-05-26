import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import path from "path";
import { mkdir, readFile } from "fs/promises";

const OUT_DIR = "/Users/passionchu/claude/jarvis-ads/output";
const CREATIVES = "/Users/passionchu/claude/jarvis-ads/creatives";

async function toDataURL(filePath) {
  const buf = await readFile(filePath);
  return `data:image/jpeg;base64,${buf.toString("base64")}`;
}

const ADS = [
  {
    // #1 — Cost of inaction math. Logic hook. Finance-minded $10K+ owners.
    id: "C1-AutomationMath",
    hook: "At $30K/month your rate is $180/hr",
    subtext: "Are you doing $10/hr tasks? Your VA automates them.",
    cta: "10 Seconds to Qualify →",
    image: `${CREATIVES}/c2-10hr-trap/c2-10hr-trap-01.jpg`,
  },
  {
    // #2 — Revenue qualifier + systems reframe. Top hook from brief.
    id: "C2-SystemsProblem",
    hook: "Doing $10K–$30K/month and still doing everything yourself?",
    subtext: "That's not a hustle problem. That's a systems problem.",
    cta: "Book Free Call →",
    image: `${CREATIVES}/c1-time-prison/c1-time-prison-v-01.jpg`,
  },
  {
    // #3 — Unique differentiator. No competitor owns this angle.
    id: "C3-OtherVAs",
    hook: "Other VAs do the work. Ours automate it.",
    subtext: "So it never comes back to you.",
    cta: "See How It Works →",
    image: `${CREATIVES}/c4-guarantee/c4-guarantee-01.jpg`,
  },
  {
    // #4 — Objection handler for warm/retargeting audiences.
    id: "C4-NeverManage",
    hook: "Every VA I hired needed constant managing. Until Jarvis.",
    subtext: "Pre-trained. Automation-ready. Live in 60 minutes.",
    cta: "Get Your VA →",
    image: `${CREATIVES}/c3-va-week/c3-va-week-01.jpg`,
  },
  {
    // #5 — Freedom/lifestyle angle. Beach girl concept. Scroll stopper.
    id: "C5-BeachAutomation",
    hook: "She's at the beach. Her VA is building automations right now.",
    subtext: "That's what $10K/month looks like with Jarvis.",
    cta: "Claim Your Spot →",
    image: `${CREATIVES}/c1-time-prison/c1-time-prison-v-05.jpg`,
  },
];

async function main() {
  await mkdir(OUT_DIR, { recursive: true });

  console.log("▶ Bundling Remotion compositions...");
  const bundled = await bundle({
    entryPoint: path.resolve("src/remotion/index.js"),
    webpackOverride: (config) => config,
  });

  for (const ad of ADS) {
    console.log(`\n  Rendering ${ad.id}...`);

    // Embed image as base64 data URL to avoid static file serving issues
    const imageSrc = await toDataURL(ad.image);

    const composition = await selectComposition({
      serveUrl: bundled,
      id: ad.id,
      inputProps: { hook: ad.hook, subtext: ad.subtext, cta: ad.cta, imageSrc, useVideo: false },
    });

    const outPath = path.join(OUT_DIR, `${ad.id}.mp4`);
    await renderMedia({
      composition,
      serveUrl: bundled,
      codec: "h264",
      outputLocation: outPath,
      inputProps: { hook: ad.hook, subtext: ad.subtext, cta: ad.cta, imageSrc, useVideo: false },
      onProgress: ({ progress }) =>
        process.stdout.write(`\r  ${Math.round(progress * 100)}%   `),
    });
    console.log(`\n  ✓ ${outPath}`);
  }

  console.log("\n╔══════════════════════════════════╗");
  console.log("║  All 5 ads rendered → output/    ║");
  console.log("╚══════════════════════════════════╝");
}

main().catch(console.error);
