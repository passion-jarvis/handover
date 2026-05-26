"""
Lead Scorer — ranks enriched leads 0-100 so SDRs work the best ones first.

Scoring breakdown (max 100):
  Recency:      0-25   (how fresh the job posting is)
  Headcount:    0-20   (ICP size band fit)
  Revenue:      0-15   (estimated annual revenue)
  Enrichment:   0-25   (data completeness)
  Keyword:      0-15   (intent signal strength per category)
"""

import re
from datetime import datetime, timedelta, timezone
from .models import EnrichedLead
from .keyword_config import KEYWORD_INTENT_WEIGHT


def score(lead: EnrichedLead) -> int:
    total = 0
    total += _recency_score(lead.posting.post_date)
    total += _headcount_score(lead.employee_count)
    total += _revenue_score(lead.revenue_estimate)
    total += _enrichment_score(lead)
    total += KEYWORD_INTENT_WEIGHT.get(lead.posting.keyword_category, 0)
    return min(100, max(0, total))


def _recency_score(post_date: str) -> int:
    """Parse various date formats from scrapers and score freshness."""
    if not post_date:
        return 5

    days = _parse_days_ago(post_date)
    if days is None:
        return 5
    if days <= 1:
        return 25
    if days <= 3:
        return 20
    if days <= 7:
        return 12
    if days <= 14:
        return 5
    return 0


def _parse_days_ago(post_date: str) -> int | None:
    lower = post_date.lower().strip()

    # "today", "just posted", "less than an hour ago"
    if any(w in lower for w in ("today", "just posted", "hour ago", "hours ago", "minute")):
        return 0

    # "1 day ago", "3 days ago"
    match = re.search(r"(\d+)\s+day", lower)
    if match:
        return int(match.group(1))

    # "1 week ago", "2 weeks ago"
    match = re.search(r"(\d+)\s+week", lower)
    if match:
        return int(match.group(1)) * 7

    # "1 month ago"
    match = re.search(r"(\d+)\s+month", lower)
    if match:
        return int(match.group(1)) * 30

    # ISO8601: "2025-01-14T00:00:00Z" or "2025-01-14"
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(post_date[:len(fmt)], fmt).replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - dt).days
        except ValueError:
            continue

    return None


def _headcount_score(employee_count: int | None) -> int:
    if employee_count is None:
        return 8  # unknown: neutral score, SDR can qualify
    if 10 <= employee_count <= 30:
        return 20  # sweet spot: small team, owner is definitely wearing hats
    if 31 <= employee_count <= 75:
        return 15
    if 5 <= employee_count <= 9:
        return 12  # very small: could be too early, but still worth a call
    if 76 <= employee_count <= 150:
        return 8
    if 151 <= employee_count <= 200:
        return 3
    return 0


def _revenue_score(revenue_estimate: str) -> int:
    if not revenue_estimate:
        return 5

    lower = revenue_estimate.lower()

    # Extract numeric value
    match = re.search(r"\$?([\d.]+)\s*([mk]?)", lower)
    if not match:
        return 5

    num = float(match.group(1))
    unit = match.group(2)
    if unit == "m":
        num *= 1_000_000
    elif unit == "k":
        num *= 1_000

    if 1_000_000 <= num <= 5_000_000:
        return 15  # core ICP: $1M-$5M
    if 5_000_001 <= num <= 10_000_000:
        return 10  # upper ICP: $5M-$10M
    if 500_000 <= num < 1_000_000:
        return 6   # below ICP but worth a call
    if num > 10_000_000:
        return 3   # above ICP, probably too big
    return 0


def _enrichment_score(lead: EnrichedLead) -> int:
    if lead.enrichment_status == "complete":
        # Has email + LinkedIn
        return 25
    if lead.enrichment_status == "partial":
        # Has email OR LinkedIn, not both
        if lead.owner_email and lead.owner_linkedin_url:
            return 20
        if lead.owner_email:
            return 15
        if lead.owner_linkedin_url:
            return 10
        return 8
    return 0  # failed enrichment


def rank(leads: list[EnrichedLead]) -> list[tuple[int, EnrichedLead]]:
    """Returns list of (score, lead) sorted descending by score."""
    scored = [(score(lead), lead) for lead in leads]
    return sorted(scored, key=lambda x: x[0], reverse=True)
