---
allowed-tools: Bash(git log:*), Bash(gh issue view:*), Read, Write, Glob
description: Analyze recent commits against issues, update LESSONS.md with patterns/mistakes
argument-hint: [commits=20]
---

# Analyze Commits & Update Lessons

Commits to analyze: $ARGUMENTS (default: 20)

## Step 1: Read Recent Commits

```bash
git log --oneline -${ARGUMENTS:-20}
```

Parse each commit for:

- Issue references (#N)
- Commit type (feature, fix, refactor)
- Files changed scope

## Step 2: Compare Against Issues

For commits with issue references (#N):

```bash
gh issue view <N> --json title,body,state
```

Check:

- Did commit match issue scope?
- Was it a single-phase or multi-commit?
- Any follow-up "fix" commits?

## Step 3: Read Existing Lessons

```bash
cat LESSONS.md 2>/dev/null
```

Keep relevant existing lessons, remove outdated ones (>30 days unless still applicable).

## Step 4: Analyze Patterns

Look for:

### Patterns That Worked

- Commits that closed issues cleanly
- Good commit message patterns
- Effective phase breakdowns

### Mistakes Repeated

- Reverts or "oops" commits
- Fix commits right after features
- Scope creep (commit exceeded issue)
- Missing tests after features

### Project Quirks

- Environment-specific issues
- Framework gotchas
- Config requirements

**Flag with ❗ if same mistake appears 3+ times.**

## Step 5: Update LESSONS.md

Write or update `LESSONS.md` (max 50 lines):

```markdown
# Project Lessons

_Last updated: [date] from [N] commits_

## Patterns That Work

- [Specific pattern with issue reference if applicable]

## Mistakes to Avoid

- [Specific mistake - how to prevent]

## Project Quirks

- [Specific quirk - workaround]
```

## Rules

- Keep total file under 50 lines
- Be specific: "run linter before commit" not "be careful"
- Reference issue numbers when relevant
- Remove lessons older than 30 days unless still recurring
- Output summary of changes made
