# Skill: market-audit

Run a full marketing audit on any URL. Returns a scored report across 6 categories with quick wins, strategic recommendations, and revenue impact estimates.

## Trigger

`/market-audit [url]`

## What It Does

1. Fetches and analyzes the target URL (homepage + key pages)
2. Scores across 6 categories (25% + 20% + 20% + 15% + 10% + 10% weights):
   - Content & Messaging
   - Conversion Optimization
   - SEO & Discoverability
   - Competitive Positioning
   - Brand & Trust
   - Growth & Strategy
3. Outputs a structured report with:
   - Overall score (0–100) and letter grade
   - Executive summary
   - Score breakdown table
   - Quick wins (this week)
   - Strategic recommendations (this month)
   - Long-term initiatives (this quarter)
   - Detailed analysis per category
   - Revenue impact summary with confidence levels and timelines
   - Next steps (week 1, week 2, weeks 3–4, month 2, month 3)

## Output

Save report to `.claude/skills/market-audit/[business]-audit-[YYYY-MM-DD].md`

## Past Audits

- [jarvis-audit-2026-04-02.md](jarvis-audit-2026-04-02.md) — Jarvis (gojarvis.ai), score 51/100, April 2, 2026
