---
allowed-tools: Bash(gh issue list:*), Bash(gh issue view:*), Bash(git status:*), Bash(git branch:*), Bash(git log:*)
description: Generate handover text for new session
---

# Session Handover

Generate a succinct handover for the next session.

## Gather Context

1. Current branch: `git branch --show-current`
2. Recent commits: `git log --oneline -3`
3. Open issues: `gh issue list --limit 5`
4. Git status: `git status --short`

## Output Format

```
## Handover

**Issue:** #<number> - <title>
**Phase:** <current phase from issue>
**Branch:** <branch-name>
**Status:** <what's done / what's next>

### Next Steps
- [ ] <immediate next action>
```

Keep it under 10 lines. No fluff.
