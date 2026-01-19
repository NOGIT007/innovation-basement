#!/bin/bash
# Logs errors to lessons-learned.md
# Receives JSON input via stdin from PostToolUse hook

INPUT=$(cat)
EXIT_CODE=$(echo "$INPUT" | jq -r '.tool_output.exit_code // 0' 2>/dev/null)

# Only log if there was an error (non-zero exit code)
if [ "$EXIT_CODE" != "0" ] && [ "$EXIT_CODE" != "null" ]; then
  TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"' 2>/dev/null)
  TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input | tostring' 2>/dev/null | head -c 200)
  ERROR_OUTPUT=$(echo "$INPUT" | jq -r '.tool_output.stderr // .tool_output.stdout // "No output"' 2>/dev/null | head -c 500)
  DATE=$(date +"%Y-%m-%d %H:%M")

  LESSONS_FILE="docs/lessons-learned.md"

  # Create file if doesn't exist
  if [ ! -f "$LESSONS_FILE" ]; then
    mkdir -p docs
    cat > "$LESSONS_FILE" << 'HEADER'
# Lessons Learned

Auto-generated error log for institutional knowledge.

---

HEADER
  fi

  # Append error
  cat >> "$LESSONS_FILE" << EOF

## $DATE - $TOOL_NAME Error

**Command/Input:** \`$TOOL_INPUT\`

**Error:**
\`\`\`
$ERROR_OUTPUT
\`\`\`

**Resolution:** _To be filled in_

---
EOF
fi

exit 0
