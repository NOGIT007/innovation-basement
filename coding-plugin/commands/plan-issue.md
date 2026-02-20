---
allowed-tools: Bash(gh issue create:*), Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Read, Write, Grep, Glob, Task, AskUserQuestion, TaskCreate, TaskUpdate, mcp__typescript-lsp__*
description: Research codebase with LSP precision, plan feature with phases, create GitHub issue
argument-hint: [#issue-number | feature-description] [@spec-file]
---

# Feature Planning & GitHub Issue Creation

Feature to plan: $ARGUMENTS

> **Tip:** Include `@file` references to provide specs or context (e.g., `/plan-issue add auth @spec.md`)

## Step 0: Verify Target Repo

Check current project repo (issue will be created here):

```bash
git remote -v
```

## Step 0.3: Detect Existing Issue

Check if `$ARGUMENTS` contains a GitHub issue reference (`#<number>`):

**If `#<number>` found:**

1. Extract issue number (strip `#` prefix)
2. Fetch issue content:
   ```bash
   gh issue view <number> --json title,body,comments --jq '{title, body, comments: [.comments[].body]}'
   ```
3. Store as `EXISTING_ISSUE_NUMBER` and `EXISTING_ISSUE_CONTENT`
4. Use the issue body + comments as primary context (same as a spec file)
5. Remaining text in `$ARGUMENTS` (after removing `#<number>`) becomes additional context
6. **Skip to Phase 1** (research) — the issue content replaces the plan source

**If no `#<number>` found:**

- Continue to Step 0.5 (current behavior)

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

- Proceed to Phase 0.7 (Explore Approaches)
- Then Phase 1 research (explore codebase)
- Generate plan from scratch based on `$ARGUMENTS`

## Phase 0.7: Explore Approaches

> **Skip this phase** when: SPEC.md exists, `@file` was provided, or a plan file was found.

Before deep research, present 2-3 approaches ranked by simplicity:

1. **Identify approaches** — What are 2-3 ways to implement this?
2. **Rank by simplicity** — Simplest first (fewest files, least risk)
3. **Present to user:**

```
## Approaches

1. **[Simplest]** — [1 sentence]. Files: ~N, Risk: low
2. **[Alternative]** — [1 sentence]. Files: ~N, Risk: medium
3. **[Most flexible]** — [1 sentence]. Files: ~N, Risk: higher

Which approach? (default: 1)
```

4. **Wait for user choice** before proceeding to Phase 1

**Why:** There might be a simpler way. This is a gentle nudge, not a gate.

## Step 0.6: Load Code Quality Rules

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

## Phase 2.5: Task Quality Gate

Before confirming, validate every task against these rules:

### Quality Checks

| Check            | Rule                                     | Fix                                         |
| ---------------- | ---------------------------------------- | ------------------------------------------- |
| File count       | Max 3 files per task                     | Split into sub-tasks                        |
| File references  | Every task has `file:line` refs          | Add precise locations                       |
| Verification     | Must be specific command                 | Replace vague "bun test" with targeted test |
| Success criteria | Each task states what success looks like | Add `expected_outcome`                      |

### Anti-Patterns (reject these)

- **Vague task:** "Improve the API" → Split into specific changes
- **Umbrella task:** "Set up auth + database + UI" → One concern per task
- **Missing verification:** "Update styles" with no way to check → Add visual/test check
- **No file refs:** "Change the handler" → Which handler? What file? What line?

### Enriched TaskCreate

Add `expected_outcome` to metadata:

```
TaskCreate(
  subject: "<imperative task title>",
  description: "<detailed steps with file:line refs>",
  activeForm: "<present continuous form>",
  metadata: {
    "verification": "<specific test command>",
    "expected_outcome": "<what success looks like>",
    "files": ["file.ts:15-30"]
  }
)
```

**Loop:** If any task fails quality checks → rewrite it before proceeding.

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

### Step 4.5: Create or Update Issue

**If enriching existing issue (`EXISTING_ISSUE_NUMBER` set):**

```bash
gh issue edit <EXISTING_ISSUE_NUMBER> --body-file .claude-issue-body.md
```

Use the existing issue number for task linking. Do NOT create a new issue.

**If creating new issue (current behavior):**

```bash
gh issue create --title "[Feature] $ARGUMENTS" --body-file .claude-issue-body.md
```

Extract issue number from output.

### Step 4.6: Link Tasks to Issue

Update all tasks with the issue number (use `EXISTING_ISSUE_NUMBER` if set, otherwise the newly created number):

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

Issue created or updated with native tasks.

Output:

**If enriching existing issue (`EXISTING_ISSUE_NUMBER` set):**

```
Issue #<number> updated with task breakdown
Tasks: <count> tasks in native task list (view with ctrl+t)

Run `/code:implement #<number>` to start.
```

**If creating new issue:**

```
Issue #<number> created
Tasks: <count> tasks in native task list (view with ctrl+t)

Run `/code:implement #<number>` to start.
```

The orchestrator creates the feature branch and manages execution automatically.
