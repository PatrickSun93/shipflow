#!/usr/bin/env bash
# ShipFlow SessionStart hook — emits brief project context.
# Silent in non-ShipFlow repos (i.e. no docs/shipflow/ directory).
set -euo pipefail

[ -d docs/shipflow ] || exit 0

echo "## ShipFlow context"
echo ""
[ -f docs/shipflow/index.md ] && echo "- Index: \`docs/shipflow/index.md\`"
[ -f docs/shipflow/stack.md ] && echo "- Stack: \`docs/shipflow/stack.md\`"

if [ -f shipflow.config.json ]; then
  echo ""
  echo "Gate modes:"
  grep -E '"gate_[1-4]"' shipflow.config.json \
    | sed -E 's/[[:space:]]*"(gate_[1-4])":[[:space:]]*"([^"]+)".*/- \1: \2/'
fi

if [ -f docs/shipflow/sessions/last.md ]; then
  echo ""
  cat docs/shipflow/sessions/last.md
fi

# Surface today's per-turn log tail (survives session pause).
TODAY_LOG="docs/shipflow/sessions/log-$(date +%Y-%m-%d).md"
if [ -f "$TODAY_LOG" ]; then
  echo ""
  echo "### Recent turns (today's log tail)"
  tail -n 30 "$TODAY_LOG"
fi

# Surface most recent /sf-checkpoint if present.
LATEST_CK=$(ls -1t docs/shipflow/sessions/checkpoint-*.md 2>/dev/null | head -1 || true)
if [ -n "$LATEST_CK" ]; then
  echo ""
  echo "### Most recent checkpoint: $LATEST_CK"
  cat "$LATEST_CK"
fi
