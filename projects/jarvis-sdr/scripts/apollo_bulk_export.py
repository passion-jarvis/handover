"""
Apollo Bulk Export
Pulls unique company domains from Supabase (recent leads) and exports
a CSV that can be uploaded directly into Apollo's bulk search UI.

Apollo bulk upload format:
  Column A = "Company Domain" (no www., no http)

Usage:
    python scripts/apollo_bulk_export.py                # last 30 days
    python scripts/apollo_bulk_export.py --days 7       # last 7 days
    python scripts/apollo_bulk_export.py --keyword ea   # EA leads only
    python scripts/apollo_bulk_export.py --output apollo_upload.csv
    python scripts/apollo_bulk_export.py --no-enriched  # skip already enriched
"""

import sys
import os
import csv
import argparse
import logging
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.WARNING)

from supabase import create_client

KEYWORD_LABELS = {
    "ea":     "EA Hire",
    "social": "Social Media Hire",
    "bdr":    "BDR Hire",
    "sales":  "Sales Hire",
    "video":  "Video Editor Hire",
}


def parse_args():
    p = argparse.ArgumentParser(description="Export Apollo bulk upload CSV from Supabase leads")
    p.add_argument("--days",        type=int,   default=30,   help="Look back N days (default: 30)")
    p.add_argument("--keyword",     default=None, choices=["ea","social","bdr","sales","video"])
    p.add_argument("--no-enriched", action="store_true",      help="Exclude leads already enriched (have ghl_contact_id)")
    p.add_argument("--output",      default=None,             help="Output CSV path (default: apollo_bulk_YYYYMMDD.csv)")
    return p.parse_args()


def run() -> None:
    args = parse_args()

    client = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )

    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()

    query = (
        client.table("scraped_leads")
        .select("company_domain, keyword_category, enrichment_status, ghl_contact_id, first_seen_at")
        .gte("first_seen_at", cutoff)
    )

    if args.keyword:
        query = query.eq("keyword_category", args.keyword)

    if args.no_enriched:
        query = query.is_("ghl_contact_id", "null")

    result = query.execute()
    rows = result.data or []

    if not rows:
        print(f"No leads found (days={args.days}, keyword={args.keyword})")
        return

    # Deduplicate domains (same domain may appear across keyword categories)
    seen = set()
    export_rows = []
    for row in rows:
        domain = row.get("company_domain", "").strip().lower().replace("www.", "")
        if not domain or domain in seen:
            continue
        seen.add(domain)
        export_rows.append({
            "Company Domain": domain,
            "Signal":         KEYWORD_LABELS.get(row.get("keyword_category", ""), row.get("keyword_category", "")),
            "Enrichment":     row.get("enrichment_status", ""),
            "In GHL":         "yes" if row.get("ghl_contact_id") else "no",
            "First Seen":     (row.get("first_seen_at") or "")[:10],
        })

    # Sort by domain for clean upload
    export_rows.sort(key=lambda r: r["Company Domain"])

    outfile = args.output or f"apollo_bulk_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(export_rows[0].keys()))
        writer.writeheader()
        writer.writerows(export_rows)

    print(f"\nApollo bulk export: {outfile}")
    print(f"Unique domains: {len(export_rows)} (from {len(rows)} lead records, last {args.days} days)")
    print(f"\nInstructions:")
    print(f"  1. Open Apollo → Search → Companies")
    print(f"  2. Click 'Import' → 'Upload CSV'")
    print(f"  3. Map 'Company Domain' column → upload {outfile}")
    print(f"  4. Filter by title: CEO, Founder, Owner, President")
    print(f"  5. Export emails → use for outreach sequences\n")


if __name__ == "__main__":
    run()
