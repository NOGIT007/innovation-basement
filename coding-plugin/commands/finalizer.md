---
allowed-tools: Bash(gh:*), Bash(git:*), Read, Write, TaskList, TaskUpdate
description: Finalize feature: close issue, merge or create PR, cleanup
argument-hint: [--pr] [issue-number]
---

# Finalizer

Arguments: $ARGUMENTS

## Step 1: Determine Issue Number

Extract from arguments (e.g., `#42` or `42`) or branch name:

```bash
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" =~ feature/([0-9]+)- ]]; then
  ISSUE_NUM="${BASH_REMATCH[1]}"
fi
```

If no issue number found → error: "Provide issue number or run from feature branch."

## Step 2: Verify All Tasks Complete

```
TaskList() → filter by metadata.issueNumber = <issue>
```

- If any task `status != "completed"` → error with list of incomplete tasks
- If no tasks found → warning, proceed without task verification

## Step 3: Determine Action

- `--pr` in arguments → create pull request
- No flag → merge directly to main

## Step 4a: Create Pull Request (if --pr)

Write `.claude-pr-body.md` using **Write tool**:

```markdown
## Summary

<brief description of the feature>

## Tasks Completed

- [x] Task 1: <subject>
- [x] Task 2: <subject>

## Related Issue

Closes #<issue-number>

---

_Created with `/code:finalizer --pr`_
```

```bash
gh pr create --title "[Feature] <issue title>" --body-file .claude-pr-body.md --base main
```

Report PR URL. Issue closes automatically when PR is merged. **Stop here.**

## Step 4b: Merge to Main (if no --pr)

```bash
git status --porcelain  # If dirty → error: "Uncommitted changes."
git checkout main
git pull origin main
git merge feature/<issue>-<slug> --no-ff -m "Merge feature/<issue>-<slug>: <title>"
git push origin main
gh issue close <number> --comment "Completed and merged to main."
git branch -d feature/<issue>-<slug>
git push origin --delete feature/<issue>-<slug>
```

## Error Handling

- **Merge conflict:** Report options: resolve manually then re-run, or use `--pr` instead. Run `git merge --abort` to cancel.
- **Branch not found:** Report current branch, ask if on correct branch.
- **PR already exists:** Report existing PR URL, suggest `gh pr merge`.

## Cleanup

After merge or PR creation, delete all tasks for this issue:

```
tasks = TaskList() → filter by metadata.issueNumber = <issue>
for each task:
  TaskUpdate(task.id, status: "deleted")
```

After direct merge: feature branch deleted (local + remote), issue closed, tasks cleaned up.
