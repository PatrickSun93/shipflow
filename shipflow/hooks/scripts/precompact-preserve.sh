#!/usr/bin/env bash
# ShipFlow PreCompact hook — records a timestamp before conversation
# compaction so agents know pre-compact state was preserved.
#
# Idea borrowed from MemPalace (github.com/MemPalace/mempalace), simplified:
# we only flag that compaction happened, not the transcript itself.
set -euo pipefail

[ -d docs/shipflow ] || exit 0
mkdir -p docs/shipflow/sessions
date +"%Y-%m-%d %H:%M %Z" > docs/shipflow/sessions/last-compact.md
