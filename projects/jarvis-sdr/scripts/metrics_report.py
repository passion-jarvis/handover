"""
Pipeline Metrics Report
Pulls data from Supabase and prints a plain-English weekly performance report.

Usage:
    python scripts/metrics_report.py
    python scripts/metrics_report.py --days 14
    python scripts/metrics_report.py --slack    # also posts to Slack
"""

import sys
import os
import argparse
import logging
from datetime import datetime, timedelta, timezone
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.WARNING)

from supabase import create_client
import requests


def parse_args():
    p = argparse.ArgumentParser(description="Pipeline metrics report")
    p.add_argument("--days",  type=int, default=7, help="Lookback window in days")
    p.add_argument("--slack", action="store_true", help="Also post report to Slack")
    return p.parse_args()


def run() -> None:
    args = parse_args()
    days = args.days
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

    rows = (
        client.table("scraped_leads")
        .select("keyword_category, enrichment_status, first_seen_at, ghl_contact_id")
        .gte("first_seen_at", cutoff)
        .execute()
        .data
    )

    if not rows:
        print(f"\nNo leads in the last {days} days.\n")
        return

    total = len(rows)
    by_status: dict[str, int] = defaultdict(int)
    by_category: dict[str, int] = defaultdict(int)
    by_day: dict[str, int] = defaultdict(int)
    ghl_pushed = 0

    for row in rows:
        by_status[row["enrichment_status"]] += 1
        by_category[row["keyword_category"]] += 1
        day = row["first_seen_at"][:10]
        by_day[day] += 1
        if row.get("ghl_contact_id"):
            ghl_pushed += 1

    complete = by_status.get("complete", 0)
    partial  = by_status.get("partial", 0)
    failed   = by_status.get("failed", 0)
    enriched = complete + partial
    hit_rate = round(enriched / total * 100) if total else 0

    lines = [
        f"",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"  Jarvis SDR Pipeline — Last {days} Days",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"",
        f"  Total leads processed:  {total}",
        f"  Pushed to GHL:          {ghl_pushed}  ({round(ghl_pushed/total*100) if total else 0}%)",
        f"  Enrichment hit rate:    {hit_rate}%",
        f"    Complete (email+LI):  {complete}",
        f"    Partial (email only): {partial}",
        f"    Failed (no contact):  {failed}",
        f"",
        f"  By keyword category:",
    ]
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        pct = round(count / total * 100) if total else 0
        lines.append(f"    {cat.upper():<10} {count:>4}  ({pct}%)")

    lines += [
        f"",
        f"  Daily volume (last {min(days, 7)} days):",
    ]
    sorted_days = sorted(by_day.keys())[-7:]
    for day in sorted_days:
        bar = "█" * min(by_day[day], 30)
        lines.append(f"    {day}  {bar}  {by_day[day]}")

    # Health checks
    lines += ["", "  Health:"]
    if hit_rate < 50:
        lines.append(f"  ⚠  Enrichment hit rate is {hit_rate}% — check Apollo API key and domain quality")
    else:
        lines.append(f"  ✓  Enrichment hit rate {hit_rate}% — on target (>50%)")

    daily_avg = round(total / days)
    if daily_avg < 30:
        lines.append(f"  ⚠  Only {daily_avg} leads/day — check scraper sources are running")
    else:
        lines.append(f"  ✓  {daily_avg} leads/day average")

    lines += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", ""]

    report = "\n".join(lines)
    print(report)

    if args.slack:
        webhook = os.environ.get("SLACK_WEBHOOK_URL")
        if webhook:
            requests.post(webhook, json={"text": f"```{report}```"}, timeout=10)
            print("Slack: sent")
        else:
            print("Slack: SLACK_WEBHOOK_URL not set")


if __name__ == "__main__":
    run()
