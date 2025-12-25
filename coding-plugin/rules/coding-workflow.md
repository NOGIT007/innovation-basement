---
name: coding-workflow
description: Simple phased workflow - plan-issue, implement, handover
---

# Coding Workflow Rules

## Workflow

```
/code:plan-issue → /code:implement → /code:handover
```

### 1. Plan Issue

`/code:plan-issue <feature>` creates a GitHub issue with:
- Research findings
- Implementation phases
- Task checkboxes per phase
- Affected files

### 2. Implement

`/code:implement #<number>` works through the issue:
- Reads phases from issue body
- Identifies current phase (first unchecked tasks)
- Implements tasks in order
- Updates checkboxes when complete
- Commits changes

### 3. Handover

`/code:handover` generates session handover:
- Current issue and phase
- Branch and status
- Next steps

## Git Discipline

- Branch: `feature/<issue-number>-<short-desc>`
- Commits: Small, atomic, descriptive
- Never commit broken code
- Commit within phases, not across

## GitHub Issue as Source of Truth

The GitHub issue tracks all progress:
- Phases with checkboxes
- Completed vs pending tasks
- Session-independent state

Between sessions, `/code:implement #<number>` reads the issue to resume.

## Critical Thinking

- **Challenge bad plans** - Flag issues before implementing
- **Ask if unclear** - Don't guess requirements
- **Lead Engineer mindset** - Consider edge cases, security, performance
- **Verify before acting** - Research before coding

## Simplicity First

Follow vibe-coding principles:
- 10 lines > 20 lines
- Working > Perfect
- Delete > Add
- One file first
