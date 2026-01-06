---
allowed-tools: Bash(gh issue view:*), Bash(gh issue edit:*), Bash(git:*), Read, Grep, Glob, Edit, Write, Task
description: Start implementation from a GitHub issue URL
argument-hint: #<issue-number> or <issue-url>
---

# Implement from GitHub Issue

Issue: $ARGUMENTS

## Step 1: Fetch Issue

```bash
gh issue view <number> --json title,body,state
```

Parse the issue body to extract:
- **Goal**: What we're building
- **Phases**: Implementation phases with checkboxes
- **Current phase**: First unchecked phase

## Step 2: Identify Current Phase

Look for the first phase with unchecked `- [ ]` tasks.

If all phases complete:
1. Congratulate user on completion
2. **Ask:** "All phases complete. Close issue #<number>?"
3. Wait for explicit "yes" before running `gh issue close`
4. **Never auto-close** - user approval required

## Step 3: Execute Current Phase

For the current phase:

1. **Read the tasks** - Understand what needs to be done
2. **Identify files** - Check the `Files:` line for affected files
3. **Implement** - Complete each task in order
4. **Test** - Verify changes work
5. **Commit** - Use descriptive commit message

### Git Discipline

- Branch: `feature/<issue-number>-<short-desc>` (if not already on it)
- Commits: Small, atomic, descriptive
- Format: `✨ <description>` for features, `🐛 <description>` for fixes

## Step 4: Update Issue

After completing phase tasks:

```bash
# Short updates
gh issue edit <number> --body "updated body with [x] checkboxes"

# Long body updates (multi-line)
# 1. Write .claude-issue-body.md with updated body
# 2. gh issue edit <number> --body-file .claude-issue-body.md
```

Mark completed tasks with `[x]`.

## Step 5: Report Progress

Tell user:
- What was completed
- What's next (next phase or done)
- Any blockers encountered

## Rules

- **Follow the plan** - Don't deviate from the issue phases
- **One phase at a time** - Complete current phase before moving on
- **Update checkboxes** - Keep issue in sync with progress
- **Ask if unclear** - Don't guess, ask the user
