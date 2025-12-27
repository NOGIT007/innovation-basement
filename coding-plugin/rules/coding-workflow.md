---
name: coding-workflow
description: Simple phased workflow - plan-issue, implement, handover
version: "2.6"
---

# Coding Workflow Rules

## Workflow

```
/code:plan-issue → /code:implement → /code:handover
```

## Plan Issue

`/code:plan-issue <feature>` creates a GitHub issue with:

1. **Explore** - Task(Explore) → file:line refs
2. **Trace** - Entry → Transform → Exit (file:line)
3. **Audit** - Conflicts, duplicates, breaks
4. **Checklist** - Data flow, edge cases, security, backward compat
5. **Draft** - Issue with file:line specifics

Issue format:
```
## Summary
## Data Flow (file:line)
## Changes (File:Line | Current | New)
## Verification
```

## Implement

`/code:implement #<number>`:

1. `gh issue view <number>`
2. Verify plan applies (Task Explore)
3. Implement at file:line
4. Verify before commit

Changed since plan? → ❗ flag and ask.

## Handover

`/code:handover` generates:
- Current issue and phase
- Branch and status
- Next steps

## Git Discipline

- Branch: `feature/<issue-number>-<short-desc>`
- Commits: Small, atomic, descriptive
- Never commit broken code

## Critical Thinking

- **Challenge bad plans** - Flag issues before implementing
- **Ask if unclear** - Don't guess requirements
- **Verify before acting** - Research before coding

## Simplicity First

- 10 lines > 20 lines
- Working > Perfect
- Delete > Add
