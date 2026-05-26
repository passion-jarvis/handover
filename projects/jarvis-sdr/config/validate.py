import os
import sys

ALL_VARS = {
    # scraping
    "SERPAPI_KEY":                  "SerpAPI — serpapi.com",
    "PROXYCURL_KEY":                "Proxycurl — proxycurl.com",
    "APIFY_KEY":                    "Apify — apify.com",
    # enrichment
    "APOLLO_KEY":                   "Apollo.io — apollo.io",
    "HUNTER_KEY":                   "Hunter.io — hunter.io (fallback enrichment)",
    # ghl
    "GHL_API_KEY":                  "GHL API key — Settings → API Keys",
    "GHL_LOCATION_ID":              "GHL Location ID — Settings → Business Info",
    "GHL_PIPELINE_ID":              "GHL Pipeline ID — run: make setup-ghl",
    "GHL_STAGE_ID_NEW":             "GHL Stage ID for 'Job Signal — New' — run: make setup-ghl",
    # supabase
    "SUPABASE_URL":                 "Supabase project URL — supabase.com",
    "SUPABASE_SERVICE_KEY":         "Supabase service role key",
    # sheets
    "GOOGLE_SHEETS_SPREADSHEET_ID": "Google Sheets spreadsheet ID from the URL",
    "GOOGLE_SERVICE_ACCOUNT_JSON":  "Path to GCP service account JSON file",
    # slack
    "SLACK_WEBHOOK_URL":            "Slack incoming webhook URL",
}

PIPELINE_CORE = [
    "SERPAPI_KEY", "APOLLO_KEY", "GHL_API_KEY", "GHL_LOCATION_ID",
    "GHL_PIPELINE_ID", "GHL_STAGE_ID_NEW", "SUPABASE_URL", "SUPABASE_SERVICE_KEY",
    "SLACK_WEBHOOK_URL",
]


def check_required(keys: list[str], exit_on_fail: bool = True) -> bool:
    missing = []
    for key in keys:
        val = os.environ.get(key, "").strip()
        if not val:
            hint = ALL_VARS.get(key, "")
            missing.append(f"  {key}  ←  {hint}" if hint else f"  {key}")

    if missing:
        print("\n✗ Missing required environment variables:\n")
        for m in missing:
            print(m)
        print("\nCopy .env.example to .env and fill in the missing values.\n")
        if exit_on_fail:
            sys.exit(1)
        return False
    return True


def check_pipeline_core() -> None:
    check_required(PIPELINE_CORE)


def check_file_exists(path_env_key: str) -> None:
    path = os.environ.get(path_env_key, "")
    if path and not os.path.isfile(path):
        print(f"\n✗ File not found: {path_env_key}={path}")
        print("  Download your GCP service account JSON and update the path in .env.\n")
        sys.exit(1)
