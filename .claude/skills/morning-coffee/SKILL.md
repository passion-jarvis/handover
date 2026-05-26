---
name: morning-coffee
description: Morning briefing skill — RPM-based daily plan using Google Calendar, Notion, and the Jarvis team scorecard. Schedules MAP blocks into calendar, sends 10 PM recap to Gmail, rolls over incomplete tasks.
---

# Morning Coffee ☕

Tony Robbins RPM daily plan. Pull all data, identify what matters, build the MAP, block it into the calendar.

## Trigger

Use this skill when Passion says:
- "/morning-coffee"
- "morning briefing"
- "plan my day"
- "morning coffee"
- "what's my day look like"

---

## Step 1: Pull Data (All in parallel)

### A. Google Calendar
- Call `gcal_list_events` for today (US/Pacific)
- Get all events: time, title, attendees
- Note every blocked window — these are conflicts that MAP actions must work around

### B. Gmail
- Call `gmail_search_messages` with query: `is:unread newer_than:2d`
- Skip newsletters, receipts, automated emails
- Sort every flagged email into exactly one of these three categories:

**Category 1 — Needs Your Attention** (requires a decision, action, or response from Passion today)
**Category 2 — Needs a Reply** (requires a written response, but not necessarily urgent)
**Category 3 — Already Judged, Not Yet Replied** (Passion has likely seen this and knows what he wants to say, but hasn't replied yet — surface it so it doesn't fall through)

Report each email under its category: Sender, Subject, one line on what's needed.
If inbox is clean across all three: "Inbox is clean."

### C. Jarvis Scorecard
Pull **both tabs in parallel**:

**Tab 1 — Daily Scorecard (current week detail):**
- Fetch CSV: `https://docs.google.com/spreadsheets/d/1asUjGTbEyhhHaqCWNZsP-GXioYh3xE9O/export?format=csv&gid=1242855012`
- Read the current week's data for all team members
- Identify which metrics are ❌ red (not achieved) vs ✅ green
- Flag any metric that is at 0 or blank with no entries yet this week
- Pay special attention to: Booked Calls (Shemily), Sales Calls (Passion/George), Deals Closed (Passion/George)

**Tab 2 — Weekly Summary (week-over-week trends):**
- Fetch CSV: `https://docs.google.com/spreadsheets/d/1asUjGTbEyhhHaqCWNZsP-GXioYh3xE9O/export?format=csv&gid=1702064739`
- Read the last 3 weeks of data for every metric
- For each metric, identify the trend: improving ↑, declining ↓, or flat →
- Flag any metric that has been ❌ for 2+ consecutive weeks — these are systemic problems, not one-off misses
- Key metrics to trend-watch: Deals Closed, Calls Completed, Booked Calls (Shemily), Creator Partners Signed, New Clients Onboarded (Ruth), VA Upsell Conversations (Ruth)
- Surface the overall Goals Achieved score (out of 18) week-over-week — is the team getting better or worse?

### D. GHL Pipeline Pulse
Pull live lead data from GoHighLevel using the API key in `.env`.

**Credentials (from `.env`):**
- `GHL_API_KEY=pit-df7a972f-254d-43c4-bf5e-0171803221a7`
- `GHL_LOCATION_ID=quW9l8ARPHQVeA5FC13T`

**API call:**
```bash
curl -s -X GET "https://services.leadconnectorhq.com/contacts/?locationId=quW9l8ARPHQVeA5FC13T&limit=50&sortBy=date_added" \
  -H "Authorization: Bearer pit-df7a972f-254d-43c4-bf5e-0171803221a7" \
  -H "Version: 2021-07-28" \
  -H "Content-Type: application/json"
```

**Parse and report:**
- Count leads added today vs yesterday — flag if below 5/day from Meta
- Detect Meta leads using the `source` field: `source == "Facebook"` or `source == "Instagram"` — do NOT use `attributionSource` or `attributions.utmCampaign`, these fields are empty due to a known UTM passthrough bug
- Break down by source: Facebook/Instagram (Meta inbound) vs Apollo (outbound) vs other
- Flag how many have NO email and NO phone (unworkable leads)
- Flag how many are UNASSIGNED (assignedTo is null) — this is a critical ops gap
- Identify the top 3-5 highest-quality Meta leads (have email + phone, source = Facebook or Instagram)
- Note: UTM campaign data is currently unavailable — JC/Adithya is fixing the Meta → GHL UTM passthrough integration

**Report in briefing under 🔁 GHL Pipeline Pulse section:**

| Source | Count Today | Has Contact Info | Assigned | 
|--------|-------------|-----------------|----------|
| Meta (FB/IG) | X | X | X |
| Apollo | X | X | X |
| Other | X | X | X |

**Top Meta leads to call today:** (name, company, phone/email)
**⚠️ Unassigned leads total:** X — flag if > 0

### E. Notion
- Call `notion-search` for any open tasks, action items, or project updates tagged to Passion
- Look for anything due today or flagged urgent

### F. Ads Status Check
**Current status (as of 2026-04-08): ALL META ADS PAUSED.**

Reason: Algorithm trained on wrong audience. 43 leads, 0 conversions. ~93% were $0-5k revenue. Decision made to pause and rebuild.

Do NOT check the budget ramp table. Instead, report the restart checklist status from `projects/jarvis-meta-ads/META-ADS-REPORT.md`:

**Report:**
- Ads status: PAUSED
- Total spent to date: $1,342.15 (US + AU campaigns)
- Restart checklist: which items are done vs pending
- Flag if any restart condition has been completed since last briefing

### G. Chase Account Check (5 min)
- Prompt Passion: "Quick — open Chase and tell me: current balance + any transactions over $500 since yesterday."
- If Passion shares the numbers, note the balance and flag anything unusual
- Add to the briefing under a 💳 Chase Pulse section
- If balance is lower than last reported, flag it as a CFO alert and suggest running `/cfo`

---

## Step 2: Build the RPM Day Plan

Apply Tony Robbins' RPM framework. RPM = **Result → Purpose → Massive Action Plan**.

Identify Passion's top 2-3 Results for today based on:
- What's red on the scorecard that Passion can directly move
- What's on the calendar that requires prep or follow-up
- What Q2 milestones are closest (from `context/current-priorities.md`)

For each Result, build a full RPM block with specific MAP actions.

---

## Step 3: Schedule MAP Blocks into Google Calendar

After building the RPM plan, schedule each MAP block as a calendar event.

### Rules for scheduling:
- Each MAP block = **90 minutes**
- Check existing calendar events from Step 1 — do NOT overlap with anything already booked
- Schedule blocks back-to-back if needed, leaving at least 15 min buffer between blocks and existing events
- Start from the earliest available time in the morning (assume 8 AM is earliest)
- If today's calendar is too full to fit all blocks, schedule overflow to the next available day
- Name each event clearly: e.g. "🎯 RPM: Review GHL Leads + Shemily Feedback"
- Add a short description to each event listing the specific MAP actions inside it

### How to schedule:
- Call `gcal_create_event` for each MAP block
- Set calendar to primary
- Set timezone to America/Los_Angeles
- After creating each event, confirm it was created and note the time slot

---

## Step 4: Schedule 10 PM Daily Recap Event

After scheduling MAP blocks, create one more calendar event:
- Title: "📋 Daily Recap — Send to passion@gojarvis.ai"
- Time: 10:00 PM – 10:15 PM today (America/Los_Angeles)
- Description: "Review which MAP blocks were completed. Draft and send recap email to passion@gojarvis.ai. Roll over incomplete tasks to tomorrow."

This event is a standing reminder. Create it every morning coffee run.

---

## Step 5: Output the Briefing

---

☕ **Good morning, Passion.**
*[Day, Date]*

---

### 📊 Team Scorecard Pulse

**This week (current):**
| Person | Metric | This Week | Target | Status |
|--------|--------|-----------|--------|--------|
[Show ALL metrics — both red and green. Include zeros explicitly. Do not skip any row.]

**Week-over-week trend (last 3 weeks):**
| Metric | 2 weeks ago | Last week | This week | Trend |
|--------|-------------|-----------|-----------|-------|
[Show the key metrics: Deals Closed, Calls Completed, Booked Calls, Creator Partners Signed, New Clients Onboarded, VA Upsells, Goals Hit (of 18)]
[Trend: ↑ improving, ↓ declining, → flat, 🆕 new data]

**Overall team score:** [X/18 goals hit this week] vs [X/18 last week] — [better/worse/same]

**What this means for today:** [2-3 sentences. Call out systemic problems (2+ weeks red) vs one-off misses. Name who Passion needs to address and why.]

---

### 📅 Today's Calendar
[List each event: **HH:MM** — Event (attendees)]
[If nothing: "Clear calendar."]

---

### 📬 Inbox Flags
[Only action items, most urgent first]
- **[Sender]** — [Subject] → [what's needed]
[If clear: "Inbox is clean."]

---

### 🎯 RPM Day Plan

For each Result block:

---

**RESULT #[N]:** [Specific, measurable outcome for today]

**PURPOSE:** [Why this matters — connect it to 22 → 100 or a specific Q2 rock. Make it emotionally real, not corporate. 1-2 sentences max.]

**MASSIVE ACTION PLAN:**
- [ ] [Specific action] — [time block assigned in calendar]
- [ ] [Specific action] — [time block assigned in calendar]
- [ ] [Specific action] — [time block assigned in calendar]

---

[Repeat for Result #2 and #3]

---

### 📆 Scheduled into Your Calendar
[List each MAP block that was created:]
- **[HH:MM – HH:MM]** — [Event title]
- **[HH:MM – HH:MM]** — [Event title]
- **10:00 PM** — Daily Recap reminder

[If any blocks couldn't fit today due to conflicts:]
- **Rolled to [tomorrow's date]:** [Action description]

---

### 🔁 GHL Pipeline Pulse
| Source | Count Today | Has Contact Info | Assigned |
|--------|-------------|-----------------|----------|
[Fill from API data]

**Top Meta leads to call today:**
[Name — Company — Phone/Email — Ad Campaign]

**⚠️ Unassigned leads:** [X total — who needs to action these?]

---

### 💳 Chase Pulse
[If Passion shared the balance:]
- **Balance:** $[X]
- **Flagged transactions:** [Any over $500 since yesterday]
- [If balance dropped significantly: "⚠️ Balance is down — run /cfo today."]
[If not shared yet: "Open Chase and drop the balance here — takes 30 seconds."]

---

### 📈 Ads Status
**Status: PAUSED as of 2026-04-08**
**Total spent: $1,342.15 | Leads: 43 | Conversions: 0**

Restart checklist (from `projects/jarvis-meta-ads/META-ADS-REPORT.md`):
- [ ] New Lead Form built from scratch
- [ ] $0-5k option removed entirely
- [ ] "Are you the business owner?" question added
- [ ] Ad copy filters by revenue in line 1
- [ ] C1-6 set as primary creative
- [ ] Shemily outbound running consistently

**[X/6 conditions met]** — [Flag which are done, which are pending]

---

### 🔔 Don't Miss Today
[3-5 items max — only what's actually relevant today]

---

### 💬 One Question
One sharp question to focus Passion's energy based on the data.

---

## Step 6: 10 PM Daily Recap (run when triggered at 10 PM or when Passion says "send recap")

When Passion triggers the recap (or at 10 PM reminder):

1. Call `gcal_list_events` for today to see which MAP block events exist
2. Ask Passion: "Which of today's MAP blocks did you complete?" (or check if Passion has flagged anything)
3. Build the recap email:

**To:** passion@gojarvis.ai
**Subject:** Daily Recap — [Day, Date]

---

**✅ Completed today:**
[List what got done]

**❌ Not completed — rolling over:**
[List what didn't get done]

**Rolling to [tomorrow's date]:**
[List each incomplete task with a proposed time block]

**One thing that moved the needle today:**
[Pull the most important win or insight from the day]

**Tomorrow's top priority:**
[Based on what's left, what's most important to attack first thing tomorrow]

---

4. Call `gmail_create_draft` to draft the recap to passion@gojarvis.ai
5. Call `gcal_create_event` to add any rolled-over MAP blocks to the next available day (same 90-min block format, check conflicts before placing)
6. Confirm back to Passion: "Recap drafted and sent. [X] tasks rolled to [date]."

---

## Rules

- Never schedule a MAP block that overlaps with an existing calendar event
- Always add 15 min buffer between MAP blocks and existing events
- Each MAP block is exactly 90 minutes — no exceptions
- Recap email goes to passion@gojarvis.ai every day without fail
- Rolled-over tasks go to the next available morning slot — not the end of day
- Scorecard pulse comes first in the briefing — sets the tone
- RPM blocks must be specific. No vague goals.
- Purpose must connect to 22 → 100 or a Q2 milestone
- Tone: direct, energized, no em dashes, no fluff
