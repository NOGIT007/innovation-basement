---
allowed-tools: Bash(gh issue create:*), Bash(gh issue list:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Read, Write, Grep, Glob, Task, AskUserQuestion, TaskCreate, TaskUpdate, mcp__typescript-lsp__*
description: Research codebase with LSP precision, plan feature with phases, create GitHub issue
argument-hint: [feature-description] [@spec-file]
---

# Feature Planning & GitHub Issue Creation

Feature to plan: $ARGUMENTS

> **Tip:** Include `@file` references to provide specs or context (e.g., `/plan-issue add auth @spec.md`)

## Step 0: Verify Target Repo

Check current project repo (issue will be created here):

```bash
git remote -v
```

## Step 0.5: Load Existing Plan

Check for plan sources in order:

**1. File reference in arguments:**
If `$ARGUMENTS` contains `@SPEC.md` or similar file reference:

- Claude Code expands `@file` automatically
- Use the expanded content as primary context
- Skip Phase 1 research

**2. Project SPEC.md:**

```bash
cat SPEC.md 2>/dev/null
```

If found:

- Read the file
- Use as primary context for issue
- Skip Phase 1 research

**3. Claude Code plan file:**

```bash
ls ~/.claude/plans/*.md 2>/dev/null
```

If found:

- Read the most recent file
- Use as primary context for issue
- Skip Phase 1 research

**If NONE found:**

- Proceed to Phase 1 research (explore codebase)
- Generate plan from scratch based on `$ARGUMENTS`

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

## Step 0.8: Load Code Quality Rules

Apply these rules during planning:

### Caller Impact Rules

Before modifying any function, check:
| Change Type | Impact |
|-------------|--------|
| Parameter added/removed | All callers must update |
| Return type changed | Callers may handle incorrectly |
| Function renamed | All imports/calls break |

**Required:** grep for callers before breaking changes.

### Security Rules

| Risk              | Bad                           | Good                           |
| ----------------- | ----------------------------- | ------------------------------ |
| SQL injection     | `f"SELECT * WHERE id = {id}"` | Parameterized queries          |
| Command injection | `os.system(f"rm {file}")`     | `subprocess.run(["rm", file])` |
| Hardcoded secrets | `API_KEY = "sk-..."`          | `os.environ["API_KEY"]`        |
| XSS               | `innerHTML = userInput`       | `textContent = userInput`      |

### Frontend Rules (if applicable)

- **Stack:** React/Next.js + Bun + Shadcn + TypeScript
- Use Shadcn components before custom
- No npm/yarn, no JavaScript files

## Phase 1: Research (LSP-Precise) — Skip if plan exists

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

## Phase 1.5: Content Specification

**Rules:**

1. **Read First:** MUST read every file you intend to modify (no exceptions)
2. **Precise Tasks:** Tasks describe WHAT to change with file:line references
3. **Pattern References:** Reference existing code patterns by location
4. **Sizing:** Each task fits within 55% context window

**Validation (all must be true before Phase 2):**

- [ ] Every modified file read with `Read` tool
- [ ] Tasks have file:line precision
- [ ] Patterns sourced from existing codebase

## Phase 2: Plan (Using Specified Content)

Break into **tasks** (not phases):

- Each task = independently testable unit
- Order by dependency (use blockedBy)
- List specific files per task
- Include verification command for each task

## Phase 3: Confirm

Show plan to user. Ask: **"Create issue in [repo-name]?"**

Wait for confirmation.

## Phase 4: Create Native Tasks & GitHub Issue

### Step 4.1: Create Native Tasks First

For each planned task, use **TaskCreate**:

```
TaskCreate(
  subject: "<imperative task title>",
  description: "<detailed steps with file:line refs>",
  activeForm: "<present continuous form>",
  metadata: {
    "verification": "<test command>",
    "files": ["file.ts:15-30"]
  }
)
```

**Important:** Create ALL tasks before setting dependencies.

### Step 4.2: Set Task Dependencies

After all tasks are created, use **TaskUpdate** to set blockedBy relationships:

```
TaskUpdate(
  taskId: "<id>",
  addBlockedBy: ["<blocker-id-1>", "<blocker-id-2>"]
)
```

Tasks will appear in `ctrl+t` task view immediately.

### Step 4.3: Write Issue Body File

Use **Write tool** to create `.claude-issue-body.md` (see format below).

Pull task subjects from the tasks just created to build the summary table.

**Do NOT use heredocs or `cat <<EOF`** — they fail silently.

### Step 4.4: Validate Body (REQUIRED)

```bash
if [ ! -s .claude-issue-body.md ]; then
  echo "ERROR: .claude-issue-body.md is empty or missing."
  exit 1
fi
echo "Body validated ($(wc -l < .claude-issue-body.md) lines)"
```

### Step 4.5: Create Issue with Body File

```bash
gh issue create --title "[Feature] $ARGUMENTS" --body-file .claude-issue-body.md
```

Extract issue number from output.

### Step 4.6: Link Tasks to Issue

Update all tasks with the issue number:

```
TaskUpdate(
  taskId: "<id>",
  metadata: { "issueNumber": <issue-number> }
)
```

## Issue Format (Task Headlines)

```markdown
## Goal

[1-2 sentences]

## Tasks

| #   | Task           | Status |
| --- | -------------- | ------ |
| 1   | <task subject> | ⏳     |
| 2   | <task subject> | ⏳     |
| 3   | <task subject> | ⏳     |

## Task Details

### Task 1: <subject>

**Files:**
| File | Lines | Change |
|------|-------|--------|
| `file1.ts` | 42-50 | Modify `functionName()` |

**Verification:** `bun run typecheck`

### Task 2: <subject>

...

## Research Summary

### Files Analyzed

| File          | Lines | Purpose               |
| ------------- | ----- | --------------------- |
| `src/file.ts` | 42-58 | [what this file does] |

### Key Code References

- `functionName()` at `src/handler.ts:42` - [what needs to change]

## Risks & Edge Cases

- [ ] Risk: [description] - Mitigation: [approach]

---

**Branch:** `feature/<issue>-<slug>`
**Tasks:** View with `ctrl+t`

_Created with `/plan-issue`_
```

## Task Sizing Guidance

When creating tasks, aim for ~55% context usage per task:

- Each task should be completable within 55% of context window
- Auto-compact handles context limits automatically
- If a task is too large, split into sub-tasks

## Next Steps

Issue created with native tasks.

Output:

```
Issue #<number> created
Tasks: <count> tasks in native task list (view with ctrl+t)

Run `/code:implement #<number>` to start.
```

The orchestrator creates the feature branch and manages execution automatically.
