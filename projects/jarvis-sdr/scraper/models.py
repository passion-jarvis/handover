from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RawPosting:
    job_title: str
    company_name: str
    company_domain: str
    location: str
    post_date: str
    job_description_snippet: str
    job_url: str
    source: str
    keyword_category: str
    salary_range: str | None = None
    remote_flag: bool = False
    scrape_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class EnrichedLead:
    posting: RawPosting
    owner_first_name: str = ""
    owner_last_name: str = ""
    owner_email: str = ""
    owner_linkedin_url: str = ""
    company_linkedin_url: str = ""
    employee_count: int | None = None
    revenue_estimate: str = ""
    enrichment_status: str = "failed"  # complete | partial | failed
    ghl_contact_id: str | None = None
    score: int = 0
