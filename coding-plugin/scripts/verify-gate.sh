#!/bin/bash
# Verification gate check after implementer agent phases
# Called on SubagentStop hook (matcher: implementer)

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
  echo '{"warning": "No test command detected - verification gate cannot auto-check"}'
  exit 0
fi

# Output verification reminder
echo "{\"verification\": \"Test command: $TEST_CMD\", \"reminder\": \"Ensure tests pass before marking tasks complete\"}"

exit 0
