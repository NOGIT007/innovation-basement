# Coding Plugin v2.12.2 🔌

**Build apps with AI, even if you can't code.**

A Claude Code plugin that turns your ideas into working software through a task-driven workflow.

> **Claude Code compatibility:** Follows features up to [v2.1.50](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md). See the [Claude Code Docs](https://code.claude.com/docs/en/) for the latest features.

---

## Guides

| Guide           | For                                                       | Link                                                     |
| --------------- | --------------------------------------------------------- | -------------------------------------------------------- |
| Getting Started | First-time users — install to first feature in 10 minutes | [docs/getting-started.md](docs/getting-started.md)       |
| User Guide      | Active users — workflows, tips, and troubleshooting       | [docs/user-guide.md](docs/user-guide.md)                 |
| Git Workflow    | When to commit, PR, or merge                              | [docs/git-workflow-guide.md](docs/git-workflow-guide.md) |
| Desktop Guide   | Using the plugin with Claude Code Desktop                 | [docs/desktop-guide.md](docs/desktop-guide.md)           |

---

## The Flow

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

### Example: Feature Development

```bash
# ══════════════════════════════════════════════════════════
# PROJECT SETUP (once)
# ══════════════════════════════════════════════════════════

# 1. Create new project
/code:bun-init my-saas-app
# → Creates Bun + Next.js + Shadcn + Docker setup

# 2. Configure project (settings + deployment)
/code:setup
# → Detects stack, generates .claude/settings.json + deployment scripts

# ══════════════════════════════════════════════════════════
# FEATURE DEVELOPMENT
# ══════════════════════════════════════════════════════════

# 4. Explore your idea
/plan (shift-tab) add dark mode toggle to the app

# 5a. Create NEW GitHub issue with tasks
/code:plan-issue add dark mode toggle
# → Issue #42 created

# 5b. OR enrich EXISTING issue (e.g. from @claude investigation)
/code:plan-issue #33
# → Issue #33 updated with task breakdown

# 6. Clear context before implementing
/clear

# 7. Run implementation (orchestrator handles everything)
/code:implement #42

# 8. Finalize when complete
/code:finalizer         # Merge directly to main
# or
/code:finalizer --pr    # Create PR for review

# ══════════════════════════════════════════════════════════
# DEPLOYMENT (after features merged)
# ══════════════════════════════════════════════════════════

# 9. Deploy to staging
/code:bun-deploy-staging
# → Builds and deploys to GCP Cloud Run staging

# 10. Test staging, then deploy to production
/code:bun-deploy-production yes
# → Requires "yes", verifies tests pass first

```

**Interrupted?** Just run `/code:implement #42` again. Native tasks track progress (`ctrl+t` to view).

---

## Task Workflow

Tasks are at the heart of this plugin. They use Claude Code's native task tracking system.

### What Are Tasks?

Tasks are work items tracked by Claude Code's built-in TaskCreate/TaskList/TaskUpdate tools. Press `ctrl+t` to view them in the terminal.

Each task has:

- **Subject** — what to implement (imperative form)
- **Description** — detailed steps with file:line references
- **Metadata** — `issueNumber`, `verification` command, `feature` name
- **Status** — pending, in_progress, completed, or blocked
- **Dependencies** — `blockedBy` relationships to other tasks

### How Tasks Are Created

`/code:plan-issue` researches your codebase, creates or updates a GitHub issue, and registers native tasks with metadata:

```bash
# From scratch — creates new issue
/code:plan-issue add dark mode toggle
# → Creates GitHub issue #42
# → Creates native tasks with metadata.issueNumber = 42

# From existing issue — enriches in-place
/code:plan-issue #33
# → Fetches issue #33 body + comments
# → Creates native tasks with metadata.issueNumber = 33
# → Updates issue #33 with task breakdown
```

### How Tasks Are Executed

When you run `/code:implement #42`:

- **Subagent mode (default):** Orchestrator spawns implementer agents per task. Each implementer runs in its own git worktree for isolation.
- **Agent Swarm mode:** Your session becomes the lead. Teammate sessions claim tasks from the shared list independently.

### Task Lifecycle

```
pending → in_progress → completed
                ↘ blocked (needs help)
```

- **pending** — waiting to be picked up
- **in_progress** — being implemented by an agent/teammate
- **completed** — implementation done, verification passed
- **blocked** — cannot proceed, needs user intervention

### Dependencies

Tasks can have `blockedBy` relationships. A task won't start until all its blockers are completed:

```
Task 3: "Add API routes" (blockedBy: [Task 1, Task 2])
  → Stays pending until Task 1 AND Task 2 are completed
  → Then auto-unblocks and gets picked up
```

### Verification Gates

Every task has a verification command that must pass (exit 0) before completion:

- **Subagent mode:** `SubagentStop` hook runs `verify-gate.sh` — detects test framework and runs tests
- **Swarm mode:** `TaskCompleted` hook runs `team-task-complete.sh` — same pattern
- Both hooks skip tests when an agent reports `BLOCKED` (uses `last_assistant_message`)

---

## Required Configuration

### Base Settings (ships with plugin)

The plugin ships default settings that apply automatically:

- `plansDirectory: "plans"` — plans saved to plans/ folder
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "70"` — auto-compact at 70% context
- `Bash(git:*)`, `Bash(gh:*)` — git and GitHub CLI permissions
- Custom spinner tips for workflow guidance

### Project-Specific Settings (you add)

Add to your project's `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_TASK_LIST_ID": "<your-project-name>-tasks"
  }
}
```

| Setting                    | Purpose                                                  |
| -------------------------- | -------------------------------------------------------- |
| `CLAUDE_CODE_TASK_LIST_ID` | Unique per project to avoid conflicts (`ctrl+t` to view) |

`/code:setup` adds stack-specific permissions (e.g., `Bash(bun:*)`) and deployment scripts on top of the base settings.

---

## Agent Swarm

Agent Swarm lets `/code:implement` use multiple independent Claude Code sessions instead of subagents. **One developer, many agents** — you become the lead, Claude spawns a swarm of coding agents that parallelize your work.

### What Is Agent Swarm?

You (single user) run one Claude Code session that becomes the **lead** (coordinator). Claude spawns multiple independent sessions (agents) that claim tasks from a shared task list, implement them in parallel, and self-coordinate. Think of it as your personal swarm of coding agents.

This is NOT a multi-user team feature. It's one person leveraging multiple parallel Claude instances to move faster on complex features.

### How It Works

```
You (lead session)
  │
  ├─ Teammate 1 → claims Task A → implements → verifies → commits
  ├─ Teammate 2 → claims Task B → implements → verifies → commits
  ├─ Teammate 3 → claims Task C → implements → verifies → commits
  └─ ...up to 5 teammates
  │
  Shared TaskList ← self-coordination
  │
  Teammates message each other directly when needed
```

- **Your session** = lead (monitors progress, updates GitHub issue)
- **Teammate sessions** = workers (claim tasks, implement, verify, commit)
- **Shared TaskList** = coordination layer (tasks auto-unblock as dependencies complete)
- **Direct messaging** = teammates can message each other for cross-task coordination

### Display Modes

Agent Swarm supports two display modes:

**In-process (default)** — works in any terminal. All agents run in the same terminal window.

```json
{ "teammateMode": "in-process" }
```

Or via CLI: `claude --teammate-mode in-process`

Use `Shift+Down` to cycle between agents and view/message them.

**Split-pane** — each agent gets its own terminal pane. Requires tmux or iTerm2.

```json
{ "teammateMode": "tmux" }
```

Or via CLI: `claude --teammate-mode tmux`

### Configure tmux for Split-Pane Mode (macOS)

Install tmux:

```bash
brew install tmux
```

Create `~/.tmux.conf`:

```bash
# Mouse support
set -g mouse on

# Scrollback buffer
set -g history-limit 10000

# Start windows and panes at 1
set -g base-index 1
setw -g pane-base-index 1

# Pane navigation with Alt+Arrow
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Status bar theme
set -g status-style 'bg=#1a1a2e fg=#e0e0e0'
set -g status-left '#[fg=#00d4aa,bold] #S '
set -g status-right '#[fg=#666]%H:%M'

# Split shortcuts
bind | split-window -h
bind - split-window -v

# Reload config
bind r source-file ~/.tmux.conf \; display "Config reloaded"

# Cheat sheet
bind h run-shell "~/.tmux/cheatsheet.sh"
```

Create `~/.tmux/cheatsheet.sh`:

```bash
#!/bin/bash
tmux display-popup -w 60 -h 20 -E "echo '
  tmux Cheat Sheet
  ════════════════════════════
  Alt+Arrow    Navigate panes
  Prefix + |   Vertical split
  Prefix + -   Horizontal split
  Prefix + r   Reload config
  Prefix + h   This cheat sheet
  Prefix + z   Toggle zoom pane
  Scroll       Mouse wheel
  ════════════════════════════
  Prefix = Ctrl+B (default)
' && read -n 1"
```

```bash
chmod +x ~/.tmux/cheatsheet.sh
```

Start Agent Swarm in tmux mode:

```bash
claude --teammate-mode tmux
```

> **Note:** Split-pane works best on macOS. Linux may need adjustments to the tmux config.

### Enable Agent Swarm

Add to your project's `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_TASK_LIST_ID": "<your-project-name>-tasks",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### When Does Agent Swarm Activate?

| Scenario                                      | Mode                             |
| --------------------------------------------- | -------------------------------- |
| Env var not set                               | Always subagent (default)        |
| Env var set + < 4 tasks                       | Subagent (auto-detected)         |
| Env var set + 4+ tasks with 60%+ independence | Swarm (auto-detected)            |
| `--team` flag                                 | Swarm (forced, requires env var) |
| `--no-team` flag                              | Subagent (forced, always works)  |

### Using Agent Swarm

```bash
# Let auto-detection decide
/code:implement #42

# Force swarm mode for a complex cross-layer feature
/code:implement #42 --team

# Force subagent mode when you want lower token usage
/code:implement #42 --no-team
```

### Keyboard Shortcuts

| Shortcut     | Action                  |
| ------------ | ----------------------- |
| `Shift+Down` | Cycle to next agent     |
| `Shift+Up`   | Cycle to previous agent |
| `Ctrl+T`     | View shared task list   |
| `Escape`     | Interrupt current agent |

### Interacting with Agents

You can message any agent directly:

1. Press `Shift+Down` to select the agent you want to talk to
2. Type your message — redirect their approach, give additional instructions, or ask for status
3. Each agent maintains its own context and continues where it left off

### Quality Gates

The plugin ships hooks that enforce verification in swarm mode:

- **`TeammateIdle` hook** — when a teammate finishes a task and goes idle, the hook directs them to pick up the next available task from TaskList
- **`TaskCompleted` hook** — runs the detected test command before accepting task completion. Uses exit code 2 to reject if tests fail (task stays in_progress for retry)

Agents cannot skip verification. The hooks run automatically.

### Token Usage

Each teammate is a separate Claude instance. Agent Swarm uses significantly more tokens than subagent mode. Use it for complex features with 4+ independent tasks where parallel work justifies the cost.

### Limitations

- **No session resumption** — if a teammate crashes, it cannot be resumed. The lead will detect the stalled task and can re-dispatch
- **One swarm per session** — you can only run one Agent Swarm at a time
- **No nested swarms** — teammates cannot spawn their own swarms
- **Lead is fixed** — the session that starts the swarm is always the lead, cannot be transferred

---

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Git configured

### Recommended MCP Servers

Install these MCP servers for LSP-powered codebase research in `/code:plan-issue`:

```
/mcp add typescript-lsp
/mcp add python-lsp
```

The `typescript-lsp` server enables go-to-definition, find-references, and type lookups during planning. The `python-lsp` server provides equivalent capabilities for Python projects.

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

## Rules

The plugin includes rules that provide patterns and guardrails.

### `bun-native.md`

Bun 1.3+ native API patterns. Prefer these over npm packages:

| Instead of            | Use Bun Native                      |
| --------------------- | ----------------------------------- |
| `pg` / `postgres`     | `import { sql } from "bun:sql"`     |
| `ioredis` / `redis`   | `import { redis } from "bun:redis"` |
| `@aws-sdk/client-s3`  | `import { S3 } from "bun:s3"`       |
| `express` / `fastify` | `Bun.serve()`                       |

### `gcp-safety.md`

GCP resource protection rules:

- **Never delete** Cloud Run services, SQL instances, GCS buckets without explicit approval
- **Require "yes"** for production deployments
- **Start small** with resource sizing (staging: 1 CPU/512Mi, production: 2 CPU/1Gi)
- **Separate environments** by project ID (`*-staging` vs `*-prod`)

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

**Key principle:** Intelligence lives in agents, not commands.

**Subagent mode** — Orchestrator runs as a background task, spawning implementers in isolated git worktrees. Lower token cost, proven workflow.

**Agent Swarm** — Main session leads. Teammates are independent sessions that communicate with each other and self-coordinate through the shared task list. Higher token cost, best for complex features with many independent tasks.

---

## Claude Code Essential Shortcuts

Quick reference for the most useful Claude Code keyboard shortcuts and commands.

### Navigation & Control

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

### Agent Swarm Navigation

| Shortcut     | Action                                |
| ------------ | ------------------------------------- |
| `Shift+Down` | Cycle to next agent (in-process mode) |
| `Shift+Up`   | Cycle to previous agent               |

### Common Workflows

```bash
# Start planning → exploring the idea
Shift+Tab → describe your feature → Shift+Tab to exit plan mode

# Check progress mid-implementation
Ctrl+T → see task statuses → Escape to dismiss

# Running out of context
/compact → continue working with compressed history

# Starting fresh after a feature
/clear → begin next feature with clean context

# Check what you've spent
/cost → see input/output tokens and cost
```

---

## Tips

- **Keep scope small** — One feature at a time
- **Trust the process** — Tests run automatically, failures get fixed
- **Claude Code auto-memory captures learnings automatically** — No manual lesson tracking needed
- **Use `/code:bun-init` for new projects** — Creates full Bun + Next.js + GCP setup
- **Use `/code:setup`** — Auto-generates permissions and deployment scripts for your project

---

## License

MIT — Created by Kennet Kusk
