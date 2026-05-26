"""
SDR Morning Brief
Runs at 8 AM PT weekdays. Pulls yesterday's top leads from Google Sheets,
posts a ranked briefing to Slack so the SDR knows who to call first.

Usage:
    python scripts/morning_brief.py              # yesterday's leads, top 5
    python scripts/morning_brief.py --top 10     # top 10 leads
    python scripts/morning_brief.py --days 2     # last 2 days (catches weekend)
    python scripts/morning_brief.py --min-score 50
"""

import sys
import os
import argparse
import logging
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.WARNING)

import gspread
from google.oauth2.service_account import Credentials
from scraper.models import RawPosting, EnrichedLead
from notifications.slack import send_morning_brief

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

COL = {
    "score":             0,
    "timestamp":         1,
    "company_name":      2,
    "company_domain":    3,
    "job_title":         4,
    "keyword_category":  5,
    "source":            6,
    "job_url":           7,
    "post_date":         8,
    "location":          9,
    "remote":            10,
    "snippet":           11,
    "contact_name":      12,
    "email":             13,
    "linkedin":          14,
    "company_linkedin":  15,
    "employee_count":    16,
    "revenue":           17,
    "enrichment_status": 18,
    "ghl_contact_id":    19,
}


def parse_args():
    p = argparse.ArgumentParser(description="Post morning SDR brief to Slack")
    p.add_argument("--top",       type=int, default=5, help="Number of leads to surface (default: 5)")
    p.add_argument("--days",      type=int, default=1, help="Look back N days (default: 1 = yesterday)")
    p.add_argument("--min-score", type=int, default=0, help="Minimum score to include")
    return p.parse_args()


def get_sheet():
    creds = Credentials.from_service_account_file(
        os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"], scopes=SCOPES
    )
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(os.environ["GOOGLE_SHEETS_SPREADSHEET_ID"])
    return spreadsheet.worksheet(os.environ.get("GOOGLE_SHEETS_TAB_NAME", "Leads"))


def row_get(row: list[str], col: str) -> str:
    idx = COL.get(col, -1)
    if idx < 0 or idx >= len(row):
        return ""
    return row[idx].strip()


def is_recent(timestamp: str, days: int) -> bool:
    if not timestamp:
        return False
    try:
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
                    "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(timestamp[: len(fmt) + 3], fmt)
                if not dt.tzinfo:
                    dt = dt.replace(tzinfo=timezone.utc)
                return (datetime.now(timezone.utc) - dt).days <= days
            except ValueError:
                continue
    except Exception:
        pass
    return True


def row_to_lead(row: list[str]) -> EnrichedLead:
    contact_parts = row_get(row, "contact_name").split(" ", 1)
    first = contact_parts[0] if contact_parts else ""
    last  = contact_parts[1] if len(contact_parts) > 1 else ""

    posting = RawPosting(
        job_title=row_get(row, "job_title"),
        company_name=row_get(row, "company_name"),
        company_domain=row_get(row, "company_domain"),
        location=row_get(row, "location"),
        post_date=row_get(row, "post_date"),
        job_description_snippet=row_get(row, "snippet"),
        job_url=row_get(row, "job_url"),
        source=row_get(row, "source"),
        keyword_category=row_get(row, "keyword_category"),
    )

    score_str = row_get(row, "score")
    score = int(score_str) if score_str.isdigit() else 0
    emp_str = row_get(row, "employee_count")

    return EnrichedLead(
        posting=posting,
        owner_first_name=first,
        owner_last_name=last,
        owner_email=row_get(row, "email"),
        owner_linkedin_url=row_get(row, "linkedin"),
        company_linkedin_url=row_get(row, "company_linkedin"),
        employee_count=int(emp_str) if emp_str.isdigit() else None,
        revenue_estimate=row_get(row, "revenue"),
        enrichment_status=row_get(row, "enrichment_status") or "failed",
        ghl_contact_id=row_get(row, "ghl_contact_id") or None,
        score=score,
    )


def run() -> None:
    args = parse_args()
    sheet = get_sheet()
    all_rows = sheet.get_all_values()
    data_rows = all_rows[1:]

    leads = []
    for row in data_rows:
        if not is_recent(row_get(row, "timestamp"), args.days):
            continue
        if row_get(row, "enrichment_status") == "failed":
            continue
        score_str = row_get(row, "score")
        score = int(score_str) if score_str.isdigit() else 0
        if score < args.min_score:
            continue
        leads.append(row_to_lead(row))

    leads.sort(key=lambda l: l.score, reverse=True)
    top_leads = leads[: args.top]

    # Monday label covers the weekend backlog
    date_str = datetime.now(timezone.utc).strftime("%A, %b %d")
    send_morning_brief(top_leads, date_str)

    print(f"Morning brief posted: {len(top_leads)} leads surfaced (pool: {len(leads)}, days: {args.days})")


if __name__ == "__main__":
    run()
