# Coding Plugin v2.9.0

**Build apps with AI, even if you can't code.**

A Claude Code plugin that turns your ideas into working software through a task-driven workflow.

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
│   Explore     Create issue              Orchestrator runs      Merge or PR           │
│   the idea    + native tasks            all tasks              + cleanup             │
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

# 5. Create GitHub issue with tasks
/code:plan-issue add dark mode toggle
# → Issue #42 created

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

#### `/code:plan-issue <feature>`

**Full path:** Research codebase and create GitHub issue with task manifest.

```bash
/code:plan-issue add user authentication
/code:plan-issue @SPEC.md              # Use spec file as input
```

**Output:** GitHub issue URL + task manifest created

---

#### `/code:implement #<issue-number>`

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
- **Claude Code auto-memory captures learnings automatically** — No manual lesson tracking needed
- **Use `/code:bun-init` for new projects** — Creates full Bun + Next.js + GCP setup
- **Use `/code:setup`** — Auto-generates permissions and deployment scripts for your project

---

## License

MIT — Created by Kennet Kusk
