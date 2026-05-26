---
name: research
description: This skill is used to do deeper research with perplexity, with the context of Passion's business and goals
---
# Research Skill

Use Perplexity AI to do deep research on any topic. Returns sourced, structured findings.

## Trigger

Use this skill when Passion asks to:
- "Research X"
- "Look up X"
- "Find out about X"
- "What do competitors do for X"
- "Get me info on X"

## How It Works

1. Read the API key from `.env` (PERPLEXITY_API_KEY)
2. Send the research query to Perplexity using the `sonar-deep-research` model
3. Return structured findings with sources

## Usage

```
/research <topic or question>
```

## Script

The research script lives at `.claude/skills/research/research.sh`.

Run it directly:
```bash
bash .claude/skills/research/research.sh "your question here"
```

## Output Format

- **Summary** — 3-5 bullet TL;DR
- **Key Findings** — detailed breakdown
- **Sources** — cited URLs
- **Action Items** — what Passion should do with this info (if applicable)

## Model

Uses `llama-3.1-sonar-large-128k-online` (Perplexity's online model with live web search).
For deeper research, uses `sonar-deep-research`.
