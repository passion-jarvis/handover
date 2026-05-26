import os
import logging
from urllib.parse import urlparse
from serpapi import GoogleSearch
from .models import RawPosting
from .keyword_config import KEYWORDS

log = logging.getLogger(__name__)

RESULTS_PER_PAGE = 10  # Google Jobs API fixed page size


def scrape(max_results: int = 50) -> list[RawPosting]:
    postings: list[RawPosting] = []

    for category, config in KEYWORDS.items():
        results = _paginate(config["google"], max_results)
        for job in results:
            postings.append(
                RawPosting(
                    job_title=job.get("title", ""),
                    company_name=job.get("company_name", ""),
                    company_domain=_extract_domain(job),
                    location=job.get("location", ""),
                    post_date=job.get("detected_extensions", {}).get("posted_at", ""),
                    job_description_snippet=(job.get("description", "") or "")[:300],
                    job_url=_extract_job_url(job),
                    source="google_jobs",
                    keyword_category=category,
                    salary_range=job.get("detected_extensions", {}).get("salary"),
                    remote_flag="remote" in (job.get("location", "") or "").lower(),
                )
            )

    return postings


def _paginate(query: str, max_results: int) -> list[dict]:
    all_results: list[dict] = []
    start = 0
    pages_needed = (max_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE

    for page in range(pages_needed):
        if len(all_results) >= max_results:
            break
        page_results = _fetch_page(query, start)
        if not page_results:
            break  # no more results
        all_results.extend(page_results)
        start += RESULTS_PER_PAGE
        log.debug(f"Google Jobs [{query}] page {page+1}: {len(page_results)} results")

    return all_results[:max_results]


def _fetch_page(query: str, start: int) -> list[dict]:
    try:
        search = GoogleSearch({
            "engine":   "google_jobs",
            "q":        query,
            "location": "United States",
            "hl":       "en",
            "gl":       "us",
            "chips":    "date_posted:week",
            "start":    start,
            "api_key":  os.environ["SERPAPI_KEY"],
        })
        return search.get_dict().get("jobs_results", [])
    except Exception as e:
        log.warning(f"Google Jobs page fetch failed (start={start}): {e}")
        return []


def _extract_job_url(job: dict) -> str:
    for link in job.get("related_links", []):
        href = link.get("link", "")
        if href.startswith("http") and "google.com" not in href:
            return href
    # fallback: construct search URL from job_id
    job_id = job.get("job_id", "")
    if job_id:
        return f"https://www.google.com/search?q=jobs&ibp=htl;jobs#htivrt=jobs&htidocid={job_id}"
    return ""


def _extract_domain(job: dict) -> str:
    for link in job.get("related_links", []):
        href = link.get("link", "")
        if href.startswith("http"):
            netloc = urlparse(href).netloc.replace("www.", "")
            if netloc and "google.com" not in netloc:
                return netloc
    return ""
