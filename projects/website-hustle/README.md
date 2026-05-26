# Website Hustle — Full Task Blueprint

**Concept:** Find local businesses with no website, build them one in 48 hours, sell it for $300.
**Status:** Active
**Lead list:** 1,460 California hair salons imported to GHL (tag: website-hustle)

---

## The Model

```
Google Maps → No-website businesses → Shemily calls → $300 close → Adithya builds → Deliver in 48hrs
```

**Unit economics:**
- Revenue per sale: $300
- Build cost: Sitedrop (free/low cost)
- Time to build: ~20 mins
- Shemily target: 2 closes/day = $600/day = $3,000/week

---

## Team Roles

| Who | What |
|-----|------|
| **Shemily** | Calls leads, pitches, closes |
| **Adithya** | Builds the site on Sitedrop.ai after close |
| **Passion** | Oversees, approves, collects payment |

---

## Step 1 — Lead Generation (Done)

- Scraper built: `/projects/website-hustle/scraper.py`
- 1,538 hair salons pulled from California Google Maps
- 1,460 imported to GHL tagged `website-hustle`
- To run more: `python3 scraper.py --type "nail salon" --state california --limit 5000`

**Shemily access:**
GHL → Contacts → Filter tag: `website-hustle`

---

## Step 2 — Shemily Calls

Full script + objection handling: `/projects/website-hustle/shemily-playbook.md`

**The pitch in one line:**
> "You have great reviews but no website — people can't find you. We build it in 48 hours for $300. You do nothing."

**Daily targets:**
- 80 calls
- 25 pickups
- 2 closes

**Call flow:**
1. Confirm they have no website
2. Compliment their reviews
3. Pitch the offer
4. Handle objections
5. Get email → send intake form
6. Collect $300 payment

---

## Step 3 — Payment Collection

- Collect $300 upfront via card before building
- Use GHL payment link or send Stripe/Zelle
- No payment = no build

---

## Step 4 — Intake Form

After close, Shemily sends this via email or WhatsApp:

> To get started I just need:
> 1. Business name (exactly how you want it written)
> 2. Services + rough prices
> 3. Hours of operation
> 4. Phone number for the site
> 5. Address
> 6. Logo (if you have one)
> 7. Photos of the salon (optional)

---

## Step 5 — Adithya Builds

- Tool: sitedrop.ai
- Time: 20-30 mins per site
- Shemily hands off intake info to Adithya via WhatsApp
- Adithya builds and sends live link within 48 hours

---

## Step 6 — Delivery

Shemily sends to client:
> "Hi [Name], your website is live! Here's the link: [URL]
> Let us know if you'd like any small tweaks — we'll handle it within 48 hours."

**Upsell:**
> "We also offer monthly hosting + updates for $50/month so you never have to touch it. Want to add that?"

---

## Tracking

Log every lead in GHL pipeline: **Website Hustle**

| Stage | Description |
|-------|-------------|
| New Lead | Pulled from list, not yet called |
| Contacted | Call made, interested |
| Demo Sent | Sitedrop preview sent |
| Closed | $300 collected |
| In Progress | Adithya building |
| Delivered | Site live, sent to client |
| Upsell | On $50/month hosting |

---

## Lead Replenishment

When list runs low, run scraper for new business types:

```bash
python3 /projects/website-hustle/scraper.py --type "nail salon" --state california --limit 5000
python3 /projects/website-hustle/scraper.py --type "barbershop" --state california --limit 5000
python3 /projects/website-hustle/scraper.py --type "restaurant" --state california --limit 5000
```

Then re-run import: `python3 /projects/website-hustle/import_to_ghl.py`

---

## Revenue Projections

| Closes/day | Weekly | Monthly |
|------------|--------|---------|
| 1 | $1,500 | $6,000 |
| 2 | $3,000 | $12,000 |
| 5 | $7,500 | $30,000 |

---

## Files

| File | Purpose |
|------|---------|
| `scraper.py` | Pull no-website leads from Google Maps |
| `import_to_ghl.py` | Import CSV leads into GHL |
| `shemily-playbook.md` | Full call script + objection handling |
| `leads_hair_salon_california_*.csv` | Lead list |
| `checkpoint_california.json` | Scraper resume state |
