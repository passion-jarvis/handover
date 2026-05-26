# Marketing Audit: Jarvis
**URL:** https://gojarvis.ai/
**Date:** 2026-04-20
**Business Type:** Agency/Services — VA matching + automation for $10K+/month business owners
**Overall Marketing Score: 54/100 (Grade: D)**

---

## Executive Summary

Jarvis scores 54/100 — below average with fixable problems. The product is genuinely differentiated (VA + automation bundle at an offshore price point) but the website barely communicates it. The biggest strength is trust signals: named testimonials with specific outcomes, a 14-day money-back guarantee, and a 200-applicant vetting claim. The biggest gap is SEO — almost no keyword targeting, broken meta tags, and a blog with 37 posts that are entirely off-ICP.

Three actions that would move the needle most, in order:

1. **Fix SEO fundamentals.** Title tags, meta descriptions, and schema are essentially broken site-wide. This is 2-3 hours of Shopify admin work and the single highest-leverage fix available right now.
2. **Collapse four CTAs to one.** "Start Your Plan," "See How It Works," "Book a Free Strategy Call," and "Start my free pre-audit" are competing. Pick one. "Book a Free Strategy Call" or "Start my free pre-audit" — not both.
3. **Fix the About/Team pages and put Passion's face on the homepage.** Founders doing $10K+/month do due diligence before spending $1,600/month. Missing "who is behind this" pages actively kill conversion.

Implementing all recommendations conservatively estimates $8,000-$25,000/month in additional revenue through higher conversion rates and organic traffic.

---

## Score Breakdown

| Category | Score | Weight | Weighted Score | Key Finding |
|----------|-------|--------|----------------|-------------|
| Content & Messaging | 67/100 | 25% | 16.75 | VA+automation bundle buried — should be the headline, not a feature bullet |
| Conversion Optimization | 51/100 | 20% | 10.20 | Pricing page 404 + 4 competing CTAs actively costing leads |
| SEO & Discoverability | 28/100 | 20% | 5.60 | No keyword targeting, broken meta tags, off-ICP blog content |
| Competitive Positioning | 52/100 | 15% | 7.80 | Real differentiator exists but not exploited; no comparison pages |
| Brand & Trust | 62/100 | 10% | 6.20 | Team/About pages 404; founder face missing from homepage |
| Growth & Strategy | 71/100 | 10% | 7.10 | Good channel mix, weak compounding loops, hourly pricing framing hurts |
| **TOTAL** | | **100%** | **53.65 → 54/100** | |

---

## Quick Wins (This Week)

**1. Fix title tag and meta description on the homepage**
- Current title: `Efficient, Scalable Virtual Assistants for Small Businesses and Agency – Jarvis` (grammatically broken)
- Fix: `Hire Pre-Trained Virtual Assistants for Business Owners | Jarvis`
- Meta: `Jarvis matches $10K+/month business owners with pre-trained VAs + automations. Stop doing everything yourself. Start your free consultation.`
- Shopify admin → Themes → Edit default theme content. 30 minutes.

**2. Collapse to one primary CTA**
- Remove "Start Your Plan" and "See How It Works" from the primary CTA position
- Make "Book a Free Strategy Call" the hero CTA. Make "Start my free pre-audit" the secondary opt-in below the fold.
- Four CTAs = no clear action = lower conversion.

**3. Fix the broken blog post URL slug**
- One post has raw HTML in the slug: `h3-data-mce-fragment-1-what-is-a-virtual-assistant...`
- Delete or 301-redirect to `/blogs/blogs/what-is-a-virtual-assistant`
- This URL will never rank and signals poor content hygiene to Google.

**4. Add a price anchor to the homepage**
- Add one line in the hero section: "Most clients start at $1,600/month. That's a full-time, pre-trained VA plus automations."
- Qualifies visitors before they book, reduces no-show rate.

**5. Fix the broken Organization schema**
- 7 of 9 `sameAs` social links are empty strings in the structured data
- Fill them in or remove the empty ones. Empty strings in schema are actively worse than no schema.
- Shopify → Edit code → `theme.liquid` → find the JSON-LD block.

**6. Rewrite the "200+ engagements" stat**
- "Engagements" is meaningless. Change to "200+ client reviews" or "22 retained clients at 4.9/5"
- The retained client count (22 paying clients) is more trust-building than a vague engagement number.

**7. Move risk reversals above the fold**
- "14-day money-back guarantee," "5-day onboarding," and "vetted from 200+ applicants" are the three biggest objection killers for this buyer
- Move all three into the hero section. Right now they're buried.

---

## Strategic Recommendations (This Month)

**1. Build About page + Team page and put Passion's face on the homepage**
- Founders doing $10K+/month Google everything before spending $1,600/month
- Missing team/about pages are a trust kill signal, especially for a service business
- Include Passion's photo, background, why Jarvis exists, and a brief team section
- Link @passionya and LinkedIn — personal brand builds founder trust for the service brand

**2. Give the VA + automation bundle its own page section (not a bullet point)**
- This is the only differentiator no competitor has. Belay, Wishup, MyOutDesk all sell VAs. None bundle automations.
- Build a 3-panel visual: "Your VA handles [list] → Automations handle [list] → You focus on [growth activities]"
- Frame it as a system, not a feature. "Jarvis doesn't give you a task-doer. It gives you an operations layer."

**3. Build 3 competitor comparison pages**
- Jarvis vs Belay, Jarvis vs Wishup, Jarvis vs MyOutDesk
- These pages capture in-market buyers who are already comparing options — highest-intent traffic possible
- Each page should address: pricing, onboarding speed, automation inclusion, vetting process, and support
- Target keywords: "Jarvis vs Belay," "Belay alternative," "virtual assistant service comparison"

**4. Reframe pricing from hourly to monthly retainer**
- "$10/hr" invites comparison to Upwork and Fiverr. "$1,600/month retainer" doesn't.
- Same math. Completely different psychological purchase.
- Build a pricing page (currently 404 at `/pricing` but accessible at `/pages/virtual-assistant-pricing`) with clear tiers, deliverables per tier, and one CTA per tier.

**5. Rewrite blog content to target buyer-intent keywords**
- 37 posts exist but are off-ICP ("building happy teams," "9 red flags in job interviews")
- Noindex or delete off-topic posts, replace with:
  - "Virtual assistant vs in-house employee cost comparison" — transactional, high intent
  - "What does a virtual assistant do for bookkeeping?" — targets the financial function ICP
  - "How to hire a VA for your $10K/month business" — direct ICP targeting
  - "Best virtual assistant services for agency owners 2025" — captures competitor searches

**6. Build an FAQ section above the footer**
- Address the top silent objections: "What if the VA isn't a good fit?", "How long before I see results?", "Do I need to train them?"
- Add FAQPage schema markup to this section for Google rich snippets

---

## Long-Term Initiatives (This Quarter)

**1. SEO content engine: "VA for [niche]" landing pages**
- Build 5-10 niche-specific landing pages: VA for real estate agents, VA for agency owners, VA for e-commerce founders, VA for consultants, VA for coaches
- Each page targets a specific keyword cluster and speaks to that ICP's specific pain
- This is how Jarvis builds organic traffic that compounds without ongoing ad spend

**2. Referral system → compounding growth loop**
- Current: Ruth manually asks 2x/day. That's a behavior, not a system.
- Build: Automated trigger (30 days after onboarding) → Ruth's personalized ask → incentive structure (cash credit, free month, upgraded service) → tracking in GHL
- A referred client has a higher close rate, lower CAC, and higher LTV than any other channel
- Goal: 5 referral leads per week compounding monthly

**3. Google Business Profile + review engine**
- Set up GBP as a service-area business (United States)
- Systematically request Google reviews from all 22 current clients via Ruth's check-in cadence
- Target: 20+ Google reviews within 60 days, 50+ within Q2
- This feeds both trust signals for direct visitors and visibility in AI-generated search summaries

---

## Detailed Analysis by Category

### Content & Messaging Analysis (67/100)

**What's working:**
- "Scale Without Burnout" passes the 5-second test — emotionally resonant, target audience self-identifies immediately
- "Vetted from 200+ applicants" is strong differentiation — most VA services don't quantify screening
- Nelson Chen's testimonial ("2x revenue, 16-day vacation") is the strongest proof asset on the page — sells the dream outcome
- 14-day money-back guarantee reduces risk friction meaningfully
- Case study metrics (72% faster responses, 40+ hours saved) are specific enough to be credible

**What's weak:**
- Subheadline ("Automate, delegate, accelerate growth") is generic — every VA service and SaaS says this. It wastes the most-read real estate after the headline.
- VA + automation bundle is the real differentiator and it's buried. This is a features bullet, not the headline promise. No competitor does this at this price point.
- "Elite virtual assistants" signals nothing — every VA company says this.
- Features list reads like a job description, not outcomes. "Calendar & inbox management" should be "Your calendar stays full. Your inbox stays zero. You stop being the bottleneck."
- Pain points aren't dramatized. There's no "you're doing $10K/month and you're still answering every email yourself" moment.
- Copy voice is corporate-neutral. The positioning should be assertive and founder-to-founder. Right now it sounds like a SaaS landing page from 2019.

### Conversion Optimization Analysis (51/100)

**Critical issues:**
- Pricing page 404 is the single biggest conversion leak. Founders doing $10K+/month are analytical. A 404 on Pricing = trust drop + immediate exit. (Note: actual URL is `/pages/virtual-assistant-pricing` — update the nav link.)
- Four competing CTAs create decision paralysis. "Start Your Plan," "See How It Works," "Book a Free Strategy Call," "Start my free pre-audit" — four asks pulling in four directions.
- "Start Your Plan" is ambiguous — what plan? What happens after clicking?
- "Free pre-audit" and "free strategy call" are competing lead magnets with no hierarchy. Pre-audit wins as the lead magnet (gives a deliverable), strategy call becomes the follow-up.
- No price anchor on homepage — "75% less than U.S. alternatives" means nothing without a number.
- No FAQ addressing the primary objection: "What if the VA isn't a good fit?"
- No urgency mechanism — nothing about limited spots, cohort onboarding, or waitlist.
- No video proof — a 60-second founder or client video would significantly lift conversion for a high-ticket service.

### SEO & Discoverability Analysis (28/100)

**Critical findings:**
- Site is built on Shopify with `/pages/[slug]` routing — all internal pages are live at the correct URLs. Not a broken site.
- Title tag is broken: `Efficient, Scalable Virtual Assistants for Small Businesses and Agency – Jarvis` — grammatically incorrect, no target keywords.
- Meta description: `Hire a Jarvis Assistant Work Less = FREEDOM in How You Grow` — not a sentence, no keywords, no CTA. Google will auto-generate this.
- Interior pages have zero meta descriptions — every page is indexed with no description.
- Organization schema has 7 of 9 `sameAs` fields as empty strings — worse than no schema.
- Blog exists (37 posts at `/blogs/blogs/`) but content is off-ICP: "building happy teams," "9 red flags in job interviews."
- One URL slug contains raw HTML: `h3-data-mce-fragment-1-what-is...` — will never rank.
- No keyword targeting on any page. Homepage H1 is "Automate, delegate, accelerate, growth" — zero search intent match.

**Target keywords the site should own:**
- `hire virtual assistant for business` (transactional)
- `virtual assistant for agency owners` (niche ICP)
- `virtual assistant automation bundle` (unique differentiator)
- `VA matching service` (category)
- `outsource business tasks` (high volume)
- `bookkeeping virtual assistant` (financial function ICP)

### Competitive Positioning Analysis (52/100)

**Landscape:**
- Premium US-based tier (Belay, Boldly, Time Etc): $40-75/hr, high trust, slow onboarding — targets established companies
- Budget/offshore tier (Wishup, Magic, MyOutDesk, Fancy Hands): price competitive, high churn — commodity race
- Jarvis sits in the gap: offshore pricing + premium onboarding + automation layer. This is a real wedge that the website doesn't explicitly communicate.

**Positioning gaps:**
- "Scale Without Burnout" could be a SaaS tool, a coaching program, or a supplement brand. Doesn't signal VA + automation.
- The $10K+/month qualifier is in the subtext — not the headline. Founders self-select out before reading far enough.
- Automation is listed as a feature alongside "calendar/inbox" — it needs its own section. It's a system transformation, not a task.
- "75% less" is logically weak without a comparison point. "$1,600/month vs $3,500+ for a U.S. VA alone from Belay" hits harder.
- No competitor comparison pages — Jarvis is letting competitors define the narrative on searches like "Belay alternative."
- No category creation language. "Virtual assistant" joins a crowded category. "Done-for-you operations layer for $10K+/month founders" creates one.

### Brand & Trust Analysis (62/100)

**What's working:**
- Named testimonials with outcomes (revenue, vacation, backend organization)
- 4.9/5 rating with specific case study metrics
- Risk reversals: 14-day money-back + 5-day onboarding + 200-applicant vetting
- Client logos present

**What's broken:**
- Team page and About page both 404 (visible in Shopify nav as broken links) — major due diligence failure for B2B service
- Passion's personal brand (@passionya, 111K) is completely disconnected from Jarvis — missed trust lever
- Hourly pricing ($10/hr) commoditizes the service before the conversation starts
- No founder story or mission statement visible
- No visible case studies with before/after numbers — testimonials are there, but case studies with revenue impact are stronger

### Growth & Strategy Analysis (71/100)

**What's working:**
- Meta ads as primary inbound is the right highest-ROI channel for this offer
- Multi-channel mix (inbound + outbound + referral + content) reduces single-point failure
- 42 warm leads from form submissions is an underutilized asset (email re-engagement)
- Creator partnerships are smart — borrowed trust from aligned audiences

**What's weak:**
- No compounding growth loop. Linear model: spend → lead → close → repeat. Referral engine needs to be a system, not a daily manual ask.
- Hourly pricing framing is the weakest possible model for a premium B2B retainer service.
- No visible retention story on the homepage — no average client tenure, no dedicated account manager mention, no replacement guarantee.
- Expansion revenue is invisible — upsell from 1 VA to 2, automation builds as add-on, premium tier. None of this is marketed.

---

## Competitor Comparison

| Factor | Jarvis | Belay | Wishup | MyOutDesk |
|--------|--------|-------|--------|-----------|
| Headline Clarity | 6/10 | 8/10 | 7/10 | 6/10 |
| Value Prop Strength | 7/10 | 7/10 | 6/10 | 5/10 |
| Automation Bundled | 10/10 | 1/10 | 2/10 | 2/10 |
| Trust Signals | 6/10 | 9/10 | 7/10 | 8/10 |
| Pricing Clarity | 4/10 | 7/10 | 8/10 | 6/10 |
| SEO Strength | 2/10 | 8/10 | 7/10 | 9/10 |
| Comparison Pages | 0/10 | 6/10 | 8/10 | 7/10 |
| Content Marketing | 2/10 | 8/10 | 7/10 | 9/10 |

Jarvis wins on automation differentiation — and loses everywhere else. That gap is entirely fixable.

---

## Revenue Impact Summary

| Recommendation | Est. Monthly Impact | Confidence | Timeline |
|---------------|---------------------|------------|----------|
| Fix title tags + meta descriptions (SEO) | $1,000-3,000 | Medium | 4-8 weeks |
| Fix pricing page 404 | $2,000-5,000 | High | This week |
| Collapse to one CTA | $500-1,500 | High | This week |
| Add price anchor on homepage | $1,000-2,000 | High | This week |
| Build competitor comparison pages | $2,000-6,000 | Medium | 3-4 weeks |
| Rewrite blog to target ICP keywords | $1,500-4,000 | Medium | 6-8 weeks |
| Fix About + Team pages | $500-2,000 | High | 2 weeks |
| Reframe hourly to monthly retainer pricing | $1,000-3,000 | High | 2 weeks |
| Build referral system | $2,000-8,000 | Medium | 4-6 weeks |
| **Total Potential** | **$11,500-$34,500/mo** | | |

---

## Financial VA Capabilities (for Marketing Content)

### What a Jarvis VA Handles Manually

**Bookkeeping**
- Categorize transactions in QuickBooks, Xero, or Wave weekly
- Reconcile bank and credit card statements monthly
- Maintain chart of accounts
- Log owner draws and reimbursements
- Code receipts to correct expense categories
- Flag uncategorized or duplicate transactions for founder review

**Invoice & Billing**
- Draft and send client invoices on schedule
- Track outstanding invoices and due dates
- Follow up on overdue payments (Day 1, Day 7, Day 14 sequences)
- Apply payments and mark invoices as paid
- Handle billing disputes and client questions
- Generate recurring invoices for retainer clients

**Expense Tracking**
- Collect and organize receipts from email, Slack, or shared folders
- Enter expenses into accounting software or spreadsheets
- Reconcile expense reports from team members
- Track subscription renewals and vendor charges
- Flag unusual charges or spending spikes

**Financial Reporting**
- Pull monthly P&L and format into a clean report
- Build weekly cash position summaries
- Track actuals vs budget
- Compile AR aging reports (what's owed and how old)
- Compile AP reports (what you owe and when it's due)

**Vendor & Contractor Coordination**
- Collect W-9s from new contractors
- Track contractor payment schedules
- Send payment reminders and coordinate ACH/wire timing
- Reconcile vendor invoices against purchase orders

**Payroll Support**
- Collect timesheets and flag discrepancies
- Prepare payroll summary for approval
- Track PTO balances
- Coordinate onboarding paperwork for new hires

**Tax Prep Support**
- Organize deductible receipts by category before year-end
- Compile mileage logs and home office documentation
- Pull together 1099-eligible contractor payments and request 1099s
- Track quarterly estimated tax deadlines
- Gather documents for accountant handoff

---

### What Gets Automated (with Tools)

**Zapier / Make**
- New invoice created → auto-email to client with payment link
- Payment received → Slack notification to founder + CRM deal stage update
- Expense submitted → auto-categorized + logged in spreadsheet
- Overdue invoice at 7 days → automated payment reminder sequence triggered
- Monthly report date → auto-pull from QuickBooks + populate Google Sheet template

**QuickBooks / Xero Native**
- Recurring invoices auto-generated and sent on schedule
- Bank feeds auto-imported daily (no manual downloads)
- Rules-based transaction categorization ("Stripe" always codes to "Revenue")
- Automatic payment matching when client pays via ACH or card
- Scheduled reports emailed to founder weekly (P&L, cash balance, AR)
- Late payment fees auto-applied after set number of days

**Invoice Auto-Generation Triggers**
- Project marked complete in Asana/Notion → invoice auto-created in QuickBooks
- Subscription renewal date hit → invoice auto-sent via Stripe/Chargebee
- Time tracked in Toggl/Harvest exceeds threshold → invoice draft generated

**Cash Flow Tracking**
- Real-time bank balance via Plaid
- 30/60/90-day cash projection auto-updated from open invoices and scheduled bills
- Alerts triggered when cash drops below defined threshold

---

### VA + Automation Power Moves (the combination Jarvis uniquely offers)

| Automation handles | VA adds on top |
|--------------------|----------------|
| Auto-sends invoices | Reviews each for accuracy, handles exceptions and disputes |
| Categorizes 90% of transactions | Codes the 10% that don't match rules using judgment |
| Sends payment reminders | Picks up the phone or writes personalized follow-ups for non-payers |
| Generates P&L report | Formats it, adds commentary, flags action items for founder |
| Tracks contractor payments | Manages the relationship — answers questions, collects missing docs |
| Sends late payment alerts | Negotiates payment plans, renegotiates terms when needed |
| Runs payroll calculations | Resolves discrepancies, answers employee questions, handles edge cases |

**Core marketing insight:** Automation handles volume and consistency. The VA handles judgment, relationships, and exceptions. You need both. Automation without a VA creates errors that pile up unnoticed. A VA without automation wastes 60% of their time on tasks a $10/month tool should handle. Jarvis delivers both for $1,600/month — less than what most businesses pay for a part-time bookkeeper alone.

---

### Ready-to-Use Marketing Copy

> "Your finances are running on memory and manual work. A Jarvis VA sets up the automations, manages the exceptions, and sends you a clean report every Monday. One hire. No bookkeeping headaches. No missed invoices. No surprises."

---

## Next Steps

1. **This week:** Fix homepage meta title/description, collapse CTAs to one, add price anchor, fix the Pricing nav link to point to `/pages/virtual-assistant-pricing`
2. **Next 2 weeks:** Build About + Team pages, add Passion's photo to homepage, reframe pricing from hourly to monthly retainer
3. **This month:** Build 3 competitor comparison pages, give automation bundle its own homepage section, rewrite blog strategy toward buyer-intent keywords

*Generated by AI Marketing Suite — `/market audit`*
