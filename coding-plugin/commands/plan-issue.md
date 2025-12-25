---
allowed-tools: Bash(gh issue create:*), Bash(gh issue list:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Read, Grep, Glob, Task, AskUserQuestion
description: Research codebase, plan feature with phases, create GitHub issue
argument-hint: [feature-description]
---

# Feature Planning & GitHub Issue Creation

Feature to plan: $ARGUMENTS

## Step 0: Verify Target Repo

Check current project repo (issue will be created here):
```bash
git remote -v
```

## Step 0.5: Check for Existing Plan in Session

If a plan already exists in the **current conversation context** (e.g., from plan mode):
1. **Use the existing plan** - Skip Phase 1 (Research) and Phase 2 (Plan)
2. **Go directly to Phase 3** - Show plan summary and confirm issue creation
3. State: "Using existing plan from this session."

Detection: Look for plan content already discussed/drafted in the conversation.

If no existing plan in session → proceed with full research workflow.

## Phase 1: Research (LSP-style) — Skip if plan exists in session

Research the **current project** codebase:

1. **Find related code** - Grep for patterns and implementations
2. **Understand architecture** - Read key files
3. **Identify affected files** - Glob for files to change
4. **Trace dependencies** - Follow imports
5. **Find patterns** - Look for similar implementations

Document:
- Affected files
- Patterns to follow
- Dependencies
- Risks

## Phase 2: Plan

Break into phases:
- Each phase = independently testable
- Order by dependency
- List specific files per phase

## Phase 3: Confirm

Show plan to user. Ask: **"Create issue in [repo-name]?"**

Wait for confirmation.

## Phase 4: Create Issue

Create in **current project repo**:

```bash
gh issue create --title "[Feature] $ARGUMENTS" --body "..."
```

Issue format:
```markdown
## Goal
[1-2 sentences]

## Implementation Phases

### Phase 1: [name]
- [ ] Task 1
- [ ] Task 2
- [ ] Files: `file1.ts`, `file2.ts`

### Phase 2: [name]
- [ ] Task 1
- [ ] Files: `file3.ts`

---

Created with `/plan-issue`
```

Output issue URL for `/code/implement #<number>`.
