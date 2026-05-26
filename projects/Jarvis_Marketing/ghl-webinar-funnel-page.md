# Jarvis Webinar Funnel Page — GHL Build Guide
**Date:** 2026-04-16
**URL slug:** /fitness-coaches (or /free-training)
**Goal:** Fitness coach watches webinar → books free 15-min call

---

## PAGE STRUCTURE (top to bottom)

```
[SECTION 1] — Pre-headline + Headline
[SECTION 2] — Video embed (the webinar)
[SECTION 3] — Primary CTA button
[SECTION 4] — What you'll learn (bullets)
[SECTION 5] — Case study / social proof
[SECTION 6] — Secondary CTA
[SECTION 7] — Footer (privacy, copyright)
```

---

## SECTION 1 — Pre-headline + Headline

**Pre-headline (small text above, uppercase, gray):**
CASE STUDY — FITNESS COACHES DOING $10K–$100K/MO

**Main headline (H1, large, dark):**
See How Jennifer Doubled Her Revenue in 60 Days Without Working More Hours

**Subheadline (H2, slightly smaller):**
One VA. One system. No developer. No extra staff. No burnout.

---

## SECTION 2 — Video Embed

**Above video (small text, centered):**
▶ Watch this 10-minute video first

**Video:** [Embed the webinar recording here — Vimeo or hosted video]

**Below video (small gray text, centered):**
Turn on sound. Watch to the end.

---

## SECTION 3 — Primary CTA Button

**Button text:**
Book Your Free 15-Min Call →

**Below button (small text, gray):**
No pitch. No pressure. We'll look at your business and tell you exactly what a VA could take off your plate.

**Below that (even smaller, green checkmarks):**
✓ $0 upfront   ✓ Starts within 5 days   ✓ 14-day guarantee

---

## SECTION 4 — What You'll Learn (bullet section)

**Section headline:**
In this video, you'll see exactly:

**Bullets:**
- → How Jennifer went from $18k/month to $34k/month in 60 days — without changing her offer or running more ads
- → The #1 reason fitness coaches cap their own income (and how to fix it this week)
- → How a pre-trained VA handles your DMs, leads, scheduling, and onboarding — starting within days
- → Why our VAs don't just do tasks — they build the automations that run without them
- → The $0-upfront model and what the 14-day guarantee actually covers

---

## SECTION 5 — Case Study / Social Proof

**Section headline (dark, bold):**
Real Coaches. Real Results.

**Card 1 — Jennifer (featured):**
> "Passion — $34k this month. My show rate doubled. I feel like a CEO for the first time."
— Jennifer, Online Fitness Coach

Stats below:
- Before: $18k/month · 60-hour weeks · Ads turned off
- After: $34k/month · Show rate 35% → 68% · Operations running

---

**Card 2:**
> "I'd tried VAs before and it never worked. Jarvis was different from day one — my VA knew our industry before they even started."
— Marcus T., Nutrition Coach, LA

---

**Card 3:**
> "I went from answering DMs at 11pm to not touching my inbox for 3 weeks. My VA handles everything."
— Jenna K., Personal Trainer, Austin TX

---

**Trust line (centered, gray):**
200+ founders freed from their own operations. 4.9/5 average rating.

---

## SECTION 6 — Secondary CTA

**Headline:**
Ready to Stop Being Your Own Assistant?

**Subline:**
One 15-minute call. We'll show you what's possible.

**Button:**
Book Your Free Call →

**Below button:**
✓ $0 upfront   ✓ Starts within 5 days   ✓ 14-day guarantee

---

## SECTION 7 — Footer

Privacy Policy | Terms of Service
© 2026 Jarvis. All rights reserved.
gojarvis.ai

---

## GHL BUILD NOTES

### Page settings
- Page type: Funnel step (no navigation bar, no header menu)
- Background: White (#FFFFFF) or off-white (#F3F2EF)
- Max content width: 800px centered
- Mobile: Must look clean — most traffic will be from mobile (Meta ads)

### Typography
- H1: 42–48px on desktop, 28–32px mobile, bold, dark (#1A1A1A)
- H2: 24–28px, semi-bold
- Body: 16–18px, #333333
- Button: 18–20px, bold, white text on dark background (#1A1A1A) or neon (#CCFF00 on black)
- Pre-headline: 12px, uppercase, letter-spaced, gray (#888888)

### CTA Button styling
- Background: #0D0D0D (dark) or #CCFF00 (neon yellow)
- Text: White (on dark) or #0D0D0D (on neon)
- Border radius: 6px
- Padding: 16px 32px
- Width: full-width on mobile, auto on desktop

### Video section
- Embed Vimeo or direct MP4 — do NOT use YouTube (autoplay restrictions)
- Ratio: 16:9
- No controls visible until user clicks (cleaner look)
- Thumbnail: frame from video showing Passion on camera

### Booking integration
- CTA button links to: Calendly booking page (or GHL calendar)
- Calendar: George's calendar for sales calls (15-min slots)
- Confirmation page: thank you page with next steps

### Tracking
- Meta Pixel fires on page load (PageView event)
- Meta Pixel fires on button click (Lead event)
- GHL form/calendar submit triggers automation:
  1. Tag contact: "webinar-lead"
  2. Send confirmation email (see email sequence doc)
  3. Notify George via Slack/WhatsApp

### URL structure
- Opt-in page: gojarvis.ai/fitness-coaches
- Thank you page: gojarvis.ai/fitness-coaches/thank-you

---

## EMAIL SEQUENCE (post-booking)

### Email 1 — Confirmation (immediate)
**Subject:** Your call is booked — here's what to expect

Hey [First Name],

Your free 15-minute call is confirmed.

Before the call, here's what I want you to think about:
- How many hours per week are you spending on tasks that have nothing to do with coaching?
- Where are leads slipping through — DMs, follow-ups, scheduling?
- What would your business look like if those were handled?

We'll walk through all of it on the call.

See you then,
Passion Chu
Founder, Jarvis
gojarvis.ai

---

### Email 2 — Reminder (24 hours before)
**Subject:** Your call is tomorrow — quick prep

Hey [First Name],

Quick reminder — your call with us is tomorrow.

One thing to have ready: a rough sense of how many leads you're getting per week and how many are converting. We'll use that to show you exactly what a VA could move.

If you need to reschedule: [link]

See you tomorrow,
Passion

---

### Email 3 — No-show follow-up (if they miss the call)
**Subject:** You missed your call — want to reschedule?

Hey [First Name],

Looks like you missed your call today. No worries — happens all the time.

If you're still interested, grab another time here: [link]

If this isn't the right time, no problem. You can reply and let me know.

Passion

---

## META AD COPY (for traffic to this page)

**Hook 1 (when ads restart):**
If your business does $10k+/month and you're still answering your own DMs — watch this 10-minute case study.

**Hook 2:**
Jennifer was making $18k/month and working 60-hour weeks. She turned off her own ads because she couldn't handle the leads.
60 days later: $34k/month. Show rate doubled.
This is what we did. →

**Hook 3:**
The reason you're capped at your current revenue isn't your offer.
It's that you're the coach, the sales rep, the follow-up machine, and the admin.
Watch this. →
