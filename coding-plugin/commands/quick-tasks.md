---
context: fork
allowed-tools: Bash(git log:*), Bash(git branch:*), Read, Write, Grep, Glob, Task, TaskCreate, TaskUpdate, mcp__typescript-lsp__*
description: LSP-precise research → native tasks (no GitHub issue)
argument-hint: [feature-description] [@spec-file]
---

# Quick Tasks: LSP Research → Native Task Manager

Feature: $ARGUMENTS

> **Fast path:** LSP-precise planning without GitHub issue overhead.
> Tasks go directly to Claude's native task manager (`ctrl+t`).

---

## Step 1: Load Context Sources

Check for existing context in order:

**1. File reference in arguments:**
If `$ARGUMENTS` contains `@file.md`:

- Use expanded content as primary context
- Still run LSP research to verify references

**2. Recent plan file:**

```bash
ls -t plans/*.md 2>/dev/null | head -1
```

If found, read and use as starting context.

**3. LESSONS.md:**

```bash
cat LESSONS.md 2>/dev/null
```

Note patterns to follow and mistakes to avoid.

---

## Step 2: LSP-Precise Research

Research the codebase with LSP tools for **exact references**:

### 2.1 Find Entry Points

```bash
# Grep for feature-related patterns
```

### 2.2 LSP Operations (REQUIRED)

Use `mcp__typescript-lsp__*` tools for precision:

| Operation            | Tool                                  | Purpose                          |
| -------------------- | ------------------------------------- | -------------------------------- |
| **Go to definition** | `mcp__typescript-lsp__getDefinition`  | Find where functions are defined |
| **Find references**  | `mcp__typescript-lsp__getReferences`  | Find all usages of a symbol      |
| **Get hover info**   | `mcp__typescript-lsp__getHover`       | Get type signatures              |
| **Get diagnostics**  | `mcp__typescript-lsp__getDiagnostics` | Check for existing errors        |

### 2.3 Document with Precision

For each affected area, capture:

```
File: src/components/Auth.tsx
Lines: 42-58
Function: handleLogin(credentials: LoginCredentials): Promise<User>
References: 3 callers (Dashboard.tsx:15, Header.tsx:88, LoginForm.tsx:102)
Types: LoginCredentials (types/auth.ts:12), User (types/user.ts:5)
```

### 2.4 Cross-Reference Matrix

Build a reference map for the task:

| Symbol        | Defined At        | Used At                         |
| ------------- | ----------------- | ------------------------------- |
| `handleLogin` | `Auth.tsx:42`     | `Dashboard:15`, `Header:88`     |
| `User`        | `types/user.ts:5` | `Auth.tsx:42`, `Profile.tsx:20` |

---

## Step 3: Plan Tasks

Break feature into **independently testable tasks**:

### Task Structure

Each task MUST include:

1. **Subject** - Imperative action (e.g., "Add login handler")
2. **Description** - Detailed steps with file:line refs
3. **Files** - Exact files and line ranges
4. **Cross-refs** - Related symbols and their locations
5. **Verification** - Command to verify task completion

### Task Sizing

- Target: ~55% context window per task
- If larger, split into sub-tasks
- Each task should be completable independently

### Dependency Order

Order tasks by dependency:

- Foundation tasks first (types, interfaces)
- Implementation tasks next
- Integration/test tasks last
- Use `blockedBy` for dependencies

---

## Step 4: Confirm Plan

Show the user:

```
Planning: [feature name]

Tasks to create:
1. [Task subject] - [files affected]
2. [Task subject] - [files affected]
...

Create [N] native tasks? (view with ctrl+t)
```

Wait for confirmation.

---

## Step 5: Create Native Tasks

### 5.1 Create All Tasks First

For each task, use **TaskCreate**:

```
TaskCreate(
  subject: "<imperative task title>",
  description: """
  ## Goal
  [What this task accomplishes]

  ## Files to Modify
  | File | Lines | Change |
  |------|-------|--------|
  | `src/file.ts` | 42-58 | Add `functionName()` |

  ## Cross-References
  - `SymbolA` defined at `file.ts:10` - needs update
  - `SymbolB` at `other.ts:25` - caller, verify still works

  ## Implementation Notes
  [Specific guidance from LSP research]

  ## Verification
  `bun run typecheck && bun test`
  """,
  activeForm: "<present continuous form>",
  metadata: {
    "feature": "<feature-name>",
    "files": ["src/file.ts:42-58", "src/other.ts:25"],
    "verification": "bun run typecheck && bun test",
    "crossRefs": ["SymbolA@file.ts:10", "SymbolB@other.ts:25"]
  }
)
```

### 5.2 Set Dependencies

After ALL tasks created, set blockedBy:

```
TaskUpdate(
  taskId: "<id>",
  addBlockedBy: ["<blocker-id>"]
)
```

---

## Step 6: Ask User - Create Only or Start Immediately?

After tasks are created, ask:

```
✅ Created [N] tasks for: [feature name]

Tasks (view with ctrl+t):
  1. [subject] - [status]
  2. [subject] - [status]
  ...

What would you like to do?

1. **Start implementing now** - I'll begin working through the tasks
2. **Just create tasks** - Stop here, implement later with /code:run-tasks

(Default: Start implementing)
```

### Option 1: Start Implementing Now (Default)

If user says "start", "yes", "go", or similar:

1. Create feature branch (if on main)
2. Begin implementing tasks in order
3. Commit after each task
4. Run simplify when done

This is the **fast path** - no command switching needed.

### Option 2: Just Create Tasks

If user says "just create", "stop", "later":

```
Tasks created. Resume later with:
  /code:run-tasks [feature-name]
```

---

## Direct Implementation Flow

When starting immediately, work through tasks using Claude's standard task management:

```
FOR each task in dependency order:
  1. TaskUpdate(task.id, status: "in_progress")
  2. Implement the changes described in the task
  3. Run verification command from task metadata
  4. If pass → TaskUpdate(task.id, status: "completed")
  5. Commit with /code:commit
  6. Continue to next task

WHEN all complete:
  1. Run /simplify on changed files
  2. Report: "All done. Merge or create PR."
```

**No orchestrator or implementer agents needed.** Claude works through the native task list directly. Press `ctrl+t` to see progress.

---

## Quick Reference: LSP Tools

```
# Get definition of symbol at position
mcp__typescript-lsp__getDefinition(file, line, character)

# Find all references to symbol
mcp__typescript-lsp__getReferences(file, line, character)

# Get type info on hover
mcp__typescript-lsp__getHover(file, line, character)

# Get file diagnostics (errors/warnings)
mcp__typescript-lsp__getDiagnostics(file)

# Get document symbols (outline)
mcp__typescript-lsp__getDocumentSymbols(file)
```

---

## Workflow Comparison

### Fast Path (This Command)

```
/plan → /code:quick-tasks → "start" → implementing → done
         └── LSP research    └── Claude works through tasks directly
         └── native tasks        using standard task manager (ctrl+t)
```

### Full Path (GitHub Issue)

```
/plan → /code:plan-issue → /clear → /code:implement #42 → /code:finalizer
         └── LSP research          └── orchestrator spawns Task agents
         └── GitHub issue              for parallel execution
         └── native tasks
```

### When to Use Which

| Use `/code:quick-tasks`     | Use `/code:plan-issue`         |
| --------------------------- | ------------------------------ |
| Solo work, quick iterations | Team visibility needed         |
| Small-medium features       | Large features, multi-day work |
| Familiar codebase           | Need audit trail               |
| Just want to build fast     | Want GitHub issue for tracking |
| Single session              | May span multiple sessions     |
