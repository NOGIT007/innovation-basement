# Coding Plugin v2.2.1

**Build apps with AI, even if you can't code.**

A Claude Code plugin that turns your ideas into working software through a task-driven workflow.

---

## The Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   /plan  →  /code:plan-issue  →  /clear  →  /code:implement  →  /code:finalizer
│     │            │                              │                    │
│     ▼            ▼                              ▼                    ▼
│   Explore     Create issue              Orchestrator runs      Merge or PR
│   the idea    + native tasks            all tasks              + cleanup
│                     │                         │                      │
│                     ▼                         ▼                      ▼
│               Output: #42              Auto-compact at 70%     Close issue
│               (ctrl+t to view)         No manual handover      Delete branch
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Example

```bash
# 1. Explore your idea
/plan (shift-tab) add dark mode toggle to the app

# 2. Create GitHub issue with tasks
/code:plan-issue add dark mode toggle
# → Issue #42 created

# 3. Clear context before implementing
/clear

# 4. Run implementation (orchestrator handles everything)
/code:implement #42

# 5. Finalize when complete

/code:finalizer         # Merge directly to main
# or
/code:finalizer --pr    # Create PR for review
```

**Interrupted?** Just run `/code:implement #42` again. Native tasks track progress (`ctrl+t` to view).

---

## Required Configuration

Add to your project's `.claude/settings.json`:

```json
{
  "plansDirectory": "plans",
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70",
    "CLAUDE_CODE_TASK_LIST_ID": "<your-project-name>-tasks"
  }
}
```

| Setting                           | Purpose                                                  |
| --------------------------------- | -------------------------------------------------------- |
| `plansDirectory`                  | Store plans in `plans/` folder                           |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Auto-compact at 70% context (agents run indefinitely)    |
| `CLAUDE_CODE_TASK_LIST_ID`        | Unique per project to avoid conflicts (`ctrl+t` to view) |

Without these settings, the Task-based workflow may not work correctly.

---

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Git configured

### Option A: Marketplace (Recommended)

If installed from the Claude Code marketplace, you're done. Verify with `/plugin` → Installed tab.

### Option B: Manual Installation

```bash
# Clone
mkdir -p ~/.claude/plugins/marketplaces
cd ~/.claude/plugins/marketplaces
git clone https://github.com/NOGIT007/innovation-basement.git
```

```
# Add marketplace
/plugin marketplace add ~/.claude/plugins/marketplaces/innovation-basement

# Install
/plugin install coding-plugin@innovation-basement
```

Restart Claude Code after installation.

---

## Commands

### `/code:plan-issue <feature>`

Research codebase and create GitHub issue with task manifest.

```bash
/code:plan-issue add user authentication
/code:plan-issue @SPEC.md              # Use spec file as input
```

**Output:** GitHub issue URL + task manifest created

---

### `/code:implement #<issue-number>`

Launch orchestrator to execute all tasks from the issue.

```bash
/code:implement #42
```

**What happens:**

- Validates issue is open
- Creates feature branch
- Spawns orchestrator agent
- Orchestrator runs tasks in parallel (up to 5 concurrent)
- Commits after each task
- Updates GitHub issue status
- Runs `/simplify` when complete

**Resume:** Run the same command again. Orchestrator reads native tasks and continues.

---

### `/code:finalizer [--pr] [issue-number]`

Finalize feature: merge or create PR, close issue, cleanup.

```bash
/code:finalizer --pr      # Create pull request for review
/code:finalizer           # Merge directly to main
/code:finalizer --pr 42   # Specify issue number
```

**What happens:**

- Verifies all tasks complete
- Creates PR (if `--pr`) or merges to main
- Closes GitHub issue
- Deletes feature branch (local + remote)

---

### `/code:commit`

Generate conventional commit from staged changes.

```bash
/code:commit
```

---

### `/code:pr`

Create GitHub PR with auto-generated description.

```bash
/code:pr
```

---

### `/code:simplify`

Analyze code for simplification opportunities and bugs.

```bash
/code:simplify
/code:simplify src/utils.ts    # Specific file
```

---

### `/code:lessons [N]`

Analyze recent commits and update LESSONS.md with patterns.

```bash
/code:lessons        # Last 5 commits
/code:lessons 10     # Last 10 commits
```

---

## Architecture

```
User
  │
  ▼
/implement #42           ← Thin launcher
  │
  ▼
Task(orchestrator)       ← Master controller
  │
  ├─┬─ Task(implementer)  ← Task 1 ─┐
  │ ├─ Task(implementer)  ← Task 2 ─┼→ parallel
  │ └─ Task(implementer)  ← Task 3 ─┘
  │
  ├── Task(implementer)  ← Task 4 (blocked by 1,2,3)
  └── Task(simplifier)   ← Cleanup
  │
  ▼
"Run /finalizer [--pr]"
```

**Key principle:** Intelligence lives in agents, not commands.

### Parallel Execution

```
Task 1 ─┐
Task 2 ─┼→ all complete → Task 4 (blocked by 1,2,3)
Task 3 ─┘
```

Tasks without dependencies run in parallel. Blocked tasks wait for their dependencies to complete.

---

## Tips

- **Keep scope small** — One feature at a time
- **Trust the process** — Tests run automatically, failures get fixed
- **Run `/code:lessons` periodically** — Builds project knowledge
- **Use `/init` in new projects** — Creates CLAUDE.md with project context

---

## License

MIT — Created by Kennet Kusk
