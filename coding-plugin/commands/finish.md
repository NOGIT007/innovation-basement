---
allowed-tools: Bash(gh issue close:*), Bash(gh pr merge:*), Bash(gh pr view:*), Bash(gh pr list:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git pull:*), Bash(git branch:*), Bash(git push:*), Skill
description: Close issue, merge PR, and update local main
argument-hint: [issue-number]
---

# Finish

Wrap up after implementation: close issue, merge PR, sync local main.

Arguments: $ARGUMENTS (optional issue number)

## Step 1: Determine Issue Number

If `$ARGUMENTS` provided → use as issue number.

Otherwise, extract from current branch:
```bash
git branch --show-current
# e.g., feature/10-add-auth → issue #10
```

If still unclear → ask user.

## Step 2: Ensure PR Exists

```bash
gh pr list --head <current-branch> --json number,state
```

**If no PR exists:**
1. Push branch: `git push -u origin <branch>`
2. Create PR: `Skill("coding-plugin:pr")`
3. Get PR number from output

**If PR exists:** Use existing PR number.

## Step 2.5: Verify PR is Mergeable

```bash
gh pr view <pr-number> --json state,mergeable,mergeStateStatus
```

Check:
- `state` = "OPEN"
- `mergeable` = "MERGEABLE"

If not mergeable → report why and stop.

## Step 3: Confirm with User

Show summary:
- Issue: #<number> - <title>
- PR: #<number> - <title>
- Actions: Close issue, merge PR, update local main

Ask: **"Merge and close?"**

Wait for explicit "yes".

## Step 4: Execute

```bash
# Merge PR (squash by default)
gh pr merge <pr-number> --squash --delete-branch

# Close issue
gh issue close <issue-number>

# Update local main
git checkout main && git pull origin main
```

## Step 5: Report

Done:
- ✅ Issue #<number> closed
- ✅ PR #<number> merged
- ✅ Local main updated

## Rules

- **Wait for confirmation** — never auto-merge
- **Squash by default** — keeps history clean
- **Delete branch** — cleanup after merge
