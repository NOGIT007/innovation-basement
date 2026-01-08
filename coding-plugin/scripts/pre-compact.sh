#!/bin/bash
# Pre-compact hook - save state before context compaction
# Called on PreCompact hook

# Auto-save handover state
DATE=$(date +"%Y-%m-%d %H:%M")
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

echo "{\"pre_compact\": \"Context compacting\", \"branch\": \"$BRANCH\", \"timestamp\": \"$DATE\"}"
echo '{"suggestion": "Consider running /handover to preserve session state"}'

exit 0
