---
allowed-tools: Bash(gh issue list:*), Bash(gh issue view:*), Bash(git status:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*), Read, Write, Glob, Grep
description: Save session state to .handover.md for resume
---

# Session Handover

Save current work state to `.handover.md` for seamless session resume.

## Step 1: Gather Context

```bash
git branch --show-current
git log --oneline -5
git status --short
git diff --stat HEAD~1 2>/dev/null
gh issue list --limit 5 --state open
```

## Step 2: Capture Session Context

From current conversation, extract:
- What was being worked on
- Key decisions made
- Files modified with specifics
- Blockers or open questions

## Step 3: Write .handover.md

**ALWAYS overwrite** the file at project root:

```markdown
# Handover

**Created:** <timestamp>
**Issue:** #<number> - <title> (if applicable)
**Branch:** <branch-name>

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

## Step 4: Confirm

```bash
cat .handover.md
```

State: "Handover saved. Resume with `/resume`"

## Gitignore Check

Ensure `.handover.md` is gitignored:
```bash
grep -q "^\.handover\.md$" .gitignore || echo ".handover.md" >> .gitignore
```
