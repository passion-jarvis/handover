"""
Purge Old Records
Deletes scraped_leads and pipeline_events older than N days from Supabase.
Run monthly (or via cron) to keep the dedup table lean.

Usage:
    python scripts/purge_old.py              # purge > 90 days (default)
    python scripts/purge_old.py --days 60    # purge > 60 days
    python scripts/purge_old.py --dry-run    # show count, don't delete
"""

import sys
import os
import argparse
import logging
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

from supabase import create_client


def parse_args():
    p = argparse.ArgumentParser(description="Purge old Supabase records")
    p.add_argument("--days",    type=int,        default=90,   help="Purge records older than N days (default: 90)")
    p.add_argument("--dry-run", action="store_true",            help="Count rows without deleting")
    return p.parse_args()


def run() -> None:
    args = parse_args()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()

    client = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )

    # Count rows to be purged
    leads_count = (
        client.table("scraped_leads")
        .select("id", count="exact")
        .lt("first_seen_at", cutoff)
        .execute()
        .count or 0
    )

    events_count = (
        client.table("pipeline_events")
        .select("id", count="exact")
        .lt("event_at", cutoff)
        .execute()
        .count or 0
    )

    log.info(f"Cutoff: {cutoff[:10]} (>{args.days} days old)")
    log.info(f"scraped_leads to purge:   {leads_count}")
    log.info(f"pipeline_events to purge: {events_count}")

    if args.dry_run:
        log.info("Dry run — nothing deleted.")
        return

    if leads_count > 0:
        client.table("scraped_leads").delete().lt("first_seen_at", cutoff).execute()
        log.info(f"Deleted {leads_count} scraped_leads rows.")

    if events_count > 0:
        client.table("pipeline_events").delete().lt("event_at", cutoff).execute()
        log.info(f"Deleted {events_count} pipeline_events rows.")

    log.info("Purge complete.")


if __name__ == "__main__":
    run()
