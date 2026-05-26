#!/bin/bash
# Research skill — powered by Perplexity AI
# Usage: bash research.sh "your question here"
# Auto-saves results to research/research-log.md with date

set -e

# Load .env from project root
SCRIPT_DIR="$(dirname "$0")"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"
LOG_FILE="$PROJECT_ROOT/research/research-log.md"

if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

if [ -z "$PERPLEXITY_API_KEY" ]; then
  echo "ERROR: PERPLEXITY_API_KEY not set in .env"
  exit 1
fi

QUERY="$1"
if [ -z "$QUERY" ]; then
  echo "Usage: bash research.sh \"your question here\""
  exit 1
fi

TODAY=$(date +"%Y-%m-%d")

echo "Researching: $QUERY"
echo "---"

RESULT=$(curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"sonar-pro\",
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are a research assistant for a CEO. Return findings in this format:\n\n## Summary\n- 3-5 bullet TL;DR\n\n## Key Findings\n- Detailed breakdown\n\n## Sources\n- Cited URLs\n\n## Action Items\n- What the CEO should do with this info (if applicable)\n\nBe direct, factual, and concise. No fluff.\"
      },
      {
        \"role\": \"user\",
        \"content\": $(echo "$QUERY" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')
      }
    ],
    \"return_citations\": true,
    \"search_recency_filter\": \"month\"
  }" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'choices' in data:
    content = data['choices'][0]['message']['content']
    print(content)
    if 'citations' in data:
        print('\n## Citations')
        for i, url in enumerate(data['citations'], 1):
            print(f'{i}. {url}')
else:
    print('Error:', json.dumps(data, indent=2))
")

# Print to terminal
echo "$RESULT"

# Auto-save to research log
mkdir -p "$PROJECT_ROOT/research"

LOG_ENTRY="
---

### $TODAY — $QUERY

$RESULT
"

# Append after the Queue section
python3 - "$LOG_FILE" "$LOG_ENTRY" <<'EOF'
import sys

log_file = sys.argv[1]
entry = sys.argv[2]

with open(log_file, 'r') as f:
    content = f.read()

# Insert after the Queue section divider
marker = "## Completed Research"
if marker in content:
    content = content.replace(marker, marker + entry, 1)
else:
    content += entry

with open(log_file, 'w') as f:
    f.write(content)

print(f"Saved to research log.")
EOF
