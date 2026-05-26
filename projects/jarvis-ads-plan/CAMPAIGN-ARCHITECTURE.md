# Jarvis Campaign Architecture — Q2 2026

_Last updated: 2026-04-04_

---

## Naming Convention

```
[Platform]_[Objective]_[Funnel Stage]_[Audience]_[Geo]_[YYYYQX]
```

Examples:
- `META_CONV_TOP_ColdProspecting_US_2026Q2`
- `META_CONV_BOT_Retargeting_US_2026Q2`
- `GOOGLE_SEARCH_Brand_US_2026Q2`
- `YT_VIDVIEW_TOP_Entrepreneurs_US_2026Q2`

---

## Meta Ads Architecture

```
Meta Business Account
│
├── C1: Cold Prospecting (CBO) ✅ ACTIVE
│   │   Budget: CBO — auto-distributes to winners
│   │   Objective: Leads (Instant Form)
│   │   Geo: United States
│   │
│   ├── C1-6: $300k Revenue Hook [WINNER — protect]
│   │   Copy: Automation angle, income qualifier in line 1
│   │   Format: Video/image (face-to-camera)
│   │   Status: Active, getting most CBO budget
│   │
│   ├── C1-3: White Women Surprise (updated 2026-04-03) [WINNER — test]
│   │   Copy: Updated with $10k/$20k/$30k qualifier in line 1
│   │   Format: Image/video (12% CTR)
│   │   Status: Active — monitor quality through 2026-04-08 review
│   │
│   ├── C1-7: Automation angle variation [NEW — no data]
│   │   Status: Active — needs 7 days of data
│   │
│   ├── C1-8: Automation angle variation 2 [NEW — no data]
│   │   Status: Active — needs 7 days of data
│   │
│   └── [New test slots — rotate 2/week]
│       Next up: Client testimonial angle, "I fired myself" hook
│
├── C2: Retargeting (Manual budgets) 🔜 BUILD
│   │   Budget: $15/day
│   │   Objective: Leads
│   │
│   ├── Website Visitors (30 days)
│   │   Exclusion: Already submitted lead form
│   │   Copy: More direct, acknowledge they've seen Jarvis
│   │
│   ├── Lead Form Openers — Didn't Submit (14 days)
│   │   Copy: Remove friction, simpler CTA
│   │
│   └── Video Viewers 50%+ (30 days)
│       Copy: Move toward offer, add social proof
│
└── C3: Lookalike Scaling 🔜 BUILD (after client list upload)
    │   Budget: $13/day (start small, scale with data)
    │   Objective: Leads
    │
    ├── 1% LAL — Existing Clients (upload from CRM)
    └── 2% LAL — Existing Clients
```

---

## Google Ads Architecture

```
Google Ads Account (NEW — build April)
│
├── Brand Search Campaign
│   Budget: $10/day
│   Bidding: Target CPA → Maximize Conversions
│   │
│   ├── Ad Group: Brand Core
│   │   Keywords: [jarvis], [gojarvis], [gojarvis.ai], [jarvis va], [jarvis virtual assistant]
│   │   Match: Exact + Phrase
│   │
│   └── Ad Group: Brand Navigational
│       Keywords: [jarvis va service], [hire jarvis va]
│
└── Non-Brand Intent Campaign
    Budget: $5/day (test in April, scale in May)
    Bidding: Maximize Clicks (cap $8 CPC) → shift to Target CPA after 30 conversions
    │
    ├── Ad Group: High Intent — VA Hire
    │   Keywords: hire virtual assistant, virtual assistant service, business virtual assistant
    │   hire a va, va for business, outsource to va
    │
    ├── Ad Group: High Intent — Delegation
    │   Keywords: outsource business tasks, hire someone to run my business, business operations help
    │   delegate tasks, business support service
    │
    └── Ad Group: Competitor Adjacent (test)
        Keywords: [competitor] alternative, best va service, va service comparison
        Note: Do NOT bid on competitor brand names — against Google policy
```

---

## YouTube Architecture

```
YouTube (via Google Ads) — Build May
│
├── Pre-Roll Prospecting (TrueView In-Stream)
│   Budget: $13/day (launch May)
│   Objective: Leads / Website traffic
│   Bidding: Target CPV or Target CPA
│   │
│   ├── Audience: Business Owners
│   │   Segments: Business owners, entrepreneurs, small business owners
│   │   In-market: Business services, HR and staffing
│   │   Age: 28-55
│   │
│   └── Placement: Entrepreneur Channels
│       Channels: Productivity, business growth, scaling, entrepreneurship
│       Suggested: Alex Hormozi-type channels, Gary Vee-adjacent
│
└── In-Feed Discovery
    Budget: $10/day (launch June if pre-roll tests positive)
    Objective: Views → warm traffic → retarget
    │
    └── Audience: Lookalike from Meta warm audience
        Copy: Same winning hooks from Meta — "$300k revenue, zero days off"
```

---

## Lead Form Structure (Meta)

Current form should include (verify this is active):
- [ ] Revenue qualifier: $0-5k / $5k-15k / $15k-30k / $30k+
- [ ] Business type field
- [ ] Phone number (required for SDR follow-up)
- [ ] "What's your biggest challenge running your business?" (open text)

**Disqualify automatically:** Anyone selecting $0-$5k → route to waiting list, not Shemily's queue.

---

## Audience Building Checklist

- [ ] Upload existing client list to Meta Custom Audiences (minimum 100 emails)
- [ ] Create 1% LAL from client list
- [ ] Create 2% LAL from client list
- [ ] Create website visitor custom audience (30d, 14d, 7d)
- [ ] Create lead form opener audience (14d)
- [ ] Create video viewer audience (50%+, 30d)
- [ ] Create Google RLSA audience from Meta traffic (30d)
- [ ] Set up offline conversion import (GHL → Meta — signed clients)
