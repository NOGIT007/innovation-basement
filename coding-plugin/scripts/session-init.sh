#!/bin/bash
# Initialize session - load context files
# Called on SessionStart hook

# Check for constitution
if [ -f "constitution.md" ]; then
  echo '{"context": "constitution.md found - project principles available"}'
fi

# Check for LESSONS.md
if [ -f "LESSONS.md" ]; then
  MODIFIED=$(stat -f "%Sm" -t "%Y-%m-%d" LESSONS.md 2>/dev/null || stat -c "%y" LESSONS.md 2>/dev/null | cut -d' ' -f1)
  echo "{\"context\": \"LESSONS.md found - last updated: $MODIFIED\"}"
fi

# Check for handover.md
if [ -f "handover.md" ]; then
  echo '{"context": "handover.md found - previous session state available, suggest /resume"}'
fi

exit 0
