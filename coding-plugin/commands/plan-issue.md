---
allowed-tools: Bash(gh issue create:*), Bash(gh issue list:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Read, Grep, Glob, Task, AskUserQuestion, mcp__typescript-lsp__*
description: Research codebase with LSP precision, plan feature with phases, create GitHub issue
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

## Step 0.6: Read Project Lessons

Check for LESSONS.md in project root:
```bash
cat LESSONS.md 2>/dev/null
```

If exists:
- Note patterns to follow
- Note mistakes to avoid
- Include relevant lessons in issue context

## Step 0.7: Check Lessons Age

If LESSONS.md older than 30 days:
```bash
stat -f "%Sm" LESSONS.md 2>/dev/null
```

Suggest: "LESSONS.md is stale. Run `/code:lessons` to refresh."

## Phase 1: Research (LSP-Precise) — Skip if plan exists in session

Research the **current project** codebase with LSP precision:

1. **Find entry points** - Grep for feature patterns
2. **LSP: Go to definition** - Use typescript-lsp to trace exact types/functions
3. **LSP: Find references** - Locate all usages of affected code
4. **Trace data flow** - Document: Entry → Transform → Exit with file:line
5. **Check types** - Use LSP to understand interfaces/types involved
6. **Find patterns** - Look for similar implementations to follow

Document with **file:line precision**:
- Exact locations: `src/api/handler.ts:42`
- Function signatures: `processData(input: InputType): OutputType`
- Type definitions: `interface UserData` at `types/user.ts:15`
- Dependencies and imports
- Risks and edge cases

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

## Context (from LESSONS.md)
- Avoid: [relevant lesson if applicable]
- Pattern: [relevant pattern if applicable]

## Data Flow
Entry: `file.ts:line` → Transform: `file.ts:line` → Exit: `file.ts:line`

## Implementation Phases

### Phase 1: [name]
**Files:**
- `file1.ts:42` - Modify `functionName()` to add X
- `file2.ts:15-20` - Update interface `TypeName`

**Tasks:**
- [ ] [Task with exact file:line reference]
- [ ] [Task with type/function specifics]

**Verification:**
- [ ] Type check passes
- [ ] Existing tests pass

### Phase 2: [name]
**Files:**
- `file3.ts:10` - Add new function

**Tasks:**
- [ ] [Task with specifics]

**Verification:**
- [ ] [How to verify this phase]

---

Created with `/plan-issue` (LSP-precise)
```

Output issue URL for `/code/implement #<number>`.
