# Higgsfield UGC

AI image/video generation using Higgsfield NanoBanana 2, automated via Claude Code + Playwright MCP.

## What This Does
Claude controls a real browser (via Playwright), navigates to Higgsfield, runs batches of prompts using the JS clear method, and saves outputs organized by date. No manual clicking between prompts.

## Setup (one-time)

1. Install Playwright MCP:
   ```
   claude mcp add playwright npx '@playwright/mcp@latest'
   ```
2. Restart Claude and verify with `/mcp` — you should see `playwright` listed.

## Running a Batch

Open Claude Code in this folder and run:

```
Generate a batch of UGC characters using NanoBanana 2.
9:16 aspect ratio, 8 images per prompt, 2K unlimited ON.
Follow the workflow in CLAUDE.md exactly.
```

Then paste your prompts.

## Folder Structure

```
higgsfield-ugc/
├── CLAUDE.md           — workflow rules Claude reads automatically
├── SESSION-RESUME.md   — crash recovery tracker
├── images/             — generated images, organized by date
│   └── YYYY-MM-DD/
├── videos/             — generated videos
├── reference/          — reference images, moodboards
└── output/             — final exports
```

## Recovery
If Claude crashes mid-batch:
> "Read SESSION-RESUME.md and continue from where we left off."

## Status
Active
