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

| Emoji | Type     | Use for            |
| ----- | -------- | ------------------ |
| ✨    | feat     | New features       |
| 🐛    | fix      | Bug fixes          |
| ♻️    | refactor | Code restructuring |
| 📝    | docs     | Documentation      |
| 🧪    | test     | Tests              |
| 🔧    | config   | Configuration      |

## Step 5: Execute Commit

### ⚠️ CRITICAL: Always Use -F Flag

**Never use `git commit -m`** — emojis and special characters cause sandbox errors.

**Always:**

1. Write message to `.claude-commit-msg.txt` using Write tool
2. Commit with `-F` flag

```bash
git commit -F .claude-commit-msg.txt
```

**Example `.claude-commit-msg.txt`:**

```
✨ feat: add user authentication

- Add login/logout endpoints
- Implement JWT token handling
- Add auth middleware

Closes #123
```

### Validation (REQUIRED)

Before committing, verify file exists:

```bash
if [ ! -s .claude-commit-msg.txt ]; then
  echo "❌ ERROR: Commit message file missing. Use Write tool first."
  exit 1
fi
```

## Rules

- **No `-m` flag** — Always use `-F .claude-commit-msg.txt`
- **No heredocs** — Always use Write tool
- **Atomic commits** — One logical change per commit
- **Present tense** — "add feature" not "added feature"
- **No period** — Subject line doesn't end with period
