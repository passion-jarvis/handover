# Skill: sdr-blueprint

Build or refresh a Jarvis SDR Call Blueprint for any rep. Takes a raw lead list and produces a fully structured Notion page: tiered by revenue, time-zoned, scripted, with a 6-touch sequence and daily checklists.

## Trigger

`/sdr-blueprint [rep name]`

## Prerequisites

- GHL API key stored in environment as `GHL_API_KEY`
- GHL Location ID stored as `GHL_LOCATION_ID`

## What It Does

1. **Pull leads from GHL** via API:
   - Endpoint: `GET https://services.leadconnectorhq.com/contacts/`
   - Filter: contacts with tag `meta-lead` or pipeline stage matching inbound ad forms
   - Required fields per contact: name, phone, business name, annual/monthly revenue (custom field), country, timezone
   - Auth header: `Authorization: Bearer $GHL_API_KEY`
2. **Tier leads by revenue:**
   - Tier 1 (🔴) — $60k–$100k+/month — call first, every day
   - Tier 2 (🟡) — $30k–$60k/month — after Tier 1 is attempted
   - Tier 3 (🟢) — $15k–$30k/month — fill remaining time
3. **Build daily call schedule** by timezone (PST-anchored):
   - 12:00–1:30 PM PST → US Eastern
   - 1:30–3:00 PM PST → US Central + Mountain
   - 3:00–5:00 PM PST → US Pacific
   - 5:00–8:00 PM PST → Australia (AEST morning)
4. **Generate per-tier lead tables** with: name, phone, business, revenue, market, timezone, best call window
5. **Generate daily checklists** per tier (called / texted / noted in GHL)
6. **Include all scripts** (do not modify without explicit instruction):
   - Voicemail script (under 30 seconds)
   - Immediate follow-up text
   - 6-touch sequence (Day 1 call + VM, Day 1 text, Day 1 email, Day 3 call, Day 3 text, Day 5 final email)
   - Per-lead touch tracker checklist
7. **Include special situations:** mailbox full, "not interested" handler, timezone call rules
8. **Include end-of-day checklist**
9. **Publish to Notion** under Sales > Sales & Marketing with title: `[Rep Name]'s Call Blueprint — Jarvis SDR`

## Scripts (Canonical — Do Not Change Without Approval)

### Voicemail
> "Hey [Name], this is [Rep] calling from Jarvis. You filled out a form recently about getting some support in your business — I just wanted to reach out personally. I'll send you a quick text too. Talk soon!"

### Immediate Text (within 5 min of VM)
> "Hey [Name]! It's [Rep] from Jarvis — just left you a voicemail. You filled out a form about getting a VA for your business. Is this still something you're looking into? Happy to chat for 10 min whenever works 😊"

### 6-Touch Sequence

**Touch 1 — Call — Day 1** (goal: get them talking, do not pitch)
- If pickup: "Hey [Name], this is [Rep] — I'm not calling to sell you anything, I just had a quick question. You filled out a form about getting some help in your business. What's been taking up most of your time lately?"
- If no answer: leave voicemail → "Hey [Name], this is [Rep] from Jarvis. You filled out a form recently — I just had one quick question about your business, not a sales call. I'll shoot you a text too. Talk soon!"

**Touch 2 — Text — Day 1** (within 5 min of VM, goal: question that makes them think)
> "Hey [Name]! [Rep] from Jarvis here. You filled out that form a little while ago — quick question: what's the one task in your business you wish you never had to deal with again? 😊"

**Touch 3 — Email — Day 1** (goal: lead with their pain, not the solution)
- Subject: *One question about [Company Name]*
> Hi [Name],
> Tried reaching you earlier — no worries.
> Most business owners doing $10K+/month tell me the same thing: they're really good at what they do, but they're stuck doing tasks that have nothing to do with actually growing the business.
> Does that sound familiar?
> Not trying to pitch you — just curious if that's where you're at.
> — [Rep]

**Touch 4 — Call — Day 3** (goal: reference their business, no VM this touch)
- If pickup: "Hey [Name], [Rep] again from Jarvis. I saw you're running [Company] — I was just curious, are you handling most of the operations yourself or do you have a team helping you?"
- If no answer: hang up, no voicemail

**Touch 5 — Text — Day 3** (goal: share a result story, not a pitch)
> "Hey [Name] — random thought. One of our clients was spending 3 hours a day just on emails and follow-ups. Got a VA, got all of that time back in the first week. When I saw your form I thought of them. Is that kind of thing eating into your day too?"

**Touch 6 — Email — Day 5** (goal: cost of inaction, final touch)
- Subject: *Closing your file — [Name]*
> Hi [Name],
> Last time reaching out — I don't want to keep bugging you.
> But before I close your file, one thing: the reason you filled out that form — whatever was going on in your business that day — is that still happening?
> Because if it is, that's not going away on its own. You either pay the price of fixing it, or you keep paying the cost of not fixing it.
> Either way — totally your call. Just wanted to make sure you had the option.
> — [Rep]
> After 6 touches with zero response → mark "Dead — No Contact" in GHL and move on.

### "Not Interested" Handler
Ask ONE question before accepting it: "Totally understand — can I ask what made you fill out the form originally?"
If they say no again → mark dead immediately. Do not push.

## Output

Publish directly to Notion. Return the URL when done.

## GHL API Notes

- Pagination: use `limit=100&startAfter=` cursor for large contact lists
- Revenue is stored as a custom field — check GHL custom field IDs for `monthly_revenue` or `annual_revenue`
- Timezone is typically in the contact's address country + state fields — map to PST call windows during ingestion
- After blueprint is built, update each contact in GHL with tag `blueprint-assigned` to avoid duplicates on next run
