# ugc-creator

Hyper-realistic AI UGC studio. Generates consistent, photorealistic image and video prompts for social media ad campaigns — indistinguishable from real iPhone-shot UGC content.

## Commands

| Command | What it does |
|---------|-------------|
| `ugc create-actor` | Build a new actor identity card (interactive) |
| `ugc generate-shot` | Assemble a full 6-layer image prompt for a given actor + shot type |
| `ugc generate-video` | Generate anchor frame + Kling API call for video output |
| `ugc validate-prompt` | Check any prompt against all hard enforcement rules |

## Required Env Vars

| Variable | Purpose |
|----------|---------|
| `FAL_KEY` | fal.ai API key for Kling video generation — never hardcode this |

Set it:
```bash
export FAL_KEY=your_key_here
```

## Module Overview

```
ugc-creator/
├── SKILL.md                          # Claude skill entry point
├── skill.json                        # Skill manifest
├── actors/
│   └── maya-01.json                  # Example actor card
├── engines/
│   └── realism.json                  # 10 mandatory realism anchors
├── profiles/
│   └── camera-profiles.json          # iPhone camera simulation profiles
├── systems/
│   ├── prompt-layers.json            # 6-layer prompt assembly schema
│   └── consistency-protocol.json    # Multi-shot consistency rules
├── shot-types/
│   └── ugc-shots.json               # 7 UGC shot types with camera + framing rules
└── integrations/
    └── kling-fal.json               # Kling 3.0 via fal.ai API config
```

## Shot Types

| Shot ID | Description | Camera |
|---------|-------------|--------|
| `unboxing` | Opening product packaging | rear-cam |
| `testimonial-talking-head` | Direct-to-camera recommendation | selfie-front-cam |
| `lifestyle-ambient` | Product in daily life | rear-cam |
| `get-ready-with-me` | Applying product at vanity/mirror | mirror-selfie |
| `before-after` | Transformation sequence | selfie-front-cam |
| `flatlay-product-feature` | Overhead product hero shot | overhead-flatlay |
| `pov-handoff` | Offering product to viewer | rear-cam |

## Hard Rules (enforced on every prompt)

1. All 10 realism anchors must be in Layer 5 — zero exceptions
2. `prompt_seed` locked per actor — same seed across every shot in a campaign
3. All 6 prompt layers must be assembled in order (1 → 6)
4. `FAL_KEY` read from environment only — never hardcoded
5. Video motion prompts use motion descriptors only (no appearance, no character identity)
6. Actor `negative_anchors` always merged with global negatives in Layer 6
7. All `distinguishing_marks` appear verbatim in Layer 1

## Example: Full Image Prompt (maya-01, testimonial-talking-head, Jarvis)

```
[Actor: maya-01] oval face, #6B4F3A almond eyes, skin tone #C68642, shoulder wavy #2C1B0E hair, small mole above lip-left, faint freckle cluster on right cheek

maya-01 is speaking directly to camera, holding phone near chest with Jarvis website visible, expression: confident and sincere

Setting: bright home office with plants, mid-morning golden window light, laptop and coffee cup in background

iPhone front camera selfie, 23mm equiv, f/1.9, Smart HDR processing, slight face-widening barrel distortion, shallow DOF background blur, close-up framing with face filling 60% of frame, shot from eye level

Realism: visible skin pores under natural light slight texture variation across nose bridge and cheeks, 2-3 stray baby hairs along hairline single flyaway crossing forehead, subtle under-eye creasing faint bluish tint beneath lower lash line, slight redness on nose tip mild discoloration on chin natural skin unevenness, fabric weave visible on clothing natural wrinkle at elbow crease slight lint, ambient dust particles in light beam background grain consistent with location, soft shadow under chin uneven highlight on forehead one side slightly cooler lit, slight chromatic aberration at frame edges subtle lens barrel distortion, natural nail with faint cuticle line slight shine variation across nail surface, necklace chain sitting naturally with slight sag earring back visible behind lobe

Negative: CGI skin, plastic texture, studio backdrop, perfect symmetry, airbrushed, oversaturated, uncanny valley, fake bokeh, HDR overdone, watermark, text overlay, smooth plastic skin, perfect symmetry, airbrushed face, studio lighting halo, heavy makeup
```

## Example: Kling Video API Call

```bash
curl -X POST "https://fal.run/fal-ai/kling-video/v1.6/standard/image-to-video" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://your-anchor-frame-url.jpg",
    "prompt": "gently raises product toward camera, soft smile, slight head tilt, natural handheld camera shake",
    "duration": "5",
    "aspect_ratio": "9:16",
    "cfg_scale": 0.5
  }'
```

## Adding New Actors

Run `ugc create-actor` — Claude will walk you through all required fields interactively and write the JSON card automatically.

Actor cards live in `actors/{actor-id}.json`. Every field is required — no optional fields allowed.
