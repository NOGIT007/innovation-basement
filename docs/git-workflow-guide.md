# 🔀 Git Workflow Guide: Commit, PR & Merge

**When to use each command in the Innovation Basement plugin workflow.**

---

## 🎯 Quick Decision Tree

```
Did you just finish a task?
  └── YES → Orchestrator auto-commits (you're done)
  └── NO, working manually → /code:commit

Ready to get code reviewed?
  └── YES → /code:finalizer --pr
  └── Just want a quick PR → /code:pr

All tasks done, ready to ship?
  └── Want review first → /code:finalizer --pr
  └── Ship directly → /code:finalizer
```

---

## 📊 Command Comparison

| Command                | What it does                               | When to use                            |
| ---------------------- | ------------------------------------------ | -------------------------------------- |
| `/code:commit`         | Creates single commit from staged changes  | Manual work outside task flow          |
| `/code:pr`             | Creates PR from current branch             | Quick PR without finalizing            |
| `/code:finalizer --pr` | Creates PR + links issue + ready for merge | **Recommended** - End of task workflow |
| `/code:finalizer`      | Merges to main + closes issue + cleanup    | Ship without review                    |

---

## 🔄 The Automated Flow (Recommended)

When using the full plugin workflow, **you rarely need to run git commands manually**:

```
/plan "feature"           → Plan created
/plan-issue               → GitHub issue + tasks created
/implement #42            → Orchestrator runs...
                             ├── Task 1 → auto-commit ✓
                             ├── Task 2 → auto-commit ✓
                             ├── Task 3 → auto-commit ✓
                             └── Simplify → auto-commit ✓
/finalizer --pr           → PR created, ready for review
```

**The orchestrator commits after each task.** You don't need to think about it.

---

## 📝 /code:commit - Single Commit

**Use when:** Working manually, outside the orchestrator flow.

```bash
# Stage your changes first
git add src/auth.ts

# Then commit with smart message generation
/code:commit
```

**What it does:**

1. Analyzes staged changes
2. Generates conventional commit message with emoji
3. Writes to `.claude-commit-msg.txt`
4. Commits with `git commit -F`

**Commit format:**

```
✨ feat: add user authentication

- Add login/logout endpoints
- Implement JWT token handling

Closes #123
```

| Emoji | Type     | Use for            |
| ----- | -------- | ------------------ |
| ✨    | feat     | New features       |
| 🐛    | fix      | Bug fixes          |
| ♻️    | refactor | Code restructuring |
| 📝    | docs     | Documentation      |
| 🧪    | test     | Tests              |
| 🔧    | config   | Configuration      |

---

## 🔀 /code:pr - Quick Pull Request

**Use when:** You want a PR but aren't using the full task workflow.

```bash
/code:pr
```

**What it does:**

1. Checks branch state
2. Auto-commits any uncommitted changes
3. Generates PR description from commits
4. Creates PR via `gh pr create`

**Output:**

```
PR created: https://github.com/user/repo/pull/45

Title: feat: add user authentication
Base: main ← feature/42-add-auth
```

**Note:** This is a "quick and dirty" PR. For proper workflow, use `/code:finalizer --pr`.

---

## 🏁 /code:finalizer - The Right Way to Finish

### Option 1: Create PR for Review (Recommended)

```bash
/code:finalizer --pr
```

**What it does:**

1. Verifies all tasks complete (via TaskList)
2. Generates comprehensive PR body:
   - Summary of changes
   - List of completed tasks
   - Link to GitHub issue
3. Creates PR with `Closes #<issue>` (auto-closes on merge)
4. **Does NOT merge** - waits for review

**Output:**

```
PR created: https://github.com/user/repo/pull/45

## Summary
Added user authentication with JWT tokens.

## Tasks Completed
- [x] Create auth types and context
- [x] Add login/logout handlers
- [x] Write integration tests

Closes #42
```

**Then:** Review on GitHub → Approve → Merge → Issue auto-closes.

---

### Option 2: Ship Directly (No Review)

```bash
/code:finalizer
```

**What it does:**

1. Verifies all tasks complete
2. Merges feature branch to main (no-ff)
3. Pushes to origin
4. Closes GitHub issue
5. Deletes feature branch (local + remote)

**Output:**

```
## Feature Finalized

✅ Issue #42 closed
✅ Branch merged to main
✅ Feature branch deleted (local + remote)
✅ Changes pushed

Done!
```

**Use when:** Solo project, small change, or CI/CD handles validation.

---

## 🆚 PR vs Direct Merge

| Factor               | `/finalizer --pr`       | `/finalizer`    |
| -------------------- | ----------------------- | --------------- |
| Code review          | ✅ Yes                  | ❌ No           |
| CI runs before merge | ✅ Yes                  | ❌ No           |
| Audit trail          | ✅ PR shows discussion  | ⚠️ Just commits |
| Speed                | Slower (needs approval) | Faster          |
| Team work            | ✅ Required             | Solo only       |
| Rollback             | Easy (revert PR)        | Harder          |

---

## Complete Workflow Example

```bash
/plan "add user authentication"          # Plan the feature
/plan-issue                               # → Issue #42 with 3 tasks
/implement #42                            # Orchestrator runs all tasks
/finalizer --pr                           # → PR #45 created
# After PR approved + merged → Issue #42 auto-closes
```

---

## Common Mistakes

- **Don't commit during orchestrator run** — it auto-commits, manual commits confuse the flow
- **Don't use `/code:pr` when tasks exist** — use `/code:finalizer --pr` (verifies tasks, links issue)
- **Don't worry about pushing** — PR commands handle it automatically
- **Don't direct merge on team projects** — always use `--pr` for review

---

## Cleanup

- **Direct merge** (`/finalizer`): branch deleted + issue closed automatically
- **PR** (`/finalizer --pr`): issue auto-closes on merge. Delete branch manually or on GitHub.

---

**The golden path:** `/plan` → `/plan-issue` → `/implement` → `/finalizer --pr`

---

_Part of the Innovation Basement Coding Plugin_
