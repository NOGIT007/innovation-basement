---
context: fork
allowed-tools: Bash(gh issue create:*), Bash(git diff:*), Bash(bun test:*), Bash(npm test:*), Bash(make test:*), Bash(pytest:*), Read, Grep, Glob, Edit, Write
description: Simplify code and create issues for bugs
argument-hint: [focus-area or --all]
---

# Simplify Code

Target: $ARGUMENTS (default: recently changed files)

Expert code simplification. Focus: clarity, consistency, maintainability while preserving functionality.

## Step 1: Determine Scope

If `$ARGUMENTS` is empty or `--recent`:
```bash
git diff --name-only HEAD~5
```

If `$ARGUMENTS` is `--all`:
- Scan entire src/ directory

If `$ARGUMENTS` is a path:
- Use that specific file/folder

## Step 2: Analyze Each File

For each file in scope:
1. Read the file
2. Identify simplification opportunities:
   - Unnecessary complexity/nesting
   - Redundant code
   - Inconsistent patterns
   - Overly clever solutions
   - Nested ternaries -> replace with switch/if-else
   - Missing explicit types (TypeScript)

## Step 3: Detect Bugs

Flag potential bugs:
- Unhandled edge cases
- Missing null checks
- Incorrect error handling
- Logic errors
- Race conditions

**If bug found:**
```bash
gh issue create --title "[Bug] <description>" --body "..."
```

Issue body format:
```markdown
## Bug Description
[what's wrong]

## Location
`file.ts:line`

## Suggested Fix
[approach]

---
Created by `/code:simplify`
```

## Step 4: Apply Simplifications

For safe refactors (no behavior change):
1. Apply edit
2. Verify tests still pass

**Rules:**
- NEVER change functionality
- Prefer explicit over compact
- Delete > Add
- 10 readable lines > 5 clever lines

## Step 5: Run Verification

```bash
# Auto-detect test command
bun test || npm test || make test || pytest
```

If tests fail after simplification -> revert and report.

## Step 6: Report Summary

Output:
- Files simplified: [list]
- Changes made: [summary]
- Issues created: [#numbers with links]
- Manual review suggested: [if any]

## Non-Negotiables

1. **Preserve functionality** - never change what code does
2. **Run tests** - verify after every change
3. **Create issues for bugs** - don't attempt risky fixes
4. **Stay scoped** - only touch files in scope unless told otherwise
