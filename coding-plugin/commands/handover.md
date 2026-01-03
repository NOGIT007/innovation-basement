---
allowed-tools: Bash(gh issue list:*), Bash(gh issue view:*), Bash(git status:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*), Read, Write, Glob, Grep
description: Save session state with issue progress to handover.md for resume
---

# Session Handover

Save current work state to `handover.md` for seamless session resume.

## Arguments

`/handover [description]`

- **No args**: Auto-detect from conversation context
- **With description**: Use as Status summary (e.g., `/handover fixing auth bug in login flow`)

## Step 1: Gather Git Context

```bash
git branch --show-current
git log --oneline -5
git status --short
git diff --stat HEAD~1 2>/dev/null
```

## Step 2: Detect and Fetch Issue

**Detection priority (use first match):**
1. Explicit argument: `/handover #123` → extract `123`
2. Branch name: `feature/123-desc` or `fix/456-bug` → extract number
3. Conversation context: Look for issue references discussed

**If issue number found:**
```bash
gh issue view <number> --json number,title,body,state
```

**Parse issue body to extract:**
- Current phase: First phase with unchecked `- [ ]` tasks
- Completed count: Number of `- [x]` checkboxes
- Total count: All checkboxes in phases
- Next task: First unchecked `- [ ]` item

If no issue found or parse fails, continue without issue context.

## Step 3: Capture Session Context

If description argument provided → Use as Status summary.

Otherwise, from current conversation, extract:
- What was being worked on
- Key decisions made
- Files modified with specifics
- Blockers or open questions

## Step 4: Write handover.md

**ALWAYS overwrite** the file at project root (never delete, always keep):

```markdown
# Handover

**Created:** <timestamp>
**Branch:** <branch-name>

## Issue Progress (if issue detected)
- **Issue:** #<number> - <title>
- **State:** open/closed
- **Current Phase:** Phase N - <phase title>
- **Progress:** X/Y tasks complete
- **Next task:** <first unchecked task text>

## Status
<1-2 sentences: what's done>

## Key Files
| File | Lines | Status |
|------|-------|--------|
| `src/file.ts` | 42-58 | Modified - added X |
| `types/index.ts` | 15 | Pending - needs Y |

## Context
<Key decisions, patterns discovered, or important notes>

## Resume Instructions
1. <Immediate next step with file:line>
2. <Following step>
3. <Verification step>

## Open Questions
- [ ] <Any unresolved decisions>
```

## Step 5: Confirm

```bash
cat handover.md
```

State: "Handover saved. Resume with `/resume`"

## Gitignore Check

Ensure `handover.md` is gitignored:
```bash
grep -q "^handover\.md$" .gitignore || echo "handover.md" >> .gitignore
```
