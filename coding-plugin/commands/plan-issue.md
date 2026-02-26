---
allowed-tools: Bash(gh issue create:*), Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Read, Write, Grep, Glob, Task, AskUserQuestion, TaskCreate, TaskUpdate, mcp__typescript-lsp__*
description: Research codebase with LSP precision, plan feature with phases, create GitHub issue
argument-hint: [#issue-number | feature-description] [@spec-file]
---

# Feature Planning & GitHub Issue Creation

Feature to plan: $ARGUMENTS

> **Tip:** Include `@file` references to provide specs or context (e.g., `/plan-issue add auth @spec.md`)

## Step 0: Verify Target Repo

```bash
git remote -v
```

## Step 0.3: Detect Existing Issue

Check if `$ARGUMENTS` contains `#<number>`:

**If found:** Extract number, fetch with `gh issue view <number> --json title,body,comments --jq '{title, body, comments: [.comments[].body]}'`. Store as `EXISTING_ISSUE_NUMBER` and `EXISTING_ISSUE_CONTENT`. Use issue body + comments as primary context. Remaining text becomes additional context. **Skip to Phase 1.**

**If not found:** Continue to Step 0.5.

## Step 0.5: Load Existing Plan

Check for plan sources in order:

1. **`@file` in arguments** — Claude Code expands automatically. Use as primary context, skip Phase 1.
2. **`SPEC.md`** in project root — read and use as context, skip Phase 1.
3. **Claude Code plan file** (`~/.claude/plans/*.md`) — read most recent, skip Phase 1.
4. **None found** — proceed to Phase 0.7, then Phase 1.

## Phase 0.7: Explore Approaches

> Skip when SPEC.md, `@file`, or plan file exists.

Present 2-3 approaches ranked by simplicity:

```
## Approaches

1. **[Simplest]** — [1 sentence]. Files: ~N, Risk: low
2. **[Alternative]** — [1 sentence]. Files: ~N, Risk: medium
3. **[Most flexible]** — [1 sentence]. Files: ~N, Risk: higher

Which approach? (default: 1)
```

Wait for user choice before Phase 1.

## Step 0.6: Load Code Quality Rules

Apply rules from `.claude/rules/` during planning. Key rules:

- **Caller impact:** Before modifying functions, grep for callers. Parameter/return type changes break callers.
- **Security:** No SQL injection, command injection, hardcoded secrets, or XSS. Use parameterized queries, subprocess arrays, env vars, textContent.
- **Frontend (if applicable):** React/Next.js + Bun + Shadcn + TypeScript. Use Shadcn components before custom. No npm/yarn, no JavaScript files.

## Phase 1: Research (LSP-Precise) — Skip if plan exists

Research the **current project** codebase with LSP precision:

1. **Find entry points** - Grep for feature patterns
2. **LSP: Go to definition** - Trace exact types/functions
3. **LSP: Find references** - Locate all usages of affected code
4. **Trace data flow** - Document: Entry → Transform → Exit with file:line
5. **Check types** - Understand interfaces/types involved
6. **Find patterns** - Look for similar implementations to follow

Document with **file:line precision**: exact locations, function signatures, type definitions, dependencies, risks.

## Phase 1.5: Content Specification

- **Read** every file you intend to modify (no exceptions)
- **Precise tasks** with file:line references
- **Pattern references** sourced from existing codebase
- **Sizing:** each task fits within 55% context window

All must be true before Phase 2.

## Phase 2: Plan (Using Specified Content)

Break into **tasks** (not phases):

- Each task = independently testable unit
- Order by dependency (use blockedBy)
- List specific files per task
- Include verification command for each task

## Phase 2.5: Task Quality Gate

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

### Step 4.1: Create Native Tasks

For each planned task, use **TaskCreate** with the enriched format from Phase 2.5. Create ALL tasks before setting dependencies.

### Step 4.2: Set Task Dependencies

Use **TaskUpdate** to set blockedBy relationships. Tasks appear in `ctrl+t` immediately.

### Step 4.3: Write Issue Body File

Use **Write tool** to create `.claude-issue-body.md` (see format below). Pull task subjects from the tasks just created. **Do NOT use heredocs or `cat <<EOF`.**

### Step 4.4: Create or Update Issue

**If enriching existing issue (`EXISTING_ISSUE_NUMBER` set):**

```bash
gh issue edit <EXISTING_ISSUE_NUMBER> --body-file .claude-issue-body.md
```

**If creating new issue:**

```bash
gh issue create --title "[Feature] $ARGUMENTS" --body-file .claude-issue-body.md
```

### Step 4.5: Link Tasks to Issue

Update all tasks with the issue number:

```
TaskUpdate(taskId: "<id>", metadata: { "issueNumber": <issue-number> })
```

## Issue Format

```markdown
## Goal

[1-2 sentences]

## Tasks

| #   | Task           | Status |
| --- | -------------- | ------ |
| 1   | <task subject> | ⏳     |

## Task Details

### Task 1: <subject>

**Files:**
| File | Lines | Change |
|------|-------|--------|
| `file1.ts` | 42-50 | Modify `functionName()` |

**Verification:** `bun run typecheck`

## Research Summary

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

## Next Steps

Output (adapt based on new vs existing issue):

```
Issue #<number> created/updated with task breakdown
Tasks: <count> tasks in native task list (view with ctrl+t)

Run `/code:implement #<number>` to start.
```

Each task targets ~55% context usage. If too large, split into sub-tasks.
