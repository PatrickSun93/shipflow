#!/usr/bin/env bash
# ShipFlow UserPromptSubmit hook — per-turn in-flight log.
# Survives session pause (Stop hook fires only on graceful exit).
# Writes to docs/shipflow/sessions/log-YYYY-MM-DD.md (daily rotation).
set -euo pipefail

[ -d docs/shipflow ] || exit 0
mkdir -p docs/shipflow/sessions

LOG="docs/shipflow/sessions/log-$(date +%Y-%m-%d).md"
TS=$(date +'%H:%M:%S')
STDIN=$(cat)

# Extract prompt field from JSON (python preferred; fall back to raw truncation).
PROMPT=$(
  echo "$STDIN" | python  -c 'import sys,json; d=json.load(sys.stdin); print(d.get("prompt","")[:300].replace(chr(10)," "))' 2>/dev/null \
  || echo "$STDIN" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("prompt","")[:300].replace(chr(10)," "))' 2>/dev/null \
  || (echo "$STDIN" | head -c 300 | tr '\n' ' ')
)

[ -f "$LOG" ] || echo "# ShipFlow session log — $(date +%Y-%m-%d)" > "$LOG"

{
  echo ""
  echo "## $TS"
  echo ""
  echo "**Prompt:** $PROMPT"
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    DIRTY=$(git status --short 2>/dev/null | head -5)
    if [ -n "$DIRTY" ]; then
      echo ""
      echo "**Dirty:**"
      echo '```'
      echo "$DIRTY"
      echo '```'
    fi
  fi
} >> "$LOG"
