---
name: social-creative-designer
description: >
  Design and generate carousel or single social media graphics as PNG images using the Nano Banana MCP.
  Use this skill whenever the user wants to create social media visuals, carousel posts, Instagram graphics,
  LinkedIn images, or any on-brand social creative — even if they don't explicitly say "carousel" or "design".
  Trigger on: "make me a carousel", "create social graphics", "design a post about X", "make slides for Instagram",
  "generate visuals for [topic]", "build a content graphic", or any request to produce images for social platforms.
---

## Purpose

Given a topic or content brief, produce on-brand social media visuals as PNG images optimized for the specified platform and format. Handles both carousel sets and single static graphics.

---

## Defaults

| Setting       | Default     | Options                                      |
|---------------|-------------|----------------------------------------------|
| Slides        | 3           | Any number the user specifies                |
| Aspect ratio  | 4:5         | `1:1`, `3:4`, `4:5`, `1.91:1` (landscape)   |
| Platform      | Instagram   | Instagram, LinkedIn, Facebook, other         |
| Mode          | Carousel    | Carousel or Single image                     |

---

## Execution Checklist

Before generating anything, confirm these — fill in defaults silently if not specified:

- [ ] Topic or content brief provided
- [ ] Number of slides confirmed (default: 3)
- [ ] Aspect ratio confirmed (default: 4:5)
- [ ] Platform confirmed (default: Instagram)
- [ ] Carousel or single image mode confirmed
- [ ] Style direction confirmed or STYLE-GUIDE.md read
- [ ] Nano Banana MCP is available

If Nano Banana MCP is unavailable, stop immediately and notify the user. Do not attempt to proceed with placeholders or text-only output. Suggest alternatives: manual design brief or another image generation tool.

---

## Carousel Slide Structure

Think of the carousel as a mini-story with a clear arc:

- **Slide 1 — Hook:** Bold, scroll-stopping headline. Minimal text. One job: make them swipe.
- **Middle Slides — Value:** Deliver the substance. Education, insight, data, or storytelling. Each slide = one idea.
- **Final Slide — CTA:** One clear action or key takeaway. End with purpose.

---

## Single Image Mode

When the user asks for a single static graphic instead of a carousel:
- Apply the same style and brand direction to a single, self-contained frame
- Prioritize visual clarity — one message, one focus
- All brand standards still apply

---

## Style & Brand Direction

**If the user specifies a style:** Use it immediately — skip the style guide lookup.

**If no style is specified:**
1. Read `/_templates/social-creatives/STYLE-GUIDE.md` to understand available style directions
2. Reference the corresponding image set in that directory for layout, typography hierarchy, and visual tone
3. Do NOT replicate reference images exactly — adapt and combine elements to fit the topic
4. Generate designs consistent with the brand's visual identity

The goal is on-brand, not templated. Let the style guide inform the aesthetic, not dictate the layout.

---

## Image Generation

Use the **Nano Banana MCP** (`mcp__nanobanana__generate_image`) to produce all visuals as PNG files.

For each slide:
- Write a detailed visual prompt: describe layout, typography placement, color palette, mood, imagery
- Specify the aspect ratio per the user's choice
- Generate one image per slide, in sequence
- Save outputs to the working directory unless the user specifies otherwise

Return all generated images to the user with a brief note on each slide's role.
