"""
Component Tester — run individual pieces without triggering the full pipeline.

Usage:
    python scripts/test_component.py scrape --source google --keyword ea --limit 3
    python scripts/test_component.py enrich --domain acme.com
    python scripts/test_component.py ghl-push --dry-run
    python scripts/test_component.py slack-test
    python scripts/test_component.py dedup --domain acme.com --keyword ea
"""

import sys
import os
import argparse
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()


def cmd_scrape(args):
    from scraper import google_jobs, linkedin_jobs, indeed_jobs
    from scraper.filters import apply as icp_filter

    source_map = {
        "google": google_jobs.scrape,
        "linkedin": linkedin_jobs.scrape,
        "indeed": indeed_jobs.scrape,
    }

    sources = [args.source] if args.source != "all" else list(source_map.keys())
    limit = args.limit or 5

    for source in sources:
        print(f"\n── {source.upper()} ──")
        try:
            postings = source_map[source](limit)
            if args.keyword:
                postings = [p for p in postings if p.keyword_category == args.keyword]
            postings = icp_filter(postings)
            for p in postings[:limit]:
                print(f"  [{p.keyword_category}] {p.company_name} — {p.job_title}")
                print(f"    domain: {p.company_domain}")
                print(f"    url:    {p.job_url}")
                print(f"    posted: {p.post_date}")
                print(f"    snippet: {p.job_description_snippet[:80]}...")
                print()
            print(f"Total: {len(postings)} postings")
        except Exception as e:
            print(f"  ✗ {e}")


def cmd_enrich(args):
    from enrichment import apollo, hunter

    domain = args.domain
    print(f"\n── Apollo enrichment for: {domain} ──")
    try:
        result = apollo.enrich(domain)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("  No match found")
            print(f"\n── Hunter fallback for: {domain} ──")
            email = hunter.find_email(domain)
            print(f"  email: {email or 'not found'}")
    except Exception as e:
        print(f"  ✗ Apollo: {e}")
        try:
            email = hunter.find_email(domain)
            print(f"  Hunter fallback: {email or 'not found'}")
        except Exception as e2:
            print(f"  ✗ Hunter: {e2}")


def cmd_ghl_push(args):
    from scraper.models import RawPosting, EnrichedLead
    from integrations.ghl import push_lead

    posting = RawPosting(
        job_title="Executive Assistant",
        company_name="Test Company Inc",
        company_domain="testcompany.com",
        location="Los Angeles, CA",
        post_date="2025-01-15",
        job_description_snippet="Looking for an EA to support the founder with scheduling, email, and admin...",
        job_url="https://linkedin.com/jobs/view/12345",
        source="test",
        keyword_category="ea",
    )
    lead = EnrichedLead(
        posting=posting,
        owner_first_name="Jane",
        owner_last_name="Smith",
        owner_email="jane@testcompany.com",
        owner_linkedin_url="https://linkedin.com/in/janesmith",
        employee_count=25,
        revenue_estimate="$2M",
        enrichment_status="complete",
    )

    dry = args.dry_run or os.environ.get("DRY_RUN", "false").lower() == "true"
    print(f"\n── GHL push test (dry_run={dry}) ──")
    try:
        contact_id = push_lead(lead, dry_run=dry)
        print(f"  ✓ contact_id: {contact_id}")
    except Exception as e:
        print(f"  ✗ {e}")


def cmd_slack_test(args):
    from scraper.models import RawPosting, EnrichedLead
    from notifications.slack import send_lead_alert, send_digest

    posting = RawPosting(
        job_title="Executive Assistant",
        company_name="Acme Corp",
        company_domain="acme.com",
        location="Remote",
        post_date="today",
        job_description_snippet="Seeking EA to support CEO with calendar, email, travel...",
        job_url="https://linkedin.com/jobs/view/99999",
        source="google_jobs",
        keyword_category="ea",
        remote_flag=True,
    )
    lead = EnrichedLead(
        posting=posting,
        owner_first_name="Tom",
        owner_last_name="Hanks",
        owner_email="tom@acme.com",
        owner_linkedin_url="https://linkedin.com/in/tomhanks",
        employee_count=18,
        revenue_estimate="$3M",
        enrichment_status="complete",
        ghl_contact_id="test-contact-id-123",
    )

    print("\n── Sending test Slack alert ──")
    try:
        send_lead_alert(lead)
        print("  ✓ Alert sent — check your Slack channel")
    except Exception as e:
        print(f"  ✗ {e}")

    print("\n── Sending test Slack digest ──")
    try:
        send_digest([lead], {"raw": 120, "after_dedup": 45, "pushed_ghl": 38, "sheets_only": 7})
        print("  ✓ Digest sent — check your Slack channel")
    except Exception as e:
        print(f"  ✗ {e}")


def cmd_dedup(args):
    from db.supabase_client import is_duplicate, record_lead

    domain = args.domain
    keyword = args.keyword or "ea"

    print(f"\n── Dedup check: {domain} / {keyword} ──")
    try:
        result = is_duplicate(domain, keyword)
        print(f"  is_duplicate: {result}")
        if not result and args.record:
            record_lead(domain, keyword, "test-contact-id", "complete")
            print(f"  Recorded. Run again to confirm dedup works.")
    except Exception as e:
        print(f"  ✗ {e}")


def main():
    p = argparse.ArgumentParser(description="Component tester")
    sub = p.add_subparsers(dest="command")

    scrape_p = sub.add_parser("scrape")
    scrape_p.add_argument("--source", default="google", choices=["google", "linkedin", "indeed", "all"])
    scrape_p.add_argument("--keyword", default=None, choices=["ea", "social", "bdr", "sales", "video"])
    scrape_p.add_argument("--limit", type=int, default=5)

    enrich_p = sub.add_parser("enrich")
    enrich_p.add_argument("--domain", required=True)

    ghl_p = sub.add_parser("ghl-push")
    ghl_p.add_argument("--dry-run", action="store_true")

    sub.add_parser("slack-test")

    dedup_p = sub.add_parser("dedup")
    dedup_p.add_argument("--domain", required=True)
    dedup_p.add_argument("--keyword", default="ea")
    dedup_p.add_argument("--record", action="store_true", help="Record the lead after checking")

    args = p.parse_args()

    dispatch = {
        "scrape":     cmd_scrape,
        "enrich":     cmd_enrich,
        "ghl-push":   cmd_ghl_push,
        "slack-test": cmd_slack_test,
        "dedup":      cmd_dedup,
    }

    if not args.command or args.command not in dispatch:
        p.print_help()
        sys.exit(1)

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
