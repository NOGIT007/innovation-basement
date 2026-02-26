---
context: fork
allowed-tools: Bash, Bash(gh:*), Bash(git:*), Bash(tmux:*), Read, Write, Edit, Grep, Glob, Task, Skill, TaskList, TaskGet, TaskUpdate
description: Start implementation from a GitHub issue
argument-hint: #<issue-number> [--team | --no-team]
---

# Implement from GitHub Issue

Arguments: $ARGUMENTS

## Step 1: Parse Arguments

Extract from `$ARGUMENTS`:

- **Issue number** (strip `#` prefix)
- **`--team`** or **`--no-team`** flag (optional)

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

```
TaskList() → filter by metadata.issueNumber = <number>
```

If tasks exist → continue to Step 5.
If no tasks found → error: "No tasks found for issue #<number>. Run `/code:plan-issue` first."

## Step 5: Detect Execution Mode

- `--team` → force team mode (requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, error if missing)
- `--no-team` → force subagent mode
- Neither → auto-detect:
  1. If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` not set → subagent
  2. Count tasks: total, independent (no blockedBy), independence ratio
  3. If total >= 4 AND ratio >= 0.6 → team mode, otherwise → subagent

Report: "Mode: team (N tasks, M% independent)" or "Mode: subagent"

## Step 6a: Launch Orchestrator (Subagent Mode)

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

The orchestrator spawns implementers in isolated worktrees, commits after each task, and reports "Run /code:finalizer [--pr] to finish." Press `ctrl+t` to view progress.

## Step 6b: Launch Agent Team (Team Mode)

You are the **team lead**. Do NOT spawn the orchestrator.

### Create the Team

Create an agent team called 'issue-<number>'. Spawn N teammates (min of independent_task_count, 5). Each teammate:

1. Read CLAUDE.md and rules
2. Use TaskList to find tasks where metadata.issueNumber = <number>
3. Claim a pending task (verify blockedBy all completed first): `TaskUpdate(taskId, status: 'in_progress', owner: '<name>')`
4. Read ALL files before modifying
5. Implement exactly what the task specifies
6. Run verification from metadata.verification
7. If pass → `TaskUpdate(taskId, status: 'completed')`, commit, pick next task
8. If fail → debug (max 3 attempts), then set blocked
9. Only claim tasks where ALL blockedBy are completed
10. One task at a time, never deviate from description

### Monitor Progress (Lead Loop)

```
LOOP every 15 seconds:
  tasks = TaskList() filtered by metadata.issueNumber
  completed, blocked, pending, in_progress = count by status

  # Update GitHub issue for newly completed tasks (⏳→🔄→✅)
  # Report: "Progress: {completed}/{total} ({in_progress} active, {blocked} blocked)"

  # Deadlock: if in_progress == 0 AND pending > 0 with incomplete blockers → report, break
  # Complete: if pending == 0 AND in_progress == 0 → break
END LOOP
```

### After All Tasks Complete

1. Message teammates to exit
2. Wait 10s, then clean up remaining tmux panes:
   ```bash
   if [ -n "$TMUX" ]; then
     LEAD_PANE=$(tmux display-message -p '#{pane_id}')
     tmux list-panes -F '#{pane_id}' | while read pane; do
       [ "$pane" != "$LEAD_PANE" ] && tmux kill-pane -t "$pane" 2>/dev/null
     done
   fi
   ```
3. Run `/simplify` on recently changed files
4. Delete completed tasks: `TaskUpdate(task.id, status: "deleted")`
5. Report: "All {total} tasks complete. Run /code:finalizer [--pr] to finish."

## Resuming Work

Run `/code:implement #<number>` again. Both modes reconstruct state from TaskList.
