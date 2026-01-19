---
context: fork
allowed-tools: Bash(git diff:*), Read, Task
description: Simplify code and create issues for bugs
argument-hint: [focus-area or --all]
---

# Simplify Code

Target: $ARGUMENTS (default: recently changed files)

## Step 1: Determine Scope

If `$ARGUMENTS` is empty or `--recent`:
```bash
git diff --name-only HEAD~5
```

If `$ARGUMENTS` is `--all`:
- Scan entire src/ directory

If `$ARGUMENTS` is a path:
- Use that specific file/folder

## Step 2: Spawn Simplifier Agent

Use Task tool with `subagent_type: coding-plugin:simplifier`:

```
Task(
  subagent_type: "coding-plugin:simplifier",
  prompt: """
  Simplify the following files:
  <file-list>

  Focus: clarity, consistency, maintainability
  Create GitHub issues for any bugs found.
  Run tests after changes.
  """
)
```

## Step 3: Report Results

Display agent's summary:
- Files simplified
- Changes made
- Issues created (with links)
- Suggestions for manual review

## Rules

- **Always fork** - large codebases need clean context
- **Trust the agent** - it handles verification
- **Report everything** - user needs visibility
