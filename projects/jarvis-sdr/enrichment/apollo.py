import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

OWNER_TITLES = ["CEO", "Founder", "Co-Founder", "Owner", "President", "Managing Director", "Principal"]

BASE_URL = "https://api.apollo.io/v1"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def enrich(company_domain: str) -> dict | None:
    resp = requests.post(
        f"{BASE_URL}/people/match",
        json={
            "api_key": os.environ["APOLLO_KEY"],
            "domain": company_domain,
            "title": OWNER_TITLES,
            "reveal_personal_emails": True,
            "reveal_phone_number": False,
        },
        timeout=20,
    )

    if resp.status_code == 404:
        return None
    resp.raise_for_status()

    data = resp.json()
    person = data.get("person")
    if not person:
        return None

    org = person.get("organization") or {}
    email = _best_email(person)

    return {
        "first_name": person.get("first_name", ""),
        "last_name": person.get("last_name", ""),
        "email": email,
        "linkedin_url": person.get("linkedin_url", ""),
        "company_linkedin_url": org.get("linkedin_url", ""),
        "employee_count": org.get("estimated_num_employees"),
        "revenue_estimate": _format_revenue(org.get("estimated_annual_revenue")),
    }


def _best_email(person: dict) -> str:
    if person.get("email") and person.get("email_status") == "verified":
        return person["email"]
    personal = person.get("personal_emails") or []
    if personal:
        return personal[0]
    return person.get("email", "")


def _format_revenue(raw: str | None) -> str:
    if not raw:
        return ""
    mapping = {
        "1000000": "$1M",
        "5000000": "$5M",
        "10000000": "$10M",
        "50000000": "$50M",
    }
    return mapping.get(str(raw), str(raw))
