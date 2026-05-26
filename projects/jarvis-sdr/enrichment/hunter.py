import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=8))
def find_email(company_domain: str) -> str | None:
    resp = requests.get(
        "https://api.hunter.io/v2/domain-search",
        params={
            "domain": company_domain,
            "type": "personal",
            "limit": 5,
            "api_key": os.environ["HUNTER_KEY"],
        },
        timeout=15,
    )

    if resp.status_code == 404:
        return None
    resp.raise_for_status()

    data = resp.json().get("data", {})
    emails = data.get("emails", [])
    if not emails:
        return None

    owner_titles = {"ceo", "founder", "owner", "co-founder", "president"}
    for entry in emails:
        position = (entry.get("position") or "").lower()
        if any(t in position for t in owner_titles):
            return entry.get("value")

    return emails[0].get("value") if emails else None
