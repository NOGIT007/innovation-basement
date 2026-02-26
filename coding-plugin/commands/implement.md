---
context: fork
allowed-tools: Bash, Bash(gh:*), Bash(git:*), Bash(tmux:*), Read, Write, Edit, Grep, Glob, Task, Skill, TaskList, TaskGet, TaskUpdate
description: Start implementation from a GitHub issue
argument-hint: #<issue-number> [--team | --no-team]
---

# Implement from GitHub Issue

Arguments: $ARGUMENTS

## Step 1: Parse Arguments

Parse `$ARGUMENTS` to extract:

- **Issue number**: strip `#` prefix (e.g. `#42` → `42`)
- **`--team` flag**: force team mode
- **`--no-team` flag**: force subagent mode

Examples: `#42`, `#42 --team`, `--team #42`, `#42 --no-team`

## Step 2: Validate Issue

```bash
gh issue view <number> --json state,title -q '.state + " " + .title'
```

If state is "CLOSED" → error: "Issue is closed."

## Step 3: Ensure Feature Branch

```bash
ISSUE_NUM=<from arguments>
CURRENT_BRANCH=$(git branch --show-current)

if [[ "$CURRENT_BRANCH" != feature/${ISSUE_NUM}-* ]]; then
  SLUG=$(gh issue view $ISSUE_NUM --json title -q '.title' | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g' | cut -c1-30)
  BRANCH="feature/${ISSUE_NUM}-${SLUG}"
  git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
  git push -u origin "$BRANCH" 2>/dev/null || true
  echo "On branch: $BRANCH"
fi
```

## Step 4: Verify Tasks Exist

Check for tasks in native task list:

```
TaskList() → filter by metadata.issueNumber = <number>
```

**If tasks exist:**

- Count tasks with matching issueNumber
- Continue to Step 5

**If no tasks found:**

Error: "No tasks found for issue #<number>. Run `/code:plan-issue` first to create the issue with tasks."

> **Note:** For backwards compatibility with old issues (without native tasks), you may fall back to parsing GitHub issue checkboxes. However, the native Task workflow is preferred.

## Step 5: Detect Execution Mode

Parse flags from arguments:

- `--team` → force team mode
- `--no-team` → force subagent mode
- Neither → auto-detect

### Auto-Detection

If auto-detecting:

1. Check: is `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var set to "1"?
   - If not set → subagent mode (default)

2. Count tasks and dependencies from TaskList (filtered by issueNumber):
   - total_tasks = count of matching tasks
   - independent_tasks = count where blockedBy is empty
   - independence_ratio = independent_tasks / total_tasks

3. Decision:
   - total_tasks >= 4 AND independence_ratio >= 0.6 → team mode
   - Otherwise → subagent mode

### Flag Override

- `--team` forces team mode
  - Still requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
  - If env var missing → error: "Enable team mode first. Add CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 to .claude/settings.json env"
- `--no-team` forces subagent mode (always works)

Report: "Mode: team (auto-detected: N tasks, M% independent)" or "Mode: subagent"

## Step 6a: Launch Orchestrator (Subagent Mode)

If subagent mode was selected, spawn the orchestrator agent to manage all task execution:

```
Task(
  subagent_type: "coding-plugin:orchestrator",
  prompt: """
  Issue: #<number>
  Title: <title>

  Execute all pending tasks for this feature.
  Use TaskList to find tasks with metadata.issueNumber = <number>.
  Update task status and GitHub issue as you complete each task.
  Run /simplify when all tasks are done.
  """
)
```

### Done (Subagent Mode)

The orchestrator now controls execution:

1. Uses TaskList to find pending tasks
2. Spawns implementer for each task (each in its own git worktree for isolation)
3. Commits after each task (worktree changes merge back automatically)
4. Updates GitHub issue status
5. Runs simplify when complete
6. Reports: "Run /code:finalizer [--pr] to finish"

> **Worktree isolation:** Each implementer runs in a separate git worktree, preventing file conflicts when multiple tasks execute in parallel. If a merge conflict occurs when merging back, the task is marked BLOCKED with conflict details.

You will see progress as tasks complete. Press `ctrl+t` to view task progress.

## Step 6b: Launch Agent Team (Team Mode)

You are now the **team lead**. Do NOT spawn the orchestrator agent.

### Create the Team

Create an agent team for this feature. Use natural language:

"Create an agent team called 'issue-<number>' to implement all tasks for
issue #<number> (<title>).

Spawn <N> teammates (where N = min(independent_task_count, 5)).

Each teammate should follow this workflow:

1. Read the project's CLAUDE.md and rules
2. Use TaskList to find tasks where metadata.issueNumber = <number>
3. Claim a pending task: check blockedBy are all completed, then
   TaskUpdate(taskId, status: 'in_progress', owner: '<teammate-name>')
4. Read ALL files before modifying them
5. Implement exactly what the task description specifies — nothing more
6. Run the verification command from metadata.verification
7. If verification passes: TaskUpdate(taskId, status: 'completed')
8. If verification fails: debug (max 3 attempts), then set status to blocked
9. After completing a task, create a conventional commit
10. Pick up the next available task (repeat from step 2)

Rules:

- Only claim tasks where ALL blockedBy tasks have status 'completed'
- One task at a time per teammate
- Never deviate from the task description
- If blocked, move to the next available task"

### Monitor Progress (Lead Loop)

As team lead, monitor until all tasks are done:

```
LOOP every 15 seconds:
  tasks = TaskList() filtered by metadata.issueNumber = <number>

  completed = count where status = "completed"
  blocked = count where status = "blocked"
  pending = count where status = "pending"
  in_progress = count where status = "in_progress"

  # Update GitHub issue for newly completed tasks
  For each newly completed task since last check:
    Update issue body status emoji (⏳→🔄→✅)

  # Report progress
  "Progress: {completed}/{total} tasks ({in_progress} active, {blocked} blocked)"

  # Deadlock detection
  if in_progress == 0 AND pending > 0 AND all pending have incomplete blockers:
    Report deadlock to user with blocked task details
    Break

  # Completion detection
  if pending == 0 AND in_progress == 0:
    All tasks done → Break

END LOOP
```

### After All Tasks Complete

1. Message each teammate: "All tasks for issue #<number> are complete. Please exit your session now."
2. Wait 10 seconds for teammates to exit gracefully:
   ```bash
   sleep 10
   ```
3. Clean up remaining tmux panes (safety net for teammates that didn't exit):
   ```bash
   if [ -n "$TMUX" ]; then
     LEAD_PANE=$(tmux display-message -p '#{pane_id}')
     tmux list-panes -F '#{pane_id}' | while read pane; do
       [ "$pane" != "$LEAD_PANE" ] && tmux kill-pane -t "$pane" 2>/dev/null
     done
   fi
   ```
4. Run `/simplify` on recently changed files
5. Clean up completed tasks:
   ```
   tasks = TaskList() filtered by metadata.issueNumber = <number>
   for each task where status == "completed":
     TaskUpdate(task.id, status: "deleted")
   ```
6. Report: "All {total} tasks complete. Run /code:finalizer [--pr] to finish."

## Resuming Work

To resume interrupted work, simply run `/code:implement #<number>` again.

Both modes reconstruct state from TaskList and continue from where they left off. No handover needed.
