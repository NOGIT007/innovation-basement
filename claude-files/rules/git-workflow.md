<!-- Rule Indicator: Add 🔀 when git work -->

# Git Workflow Rules

## GitHub CLI First

Use `gh` for GitHub operations. Stay in terminal.

| Operation           | Command                                        |
| ------------------- | ---------------------------------------------- |
| Create issue        | `gh issue create -t "..." -b "..."`            |
| Create issue (long) | `gh issue create -t "..." --body-file file.md` |
| View issue          | `gh issue view <number>`                       |
| List issues         | `gh issue list`                                |
| Close issue         | `gh issue close <number>`                      |
| Create PR           | `gh pr create -t "..." -b "..."`               |
| Create PR (long)    | `gh pr create -t "..." --body-file file.md`    |

---

## ⚠️ CRITICAL: No Heredocs in Sandbox

Heredocs fail silently — sandbox can't create temp files. **This causes empty content.**

### Short content → Single quotes

```bash
gh issue create --title "Title" --body 'Short body here'
git commit -m 'Short message'
```

### Long content → Write to fixed temp file (no cleanup needed)

Use `.claude-` prefixed filenames that are gitignored and overwritten each time:

| Use Case       | Filename                 |
| -------------- | ------------------------ |
| Issue body     | `.claude-issue-body.md`  |
| PR body        | `.claude-pr-body.md`     |
| Commit message | `.claude-commit-msg.txt` |

```bash
# 1. Use Write tool to create file
# Write .claude-issue-body.md with full content...

# 2. Reference file (no cleanup - gitignored, overwritten next time)
gh issue create --title "[Feature] Name" --body-file .claude-issue-body.md
```

### Commits with long messages

```bash
# 1. Write commit message to file
# Write .claude-commit-msg.txt...

# 2. Commit with file (no cleanup needed)
git commit -F .claude-commit-msg.txt
```

### Updating issues with long body

```bash
# 1. Write updated body to file
# Write .claude-issue-body.md...

# 2. Update issue
gh issue edit <number> --body-file .claude-issue-body.md
```

> **Note:** Add these to your project's `.gitignore`:
>
> ```
> .claude-issue-body.md
> .claude-pr-body.md
> .claude-commit-msg.txt
> ```

### What NOT to do

```bash
# ❌ NEVER - fails silently, produces empty content
gh issue create --body "$(cat <<'EOF'
content here
EOF
)"

# ❌ NEVER
git commit -m "$(cat <<'EOF'
message
EOF
)"
```

**Non-negotiable. Heredocs = empty content = wasted work.**

---

## Before Every Commit

1. `git status` — review changes
2. `git diff -- <file>` — verify content (always use `--`)
3. Run tests if applicable
4. Commit with format below

---

## Commit Format

```
<emoji> <type>: <subject>

[body if complex]

[Closes #123 if applicable]
```

| Emoji | Type     | Example                      |
| ----- | -------- | ---------------------------- |
| ✨    | Feature  | `✨ feat: add auth`          |
| 🐛    | Bug fix  | `🐛 fix: redirect loop`      |
| ♻️    | Refactor | `♻️ refactor: extract logic` |
| 📝    | Docs     | `📝 docs: update readme`     |
| 🧪    | Tests    | `🧪 test: add unit tests`    |
| 🔧    | Config   | `🔧 config: update eslint`   |

---

## Branch Conventions

| Branch           | Purpose      |
| ---------------- | ------------ |
| `main`           | Production   |
| `feature/<name>` | New features |
| `fix/<name>`     | Bug fixes    |

---

## Push Setup

First push may fail with "no upstream branch".

```bash
# One-time fix (run in regular terminal, not sandbox):
git config --global push.autoSetupRemote true

# Or per-push:
git push --set-upstream origin <branch>
```

---

## Git Diff Syntax

Always use `--` before file paths to avoid ambiguity:

```bash
# ❌ Ambiguous - may fail
git diff path/to/file.ts

# ✅ Correct
git diff -- path/to/file.ts
git diff HEAD -- path/to/file.ts
git diff main -- path/to/file.ts
```

---

## Proactive Flags

Stop and warn (❗) if:

- ❗ About to use heredoc → use `--body-file` instead
- ❗ `git diff` without `--` separator
- ❗ Committing without `git status` first
- ❗ Large commit (>10 files) → split it
- ❗ Missing issue reference in feature commit
- ❗ Push fails with no upstream → suggest fix
- ❗ Merge conflicts detected
- ❗ Sensitive files staged (.env, secrets)
