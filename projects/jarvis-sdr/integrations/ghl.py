import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from scraper.models import EnrichedLead

BASE_URL = "https://services.leadconnectorhq.com"

KEYWORD_TAGS = {
    "ea":     "hiring-ea",
    "social": "hiring-social",
    "bdr":    "hiring-bdr",
    "sales":  "hiring-sales",
    "video":  "hiring-video",
}


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {os.environ['GHL_API_KEY']}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
    }


def push_lead(lead: EnrichedLead, dry_run: bool = False) -> str | None:
    if dry_run:
        print(f"[DRY RUN] Would push: {lead.posting.company_name} <{lead.owner_email}>")
        return "dry-run-id"

    contact_id = _find_existing_contact(lead.owner_email, lead.posting.company_domain)
    if not contact_id:
        contact_id = _create_contact(lead)
    if not contact_id:
        return None

    _create_opportunity(contact_id, lead)
    _add_note(contact_id, lead)
    return contact_id


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _find_existing_contact(email: str, domain: str) -> str | None:
    if email:
        resp = requests.get(
            f"{BASE_URL}/contacts/search/duplicate",
            params={"email": email, "locationId": os.environ["GHL_LOCATION_ID"]},
            headers=_headers(),
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            contacts = data.get("contacts", [])
            if contacts:
                return contacts[0]["id"]
    return None


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _create_contact(lead: EnrichedLead) -> str | None:
    p = lead.posting
    keyword_tag = KEYWORD_TAGS.get(p.keyword_category, "job-signal")

    payload = {
        "locationId": os.environ["GHL_LOCATION_ID"],
        "firstName": lead.owner_first_name,
        "lastName": lead.owner_last_name,
        "email": lead.owner_email,
        "companyName": p.company_name,
        "website": f"https://{p.company_domain}" if p.company_domain else "",
        "source": "Job Signal Scraper",
        "tags": ["job-signal", keyword_tag, f"enrichment:{lead.enrichment_status}"],
        "customFields": _build_custom_fields(lead),
    }

    resp = requests.post(
        f"{BASE_URL}/contacts/",
        json=payload,
        headers=_headers(),
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("contact", {}).get("id")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _create_opportunity(contact_id: str, lead: EnrichedLead) -> None:
    p = lead.posting
    resp = requests.post(
        f"{BASE_URL}/opportunities/",
        json={
            "pipelineId": os.environ["GHL_PIPELINE_ID"],
            "pipelineStageId": os.environ["GHL_STAGE_ID_NEW"],
            "contactId": contact_id,
            "name": f"{p.company_name} — {p.job_title} Signal",
            "source": "Job Posting Scraper",
            "status": "open",
        },
        headers=_headers(),
        timeout=15,
    )
    resp.raise_for_status()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _add_note(contact_id: str, lead: EnrichedLead) -> None:
    p = lead.posting
    body = (
        f"JOB SIGNAL ALERT\n\n"
        f"Title: {p.job_title}\n"
        f"Posted: {p.post_date}\n"
        f"Source: {p.source}\n"
        f"URL: {p.job_url}\n\n"
        f"Snippet:\n{p.job_description_snippet}\n\n"
        f"---\n"
        f"Revenue: ~{lead.revenue_estimate}\n"
        f"Employees: {lead.employee_count}\n"
        f"LinkedIn: {lead.owner_linkedin_url}"
    )
    resp = requests.post(
        f"{BASE_URL}/contacts/{contact_id}/notes",
        json={"body": body},
        headers=_headers(),
        timeout=15,
    )
    resp.raise_for_status()


def _build_custom_fields(lead: EnrichedLead) -> list[dict]:
    p = lead.posting
    fields = {
        "GHL_CF_JOB_TITLE":         p.job_title,
        "GHL_CF_JOB_URL":           p.job_url,
        "GHL_CF_JOB_POST_DATE":     p.post_date,
        "GHL_CF_KEYWORD_CATEGORY":  p.keyword_category,
        "GHL_CF_EMPLOYEE_COUNT":    str(lead.employee_count or ""),
        "GHL_CF_REVENUE_ESTIMATE":  lead.revenue_estimate,
        "GHL_CF_ENRICHMENT_STATUS": lead.enrichment_status,
    }
    return [
        {"key": os.environ.get(env_key, ""), "value": value}
        for env_key, value in fields.items()
        if os.environ.get(env_key) and value
    ]
