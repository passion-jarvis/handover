import os
import requests
from scraper.models import EnrichedLead

KEYWORD_LABELS = {
    "ea":     "EA Hire",
    "social": "Social Media Hire",
    "bdr":    "BDR Hire",
    "sales":  "Sales Hire",
    "video":  "Video Editor Hire",
}


def _post(webhook: str, text: str) -> None:
    requests.post(webhook, json={"text": text}, timeout=10)


def send_lead_alert(lead: EnrichedLead) -> None:
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        return

    p = lead.posting
    contact_line = (
        f"*Contact:* {lead.owner_first_name} {lead.owner_last_name} | {lead.owner_email}"
        if lead.owner_email
        else f"*Contact:* {lead.owner_first_name} {lead.owner_last_name} (no email)"
    )
    ghl_link = (
        f"https://app.gohighlevel.com/contacts/{lead.ghl_contact_id}"
        if lead.ghl_contact_id and lead.ghl_contact_id != "dry-run-id"
        else "n/a"
    )
    score_bar = "█" * (lead.score // 10) + "░" * (10 - lead.score // 10)

    text = (
        f"*New Job Signal*  `{lead.score}/100` {score_bar}\n"
        f"*Company:* {p.company_name}  |  {p.company_domain}\n"
        f"*Signal:* {p.job_title} ({KEYWORD_LABELS.get(p.keyword_category, p.keyword_category)}) — {p.post_date}\n"
        f"*Source:* {p.source}\n"
        f"{contact_line}\n"
        f"*LinkedIn:* {lead.owner_linkedin_url or 'n/a'}\n"
        f"*Size:* ~{lead.employee_count or '?'} employees  |  ~{lead.revenue_estimate or '?'}\n"
        f"*Job:* {p.job_url}\n"
        f"*GHL:* {ghl_link}"
    )
    _post(webhook, text)


def send_digest(leads: list[EnrichedLead], run_stats: dict) -> None:
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        return

    complete = sum(1 for l in leads if l.enrichment_status == "complete")
    partial  = sum(1 for l in leads if l.enrichment_status == "partial")
    failed   = sum(1 for l in leads if l.enrichment_status == "failed")

    by_category: dict[str, int] = {}
    for lead in leads:
        cat = lead.posting.keyword_category
        by_category[cat] = by_category.get(cat, 0) + 1

    category_lines = "\n".join(
        f"  • {KEYWORD_LABELS.get(cat, cat.upper())}: {count}"
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1])
    )

    top_lead = max(leads, key=lambda l: l.score, default=None)
    top_line = ""
    if top_lead and top_lead.score > 0:
        top_line = (
            f"\n*Top lead today:* {top_lead.posting.company_name} "
            f"({top_lead.owner_first_name} {top_lead.owner_last_name}) — score {top_lead.score}/100"
        )

    text = (
        f"*SDR Pipeline Run Complete*\n\n"
        f"*Scraped:* {run_stats.get('raw', 0)}  →  "
        f"*After dedup/filter:* {run_stats.get('after_dedup', 0)}  →  "
        f"*Pushed to GHL:* {run_stats.get('pushed_ghl', 0)}\n"
        f"*Sheets-only (no contact):* {run_stats.get('sheets_only', 0)}\n\n"
        f"*Enrichment:* Complete {complete} | Partial {partial} | Failed {failed}\n\n"
        f"*By signal type:*\n{category_lines}"
        f"{top_line}"
    )
    _post(webhook, text)


def send_morning_brief(top_leads: list[EnrichedLead], date_str: str) -> None:
    """Post the top leads for the day to Slack at 8 AM so SDR knows exactly who to call first."""
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        return
    if not top_leads:
        _post(webhook, f"*SDR Morning Brief — {date_str}*\nNo new leads from yesterday's run.")
        return

    lines = [f"*SDR Morning Brief — {date_str}*", f"Top {len(top_leads)} leads to work today:\n"]

    for i, lead in enumerate(top_leads, 1):
        p = lead.posting
        ghl_link = (
            f"https://app.gohighlevel.com/contacts/{lead.ghl_contact_id}"
            if lead.ghl_contact_id and lead.ghl_contact_id != "dry-run-id"
            else ""
        )
        name = f"{lead.owner_first_name} {lead.owner_last_name}".strip() or "unknown contact"
        lines.append(
            f"*{i}. [{lead.score}] {p.company_name}*  —  {KEYWORD_LABELS.get(p.keyword_category, p.keyword_category)}\n"
            f"   {name} | {lead.owner_email or 'no email'}\n"
            f"   ~{lead.employee_count or '?'} employees | ~{lead.revenue_estimate or '?'} revenue\n"
            f"   {ghl_link or p.job_url}"
        )

    _post(webhook, "\n".join(lines))
