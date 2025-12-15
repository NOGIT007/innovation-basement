#!/bin/bash
# Creates GitHub issue for a phase
# Usage: create-phase-issue.sh <phase-type> <description>

PHASE_TYPE="$1"
DESCRIPTION="$2"
LABEL="phase:${PHASE_TYPE}"

gh issue create \
  --title "[$PHASE_TYPE] $DESCRIPTION" \
  --label "$LABEL" \
  --body "## Phase: $PHASE_TYPE

### Description
$DESCRIPTION

### Checklist
- [ ] Phase objectives defined
- [ ] Work completed
- [ ] User approved

### Notes
_Add notes as work progresses_"
