import os
from apify_client import ApifyClient
from .models import RawPosting
from .keyword_config import KEYWORDS


def scrape(max_results: int = 50) -> list[RawPosting]:
    client = ApifyClient(os.environ["APIFY_KEY"])
    postings: list[RawPosting] = []

    for category, config in KEYWORDS.items():
        jobs = _run_actor(client, config["indeed"], max_results)
        for job in jobs:
            postings.append(
                RawPosting(
                    job_title=job.get("positionName", ""),
                    company_name=job.get("company", ""),
                    company_domain=_extract_domain(job),
                    location=job.get("location", ""),
                    post_date=job.get("postedAt", ""),
                    job_description_snippet=(job.get("description", "") or "")[:300],
                    job_url=job.get("url", ""),
                    source="indeed",
                    keyword_category=category,
                    salary_range=job.get("salary", None),
                    remote_flag=job.get("isRemote", False),
                )
            )

    return postings


def _run_actor(client: ApifyClient, keyword: str, max_results: int) -> list[dict]:
    run = client.actor("apify/indeed-scraper").call(
        run_input={
            "queries": [keyword],
            "location": "United States",
            "country": "US",
            "maxItems": min(max_results, 200),
            "saveOnlyUniqueItems": True,
            "proxyConfiguration": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
        }
    )
    if not run:
        return []
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())


def _extract_domain(job: dict) -> str:
    url = job.get("externalApplyUrl", "") or job.get("url", "") or ""
    if not url:
        return ""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    netloc = parsed.netloc.replace("www.", "")
    if "indeed.com" in netloc:
        return ""
    return netloc
