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
