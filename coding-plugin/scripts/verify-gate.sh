#!/bin/bash
# Verification gate check after implementer agent phases
# Called on SubagentStop hook (matcher: implementer)
# Actually runs detected test command and exits non-zero on failure

# Detect test command
detect_test_cmd() {
  if [ -f "package.json" ]; then
    if grep -q '"test"' package.json; then
      if command -v bun &> /dev/null; then
        echo "bun test"
      else
        echo "npm test"
      fi
      return
    fi
  fi

  if [ -f "Makefile" ] && grep -q "^test:" Makefile; then
    echo "make test"
    return
  fi

  if [ -f "pyproject.toml" ]; then
    if command -v uv &> /dev/null; then
      echo "uv run pytest"
    else
      echo "pytest"
    fi
    return
  fi

  if [ -f "Cargo.toml" ]; then
    echo "cargo test"
    return
  fi

  echo ""
}

TEST_CMD=$(detect_test_cmd)

if [ -z "$TEST_CMD" ]; then
  echo '{"warning": "No test command detected - verification gate skipped"}'
  exit 0
fi

echo "{\"verification\": \"Running: $TEST_CMD\"}"

# Run tests with 120s timeout
if command -v timeout &> /dev/null; then
  timeout 120 $TEST_CMD
else
  # macOS fallback: use perl for timeout
  perl -e "alarm 120; exec @ARGV" $TEST_CMD
fi

EXIT_CODE=$?

if [ $EXIT_CODE -eq 124 ]; then
  echo '{"error": "Tests timed out after 120 seconds"}'
  exit 1
elif [ $EXIT_CODE -ne 0 ]; then
  echo "{\"error\": \"Tests failed with exit code $EXIT_CODE\"}"
  exit $EXIT_CODE
fi

echo '{"verification": "Tests passed"}'
exit 0
