"""
GHL Setup Script
Run once before first pipeline run.

Usage:
    python -m integrations.ghl_setup

What it does:
1. Creates all 7 custom fields in your GHL location
2. Lists all pipelines so you can identify the right one and its stages
3. Prints a ready-to-paste .env block with all generated field keys
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://services.leadconnectorhq.com"

CUSTOM_FIELDS = [
    ("Job Title",           "TEXT",    "GHL_CF_JOB_TITLE"),
    ("Job URL",             "TEXT",    "GHL_CF_JOB_URL"),
    ("Job Post Date",       "TEXT",    "GHL_CF_JOB_POST_DATE"),
    ("Keyword Category",    "TEXT",    "GHL_CF_KEYWORD_CATEGORY"),
    ("Employee Count",      "TEXT",    "GHL_CF_EMPLOYEE_COUNT"),
    ("Revenue Estimate",    "TEXT",    "GHL_CF_REVENUE_ESTIMATE"),
    ("Enrichment Status",   "TEXT",    "GHL_CF_ENRICHMENT_STATUS"),
]


def headers() -> dict:
    return {
        "Authorization": f"Bearer {os.environ['GHL_API_KEY']}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
    }


def create_custom_fields() -> dict[str, str]:
    location_id = os.environ["GHL_LOCATION_ID"]
    env_map: dict[str, str] = {}

    print("\n── Creating Custom Fields ──")
    for field_name, data_type, env_key in CUSTOM_FIELDS:
        resp = requests.post(
            f"{BASE_URL}/locations/{location_id}/customFields",
            json={"name": field_name, "dataType": data_type, "position": 0},
            headers=headers(),
            timeout=15,
        )
        if resp.status_code in (200, 201):
            field_key = resp.json().get("customField", {}).get("fieldKey", "")
            env_map[env_key] = field_key
            print(f"  ✓ {field_name} → {field_key}")
        elif resp.status_code == 422:
            # Field already exists — try to fetch it
            existing = _find_existing_field(location_id, field_name)
            if existing:
                env_map[env_key] = existing
                print(f"  ~ {field_name} already exists → {existing}")
            else:
                print(f"  ✗ {field_name} — could not create or find: {resp.text}")
        else:
            print(f"  ✗ {field_name} — {resp.status_code}: {resp.text}")

    return env_map


def _find_existing_field(location_id: str, name: str) -> str | None:
    resp = requests.get(
        f"{BASE_URL}/locations/{location_id}/customFields",
        headers=headers(),
        timeout=15,
    )
    if resp.status_code != 200:
        return None
    fields = resp.json().get("customFields", [])
    for f in fields:
        if f.get("name", "").lower() == name.lower():
            return f.get("fieldKey", "")
    return None


def list_pipelines() -> None:
    location_id = os.environ["GHL_LOCATION_ID"]
    resp = requests.get(
        f"{BASE_URL}/opportunities/pipelines",
        params={"locationId": location_id},
        headers=headers(),
        timeout=15,
    )
    if resp.status_code != 200:
        print(f"\n✗ Could not fetch pipelines: {resp.status_code}: {resp.text}")
        return

    print("\n── Pipelines & Stages ──")
    pipelines = resp.json().get("pipelines", [])
    for pl in pipelines:
        print(f"\n  Pipeline: {pl['name']}")
        print(f"    GHL_PIPELINE_ID={pl['id']}")
        for stage in pl.get("stages", []):
            print(f"    Stage: {stage['name']}")
            print(f"      GHL_STAGE_ID_NEW={stage['id']}  ← use this for 'Job Signal — New'")


def print_env_block(env_map: dict[str, str]) -> None:
    print("\n── Paste this into your .env ──\n")
    for env_key, field_key in env_map.items():
        print(f"{env_key}={field_key}")
    print()


def run() -> None:
    required = ["GHL_API_KEY", "GHL_LOCATION_ID"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"✗ Missing required env vars: {', '.join(missing)}")
        sys.exit(1)

    env_map = create_custom_fields()
    list_pipelines()
    print_env_block(env_map)

    print("Next steps:")
    print("  1. Copy GHL_PIPELINE_ID and GHL_STAGE_ID_NEW from the pipelines list above")
    print("  2. Create stage 'Job Signal — New' in GHL if it doesn't exist yet")
    print("  3. Add all values to your .env file")
    print("  4. Run: make dry-run\n")


if __name__ == "__main__":
    run()
