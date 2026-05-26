import os
import gspread
from google.oauth2.service_account import Credentials
from scraper.models import EnrichedLead

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

_sheet_cache = None


def _get_sheet():
    global _sheet_cache
    if _sheet_cache is None:
        creds = Credentials.from_service_account_file(
            os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"],
            scopes=SCOPES,
        )
        gc = gspread.authorize(creds)
        spreadsheet = gc.open_by_key(os.environ["GOOGLE_SHEETS_SPREADSHEET_ID"])
        tab = os.environ.get("GOOGLE_SHEETS_TAB_NAME", "Leads")
        try:
            _sheet_cache = spreadsheet.worksheet(tab)
        except gspread.WorksheetNotFound:
            _sheet_cache = spreadsheet.add_worksheet(title=tab, rows=5000, cols=22)
            _write_header(_sheet_cache)
    return _sheet_cache


def _write_header(sheet) -> None:
    sheet.append_row([
        "Score", "Timestamp", "Company Name", "Company Domain", "Job Title", "Keyword Category",
        "Source", "Job URL", "Post Date", "Location", "Remote",
        "Job Description Snippet", "Contact Name", "Contact Email", "Contact LinkedIn",
        "Company LinkedIn", "Employee Count", "Revenue Estimate", "Enrichment Status",
        "GHL Contact ID", "SDR Assigned", "Notes",
    ])


def append_lead(lead: EnrichedLead) -> None:
    p = lead.posting
    sheet = _get_sheet()
    sheet.append_row([
        lead.score,
        p.scrape_timestamp,
        p.company_name,
        p.company_domain,
        p.job_title,
        p.keyword_category,
        p.source,
        p.job_url,
        p.post_date,
        p.location,
        str(p.remote_flag),
        p.job_description_snippet,
        f"{lead.owner_first_name} {lead.owner_last_name}".strip(),
        lead.owner_email,
        lead.owner_linkedin_url,
        lead.company_linkedin_url,
        str(lead.employee_count or ""),
        lead.revenue_estimate,
        lead.enrichment_status,
        lead.ghl_contact_id or "",
        "",
        "",
    ])
