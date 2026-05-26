"""
Jarvis SDR Job Signal Pipeline
Run: python pipeline.py
Schedule: daily at 6 AM PT via GitHub Actions (.github/workflows/daily-pipeline.yml)

Flags:
    --source    google|linkedin|indeed|all  (default: all)
    --keyword   ea|social|bdr|sales|video   (default: all)
    --limit     N per keyword per source    (default: env MAX_RESULTS_PER_KEYWORD)
    --dry-run   skip GHL writes             (default: env DRY_RUN)
"""

import os
import sys
import logging
import argparse
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

from config.validate import check_pipeline_core, check_file_exists
from scraper import google_jobs, linkedin_jobs, indeed_jobs
from scraper.models import RawPosting, EnrichedLead
from scraper.filters import apply as icp_filter, passes_headcount_filter
from scraper import lead_scorer
from enrichment import apollo, hunter
from integrations import ghl, sheets
from notifications import slack
from db import supabase_client

DEDUP_WINDOW = int(os.environ.get("DEDUP_WINDOW_DAYS", "30"))

SOURCE_MAP = {
    "google":   google_jobs.scrape,
    "linkedin": linkedin_jobs.scrape,
    "indeed":   indeed_jobs.scrape,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Jarvis SDR Job Signal Pipeline")
    p.add_argument("--source",   default="all", choices=["google", "linkedin", "indeed", "all"])
    p.add_argument("--keyword",  default=None,  choices=["ea", "social", "bdr", "sales", "video"])
    p.add_argument("--limit",    type=int,      default=int(os.environ.get("MAX_RESULTS_PER_KEYWORD", "50")))
    p.add_argument("--dry-run",  action="store_true", default=os.environ.get("DRY_RUN", "false").lower() == "true")
    return p.parse_args()


def run(args: argparse.Namespace) -> None:
    log.info(f"Pipeline start — source={args.source} keyword={args.keyword or 'all'} limit={args.limit} dry_run={args.dry_run}")
    stats = {"raw": 0, "after_dedup": 0, "pushed_ghl": 0, "sheets_only": 0}

    # 1. SCRAPE
    sources = [args.source] if args.source != "all" else list(SOURCE_MAP.keys())
    raw: list[RawPosting] = []
    for source in sources:
        raw += _safe_scrape(source, SOURCE_MAP[source], args.limit)

    if args.keyword:
        raw = [p for p in raw if p.keyword_category == args.keyword]

    stats["raw"] = len(raw)
    log.info(f"Scraped {len(raw)} raw postings")

    # 2. ICP FILTER
    raw = icp_filter(raw)

    # 3. DEDUP
    new_postings = _dedup(raw)
    stats["after_dedup"] = len(new_postings)
    log.info(f"{len(new_postings)} postings after ICP filter + dedup")

    # 4. ENRICH
    enriched: list[EnrichedLead] = []
    for posting in new_postings:
        lead = _enrich(posting)
        enriched.append(lead)

    # 5. SCORE + SORT (best leads routed first, SDR sees them first in GHL)
    ranked = lead_scorer.rank(enriched)
    for s, lead in ranked:
        lead.score = s
    enriched = [lead for _, lead in ranked]
    log.info(f"Lead scores: min={ranked[-1][0] if ranked else 0} max={ranked[0][0] if ranked else 0}")

    # 6. ROUTE
    for lead in enriched:
        _route(lead, stats, dry_run=args.dry_run)

    # 6. DIGEST
    slack.send_digest(enriched, stats)
    log.info(f"Pipeline complete: {stats}")


def _safe_scrape(name: str, fn, max_results: int) -> list[RawPosting]:
    try:
        results = fn(max_results)
        log.info(f"{name}: {len(results)} postings")
        return results
    except Exception as e:
        log.error(f"{name} scrape failed: {e}")
        return []


def _dedup(postings: list[RawPosting]) -> list[RawPosting]:
    seen_in_run: set[tuple] = set()
    result: list[RawPosting] = []

    for p in postings:
        domain = (p.company_domain or p.company_name).lower().strip()
        if not domain:
            continue

        run_key = (domain, p.keyword_category)
        if run_key in seen_in_run:
            continue
        seen_in_run.add(run_key)

        try:
            if supabase_client.is_duplicate(domain, p.keyword_category, DEDUP_WINDOW):
                log.debug(f"Dedup skip: {domain} / {p.keyword_category}")
                continue
        except Exception as e:
            log.warning(f"Supabase dedup check failed ({domain}): {e} — proceeding")

        result.append(p)

    return result


def _enrich(posting: RawPosting) -> EnrichedLead:
    lead = EnrichedLead(posting=posting)
    domain = posting.company_domain

    if not domain:
        log.debug(f"No domain for {posting.company_name} — skipping enrichment")
        lead.enrichment_status = "failed"
        return lead

    try:
        result = apollo.enrich(domain)
        if result:
            lead.owner_first_name     = result.get("first_name", "")
            lead.owner_last_name      = result.get("last_name", "")
            lead.owner_email          = result.get("email", "")
            lead.owner_linkedin_url   = result.get("linkedin_url", "")
            lead.company_linkedin_url = result.get("company_linkedin_url", "")
            lead.employee_count       = result.get("employee_count")
            lead.revenue_estimate     = result.get("revenue_estimate", "")
    except Exception as e:
        log.warning(f"Apollo enrichment failed ({domain}): {e}")

    if not passes_headcount_filter(lead.employee_count):
        log.debug(f"ICP headcount filter: {posting.company_name} ({lead.employee_count} employees)")
        lead.enrichment_status = "failed"
        return lead

    if lead.owner_email:
        lead.enrichment_status = "complete" if lead.owner_linkedin_url else "partial"
    else:
        try:
            fallback_email = hunter.find_email(domain)
            if fallback_email:
                lead.owner_email = fallback_email
                lead.enrichment_status = "partial"
            else:
                lead.enrichment_status = "failed"
        except Exception as e:
            log.warning(f"Hunter fallback failed ({domain}): {e}")
            lead.enrichment_status = "failed"

    log.info(f"Enriched: {posting.company_name} — {lead.enrichment_status} | email={bool(lead.owner_email)}")
    return lead


def _route(lead: EnrichedLead, stats: dict, dry_run: bool) -> None:
    p = lead.posting
    domain = (p.company_domain or p.company_name).lower()

    try:
        sheets.append_lead(lead)
    except Exception as e:
        log.error(f"Sheets append failed ({p.company_name}): {e}")

    if lead.enrichment_status == "failed":
        stats["sheets_only"] += 1
        log.info(f"Sheets-only (no contact data): {p.company_name}")
        return

    try:
        contact_id = ghl.push_lead(lead, dry_run=dry_run)
        lead.ghl_contact_id = contact_id
        stats["pushed_ghl"] += 1
        log.info(f"GHL pushed: {p.company_name} [{contact_id}]")
    except Exception as e:
        log.error(f"GHL push failed ({p.company_name}): {e}")
        stats["sheets_only"] += 1

    try:
        slack.send_lead_alert(lead)
    except Exception as e:
        log.warning(f"Slack alert failed: {e}")

    if not dry_run:
        try:
            supabase_client.record_lead(domain, p.keyword_category, lead.ghl_contact_id, lead.enrichment_status)
        except Exception as e:
            log.warning(f"Supabase record failed ({domain}): {e}")


if __name__ == "__main__":
    check_pipeline_core()
    check_file_exists("GOOGLE_SERVICE_ACCOUNT_JSON")
    run(parse_args())
