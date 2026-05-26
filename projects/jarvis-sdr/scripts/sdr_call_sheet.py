"""
SDR Call Sheet Generator
Pulls today's (or last N days') leads from Google Sheets, sorts by score,
exports a clean CSV ready for the SDR to work from.

Usage:
    python scripts/sdr_call_sheet.py                   # today's leads
    python scripts/sdr_call_sheet.py --days 3          # last 3 days
    python scripts/sdr_call_sheet.py --keyword ea      # EA leads only
    python scripts/sdr_call_sheet.py --min-score 60    # score ≥ 60 only
    python scripts/sdr_call_sheet.py --output calls.csv

Output columns (SDR-facing, no internal IDs):
    Priority | Score | Company | Contact | Email | LinkedIn | Phone | Revenue | Size | Signal | Job URL | GHL Link | Notes
"""

import sys
import os
import csv
import argparse
import logging
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.WARNING)

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Match sheets.py header order (0-based)
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

KEYWORD_LABELS = {
    "ea":     "EA Hire",
    "social": "Social Media Hire",
    "bdr":    "BDR Hire",
    "sales":  "Sales Hire",
    "video":  "Video Editor Hire",
}


def parse_args():
    p = argparse.ArgumentParser(description="Generate SDR call sheet from Sheets leads")
    p.add_argument("--days",      type=int,   default=1,    help="Leads from last N days (default: 1)")
    p.add_argument("--keyword",   default=None, choices=["ea","social","bdr","sales","video"])
    p.add_argument("--min-score", type=int,   default=0,    help="Minimum lead score to include")
    p.add_argument("--output",    default=None, help="Output CSV path (default: sdr_calls_YYYYMMDD.csv)")
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
        from datetime import datetime, timedelta, timezone
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(timestamp[:len(fmt)+3], fmt)
                if not dt.tzinfo:
                    dt = dt.replace(tzinfo=timezone.utc)
                return (datetime.now(timezone.utc) - dt).days <= days
            except ValueError:
                continue
    except Exception:
        pass
    return True  # if we can't parse, include it


def run() -> None:
    args = parse_args()
    sheet = get_sheet()

    all_rows = sheet.get_all_values()
    data_rows = all_rows[1:]  # skip header

    output_rows = []
    priority = 1

    for i, row in enumerate(data_rows):
        # Filters
        timestamp = row_get(row, "timestamp")
        if not is_recent(timestamp, args.days):
            continue

        enrichment = row_get(row, "enrichment_status")
        if enrichment == "failed":
            continue  # no contact data, SDR can't call

        score_str = row_get(row, "score")
        score = int(score_str) if score_str.isdigit() else 0
        if score < args.min_score:
            continue

        keyword = row_get(row, "keyword_category")
        if args.keyword and keyword != args.keyword:
            continue

        ghl_id = row_get(row, "ghl_contact_id")
        ghl_link = f"https://app.gohighlevel.com/contacts/{ghl_id}" if ghl_id else ""

        output_rows.append({
            "Priority":    priority,
            "Score":       score,
            "Company":     row_get(row, "company_name"),
            "Website":     row_get(row, "company_domain"),
            "Contact":     row_get(row, "contact_name"),
            "Email":       row_get(row, "email"),
            "LinkedIn":    row_get(row, "linkedin"),
            "Revenue Est": row_get(row, "revenue"),
            "Employees":   row_get(row, "employee_count"),
            "Signal":      KEYWORD_LABELS.get(keyword, keyword),
            "Job Title":   row_get(row, "job_title"),
            "Posted":      row_get(row, "post_date"),
            "Job URL":     row_get(row, "job_url"),
            "GHL":         ghl_link,
            "Enrichment":  enrichment,
            "Location":    row_get(row, "location"),
            "Notes":       "",
        })
        priority += 1

    # Sort by score descending
    output_rows.sort(key=lambda r: r["Score"], reverse=True)
    for i, r in enumerate(output_rows, 1):
        r["Priority"] = i

    if not output_rows:
        print(f"No leads match filters (days={args.days}, keyword={args.keyword}, min_score={args.min_score})")
        return

    outfile = args.output or f"sdr_calls_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nCall sheet exported: {outfile}")
    print(f"Leads: {len(output_rows)} | Score range: {output_rows[-1]['Score']}–{output_rows[0]['Score']}")
    print(f"Top 5 leads:")
    for r in output_rows[:5]:
        print(f"  [{r['Score']}] {r['Company']} — {r['Contact']} | {r['Signal']}")
    print()


if __name__ == "__main__":
    run()
