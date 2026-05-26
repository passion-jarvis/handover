# Setup Checklist — Jarvis SDR Job Signal Pipeline

## Day 1: Accounts (2 hours)

- [ ] **SerpAPI** — serpapi.com → sign up, copy API key
- [ ] **Proxycurl** — proxycurl.com → sign up, copy API key
- [ ] **Apify** — apify.com → sign up, copy API key, add $20 credit
- [ ] **Apollo.io** — apollo.io → sign up ($99/month Basic), copy API key
- [ ] **Hunter.io** — hunter.io → sign up ($49/month Starter), copy API key
- [ ] **Supabase** — supabase.com → create project, run `db/schema.sql` in SQL editor, copy URL + service key
- [ ] **Slack** — create an incoming webhook at api.slack.com/apps → Incoming Webhooks, copy URL

## Day 2: GHL Setup (1 hour)

1. Create custom fields in GHL (Settings → Custom Fields → Contacts):
   - `Job Title` → copy the field key to `GHL_CF_JOB_TITLE`
   - `Job URL` → copy to `GHL_CF_JOB_URL`
   - `Job Post Date` → copy to `GHL_CF_JOB_POST_DATE`
   - `Keyword Category` → copy to `GHL_CF_KEYWORD_CATEGORY`
   - `Employee Count` → copy to `GHL_CF_EMPLOYEE_COUNT`
   - `Revenue Estimate` → copy to `GHL_CF_REVENUE_ESTIMATE`
   - `Enrichment Status` → copy to `GHL_CF_ENRICHMENT_STATUS`

2. Create pipeline stage "Job Signal — New" in your existing pipeline
   - Note the Pipeline ID and Stage ID from the URL or GHL API

3. Create these tags in GHL: `job-signal`, `hiring-ea`, `hiring-social`, `hiring-bdr`, `hiring-sales`, `hiring-video`, `enrichment:complete`, `enrichment:partial`, `enrichment:failed`

4. Get your GHL API key: Settings → API Keys → Create

## Day 3: Google Sheets (30 min)

1. Create a new Google Sheet, note the Spreadsheet ID from the URL
2. Go to GCP Console → Create project → Enable Google Sheets API
3. Create a Service Account → download JSON → save as `service_account.json` in project root
4. Share the Google Sheet with the service account email (Editor access)

## Day 4: Deploy (1 hour)

### Local test first

```bash
cd projects/jarvis-sdr
cp .env.example .env
# Fill in all values in .env
pip install -r requirements.txt
DRY_RUN=true python pipeline.py
```

Check the output — you should see scraping and enrichment logs, and a Slack message.

### GitHub Actions deployment

1. Push this folder to a GitHub repo
2. Go to repo Settings → Secrets → Actions
3. Add every key from `.env.example` as a secret (paste the full service account JSON for `GOOGLE_SERVICE_ACCOUNT_JSON`)
4. Go to Actions tab → Daily SDR Pipeline → Run workflow (manual trigger to test)
5. Once confirmed working, it auto-runs Mon–Fri at 6 AM PT

## GHL Workflow (after pipeline is running)

Create this workflow in GHL triggered on `tag added = job-signal`:
1. Wait 2 hours
2. Check: if opportunity stage has moved → end
3. If not moved → send Email Template #1 (see `references/email-templates.md`)
4. Wait 3 days
5. If no reply → send Email Template #2
6. Wait 2 days
7. If no reply → create Task: "Call [contact name] — job signal follow-up"

## ICP Filter Tuning

In `pipeline.py`, adjust these constants based on your first week of data:
- `ICP_MAX_EMPLOYEES = 200` — lower to 100 if too many large companies coming through
- `ICP_MIN_EMPLOYEES = 5` — raise to 10 if solo freelancers are coming through

## Monitoring

- GitHub Actions: check the Actions tab daily for run logs
- Slack: `#sdr-alerts` (or whatever channel you pointed the webhook to)
- Google Sheets: full audit trail of every lead, enrichment status, and GHL ID
