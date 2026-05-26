# Intern SOP: Weekly KPI Tracker — Website & Data Entry

**Role:** Data Intern
**Cadence:** Every Monday before 10am
**Sheet:** Weekly KPI Tracker tab (Google Sheets)

---

## Background (Read This First)

Jarvis (gojarvis.ai) is a VA matching service. We connect business owners doing $10K+/month with pre-trained virtual assistants. This tracker measures whether our marketing and sales efforts are working week over week. Your job is to keep the data accurate so Passion can make decisions fast.

---

## One-Time Setup: GA4 Access + Google Sheets Add-on

### Step 1: Accept GA4 access
- Passion will add your Gmail to Google Analytics 4 as a Viewer
- You'll get an email invite — accept it
- Log in at analytics.google.com and confirm you can see gojarvis.ai data

### Step 2: Install the GA4 Add-on in Google Sheets
- Open the KPI Tracker sheet
- Top menu → Extensions → Add-ons → Get add-ons
- Search "Google Analytics" → Install
- After install: Extensions → Google Analytics → Create new report

### Step 3: Create a report (one-time)

Set it up with these fields:

| Field | Value |
|---|---|
| Report Name | Jarvis Weekly Traffic |
| Account | Jarvis (gojarvis.ai) |
| Property | GA4 property |
| Metrics | Sessions, Average engagement time, Total users |
| Dimensions | Week (date range by week) |

- Run the report → it creates a new tab called "Report Configuration"
- Every week: Extensions → Google Analytics → Run reports → data refreshes automatically

---

## Weekly Entry: Every Monday, Enter Last Week's Data

**Time required: ~20–30 min**

> Date range: always set to the previous Mon–Sun before entering any numbers.

### WEBSITE Section (from GA4)

Go to analytics.google.com → Reports → Engagement

| Column in Sheet | Where to Find It | Notes |
|---|---|---|
| Landing Page Visits | GA4 → Reports → Engagement → Landing page → filter "/" (homepage) → Sessions | Homepage only |
| Avg Engagement | GA4 → Reports → Overview → Average engagement time | Site-wide |
| Funnel Opt-Ins | GA4 → Reports → Conversions → "generate_lead" or "form_submit" event | Count of booking/contact form submissions |
| Total Website | GA4 → Reports → Overview → Sessions | All pages, full site |

### All Other Blue Cells (Manual Entry from Team)

| Section | Source |
|---|---|
| Leads by Source | GHL pipeline + Meta Ads Manager + LinkedIn |
| Calls | GHL calendar / George's weekly report |
| Revenue / New Clients | GHL closed deals |
| Email metrics | Email platform (ask Passion which tool) |
| LinkedIn | LinkedIn Campaign Manager + outreach tracking |
| Content | Kamille's weekly report |
| Creator Partnerships | Kamille's weekly report |

---

## Backfilling Historical Data

The tracker starts Mar 19, 2026. For any weeks already passed:
1. Go to GA4, set the exact date range for that week (Mon–Sun)
2. Pull the 4 website metrics and fill them in
3. For business metrics (leads, calls, clients) — ask Passion for the old sheet or Daily Scorecard numbers

---

## Rules

- Never delete a row or change formulas (auto-calculated cells are locked or color-coded)
- Blue cells = manual entry only
- If a number is 0, enter 0. Don't leave it blank.
- If you're unsure about a number, flag it with a comment (right-click → Insert comment) and ping Passion on WhatsApp
