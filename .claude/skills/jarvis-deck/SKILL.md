---
name: jarvis-deck
description: Create branded Jarvis presentation decks (.pptx) that match the official template — correct colors, fonts, layouts, and slide narrative structure. Extends document-skills:pptx.
---

# Jarvis Deck — Branded Presentation Skill

Build polished, on-brand `.pptx` decks for Jarvis strategy, campaigns, sales, and partnerships. Every deck must match the official template exactly.

## Trigger

Use this skill when Passion says:
- `/jarvis-deck`
- "build a deck"
- "create a presentation"
- "make slides for..."
- "put together a deck"

---

## Core Dependencies

This skill **extends `document-skills:pptx`**. Always invoke `document-skills:pptx` as the execution engine. This skill supplies the brand constraints on top of it.

**Design system reference (read this first, every time):**
`.claude/skills/jarvis-deck/assets/deck_template_analysis.md`

**Source template file:**
`projects/Jarvis_Marketing/_templates/Jarvis_-_Spin_up_your_operation_dream_team (1).pdf`
_(Use as visual reference. A .pptx base file should be placed at `projects/Jarvis_Marketing/_templates/deck_template.pptx` when available.)_

---

## Step 1: Clarify the Brief

Before building anything, confirm:

1. **Deck purpose** — sales pitch, strategy deck, campaign brief, partnership proposal, internal review?
2. **Audience** — prospect, partner, team, investor?
3. **Key message** — what is the ONE thing they should leave believing?
4. **Slides needed** — specific slides requested, or full narrative deck?
5. **Output path** — where to save the .pptx file

If the user provides enough context, proceed without asking. Only ask for what's genuinely missing.

---

## Step 2: Map the Narrative Structure

Use the Jarvis narrative arc as the default backbone. Adapt based on deck purpose.

| Act | Slides | Purpose |
|-----|--------|---------|
| **Hook** | 1 | Big cinematic statement — the world has changed or a problem is urgent |
| **Problem Agitation** | 2–4 | Market evidence → pain points → old solutions fail |
| **Solution Introduction** | 5–6 | "What if..." + Jarvis positioning |
| **Product/Service Deep Dive** | 7–12 | Features, proof, process, differentiators |
| **Emotional Close** | 13–14 | Mission statement + engagement question |
| **CTA** | 15 | Clear next step |

Adjust length based on context. A 5-slide intro deck is fine. A 20-slide strategy deck is fine. The arc is the guide.

---

## Step 3: Select Layouts Per Slide

Match each slide's content to the correct layout from the design system. Never freestyle — always use one of these:

| Layout | When to use |
|--------|------------|
| **A — Cinematic Hero** | Cover, mission statements, emotional pivots |
| **B — Full-Width Headline + Content** | Problem slides, competitor takedowns, arguments |
| **C — 3-Column Equal** | Reasons, benefits, 3-part features |
| **D — Left Text + Right Illustration** | Solution intro, retention, matching stories |
| **E — Stats Highlight** | Key metrics (speed, retention, cost savings) |
| **F — Rounded Pill Cards** | Feature/service lists |
| **G — 4 Bordered Cards** | Process steps, vetting stages |
| **H — Two-Column Compare** | Before/after, problem/solution, input/output |
| **I — Dark CTA Close** | Closing slide, next step |
| **J — Centered Question** | Engagement/transition, discussion prompt |

---

## Step 4: Apply Brand Rules (Non-Negotiable)

### Colors — exact values

```
Neon yellow-green:  #CCFF00  (keyword highlights, stats, logo, arrows)
Dark cinematic bg:  #0D0D0D  (dark slides only)
Off-white bg:       #F3F2EF  (light slides only)
Headline text:      #1A1A1A  (on light slides)
Body text:          #333333
Secondary text:     #888888
White text:         #FFFFFF  (on dark slides only)
Red X icon:         #E63946
Green check icon:   #2D7A3A
Keyword box bg:     #111111
```

### Typography

- **Font family:** Barlow Black / Montserrat ExtraBold for headlines (weight 800–900). Regular (400) for body. Bold (600–700) for labels.
- If Barlow is unavailable, use Montserrat or Inter as fallback.
- Headlines: Title case, heavy weight
- Body: Sentence case, regular weight
- NO italic. NO underline. NO all-caps body text.

### The Keyword Highlight Rule

Every headline on every content slide gets **exactly one keyword** highlighted:
- Wrap the key word in a black rectangle (`#111111`)
- Set that word's text color to neon yellow (`#CCFF00`)
- All other headline words stay in dark `#1A1A1A`
- This is the single most important design signature of the Jarvis brand

### Stats Slides

- Large stat number: neon yellow (`#CCFF00`), 60–72px, inside a black rectangle
- Label above: small, regular weight, dark gray
- Description below: small body text

### Bullet Style

- Use `→` (right arrow, plain text) as bullet markers — never round dots or dashes on brand slides
- Red X icons for "things that are wrong/old"
- Green checkmarks for "things that are right/Jarvis"

### Logo Bug (every slide, no exceptions)

- Bottom-right corner, ~20–25px margin
- Composition: Jarvis V-icon in yellow circle + bold JARVIS wordmark
- Must appear on every single slide

### Dark vs. Light Slide Rule

- Dark slides: use for cover, mission, emotional close, CTA only
- Light slides: use for everything informational/logical
- Never mix content types with wrong backgrounds

### Font Sizes (1440×810 canvas)

| Element | Size |
|---------|------|
| Hero headline | 56–72px |
| Content headline | 44–56px |
| Column/section label | 20–24px |
| Body text | 16–18px |
| Stat number | 60–72px |
| Footer | 12px |

---

## Step 5: Build with document-skills:pptx

Hand off to `document-skills:pptx` with:
1. Full slide-by-slide content spec (headline, body, layout type, dark/light)
2. Brand color values above
3. Font specifications above
4. Logo bug placement instruction for every slide
5. Output file path

**Always specify the output path:** `projects/Jarvis_Marketing/decks/[deck-name].pptx`

---

## Step 6: QA Checklist Before Delivering

Before presenting the output, verify:

- [ ] Logo bug present on every slide (bottom-right)
- [ ] Exactly one keyword highlighted per content slide headline
- [ ] Stats use black box + neon yellow text
- [ ] Dark slides only for: cover, mission, emotional close, CTA
- [ ] No italic, no underline, no all-caps body text
- [ ] Arrow bullets `→` used (not dots/dashes)
- [ ] X icons red, checkmark icons green
- [ ] Body text on light slides is dark gray `#333333`, not black
- [ ] Secondary/supporting text is medium gray `#888888`
- [ ] Font weights: headlines 800–900, labels 600–700, body 400

---

## Slide Content Rules

### Writing headlines

- Bold, direct, conversational — not corporate
- End with a period or question mark (Jarvis template always does)
- One idea per slide
- The keyword highlight should land on the most impactful word (a verb or outcome)

### Writing body text

- Short sentences
- No filler phrases ("in order to", "leverage synergies", etc.)
- Results-focused always
- On benefit lists: action verb first ("Source VAs", "Vet candidates", "Match workflows")

### Slide count guidance

| Deck type | Typical slide count |
|-----------|-------------------|
| Quick intro / cold outreach | 5–8 slides |
| Sales deck | 12–18 slides |
| Strategy / campaign brief | 15–25 slides |
| Partnership proposal | 8–12 slides |
| Internal team update | 6–10 slides |

---

## Output

Save to: `projects/Jarvis_Marketing/decks/[descriptive-name].pptx`

Name format: `jarvis-[purpose]-[YYYY-MM-DD].pptx`
Examples:
- `jarvis-sales-deck-2026-04-06.pptx`
- `jarvis-q2-campaign-brief-2026-04-06.pptx`
- `jarvis-partnership-pitch-2026-04-06.pptx`

After building, confirm:
- File path
- Slide count
- Any elements that could not be reproduced from scratch (see assets/deck_template_analysis.md Section 7 — items that must be extracted from source)
