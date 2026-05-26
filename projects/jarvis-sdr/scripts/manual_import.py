"""
Manual CSV Import — Week 1 MVP
Takes a CSV of company domains/names, enriches via Apollo, pushes to GHL.

Usage:
    python scripts/manual_import.py --csv leads.csv
    python scripts/manual_import.py --csv leads.csv --dry-run
    python scripts/manual_import.py --csv leads.csv --keyword ea --limit 20

CSV format (header row required):
    company_name, company_domain, job_title, job_url, post_date, keyword_category, location, source

Minimum required columns: company_name OR company_domain
All other columns are optional — will be blank in GHL note if missing.

Example minimal CSV:
    company_name,company_domain,job_title,keyword_category
    Acme Corp,acme.com,Executive Assistant,ea
    Widget Co,,Social Media Manager,social
"""

import sys
import os
import csv
import argparse
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

from scraper.models import RawPosting, EnrichedLead
from enrichment import apollo, hunter
from integrations import ghl, sheets
from notifications import slack
from db import supabase_client
from config.validate import check_required


REQUIRED_FOR_IMPORT = ["APOLLO_KEY", "GHL_API_KEY", "GHL_LOCATION_ID", "GHL_PIPELINE_ID", "GHL_STAGE_ID_NEW"]


def parse_args():
    p = argparse.ArgumentParser(description="Manual CSV → GHL importer")
    p.add_argument("--csv",      required=True, help="Path to CSV file")
    p.add_argument("--keyword",  default=None,  help="Override keyword_category for all rows (ea|social|bdr|sales|video)")
    p.add_argument("--limit",    type=int,      help="Max rows to process")
    p.add_argument("--dry-run",  action="store_true", help="Enrich but skip GHL writes")
    p.add_argument("--skip-enrichment", action="store_true", help="Skip Apollo/Hunter, push raw CSV data only")
    return p.parse_args()


def load_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def row_to_posting(row: dict, keyword_override: str | None) -> RawPosting:
    return RawPosting(
        job_title=row.get("job_title", "").strip(),
        company_name=row.get("company_name", "").strip(),
        company_domain=row.get("company_domain", "").strip().replace("https://", "").replace("http://", "").replace("www.", ""),
        location=row.get("location", "").strip(),
        post_date=row.get("post_date", "").strip(),
        job_description_snippet=row.get("job_description_snippet", "").strip()[:300],
        job_url=row.get("job_url", "").strip(),
        source=row.get("source", "manual_import").strip(),
        keyword_category=(keyword_override or row.get("keyword_category", "ea")).strip(),
        remote_flag=row.get("remote_flag", "").lower() in ("true", "yes", "1"),
    )


def enrich_posting(posting: RawPosting, skip_enrichment: bool) -> EnrichedLead:
    lead = EnrichedLead(posting=posting)

    if skip_enrichment:
        lead.enrichment_status = "partial"
        return lead

    domain = posting.company_domain
    if not domain:
        log.warning(f"No domain for {posting.company_name} — skipping enrichment")
        lead.enrichment_status = "failed"
        return lead

    try:
        result = apollo.enrich(domain)
        if result:
            lead.owner_first_name     = result.get("first_name", "")
            lead.owner_last_name      = result.get("last_name", "")
            lead.owner_email          = result.get("email", "")
            lead.owner_linkedin_url   = result.get("linkedin_url", "")
            lead.company_linkedin_url = result.get("company_linkedin_url", "")
            lead.employee_count       = result.get("employee_count")
            lead.revenue_estimate     = result.get("revenue_estimate", "")
    except Exception as e:
        log.warning(f"Apollo failed ({domain}): {e}")

    if lead.owner_email:
        lead.enrichment_status = "complete" if lead.owner_linkedin_url else "partial"
    else:
        try:
            fallback = hunter.find_email(domain)
            if fallback:
                lead.owner_email = fallback
                lead.enrichment_status = "partial"
            else:
                lead.enrichment_status = "failed"
        except Exception as e:
            log.warning(f"Hunter failed ({domain}): {e}")
            lead.enrichment_status = "failed"

    return lead


def run() -> None:
    args = parse_args()
    dry_run = args.dry_run or os.environ.get("DRY_RUN", "false").lower() == "true"

    check_required(REQUIRED_FOR_IMPORT)

    rows = load_csv(args.csv)
    if args.limit:
        rows = rows[:args.limit]

    log.info(f"Loaded {len(rows)} rows from {args.csv} — dry_run={dry_run}")

    stats = {"total": len(rows), "enriched": 0, "pushed": 0, "skipped": 0, "failed": 0}

    for i, row in enumerate(rows, 1):
        posting = row_to_posting(row, args.keyword)
        log.info(f"[{i}/{len(rows)}] {posting.company_name} ({posting.company_domain})")

        lead = enrich_posting(posting, args.skip_enrichment)
        log.info(f"  Enrichment: {lead.enrichment_status} | email={lead.owner_email or 'none'}")

        if lead.enrichment_status != "failed":
            stats["enriched"] += 1

        # Dedup check
        domain = (posting.company_domain or posting.company_name).lower()
        try:
            if supabase_client.is_duplicate(domain, posting.keyword_category):
                log.info(f"  Dedup skip: {domain}")
                stats["skipped"] += 1
                continue
        except Exception as e:
            log.warning(f"  Dedup check failed: {e} — continuing")

        # Route to GHL
        if lead.enrichment_status in ("complete", "partial"):
            try:
                contact_id = ghl.push_lead(lead, dry_run=dry_run)
                lead.ghl_contact_id = contact_id
                stats["pushed"] += 1
                log.info(f"  GHL: {contact_id}")
            except Exception as e:
                log.error(f"  GHL push failed: {e}")
                stats["failed"] += 1
        else:
            stats["failed"] += 1
            log.info(f"  Sheets-only (no contact data)")

        # Google Sheets — always
        try:
            sheets.append_lead(lead)
        except Exception as e:
            log.warning(f"  Sheets append failed: {e}")

        # Dedup record
        if not dry_run:
            try:
                supabase_client.record_lead(domain, posting.keyword_category, lead.ghl_contact_id, lead.enrichment_status)
            except Exception as e:
                log.warning(f"  Dedup record failed: {e}")

    log.info(f"\nImport complete: {stats}")
    print(f"\n{'='*40}")
    print(f"Total rows:      {stats['total']}")
    print(f"Enriched:        {stats['enriched']}")
    print(f"Pushed to GHL:   {stats['pushed']}")
    print(f"Skipped (dedup): {stats['skipped']}")
    print(f"Failed:          {stats['failed']}")
    print(f"{'='*40}\n")


if __name__ == "__main__":
    run()
