---
allowed-tools: Bash(gh:*), Bash(git:*), Read, Write, TaskList
description: Finalize feature: close issue, merge or create PR, cleanup
argument-hint: [--pr] [issue-number]
---

# Finalizer

Arguments: $ARGUMENTS

Finalize the feature implementation by closing the issue and merging or creating a PR.

## Step 1: Determine Issue Number

Extract issue number from:

1. **Arguments** - if provided directly (e.g., `#42` or `42`)
2. **Branch name** - if on `feature/<num>-*` branch

```bash
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" =~ feature/([0-9]+)- ]]; then
  ISSUE_NUM="${BASH_REMATCH[1]}"
fi
```

If no issue number found → error: "Provide issue number or run from feature branch."

## Step 2: Verify All Tasks Complete

Check tasks via native TaskList:

```
TaskList() → filter by metadata.issueNumber = <issue>
```

**If any task has `status != "completed"`:**

Error: "Tasks incomplete. Run `/code:implement #<number>` to finish."

List incomplete tasks:

```
Incomplete tasks:
- Task 1: <subject> (in_progress)
- Task 3: <subject> (pending)
```

**If no tasks found:**

Warning: "No tasks found for issue #<number>. Proceeding without task verification."

## Step 3: Determine Action (PR or Merge)

Check if `--pr` flag is in arguments:

- **If `--pr`**: Create pull request for review
- **If no flag**: Merge directly to main

## Step 4a: Create Pull Request (if --pr)

### Write PR Body

Use **Write tool** to create `.claude-pr-body.md`:

```markdown
## Summary

<brief description of the feature>

## Tasks Completed

- [x] Task 1: <subject>
- [x] Task 2: <subject>
- [x] Task 3: <subject>

## Related Issue

Closes #<issue-number>

---

_Created with `/code:finalizer --pr`_
```

### Create PR

```bash
gh pr create --title "[Feature] <issue title>" --body-file .claude-pr-body.md --base main
```

### Report

```
PR created: <PR URL>

Issue #<number> will close automatically when PR is merged.
```

**Stop here if --pr** (don't merge or close issue)

## Step 4b: Merge to Main (if no --pr)

### Ensure clean state

```bash
git status --porcelain
```

If dirty → error: "Uncommitted changes. Commit or stash first."

### Merge

```bash
git checkout main
git pull origin main
git merge feature/<issue>-<slug> --no-ff -m "Merge feature/<issue>-<slug>: <title>"
git push origin main
```

### Close Issue

```bash
gh issue close <number> --comment "Completed and merged to main."
```

### Delete Branch

```bash
# Delete local
git branch -d feature/<issue>-<slug>

# Delete remote
git push origin --delete feature/<issue>-<slug>
```

### Report

```
## Feature Finalized

✅ Issue #<number> closed
✅ Branch merged to main
✅ Feature branch deleted (local + remote)
✅ Changes pushed

Done!
```

## Error Handling

### Merge Conflicts

If merge fails:

```
Merge conflict detected.

Options:
1. Resolve conflicts manually, then re-run /code:finalizer
2. Use --pr to create a pull request instead

Run: git merge --abort to cancel
```

### Branch Not Found

```
Feature branch not found: feature/<issue>-<slug>

Are you on the correct branch?
Current branch: <current>
```

### PR Already Exists

If PR already exists for this branch:

```
PR already exists: <PR URL>

Use 'gh pr merge <number>' to merge, or review and merge via GitHub.
```

## Cleanup

After successful completion, cleanup is automatic:

- Local feature branch deleted
- Remote feature branch deleted
- Native tasks remain in task list (visible via `ctrl+t`)
