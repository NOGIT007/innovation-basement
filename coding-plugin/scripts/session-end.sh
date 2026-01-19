#!/bin/bash
# Clean up session - remind about handover
# Called on SessionEnd hook

# Check for uncommitted changes
if git status --porcelain 2>/dev/null | grep -q .; then
  echo '{"warning": "Uncommitted changes detected - consider /handover before ending"}'
fi

exit 0
