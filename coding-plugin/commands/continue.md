---
allowed-tools: Bash(gh issue view:*), Bash(git status:*), Bash(git branch:*), Bash(git log:*), Read, Glob, Grep, Task, Edit, Write
description: Continue work from handover.md
---

# Continue Session

Load `handover.md` and continue work from where it left off.

## Step 1: Load Handover

```bash
cat handover.md 2>/dev/null || echo "No handover file found"
```

If no file exists → Ask user what to work on.

## Step 2: Verify State

Confirm git state matches handover:

```bash
git branch --show-current
git status --short
```

If mismatch → Warn user, ask how to proceed.

## Step 3: Load Issue Context (if referenced)

If handover references an issue:

```bash
gh issue view <number>
```

## Step 4: Read Key Files

For each file in "Key Files" table:

- Read the file at specified lines
- Verify status matches (modified/pending)

## Step 4.5: Check Agent Mode

Parse the `**Agent:** <mode>` field from the handover header (first few lines).

| Agent Value         | Behavior                          |
| ------------------- | --------------------------------- |
| `implementer`       | Apply implementer rules in Step 5 |
| `normal` or missing | Run as normal session             |

This ensures backwards compatibility with older handover files that lack the Agent field.

## Step 5: Execute Continue Instructions

Work through "Continue Instructions" sequentially:

1. Start with immediate next step
2. Mark progress as you go
3. Stop at verification steps to confirm

**If Agent mode is `implementer`**, apply these additional rules:

- **Verification Gate:** BLOCKED from marking tasks `[x]` until tests pass (exit code 0)
- **Context Monitoring:** Watch `context_window.used_percentage`, trigger handover at 55%
- **Test Loop:** If tests fail, read error log, fix code, retry until pass
- **Evidence Logging:** Quote passing test output before marking complete

**If Agent mode is `normal` or missing**, proceed without special rules.

## Step 6: Update Handover

When work complete:

- Update `handover.md` with new state (always overwrite, never delete)
- Mark completed tasks, add new context for next session

State progress: "Continuing from handover. Starting: <first instruction>"
