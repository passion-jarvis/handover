"""
Retry Failed GHL Pushes
Reads the Google Sheet, finds rows where:
  - enrichment_status is "complete" or "partial"
  - ghl_contact_id is blank (push failed or was skipped)
Then re-attempts the GHL push.

Usage:
    python scripts/retry_failed.py
    python scripts/retry_failed.py --dry-run
    python scripts/retry_failed.py --limit 20
"""

import sys
import os
import argparse
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

import gspread
from google.oauth2.service_account import Credentials
from scraper.models import RawPosting, EnrichedLead
from integrations import ghl
from db import supabase_client

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Column indices (0-based), matching sheets.py header order
COL = {
    "score":              0,
    "timestamp":          1,
    "company_name":       2,
    "company_domain":     3,
    "job_title":          4,
    "keyword_category":   5,
    "source":             6,
    "job_url":            7,
    "post_date":          8,
    "location":           9,
    "remote":             10,
    "snippet":            11,
    "contact_name":       12,
    "email":              13,
    "linkedin":           14,
    "company_linkedin":   15,
    "employee_count":     16,
    "revenue":            17,
    "enrichment_status":  18,
    "ghl_contact_id":     19,
}


def parse_args():
    p = argparse.ArgumentParser(description="Retry failed GHL pushes from Google Sheets")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit",   type=int, help="Max rows to retry")
    return p.parse_args()


def get_sheet():
    creds = Credentials.from_service_account_file(
        os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"], scopes=SCOPES
    )
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(os.environ["GOOGLE_SHEETS_SPREADSHEET_ID"])
    return spreadsheet.worksheet(os.environ.get("GOOGLE_SHEETS_TAB_NAME", "Leads"))


def row_to_lead(row: list[str]) -> EnrichedLead | None:
    def get(col: str) -> str:
        idx = COL.get(col, -1)
        if idx < 0 or idx >= len(row):
            return ""
        return row[idx].strip()

    enrichment_status = get("enrichment_status")
    if enrichment_status not in ("complete", "partial"):
        return None
    if get("ghl_contact_id"):
        return None  # already pushed

    first, *rest = (get("contact_name") + " ").split(" ", 1)
    last = rest[0].strip() if rest else ""

    posting = RawPosting(
        job_title=get("job_title"),
        company_name=get("company_name"),
        company_domain=get("company_domain"),
        location=get("location"),
        post_date=get("post_date"),
        job_description_snippet=get("snippet"),
        job_url=get("job_url"),
        source=get("source") or "retry",
        keyword_category=get("keyword_category") or "ea",
        remote_flag=get("remote").lower() == "true",
    )
    return EnrichedLead(
        posting=posting,
        owner_first_name=first,
        owner_last_name=last,
        owner_email=get("email"),
        owner_linkedin_url=get("linkedin"),
        company_linkedin_url=get("company_linkedin"),
        employee_count=int(get("employee_count")) if get("employee_count").isdigit() else None,
        revenue_estimate=get("revenue"),
        enrichment_status=enrichment_status,
        score=int(get("score")) if get("score").isdigit() else 0,
    )


def run() -> None:
    args = parse_args()
    dry_run = args.dry_run or os.environ.get("DRY_RUN", "false").lower() == "true"

    log.info(f"Retry script start — dry_run={dry_run}")
    sheet = get_sheet()
    all_rows = sheet.get_all_values()

    # Skip header row
    data_rows = all_rows[1:]
    retry_candidates = []
    for i, row in enumerate(data_rows, start=2):  # row 2 = first data row in Sheets
        lead = row_to_lead(row)
        if lead:
            retry_candidates.append((i, row, lead))

    if args.limit:
        retry_candidates = retry_candidates[:args.limit]

    log.info(f"Found {len(retry_candidates)} rows to retry")

    pushed = 0
    failed = 0

    for sheet_row_num, raw_row, lead in retry_candidates:
        p = lead.posting
        log.info(f"Retrying: {p.company_name} <{lead.owner_email}>")

        try:
            contact_id = ghl.push_lead(lead, dry_run=dry_run)
            lead.ghl_contact_id = contact_id
            pushed += 1
            log.info(f"  GHL: {contact_id}")

            if not dry_run:
                # Update GHL Contact ID column in the sheet
                sheet.update_cell(sheet_row_num, COL["ghl_contact_id"] + 1, contact_id or "")

                # Record in dedup store
                domain = (p.company_domain or p.company_name).lower()
                supabase_client.record_lead(domain, p.keyword_category, contact_id, lead.enrichment_status)

        except Exception as e:
            log.error(f"  Failed: {e}")
            failed += 1

    log.info(f"\nRetry complete — pushed: {pushed} | failed: {failed}")


if __name__ == "__main__":
    run()
