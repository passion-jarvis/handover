# Jarvis Deck Template — Design System Reference

_Source: `deck_template.pptx` / `Jarvis_-_Spin_up_your_operation_dream_team (1).pdf`_
_Analyzed: 2026-04-06 | 18 slides_

---

## 1. COLOR SYSTEM

### Background Colors

| Name | Hex (approx) | Used on |
|------|-------------|---------|
| Dark cinematic | `#0D0D0D` (+ space photo overlay, darkened) | Slides: cover, feature list, mission, CTA close |
| Off-white content | `#F3F2EF` | All informational/content slides |

### Accent Colors

| Name | Hex (approx) | Role |
|------|-------------|------|
| Neon yellow-green | `#CCFF00` | JARVIS wordmark, keyword highlight boxes, stat numbers, arrows, logo icon |
| Black (highlight bg) | `#111111` | Background box behind highlighted keyword |
| White | `#FFFFFF` | All text on dark slides |
| Dark text | `#1A1A1A` | Headlines on light slides |
| Medium gray | `#888888` | Secondary/supporting body text on light slides |
| Dark gray | `#333333` | Primary body text on light slides |
| Red | `#E63946` | X-mark icons (competitor comparison) |
| Dark green | `#2D7A3A` | Checkmark icons (benefit lists) |

### Color Usage Rules

- **Dark slides** = cinematic, emotional moments: cover, mission statements, closing CTA
- **Light slides** = logical content: arguments, data, features, process steps
- **Neon yellow** = reserved for the single most important word in a headline (black box, yellow text)
- **Stats** = large neon yellow number inside a black rectangle (slide 10 pattern)
- Never use neon yellow as a general body color — only for emphasis

---

## 2. TYPOGRAPHY

### Fonts

| Element | Font | Notes |
|---------|------|-------|
| JARVIS wordmark | Custom distressed display font, all-caps | Extract from original asset — cannot be reproduced |
| Headlines | Barlow Black or Montserrat ExtraBold (weight 800–900) | Heavy geometric sans-serif |
| Body text | Same family, Regular (weight 400) | |
| Subheadings / labels | Same family, Bold (weight 600–700) | |

### Text Style Rules

- Headlines: Title case, black/extrabold weight, no letter-spacing
- One keyword per slide headline gets the highlight treatment (black rect + neon yellow text)
- Body text: Sentence case, regular weight, dark gray `#333333`
- Secondary/supporting text: Regular weight, medium gray `#888888` (visually de-emphasized)
- Arrow bullets: `→` plain text character (not icons), dark gray
- No underlines. No italic. No all-caps body text.

### Font Sizes (approximate, 1440×810 canvas)

| Element | Size |
|---------|------|
| Hero headline (dark slides) | 56–72px |
| Content headline (light slides) | 44–56px |
| Column/section label | 20–24px |
| Body / description | 16–18px |
| Stat numbers (highlight boxes) | 60–72px |
| Footer / URL | 12px |

---

## 3. LAYOUT PATTERNS

### Layout A — Cinematic Hero (dark slides)
**Used for:** Cover, mission statement, emotional pivots
- Full-bleed dark photo (space/earth), heavily darkened overlay
- White bold headline: centered or left-aligned, large
- JARVIS wordmark: top-center (neon yellow)
- Logo bug: bottom-right (always)
- Optional: URL/handle bottom-right instead of logo bug (cover only)

### Layout B — Full-Width Headline + Content Below (light)
**Used for:** Problem statements, competitor takedowns, argument slides
- Off-white background
- Large black headline spanning full width, top-left
- Content directly below (list, grid, or copy)
- Logo bug: bottom-right

### Layout C — 3-Column Equal (light)
**Used for:** Reasons, benefits, features in threes
- Headline top
- 3 equal-width columns below
- Each column: bold label + body description
- Optional: keyword highlight in headline
- Logo bug: bottom-right

### Layout D — Left Text + Right Illustration (light)
**Used for:** Solution introduction, culture/retention, matching engine
- Left ~50%: text/copy block
- Right ~50%: flat vector illustration
- Logo bug: bottom-right

### Layout E — Stats Highlight (light)
**Used for:** Key metrics (speed, retention, time saved)
- Headline top
- 3 columns, each: small category label → large neon stat in black box → explanatory text below
- Logo bug: bottom-right

### Layout F — Rounded Pill Cards (dark or light)
**Used for:** Feature/service lists
- Pill-shaped cards (high border-radius ~30px), light gray fill
- 1 or 2 columns, staggered or flush
- Text inside cards: bold, no icons
- On dark slides: semi-transparent dark fill pills

### Layout G — 4 Equal Bordered Cards (light)
**Used for:** Process steps, vetting stages
- 4 cards in a row
- Rounded corners, 1px border, no fill (white bg)
- Content: bold title + body text, centered
- Logo bug: bottom-right

### Layout H — Two-Column Compare (light)
**Used for:** Input → output, problem → solution, quote → match
- Left column: gray/muted text (the "before" or "problem")
- Right column: bold checklist (the "after" or "solution")
- Column headers in bold
- Logo bug: bottom-right

### Layout I — Dark CTA Close (dark)
**Used for:** Closing slide, next step
- Dark background
- JARVIS wordmark: top-left (neon yellow)
- Large bold headline + contact info: left side
- Flat illustration: right side
- Large neon yellow arrow graphic rising upward
- Logo bug: bottom-right

### Layout J — Centered Question (light)
**Used for:** Engagement/transition slides, discussion prompts
- Off-white background
- JARVIS wordmark: top-center (black)
- Large centered bold question
- Illustration centered below
- Logo bug: bottom-right

---

## 4. DECORATIVE ELEMENTS

| Element | Description | Reproducible? |
|---------|-------------|--------------|
| Neon keyword highlight box | Black rect behind 1 word in headline, text color = `#CCFF00` | Yes — shape + text color |
| Rounded pill cards | `border-radius: 30px`, light gray fill `#E8E8E8` | Yes |
| Bordered feature cards | `border-radius: 12px`, `border: 1px solid #CCCCCC`, no fill | Yes |
| Arrow bullets `→` | Plain text character, dark gray | Yes |
| Red X icons | Simple icon, competitor slides | Yes (use icon library) |
| Green checkmark icons | Simple icon, benefit/solution slides | Yes (use icon library) |
| Earth/space photography | Full-bleed, heavily darkened overlay | Extract from original |
| JARVIS distressed wordmark | Custom lettered logo, all-caps | Extract from original |
| Flat vector illustrations | People/scenes in yellow-green tones, multiple slides | Extract from original |
| Large neon yellow arrow | Rising arrow graphic, closing slide | Extract from original |

---

## 5. RECURRING ELEMENTS

### Logo Bug (every single slide, no exceptions)
- Position: **bottom-right corner**, ~20–25px from edges
- Composition: triangle/V-shape icon inside neon yellow circle + bold "JARVIS" wordmark
- Size: ~32px tall
- This is the one non-negotiable element on every slide

### Cover Slide Exceptions
- Large JARVIS wordmark: **top-center**, neon yellow, large
- Standalone logo mark: **bottom-left**, larger size
- `www.gojarvis.ai` + `@gojarvis.ai`: **bottom-right** (replaces logo bug)

### Section/Transition Slides
- JARVIS wordmark: **top-center** (black text on light bg) or **top-left** (neon yellow on dark bg)

### What Never Appears
- Page numbers
- Horizontal dividers / rules
- Header bars
- Drop shadows on text
- Italic text

---

## 6. SLIDE NARRATIVE STRUCTURE

The 18-slide deck follows a proven sales narrative arc. When building new decks, map to this structure:

| Act | Slides | Purpose |
|-----|--------|---------|
| **Hook** | 1 | Big cinematic statement — world has changed |
| **Problem Agitation** | 2–5 | Market evidence → pain points → old solutions fail |
| **Solution Introduction** | 6–7 | "What if..." + brand positioning |
| **Product Deep Dive** | 8–15 | Features, proof, process, differentiators |
| **Emotional Close** | 16–17 | Mission + engagement question |
| **CTA** | 18 | Clear next step |

---

## 7. WHAT TO EXTRACT vs. RECREATE

| Must extract from source file | Can build from scratch |
|-------------------------------|----------------------|
| JARVIS distressed wordmark (PNG/SVG) | All layout structures |
| Earth/space photography | Keyword highlight box |
| Flat vector illustrations | Pill cards + bordered cards |
| Large yellow arrow (closing slide) | Typography hierarchy |
| Logo bug (icon + wordmark combo) | Arrow bullets, X/checkmark icons |
|  | Color system |
|  | Spacing and alignment rules |
