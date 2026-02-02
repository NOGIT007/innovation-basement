---
context: fork
allowed-tools: Bash(git:*), Read, Task, TaskList, TaskUpdate
description: Run pending tasks from native task manager (no GitHub issue required)
argument-hint: [feature-name]
---

# Run Tasks (Native Task Manager)

Feature filter: $ARGUMENTS

> **For use after `/code:quick-tasks`** - executes tasks without GitHub issue dependency.

---

## Step 1: Find Pending Tasks

Use TaskList to find work:

```
TaskList() → filter by:
  - status: "pending" or "in_progress"
  - (optional) metadata.feature matches $ARGUMENTS
```

**If no tasks found:**

```
No pending tasks found.

Create tasks with:
  • /code:quick-tasks <feature>  (LSP research, no GitHub issue)
  • /code:plan-issue <feature>   (LSP research + GitHub issue)
```

**If tasks found:**

Show task summary:

```
Found [N] pending tasks:
  1. [subject] - pending
  2. [subject] - pending (blocked by #1)
  ...

Starting orchestrator...
```

---

## Step 2: Ensure Working Branch

```bash
CURRENT_BRANCH=$(git branch --show-current)
FEATURE_NAME="$ARGUMENTS"

# If on main, create feature branch
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  SLUG=$(echo "$FEATURE_NAME" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g' | cut -c1-30)
  BRANCH="feature/${SLUG}"
  git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
  echo "On branch: $BRANCH"
else
  echo "Using current branch: $CURRENT_BRANCH"
fi
```

---

## Step 3: Launch Orchestrator

Spawn the orchestrator to manage execution:

```
Task(
  subagent_type: "coding-plugin:orchestrator",
  prompt: """
  Mode: Native tasks only (no GitHub issue)
  Feature: <feature-name>

  Execute all pending tasks.
  Use TaskList to find pending tasks.

  For each task:
  1. Mark in_progress with TaskUpdate
  2. Spawn implementer
  3. Wait for completion
  4. Commit changes
  5. Mark completed with TaskUpdate

  Skip GitHub issue updates (no issue exists).
  Run /simplify when all tasks are done.
  """
)
```

---

## Done

Orchestrator now runs tasks:

1. TaskList to find pending work
2. Spawns implementer for each task
3. Commits after each task
4. Marks complete via TaskUpdate
5. Runs simplify when done

Press `ctrl+t` to view task progress.

---

## When Complete

When all tasks are done, you can:

```bash
# Merge directly to main
git checkout main && git merge <branch> --no-ff

# Or create PR for review
/code:pr
```

No `/code:finalizer` needed (that's for GitHub issue workflow).

---

## Resuming Work

To resume interrupted work:

```
/code:run-tasks [feature-name]
```

Orchestrator uses TaskList and continues from where it left off.
