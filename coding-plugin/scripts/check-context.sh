#!/bin/bash
# Estimates context usage and outputs warnings
# Called on Stop hook

# This is a heuristic - Claude Code doesn't expose exact context usage
# We use conversation length as a proxy

INPUT=$(cat 2>/dev/null)

# Count approximate messages/turns
# In practice, this would need to be more sophisticated
# For now, just output a reminder

echo '{"reminder": "Check context health with /workflow status if conversation feels long"}'

exit 0
