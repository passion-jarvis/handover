# Skill: lead-scraper

Scrape Google Maps for local businesses with no website. Returns a CSV lead list ready for outreach.

## Trigger phrases
- "find [business type] in [city] with no website"
- "scrape [city] [business type] leads"
- "pull no-website leads for [business type]"

## How to run

```bash
python3 /Users/passionchu/claude/projects/website-hustle/scraper.py \
  --type "[business type]" \
  --city "[city]" \
  --limit [number]
```

## Supported cities (built-in)
Los Angeles, New York, Chicago, Houston, Miami, San Francisco, Dallas, Atlanta, Phoenix, Seattle

## Business type examples
- hair salon
- nail salon
- restaurant
- barbershop
- beauty salon
- massage therapy
- auto repair
- dry cleaning

## Output
CSV saved to: `/Users/passionchu/claude/projects/website-hustle/`
Columns: Business Name, Phone, Address, Rating, Reviews, Google Maps URL, Website

## After running
Show the user:
1. How many leads found
2. File path
3. First 5 results as a preview table
