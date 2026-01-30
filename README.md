# Coding Plugin v2.4.1

**Build apps with AI, even if you can't code.**

A Claude Code plugin that turns your ideas into working software through a task-driven workflow.

---

## The Flow

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│   /plan  →  /code:interview  →  /code:plan-issue  →  /clear  →  /code:implement  →  /code:finalizer
│     │            │                    │                              │                    │
│     ▼            ▼                    ▼                              ▼                    ▼
│   Explore     Clarify             Create issue              Orchestrator runs      Merge or PR
│   the idea    requirements        + native tasks            all tasks              + cleanup
│               (optional)                │                         │                      │
│                                         ▼                         ▼                      ▼
│                                   Output: #42              Auto-compact at 70%     Close issue
│                                   (ctrl+t to view)         No manual handover      Delete branch
│                                                                                         │
├──────────────────────────────────────────────────────────────────────────────────────┤
│   Maintenance (run periodically):                                                    │
│                                                                                      │
│   /code:lessons  →  /code:cleanup                                                    │
│        │                 │                                                           │
│        ▼                 ▼                                                           │
│   Analyze commits    Refactor CLAUDE.md                                              │
│   Update LESSONS.md  Progressive disclosure                                          │
│        │                                                                             │
│        └──────────────────────────► LESSONS.md read by /code:plan-issue              │
│                                     (informs future feature planning)                │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### Example

```bash
# 1. Explore your idea
/plan (shift-tab) add dark mode toggle to the app

# 2. (Optional) Clarify requirements
/code:interview
# → Answers questions, updates plan with details

# 3. Create GitHub issue with tasks
/code:plan-issue add dark mode toggle
# → Issue #42 created

# 4. Clear context before implementing
/clear

# 5. Run implementation (orchestrator handles everything)
/code:implement #42

# 6. Finalize when complete

/code:finalizer         # Merge directly to main
# or
/code:finalizer --pr    # Create PR for review

# 7. (Periodic) Update project knowledge
/code:lessons           # Analyze commits, update LESSONS.md
/code:cleanup           # Refactor context files
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

### `/code:interview [plan-file]`

Deep requirement clarification through structured questioning. Use between `/plan` and `/code:plan-issue`.

```bash
/code:interview              # Uses most recent plan
/code:interview plans/my.md  # Specific plan file
```

**What happens:**

- Finds most recent plan in `plans/` folder
- Analyzes plan for ambiguous areas (breadth-first)
- Asks 2-3 related questions per round
- Continues until you say `done`, `stop`, or `enough`
- Merges answers into `## Details` section of plan

**Note:** Interview is optional. Skip directly to `/code:plan-issue` if requirements are clear.

---

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

### `/code:cleanup`

Refactor CLAUDE.md and LESSONS.md for progressive disclosure. Keeps context files lean and contradiction-free.

```bash
/code:cleanup
```

**What happens:**

1. Finds all CLAUDE.md and LESSONS.md files
2. Detects contradictions (asks you to resolve)
3. Categorizes instructions (Essential, TypeScript, Testing, Git, etc.)
4. Flags redundant/stale/obvious items (asks you to confirm)
5. Creates `.claude/rules/` structure for detailed rules
6. Writes minimal root CLAUDE.md (target: <50 lines)
7. Archives LESSONS.md content (never deletes)

**Output:** Summary showing before/after line counts and changes made.

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
