---
name: coding-workflow
description: Phased workflow with spec interviews and project principles
version: "3.5.0"
---

# Coding Workflow Rules

## Workflow

```
/code:interview → /code:constitution → /code:plan-issue → /code:implement → /code:handover → /code:resume
       ↓                ↓                    ↓
   spec-spec.md    constitution.md     (reads both)
```

## Development Modes

**Web/Desktop (Quick Mode)**
- Bug triage and exploration
- Single-file fixes
- TODO resolution
- No phase tracking required

**CLI (Full Mode)**
- Phased workflow (`/plan-issue` → `/implement`)
- Testing and merging
- Session continuity with `/handover`

Use GitHub issues as the handover point between modes.

**New commands:**
- `/code:interview <spec>` - Interview to develop spec → `<spec>-spec.md`
- `/code:constitution` - Interview to define principles → `constitution.md`

Both are optional. `/plan-issue` auto-reads `constitution.md` if it exists.

## Interview (New)

`/code:interview <spec-file>` develops vague ideas into specs:

1. **Read** - Load input spec file
2. **Analyze** - What's covered vs. gaps
3. **Interview** - Multi-choice questions (6 categories)
4. **Write** - Output `<spec>-spec.md` in same folder

Categories: Vision, UX, Technical, Risks, Dependencies, Verification

## Constitution (New)

`/code:constitution` creates project principles:

1. **Check** - Warn if constitution.md exists
2. **Interview** - Multi-choice questions (4 categories)
3. **Write** - Output `constitution.md` at project root

Categories: Core Values, Boundaries, Priorities, Non-Negotiables

Output is auto-read by `/plan-issue`.

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

`/code:handover` saves session state to `.handover.md`:
- Current issue and phase
- Key files table (file:line + status)
- Context and decisions
- Resume instructions

File is gitignored and overwritten each time.

## Resume

`/code:resume` continues from `.handover.md`:
1. Loads handover file
2. Verifies git state matches
3. Reads key files
4. Executes resume instructions
5. Clears file when done

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
