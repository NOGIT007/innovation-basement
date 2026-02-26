# Coding Plugin v2.14.0 🔌

**Build apps with AI, even if you can't code.**

A Claude Code plugin that turns your ideas into working software through a task-driven workflow.

> **Claude Code compatibility:** Follows features up to [v2.1.50](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md). See the [Claude Code Docs](https://code.claude.com/docs/en/) for the latest features.

---

## What is Innovation Basement

- **Task-driven workflow** — plan → implement → ship, one command per stage
- **Autonomous agents** that research, code, test, and commit for you
- **Works with any stack** — Bun, npm, Python, Rust, Go, and more
- **GitHub-native** — issues become task lists, PRs close issues automatically
- **Optional Agent Swarm** — parallel execution with multiple Claude sessions for complex features

---

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Git configured

### Recommended Plugins

| Plugin              | Marketplace               | What it does                                                     |
| ------------------- | ------------------------- | ---------------------------------------------------------------- |
| `vtsls`             | `claude-code-lsps`        | Go-to-definition, find-references, type lookups for JS/TS        |
| `pyright`           | `claude-code-lsps`        | Same capabilities for Python projects                            |
| `rust-analyzer-lsp` | `claude-plugins-official` | Go-to-definition, find-references, type lookups for Rust         |
| `frontend-design`   | `claude-plugins-official` | Generate production-grade UI components with high design quality |
| `code-review`       | `claude-plugins-official` | Review pull requests with structured feedback                    |
| `agent-sdk-dev`     | `claude-plugins-official` | Scaffold and verify Claude Agent SDK applications                |

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

### Configuration

The plugin ships default settings that apply automatically:

- `plansDirectory: "plans"` — plans saved to plans/ folder
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "70"` — auto-compact at 70% context
- `Bash(git:*)`, `Bash(gh:*)` — git and GitHub CLI permissions
- Custom spinner tips for workflow guidance

Add a unique task list ID to your project's `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_TASK_LIST_ID": "<your-project-name>-tasks"
  }
}
```

`/code:setup` adds stack-specific permissions (e.g., `Bash(bun:*)`) and deployment scripts on top of the base settings.

---

## Quick Start

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│   Project Setup (once per project):                                                  │
│                                                                                      │
│   /code:bun-init my-app  →  /code:setup                                              │
│         │                       │                                                    │
│         ▼                       ▼                                                    │
│   Create Bun + Next.js     Detect stack, generate permissions                        │
│   + Shadcn + Docker        + deployment scripts                                      │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────┤
│   Feature Development:                                                               │
│                                                                                      │
│   /plan  →  /code:plan-issue  →  /clear  →  /code:implement  →  /code:finalizer      │
│     │            │                              │                    │               │
│     ▼            ▼                              ▼                    ▼               │
│   Explore     Create new issue          Orchestrator runs      Merge or PR           │
│   the idea    OR enrich existing #33    all tasks              + cleanup             │
│                     │                         │                      │               │
│                     ▼                         ▼                      ▼               │
│               Output: #42              Auto-compact at 70%     Close issue           │
│               (ctrl+t to view)         No manual handover      Delete branch         │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────┤
│   Deployment (after features merged):                                                │
│                                                                                      │
│   /code:bun-deploy-staging  →  test  →  /code:bun-deploy-production yes              │
│            │                              │                                          │
│            ▼                              ▼                                          │
│   Deploy to GCP staging            Deploy to production                              │
│   (1 CPU, 512Mi, 0-3 inst)         (requires "yes", tests must pass)                 │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────┤
│   Maintenance: /code:cleanup (refactor CLAUDE.md + organize auto-memory)             │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### Your First Feature

```bash
# Project setup (once)
/code:bun-init my-saas-app       # Bun + Next.js + Shadcn + Docker
/code:setup                       # Detect stack, generate permissions + scripts

# Feature development
/plan (shift-tab) add dark mode toggle      # Explore the idea
/code:plan-issue add dark mode toggle       # → Issue #42 created
# OR enrich existing: /code:plan-issue #33
/clear                                       # Free context before implementing
/code:implement #42                          # Orchestrator handles everything
/code:finalizer --pr                         # Create PR for review
# OR: /code:finalizer                        # Merge directly to main

# Deployment
/code:bun-deploy-staging                     # Deploy to GCP staging
/code:bun-deploy-production yes              # Deploy to production (requires "yes")
```

**Interrupted?** Just run `/code:implement #42` again. Native tasks track progress (`ctrl+t` to view).

---

## Commands

### Project Setup

#### `/code:bun-init <project-name>`

Initialize a new Bun + Next.js + Shadcn/UI project with GCP Cloud Run deployment setup.

```bash
/code:bun-init my-app
```

**Creates:** Bun 1.3.8 + Next.js 14+ + Shadcn/UI + TypeScript + Tailwind + Docker + Bun test runner.

---

#### `/code:setup`

Detect project stack and configure Claude Code settings + deployment scripts.

```bash
/code:setup
```

**Detects:** Bun/npm/pnpm, Python, Rust, Go, Next.js/Vite, Firebase/Docker and generates:

- `.claude/settings.json` — Permissions tailored to your stack
- `scripts/dev.sh` — Local development
- `scripts/deploy-staging.sh` — Staging deployment
- `scripts/deploy-production.sh` — Production (requires "yes" confirmation)

---

### Feature Development

#### `/code:plan-issue [#issue | feature] [@spec-file]`

Research codebase, create native tasks, and create or update a GitHub issue.

```bash
# Create new issue from description
/code:plan-issue add user authentication

# Enrich existing issue (e.g. from @claude investigation)
/code:plan-issue #33

# Enrich existing issue with extra context
/code:plan-issue #33 focus on the storage layer

# Use spec file as input
/code:plan-issue @SPEC.md
```

**Existing issue mode (`#<number>`):** Fetches issue body + comments, creates native tasks from the findings, and updates the issue in-place with a task breakdown. Bridges GitHub's `@claude` agent mode with `/code:implement`.

**New issue mode (default):** Researches codebase, creates a new GitHub issue with task manifest.

**Output:** Issue URL + native tasks created (`ctrl+t` to view)

---

#### `/code:implement #<issue-number> [--team | --no-team]`

Launch task execution for all tasks from the issue.

```bash
/code:implement #42             # Auto-detect execution mode
/code:implement #42 --team      # Force Agent Swarm (experimental)
/code:implement #42 --no-team   # Force subagent orchestrator
```

**Execution Modes:**

| Mode                     | When                                   | How It Works                                                               |
| ------------------------ | -------------------------------------- | -------------------------------------------------------------------------- |
| **Subagent** (default)   | < 4 tasks, or many dependencies        | Orchestrator spawns implementer per task (proven, lower token cost)        |
| **Swarm** (experimental) | 4+ independent tasks, or `--team` flag | Main session leads an Agent Swarm — each teammate is a full Claude session |

Auto-detection picks swarm mode when 4+ tasks exist with 60%+ independence. Override with flags.

**Swarm mode requires setup** — see [Agent Swarm](#agent-swarm) section.

**What happens (both modes):**

- Validates issue is open
- Creates feature branch
- Runs tasks in parallel (up to 5 concurrent)
- Commits after each task
- Updates GitHub issue status
- Runs `/simplify` when complete

**Resume:** Run the same command again. Both modes reconstruct state from TaskList.

---

#### `/code:finalizer [--pr] [issue-number]`

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

### Deployment

#### `/code:bun-deploy-staging`

Deploy to GCP Cloud Run staging environment.

```bash
/code:bun-deploy-staging
```

**Config:** 1 CPU, 512Mi, 0-3 instances, unauthenticated. Requires `GCP_PROJECT_STAGING`, `GCP_REGION`, `SERVICE_NAME` in `.env`.

---

#### `/code:bun-deploy-production yes`

Deploy to GCP Cloud Run production. Requires explicit "yes" confirmation.

```bash
/code:bun-deploy-production yes
```

**Safety:** Staging must exist, tests must pass, explicit "yes" required.
**Config:** 2 CPU, 1Gi, 1-10 instances, authenticated, CPU boost.

---

### Utility

#### `/code:commit`

Generate conventional commit from staged changes.

```bash
/code:commit
```

---

#### `/code:pr`

Create GitHub PR with auto-generated description.

```bash
/code:pr
```

---

#### `/code:simplify`

Analyze code for simplification opportunities and bugs.

```bash
/code:simplify
/code:simplify src/utils.ts    # Specific file
```

---

### Maintenance

#### `/code:cleanup`

Refactor CLAUDE.md and organize auto-memory for progressive disclosure. Keeps context files lean and contradiction-free.

```bash
/code:cleanup
```

**What happens:**

1. Finds all CLAUDE.md files
2. Detects contradictions (asks you to resolve)
3. Categorizes instructions (Essential, TypeScript, Testing, Git, etc.)
4. Flags redundant/stale/obvious items (asks you to confirm)
5. Creates `.claude/rules/` structure for detailed rules
6. Writes minimal root CLAUDE.md (target: <50 lines)
7. Organizes auto-memory (deduplicates, removes stale entries)

**Output:** Summary showing before/after line counts and changes made.

---

## Task System

Tasks use Claude Code's native task tracking (`ctrl+t` to view). Each task has a subject, description with file:line references, metadata (`issueNumber`, `verification`), status, and `blockedBy` dependencies.

`/code:plan-issue` creates tasks from codebase research. `/code:implement` executes them — subagent mode spawns implementer agents in isolated worktrees, swarm mode uses independent Claude sessions.

```
pending → in_progress → completed
                ↘ blocked (needs help)
```

Verification gates run automatically: `SubagentStop` hook (subagent mode) and `TaskCompleted` hook (swarm mode) detect and run your test command. Tasks cannot complete without passing tests.

---

## Architecture

```
Subagent Mode (default)                Agent Swarm (experimental)

User                                   User
  │                                      │
  ▼                                      ▼
/implement #42                         /implement #42 --team
  │                                      │
  ▼                                      ▼
Task(orchestrator) ← background        Main session = swarm lead
  │                                      │
  ├─┬─ Task(implementer) ← worktree ─┐  ├─ Teammate 1 (claims tasks)
  │ ├─ Task(implementer) ← worktree ─┼→ ├─ Teammate 2 (claims tasks)
  │ └─ Task(implementer) ← worktree ─┘  └─ Teammate N (max 5)
  │                                      │
  ├── Task(implementer) ← Task 4        Teammates self-coordinate via
  └── Task(simplifier)                   shared TaskList
  │                                      │
  ▼                                      ▼
"Run /finalizer [--pr]"               "Run /finalizer [--pr]"
```

---

## Agent Swarm

> **Experimental** — multiple independent Claude sessions instead of subagents. Best for complex features with 4+ independent tasks.

Enable in `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Use flags: `--team` (force swarm), `--no-team` (force subagent). Auto-detection picks swarm when 4+ tasks exist with 60%+ independence.

See [docs/agent-swarm.md](docs/agent-swarm.md) for full setup including tmux config, display modes, keyboard shortcuts, and limitations.

---

## Best Practices

### Tips

- **Keep scope small** — One feature at a time
- **Trust the process** — Tests run automatically, failures get fixed
- **Claude Code auto-memory captures learnings automatically** — No manual lesson tracking needed
- **Use `/code:bun-init` for new projects** — Creates full Bun + Next.js + GCP setup
- **Use `/code:setup`** — Auto-generates permissions and deployment scripts for your project

### Keyboard Shortcuts

| Shortcut    | Action                                          |
| ----------- | ----------------------------------------------- |
| `Ctrl+T`    | View task list (see progress during /implement) |
| `Shift+Tab` | Toggle plan mode (explore before coding)        |
| `Escape`    | Interrupt current generation                    |
| `Ctrl+C`    | Cancel and return to input                      |
| `/clear`    | Clear conversation context (fresh start)        |
| `/compact`  | Manually compact context to free up space       |
| `/cost`     | View token usage for the session                |
| `Up Arrow`  | Recall previous message                         |

---

## Guides

See [docs/](docs/) for guides: [getting-started](docs/getting-started.md), [user-guide](docs/user-guide.md), [git-workflow](docs/git-workflow-guide.md), [desktop](docs/desktop-guide.md), [agent-swarm](docs/agent-swarm.md).

---

## License

MIT — Created by Kennet Kusk
