#!/usr/bin/env bash
# ShipFlow Stop hook — records a minimal "last session" marker so the next
# SessionStart can surface where we left off. Silent in non-ShipFlow repos.
#
# Idea borrowed from MemPalace's stop hook (github.com/MemPalace/mempalace),
# but implemented as a thin markdown marker rather than a verbatim transcript
# store — ShipFlow's source of truth stays in committed markdown.
set -euo pipefail

[ -d docs/shipflow ] || exit 0
mkdir -p docs/shipflow/sessions

{
  echo "# Last session"
  echo ""
  echo "- Ended: $(date +'%Y-%m-%d %H:%M %Z')"
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "- Branch: $(git branch --show-current 2>/dev/null || echo '(detached)')"
    echo "- Last commit: $(git log -1 --format='%h %s' 2>/dev/null || echo '(none)')"
    DIRTY=$(git status --short 2>/dev/null | head -5)
    if [ -n "$DIRTY" ]; then
      echo "- Dirty files (first 5):"
      echo "$DIRTY" | sed 's/^/  /'
    fi
  fi
} > docs/shipflow/sessions/last.md
