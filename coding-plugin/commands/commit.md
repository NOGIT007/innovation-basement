---
allowed-tools: Bash(git:*), Write
description: Generate conventional commit from staged changes
---

# Smart Commit

Generate a conventional commit message from staged changes.

## Step 1: Check Staged Changes

```bash
git status --short
git diff --cached --stat
```

If nothing staged → Tell user to stage changes first (`git add`).

## Step 2: Analyze Changes

Read the staged diff:
```bash
git diff --cached
```

Determine:
- Type: feat/fix/refactor/docs/test/config
- Scope: affected area (optional)
- Summary: what changed and why

## Step 3: Check Recent History

```bash
git log -5 --oneline
```

Match the project's commit style.

## Step 4: Generate Commit

Format: `<emoji> <type>: <subject>`

| Emoji | Type | Use for |
|-------|------|---------|
| ✨ | feat | New features |
| 🐛 | fix | Bug fixes |
| ♻️ | refactor | Code restructuring |
| 📝 | docs | Documentation |
| 🧪 | test | Tests |
| 🔧 | config | Configuration |

## Step 5: Execute Commit

**Short message (< 50 chars):**
```bash
git commit -m "✨ feat: add user authentication"
```

**Long message (multi-line):**
1. Write to `.claude-commit-msg.txt`:
   ```
   ✨ feat: add user authentication

   - Add login/logout endpoints
   - Implement JWT token handling
   - Add auth middleware

   Closes #123
   ```
2. Commit with file:
   ```bash
   git commit -F .claude-commit-msg.txt
   ```

## Rules

- **No heredocs** - Always use Write tool + `-F` flag for long messages
- **Atomic commits** - One logical change per commit
- **Present tense** - "add feature" not "added feature"
- **No period** - Subject line doesn't end with period
