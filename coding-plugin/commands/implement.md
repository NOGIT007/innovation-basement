---
context: fork
allowed-tools: Bash(gh issue view:*), Bash(git:*), Read, Task, TaskList
description: Start implementation from a GitHub issue
argument-hint: #<issue-number>
---

# Implement from GitHub Issue

Issue: $ARGUMENTS

This is a **thin launcher** that spawns the orchestrator agent.

## Step 1: Validate Issue

```bash
gh issue view <number> --json state,title -q '.state + " " + .title'
```

If state is "CLOSED" → error: "Issue is closed."

## Step 2: Ensure Feature Branch

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

## Step 3: Verify Tasks Exist

Check for tasks in native task list:

```
TaskList() → filter by metadata.issueNumber = <number>
```

**If tasks exist:**

- Count tasks with matching issueNumber
- Continue to Step 4

**If no tasks found:**

Error: "No tasks found for issue #<number>. Run `/code:plan-issue` first to create the issue with tasks."

> **Note:** For backwards compatibility with old issues (without native tasks), you may fall back to parsing GitHub issue checkboxes. However, the native Task workflow is preferred.

## Step 4: Launch Orchestrator

Spawn the orchestrator agent to manage all task execution:

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

## Done

The orchestrator now controls execution:

1. Uses TaskList to find pending tasks
2. Spawns implementer for each task
3. Commits after each task
4. Updates GitHub issue status
5. Runs simplify when complete
6. Reports: "Run /code:finalizer [--pr] to finish"

You will see progress as tasks complete. Press `ctrl+t` to view task progress.

## Resuming Work

To resume interrupted work, simply run `/code:implement #<number>` again.

The orchestrator uses TaskList and continues from where it left off. No handover needed.
