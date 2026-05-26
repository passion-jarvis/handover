"""
Import no-website leads into GHL
Creates contacts with tag "website-hustle" and source "Website Hustle"
"""

import csv
import requests
import time
import sys
import json

API_KEY = "pit-a4d0717b-7349-4eb3-8e37-cb3f1da9a498"
LOCATION_ID = "quW9l8ARPHQVeA5FC13T"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Content-Type": "application/json"
}

CSV_FILE = "/Users/passionchu/claude/projects/website-hustle/leads_hair_salon_california_20260405_2240.csv"


def import_leads():
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total = len(rows)
    success = 0
    skipped = 0
    failed = 0

    print(f"Importing {total} leads to GHL...\n")

    for i, row in enumerate(rows):
        name = row.get("Business Name", "").strip()
        phone = row.get("Phone", "").strip()
        address = row.get("Address", "").strip()
        rating = row.get("Rating", "").strip()
        reviews = row.get("Reviews", "").strip()
        maps_url = row.get("Google Maps URL", "").strip()

        if not name:
            skipped += 1
            continue

        # Clean phone
        phone_clean = phone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        if phone_clean and not phone_clean.startswith("+"):
            phone_clean = f"+1{phone_clean}"

        payload = {
            "locationId": LOCATION_ID,
            "name": name,
            "companyName": name,
            "phone": phone_clean if phone_clean else None,
            "address1": address,
            "source": "Website Hustle",
            "tags": ["website-hustle", "no-website", "hair-salon"],
            "customFields": [
                {"key": "google_rating", "field_value": rating},
                {"key": "google_reviews", "field_value": reviews},
                {"key": "google_maps_url", "field_value": maps_url},
            ]
        }

        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            res = requests.post(
                "https://services.leadconnectorhq.com/contacts/",
                headers=HEADERS,
                json=payload,
                timeout=10
            )

            if res.status_code in [200, 201]:
                success += 1
                print(f"  [{i+1}/{total}] ✓ {name}")
            elif res.status_code == 422:
                skipped += 1
                print(f"  [{i+1}/{total}] ~ {name} (duplicate)")
            else:
                failed += 1
                print(f"  [{i+1}/{total}] ✗ {name} — {res.status_code}: {res.text[:80]}")

        except Exception as e:
            failed += 1
            print(f"  [{i+1}/{total}] ✗ {name} — {e}")

        # Rate limit: 10 requests/sec max
        time.sleep(0.15)

        # Progress checkpoint every 100
        if (i + 1) % 100 == 0:
            print(f"\n  --- {i+1}/{total} done | {success} imported | {skipped} skipped | {failed} failed ---\n")

    print(f"\nDone. {success} imported | {skipped} skipped | {failed} failed")


if __name__ == "__main__":
    import_leads()
