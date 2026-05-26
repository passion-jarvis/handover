# Jarvis Meta Ads — Health Report
**Period:** March 9 – April 7, 2026 (30 days)
**Generated:** 2026-04-08
**Data source:** Ads Manager CSV export (campaign level)

---

## Meta Ads Health Score

```
Meta Ads Health Score: 38/100  Grade: F

Pixel / CAPI Health:  ?/100   ██░░░░░░░░  (30%) — NO DATA, requires Events Manager
Creative:            55/100   █████░░░░░  (30%) — partial (no ad-level breakdown)
Account Structure:   20/100   ██░░░░░░░░  (20%) — critical failures
Audience:            55/100   █████░░░░░  (20%) — frequency good, CPM alarming
```

> Note: Score is suppressed by structural failures and missing Pixel/CAPI data. Fix structure first, then pull Events Manager data to re-score.

---

## Critical Numbers

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Leads/day (US) | ~1/day | 20/day | **-19 leads/day** |
| US daily budget | $60/day | $511/day | **-$451/day** |
| US CPL | $25.56 | <$30 | PASS |
| AU CPL | $44.27 | — | 73% worse than US |
| US CPM | $136.27 | $20-50 | **3-6x too high** |
| AU campaign status | ACTIVE | PAUSED | **NOT PAUSED — still burning $57/day** |

---

## Findings by Category

### Pixel / CAPI Health — UNKNOWN (No Events Manager data)

| Check | Status | Notes |
|-------|--------|-------|
| Pixel installed + firing | UNKNOWN | Need Events Manager screenshot |
| CAPI active | UNKNOWN | Without CAPI, post-iOS 14.5 = 30-40% data loss |
| Event deduplication | UNKNOWN | Need event_id config check |
| EMQ score (Lead event) | UNKNOWN | Need ≥8.0 for quality matching |
| Domain verification | UNKNOWN | — |
| Attribution window | PASS | 7-day click, 1-day view (standard) |
| AU attribution | WARNING | "Multiple attribution settings" — inconsistent, makes comparison unreliable |

**Action required:** Pull Events Manager data. If CAPI is not active, this is the single highest-ROI fix available — up to 40% data recovery.

---

### Creative — 55/100 (Partial)

| Check | Status | Notes |
|-------|--------|-------|
| CTR (US Campaign A) | PASS | 6.09% — strong signal (benchmark ≥1%) |
| CTR (AU Campaign B) | PASS | 2.50% — acceptable |
| Creative formats ≥3 | UNKNOWN | No ad-level data in export |
| Creatives per ad set ≥5 | UNKNOWN | README shows 3 active ads — likely FAIL |
| Creative fatigue signals | UNKNOWN | Need 14-day CTR trend per ad |
| Copy: headline ≤40 chars | UNKNOWN | — |
| Copy: primary text ≤125 chars | UNKNOWN | — |
| UGC/testimonial tested | PARTIAL | UGC ads paused — may have been premature |
| Creative refresh cadence | UNKNOWN | — |

**Known from README:**
- C1-3 (white women surprise): visual winner, 12% CTR historical. Copy updated 2026-04-03 — no performance data yet.
- C1-6 ($300k revenue): Best quality ratio — 2/3 qualified. Should be getting more budget via CBO.
- C1-7, C1-8 (automation angle): New, no data yet.
- UGC female in car + C1-4 + C1-9: Correctly paused — all 0/2 qualified.

**Flag:** Only 3 active creatives. Meta recommends ≥5 per ad set. Under-tested.

---

### Account Structure — 20/100

| Check | Status | Notes |
|-------|--------|-------|
| CBO on US Campaign A | PASS | Correct structure |
| AU Campaign B budget type | WARNING | Using ad set budget ($57/day), not CBO |
| AU campaign paused | **FAIL** | Decision was 2026-04-03. Still active as of data export. Burning ~$57/day unnecessarily. |
| Budget vs lead goal | **FAIL** | $60/day → ~2.3 leads/day. Need $511/day for 20 leads/day. 88% underfunded. |
| Campaign consolidation | WARNING | 20 campaigns total, only 2 active. High inactive clutter. |
| Naming conventions | WARNING | Mixed: brackets, emojis, AU/US prefixes inconsistent |
| Learning phase health | UNKNOWN | Need ad set level breakdown |
| Advantage+ Shopping | N/A | Service business, not e-commerce |
| Budget per ad set ≥5x CPA | PARTIAL | US: $60/day ÷ $25.56 = 2.3x CPA — below recommended 5x |

**The core math problem:**

```
Goal: 20 leads/day
US CPL: $25.56
Budget needed: 20 × $25.56 = $511/day
Current budget: $60/day
Current yield: ~2.3 leads/day

You are 8.5x underfunded for your lead goal.
```

---

### Audience & Targeting — 55/100

| Check | Status | Notes |
|-------|--------|-------|
| US Frequency (7-day) | PASS | 1.20 — healthy (threshold <3.0) |
| AU Frequency (7-day) | PASS | 1.62 — healthy |
| US CPM $136.27 | **WARNING** | 3-6x above typical ($20-50). Indicates very narrow audience or high competition. |
| AU CPM $81.67 | WARNING | High for AU market. Narrow targeting likely. |
| Warm CPM $211.21 | FAIL | This was why warm campaign killed itself |
| Custom Audiences | UNKNOWN | No audience breakdown in export |
| Lookalike Audiences | UNKNOWN | — |
| Advantage+ Audience | UNKNOWN | Not confirmed in data |
| Exclusions configured | UNKNOWN | — |

**CPM interpretation:** $136 CPM means every 1,000 people you reach costs $136. At 6% CTR, that's ~60 clicks per $136 = $2.27 CPC. This is workable only if close rate stays high. The real risk: audience is small and will exhaust fast. Need broader top-of-funnel or Lookalike expansion.

---

## Lead Quality (from README — not in CSV)

| Ad | Leads | Qualified | Quality Rate |
|----|-------|-----------|-------------|
| C1-6: $300k revenue | 3 | 2 | 67% |
| C1-3: White women surprise (old copy) | 6 | 2 | 33% |
| UGC female in car | 2 | 0 | 0% |
| C1-4: $10 vs $500 | 3 | 0 | 0% |
| C1-9: Find your VA | 2 | 0 | 0% |

**Best quality:** C1-6 at 67% qualified. This should be the primary scaling creative.
**Revenue filter in form:** ($0-$5k, $5k-$15k, $15k-$30k, $30k+) — correct, keep it.

---

## Data Gaps — Pull These Before Next Review

1. **Events Manager** — Pixel status, CAPI status, EMQ score for Lead event, dedup rate
2. **Ad-level export** — CTR per creative, spend per ad, 14-day trend
3. **Audience breakdown** — what audiences are targeting each campaign
4. **Ad set breakdown** — learning phase status, budget per ad set

---

## Quick Wins (Ranked by Impact)

### #1 — Pause AU Campaign B NOW
- Saving: $57/day = $399/week
- Decision was already made 2026-04-03
- Reallocate to US Campaign A immediately

### #2 — Increase US budget 3-5x (from $60 → $200-$300/day)
- Current: 2.3 leads/day
- At $200/day: ~7.8 leads/day
- At $300/day: ~11.7 leads/day
- At $25.56 CPL this is still profitable math if even 5% close
- Don't jump to $511/day yet — validate lead quality at $25.56 CPL with new copy first

### #3 — Pull Events Manager data + confirm CAPI is live
- If CAPI is off, you're flying blind on attribution
- This is free ROI — just a setup task
- If EMQ <8.0, add email + phone to form capture

### #4 — Test C1-6 as the main scaling creative
- Highest quality rate (67% qualified)
- Give it dedicated budget to confirm at scale
- C1-3 new copy (updated 2026-04-03) needs 7-10 more days of data before judgment

### #5 — Add more creatives to the active ad set (minimum 5)
- Currently 3 active ads — below Meta's recommended 5
- Test: new static with "$300k revenue" hook + direct call to action
- Test: founder voice (Copy D from README) — not yet live

### #6 — Broaden audience targeting to reduce CPM
- $136 CPM is unsustainable at scale
- Options: test Advantage+ Audience, expand interest targeting, test 1% → 3% Lookalike
- Target CPM: $40-60 for this audience type

---

## Decision Needed

**Scale budget now or wait for copy data?**

- C1-3 copy was updated 2026-04-03 (today is 2026-04-08 = 5 days of data)
- You need 7-14 days minimum to judge new copy
- **Recommendation:** Pause AU today (saves $57/day), redirect $50 to US ($110 total US), wait until 2026-04-15 to evaluate C1-3 new copy, then decide on full budget increase

---

## Hot Lead Follow-Up

| Name | Company | Revenue | Contact | Status |
|---|---|---|---|---|
| Kenneth Spangenberger | Fort Knox EMS | $60k-$100k/mo | dc979@yahoo.com | Email sent 2026-04-03, voicemail full |

Action: Try a different channel — LinkedIn search, company website, second email.

---

## Decision Log

**2026-04-08 — ALL ADS PAUSED**
- US Campaign A: OFF
- AU Campaign B: OFF
- Total spent: $1,342.15 across both campaigns
- Total leads generated: 43
- Total conversions: 0
- Reason: Algorithm trained on wrong audience ($0-5k revenue leads). Walmart employees, school workers, tradespeople — zero business owners at $10k+/month. Zero conversions across full campaign lifetime.
- Lead quality breakdown: ~93% under $5k revenue. Only 1 confirmed qualified lead (Robert York, Genpak, $15-30k) — never converted.

## Restart Conditions (do NOT relaunch until these are met)

- [ ] New Lead Form built from scratch (no duplicates of v2-copy-copy)
- [ ] $0-5k revenue option removed entirely from form (not just disqualified)
- [ ] "Are you the business owner?" qualifier question added
- [ ] Ad copy updated: first line filters by revenue ("If your business does $10k+/month...")
- [ ] Primary creative: C1-6 ($300k revenue hook) — only confirmed qualified leads came from this
- [ ] Shemily outbound running consistently (ads amplify, not replace)

## Next Review Date
**TBD — only after restart conditions are met**
