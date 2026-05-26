import os
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client

_client: Client | None = None


def _get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_SERVICE_KEY"],
        )
    return _client


def is_duplicate(company_domain: str, keyword_category: str, window_days: int = 30) -> bool:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=window_days)).isoformat()
    result = (
        _get_client()
        .table("scraped_leads")
        .select("id, first_seen_at")
        .eq("company_domain", company_domain.lower())
        .eq("keyword_category", keyword_category)
        .gte("first_seen_at", cutoff)
        .execute()
    )
    return len(result.data) > 0


def record_lead(company_domain: str, keyword_category: str, ghl_contact_id: str | None, enrichment_status: str) -> None:
    _get_client().table("scraped_leads").upsert(
        {
            "company_domain": company_domain.lower(),
            "keyword_category": keyword_category,
            "first_seen_at": datetime.now(timezone.utc).isoformat(),
            "ghl_contact_id": ghl_contact_id,
            "enrichment_status": enrichment_status,
        },
        on_conflict="company_domain,keyword_category",
    ).execute()
