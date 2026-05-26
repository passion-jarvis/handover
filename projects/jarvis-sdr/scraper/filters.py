"""
ICP filters applied to raw postings before enrichment.
Drops enterprise job postings and noise before we spend API credits on them.
"""

from .models import RawPosting

# Enterprise signals in job description → these are 200+ person companies
ENTERPRISE_SIGNALS = [
    "fortune 500", "fortune500", "publicly traded", "nasdaq", "nyse",
    "10,000 employees", "50,000 employees", "global team of",
    "series d", "series e", "series f",
    "vp of", "chief of staff to the ceo",    # enterprise-level EA roles
    "staffing agency", "recruiting firm",     # we're not a recruiter
    "w2 employee", "w-2 employee",
]

# Noise signals — staffing companies, job boards posting on behalf of others
NOISE_COMPANY_SIGNALS = [
    "staffing", "recruiting", "talent solutions", "workforce solutions",
    "hired.com", "linkedin", "indeed", "glassdoor", "ziprecruiter",
]

# ICP headcount band
ICP_MIN_EMPLOYEES = 5
ICP_MAX_EMPLOYEES = 200


def is_icp(posting: RawPosting) -> bool:
    """Returns True if the posting passes all ICP filters."""
    if _is_enterprise_description(posting.job_description_snippet):
        return False
    if _is_noise_company(posting.company_name):
        return False
    return True


def _is_enterprise_description(snippet: str) -> bool:
    lower = snippet.lower()
    return any(signal in lower for signal in ENTERPRISE_SIGNALS)


def _is_noise_company(company_name: str) -> bool:
    lower = company_name.lower()
    return any(signal in lower for signal in NOISE_COMPANY_SIGNALS)


def passes_headcount_filter(employee_count: int | None) -> bool:
    if employee_count is None:
        return True  # unknown headcount: let it through, SDR can qualify manually
    return ICP_MIN_EMPLOYEES <= employee_count <= ICP_MAX_EMPLOYEES


def apply(postings: list[RawPosting]) -> list[RawPosting]:
    before = len(postings)
    filtered = [p for p in postings if is_icp(p)]
    dropped = before - len(filtered)
    if dropped:
        import logging
        logging.getLogger(__name__).info(f"ICP filter dropped {dropped}/{before} postings")
    return filtered
