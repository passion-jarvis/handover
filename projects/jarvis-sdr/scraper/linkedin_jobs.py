import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from .models import RawPosting
from .keyword_config import KEYWORDS

US_GEO_ID = "103644278"


def scrape(max_results: int = 50) -> list[RawPosting]:
    postings: list[RawPosting] = []

    for category, config in KEYWORDS.items():
        jobs = _fetch(config["linkedin"], max_results)
        for job in jobs:
            postings.append(
                RawPosting(
                    job_title=job.get("title", ""),
                    company_name=job.get("company", {}).get("name", ""),
                    company_domain=_extract_domain(job),
                    location=job.get("location", ""),
                    post_date=job.get("listed_at", ""),
                    job_description_snippet=(job.get("description", "") or "")[:300],
                    job_url=job.get("job_url", ""),
                    source="linkedin",
                    keyword_category=category,
                    remote_flag="remote" in (job.get("work_type", "") or "").lower(),
                )
            )

    return postings


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _fetch(keyword: str, max_results: int) -> list[dict]:
    resp = requests.get(
        "https://nubela.co/proxycurl/api/linkedin/jobs",
        params={
            "keyword": keyword,
            "geo_id": US_GEO_ID,
            "date_posted": "past-week",
            "count": min(max_results, 100),
        },
        headers={"Authorization": f"Bearer {os.environ['PROXYCURL_KEY']}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("job", [])


def _extract_domain(job: dict) -> str:
    url = job.get("company", {}).get("url", "") or ""
    if not url:
        return ""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return parsed.netloc.replace("www.", "")
