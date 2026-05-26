-- Run this once in your Supabase SQL editor

CREATE TABLE IF NOT EXISTS scraped_leads (
    id              SERIAL PRIMARY KEY,
    company_domain  TEXT NOT NULL,
    keyword_category TEXT NOT NULL,
    first_seen_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ghl_contact_id  TEXT,
    enrichment_status TEXT,
    CONSTRAINT uq_domain_keyword UNIQUE (company_domain, keyword_category)
);

CREATE INDEX IF NOT EXISTS idx_first_seen ON scraped_leads (first_seen_at);

-- ── PIPELINE EVENTS ──────────────────────────────────────────────────────────
-- Tracks funnel stage transitions: scraped → enriched → pushed_ghl → contacted
-- → meeting_booked → closed_won / closed_lost
-- One row per event — append-only. Join to scraped_leads on company_domain + keyword_category.

CREATE TABLE IF NOT EXISTS pipeline_events (
    id               SERIAL PRIMARY KEY,
    company_domain   TEXT        NOT NULL,
    keyword_category TEXT        NOT NULL,
    ghl_contact_id   TEXT,
    event_type       TEXT        NOT NULL,  -- scraped | enriched | pushed_ghl | contacted | meeting | closed_won | closed_lost
    event_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata         JSONB       DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_pe_domain   ON pipeline_events (company_domain, keyword_category);
CREATE INDEX IF NOT EXISTS idx_pe_event_at ON pipeline_events (event_at);
CREATE INDEX IF NOT EXISTS idx_pe_type     ON pipeline_events (event_type);
