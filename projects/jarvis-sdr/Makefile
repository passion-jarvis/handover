.PHONY: install setup-ghl dry-run run test-google test-linkedin test-indeed test-enrich test-ghl test-slack import retry metrics call-sheet morning-brief apollo-export purge help

help:
	@echo ""
	@echo "  Jarvis SDR Pipeline — Commands"
	@echo ""
	@echo "  Setup:"
	@echo "    make install      Install Python dependencies"
	@echo "    make setup-ghl    Create GHL custom fields + list pipelines (run once)"
	@echo ""
	@echo "  Run pipeline:"
	@echo "    make dry-run      Full pipeline, no GHL writes (safe to test)"
	@echo "    make run          Full production run"
	@echo "    make run-google   Google Jobs only"
	@echo "    make run-linkedin LinkedIn only"
	@echo "    make run-indeed   Indeed only"
	@echo "    make run-ea       Executive assistant keyword only"
	@echo ""
	@echo "  Test individual components:"
	@echo "    make test-google  Scrape 5 Google Jobs and print results"
	@echo "    make test-enrich  Enrich a domain via Apollo (set DOMAIN=acme.com)"
	@echo "    make test-ghl     Push a test contact to GHL (dry run)"
	@echo "    make test-slack   Send a test Slack alert"
	@echo "    make test-dedup   Check dedup for a domain (set DOMAIN=acme.com)"
	@echo ""
	@echo "  Week 1 manual import:"
	@echo "    make import CSV=leads.csv"
	@echo "    make import CSV=leads.csv DRY=true"
	@echo ""
	@echo "  Operations:"
	@echo "    make retry              Re-push failed GHL leads from Sheets"
	@echo "    make retry DRY=true     Retry dry run"
	@echo "    make metrics            Weekly pipeline health report"
	@echo "    make metrics DAYS=14    Last 14 days"
	@echo "    make call-sheet         Export today's SDR call sheet CSV"
	@echo "    make call-sheet DAYS=3  Last 3 days"
	@echo "    make call-sheet SCORE=60  Score >= 60 only"
	@echo "    make morning-brief      Post top 5 leads to Slack now"
	@echo "    make morning-brief TOP=10 DAYS=2  Top 10 from last 2 days"
	@echo "    make apollo-export      Export domains CSV for Apollo bulk upload"
	@echo "    make apollo-export KEYWORD=ea  EA leads only"
	@echo "    make purge              Purge Supabase records > 90 days"
	@echo "    make purge DRY=true     Preview purge count without deleting"
	@echo ""

install:
	pip install -r requirements.txt

setup-ghl:
	python -m integrations.ghl_setup

dry-run:
	DRY_RUN=true python pipeline.py

run:
	python pipeline.py

run-google:
	python pipeline.py --source google

run-linkedin:
	python pipeline.py --source linkedin

run-indeed:
	python pipeline.py --source indeed

run-ea:
	python pipeline.py --keyword ea

run-social:
	python pipeline.py --keyword social

run-bdr:
	python pipeline.py --keyword bdr

test-google:
	python scripts/test_component.py scrape --source google --limit 5

test-linkedin:
	python scripts/test_component.py scrape --source linkedin --limit 5

test-indeed:
	python scripts/test_component.py scrape --source indeed --limit 5

test-enrich:
	python scripts/test_component.py enrich --domain $(DOMAIN)

test-ghl:
	python scripts/test_component.py ghl-push --dry-run

test-slack:
	python scripts/test_component.py slack-test

test-dedup:
	python scripts/test_component.py dedup --domain $(DOMAIN)

import:
	python scripts/manual_import.py --csv $(CSV) $(if $(DRY),--dry-run,) $(if $(KEYWORD),--keyword $(KEYWORD),) $(if $(LIMIT),--limit $(LIMIT),)

retry:
	python scripts/retry_failed.py $(if $(DRY),--dry-run,) $(if $(LIMIT),--limit $(LIMIT),)

metrics:
	python scripts/metrics_report.py $(if $(DAYS),--days $(DAYS),) $(if $(SLACK),--slack,)

call-sheet:
	python scripts/sdr_call_sheet.py $(if $(DAYS),--days $(DAYS),) $(if $(KEYWORD),--keyword $(KEYWORD),) $(if $(SCORE),--min-score $(SCORE),) $(if $(OUT),--output $(OUT),)

morning-brief:
	python scripts/morning_brief.py $(if $(TOP),--top $(TOP),) $(if $(DAYS),--days $(DAYS),) $(if $(SCORE),--min-score $(SCORE),)

apollo-export:
	python scripts/apollo_bulk_export.py $(if $(DAYS),--days $(DAYS),) $(if $(KEYWORD),--keyword $(KEYWORD),) $(if $(OUT),--output $(OUT),)

purge:
	python scripts/purge_old.py $(if $(DAYS),--days $(DAYS),) $(if $(DRY),--dry-run,)
