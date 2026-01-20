---
allowed-tools: Bash(gh issue close:*), Bash(git checkout:*), Bash(git pull:*), Bash(git merge:*), Bash(git push:*), Bash(git branch:*)
description: Close issue, merge branch to main, cleanup
argument-hint: [issue-number]
---

# Finish

Wrap up after implementation: merge branch to main, close issue, cleanup.

Arguments: $ARGUMENTS (optional issue number)

## Step 1: Determine Issue Number

If `$ARGUMENTS` provided → use as issue number.

Otherwise, extract from current branch:
```bash
git branch --show-current
# e.g., feature/10-add-auth → issue #10
```

## Step 2: Merge to Main

```bash
BRANCH=$(git branch --show-current)
git checkout main
git pull origin main
git merge $BRANCH --no-ff -m "Merge $BRANCH"
git push origin main
```

If merge conflict → report and stop.

## Step 3: Cleanup

```bash
# Delete local branch
git branch -d $BRANCH

# Delete remote branch
git push origin --delete $BRANCH

# Close issue
gh issue close <issue-number>
```

## Step 4: Report

Done:
- ✅ Branch `<branch>` merged to main
- ✅ Branch deleted (local + remote)
- ✅ Issue #<number> closed
