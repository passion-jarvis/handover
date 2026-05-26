# Jarvis Ads Strategy — Q2 2026

_Last updated: 2026-04-04_

---

## Business Context

**Goal:** 22 → 100 active clients by June 30, 2026 (13 weeks)
**Revenue model:** $1,600/month per client
**Target client:** Business owner doing $10k+/month, still running everything themselves
**Sales motion:** Ad → Lead form → SDR follow-up → Booked call → George closes → Signed

**Math to hit 100 clients:**
- Need 78 more clients in 39 weeks (by Dec 30) = **2 closes/week**
- At 30% close rate = 7 booked calls/week
- At 15% book rate from leads = 47 leads/week = **~7 leads/day target**
- Current rate: 3 leads/day at $60/day → need to roughly 2-3x spend to hit target

---

## Current State (as of 2026-04-03)

| Channel | Status | Performance |
|---------|--------|-------------|
| Meta Ads (US) | Active | Best quality leads. CBO running. C1-6 and C1-3 (new copy) winning |
| Meta Ads (AU) | Paused | No SDR coverage, revisit when US stable |
| Google Search | None | Untapped brand + intent traffic |
| YouTube | None | Untapped video audience |
| LinkedIn | N/A | Too expensive for this ICP, skip |
| TikTok | N/A | Demographic mismatch, skip |

**Lead quality diagnosis:** Broad hooks attracted $0-$5k founders. Fix applied 2026-04-03: income signal in copy line 1. Winner structure: revenue qualifier in line 1 + automation angle + filter copy.

---

## Platform Strategy

### Primary: Meta Ads (70% of budget)
Meta is the proven channel. Highest connect rate, highest close rate. Scale what's working.

**Why Meta works for Jarvis:**
- Business owners scroll FB/IG, not LinkedIn
- CBO auto-allocates to winners — let it run
- Lead form friction filters casually interested
- Video + image + carousel = full creative arsenal

**Strategy:**
- Keep CBO campaign structure — Meta is already learning
- Scale budget 20% per week on winning ad sets only
- Test 2 new creatives per week minimum (one hook variation, one angle variation)
- Retargeting layer: website visitors + form starters who didn't submit

### Secondary: Google Search (10% of budget)
Low volume, high intent. Protect brand. Catch people actively searching.

**Why add Google:**
- "Hire virtual assistant" and "VA service" searches are bottom-funnel
- Brand protection: if competitors run on "Jarvis VA" terms, you're losing warm clicks
- Low CPL for high-intent terms relative to Meta
- Small investment, meaningful close rate uplift

**Strategy:**
- Brand campaign: Jarvis, gojarvis.ai, Jarvis VA (exact + phrase)
- Non-brand: virtual assistant service, hire VA, outsource tasks, business VA
- RLSA layer: bid 50% higher for Meta lead form visitors who didn't convert

### Testing: YouTube (20% of budget)
Business owners watch YouTube. Creator-style video = native, not ad-feeling.

**Why test YouTube:**
- Founder/entrepreneur audience is highly accessible on YouTube
- Can repurpose top Meta video creatives (C1-6 format)
- YouTube retargeting syncs with Google
- 15-30s skippable pre-roll + in-feed discovery = two formats to test

**Strategy:**
- Repurpose C1-6 ("$300k revenue, zero days off") as 30s YouTube pre-roll
- Target: Business owners, entrepreneurs, in-market for business services
- Placement targeting: Gary Vee, Alex Hormozi, BIAB-adjacent channels
- Retargeting: website visitors (30 days)

---

## Targeting

### Meta
- **Cold prospecting:** US business owners 28-55, interests in entrepreneurship, business operations, Shopify, Agency, marketing
- **Income signal:** Household income top 10-25% + homeowner + business page admin
- **Lookalikes:** 1% LAL from existing clients (upload CRM list) + 2% LAL
- **Retargeting:** Website visitors 30d, lead form openers who didn't submit, video viewers 50%+
- **Exclusions:** Current clients, employees, VA job seekers

### Google
- **Brand:** [Jarvis], [gojarvis.ai], [Jarvis virtual assistant]
- **Intent:** virtual assistant service, hire VA, business virtual assistant, VA for business owners
- **Negative:** jobs, freelance VA, VA certification, cheap VA, free VA

### YouTube
- **Audiences:** Business owners, entrepreneurs, company owners (Google audience segments)
- **Placements:** Entrepreneurship, business operations, productivity channels
- **In-market:** Business software and services, HR and staffing

---

## Creative Direction

See [CREATIVE-BRIEF.md](CREATIVE-BRIEF.md) for full production plan.

**Winners to protect (do not kill):**
- C1-6: "$300k revenue, zero days off" — best quality ratio, keep feeding CBO
- C1-3 (updated): White women surprise, 12% CTR, new income-filtered copy

**Creative hypothesis for Q2:**
- Hook structure that wins: Revenue qualifier + pain + automation angle
- Format that wins: Face-to-camera surprise reaction, then pivot to value
- Copy structure that wins: Line 1 = income qualifier → Line 2 = reframe → CTA

---

## Tracking & Attribution

| Platform | Client-Side | Server-Side | Status |
|----------|------------|-------------|--------|
| Meta | Pixel | CAPI recommended | Set up CAPI |
| Google | gtag.js | Enhanced Conversions | Set up when launching |
| YouTube | (Google Ads tag) | (same as Google) | Set up when launching |

**Conversion events to track:**
1. Lead form submit (primary — Meta lead form + website form)
2. Booked call (secondary — GHL integration)
3. Signed client (offline conversion — upload to Meta monthly)

**GHL → Meta offline conversions:** Upload closed deals monthly to train Meta's algorithm on what a real client looks like, not just a lead form submission. This is the single highest-leverage tracking improvement available.

---

## KPI Targets

| Metric | Today | Apr 30 | Jun 30 | Sep 30 | Dec 30 |
|--------|-------|--------|--------|--------|--------|
| Leads/day | 3 | 5 | 7 | 10 | 12+ |
| Qualified leads/day | ~1 | 2-3 | 3-4 | 5 | 6+ |
| CPL | $20.75 | <$20 | <$18 | <$16 | <$15 |
| Booked calls/week | TBD | 4 | 7 | 10 | 10+ |
| Closes/week | TBD | 1 | 2 | 3 | 3+ |
| Active clients | 22 | 26 | 38 | 60 | 100 |
| Ad spend/month | $1,800 | $3,000 | $4,500 | $7,000 | $9,000 |

---

## Decision Rules

1. **Scale rule:** CPA consistently under target for 2 consecutive weeks → increase budget 20%
2. **Kill rule:** Ad set at 3x target CPA for 7+ days → pause
3. **Creative kill:** CTR 50% below account average after 1,000 impressions → kill
4. **Platform kill:** Platform at 2x Meta CPL with no improvement after 4 weeks → cut
5. **Budget lock:** Never increase any campaign >20% in a single week — breaks learning phase

---

## Weekly Review Cadence

| Day | Action |
|-----|--------|
| Monday | Pull numbers: leads, quality rate, CPL, calls booked, closes |
| Tuesday | Creative decisions: what to pause, what to scale, what to test next |
| Thursday | New creatives live for weekend traffic |
| Friday | Budget check: pacing on target? |
