# User Guide

**Workflow reference for active users of the Coding Plugin.**

This guide covers each stage of the development workflow. For first-time setup, see [Getting Started](getting-started.md). For the full command reference, see the [README](../README.md).

---

## Planning

Before writing code, explore the idea in plan mode.

```bash
/plan add user authentication
```

Or press `Shift+Tab` to toggle plan mode. Plan mode is read-only — Claude explores without making changes.

**When to use:** New features (explore architecture), bug investigation (trace before fixing), refactoring (understand dependencies).

**Spec files:** For complex features, pass a spec file: `/code:plan-issue @SPEC.md`. Structured context (acceptance criteria, constraints, API shapes) produces more precise task breakdowns.

---

## Creating Tasks

### The Plan-Issue Command

```bash
# Create new issue from a description
/code:plan-issue add dark mode toggle

# Enrich an existing issue (e.g. from @claude investigation)
/code:plan-issue #33

# Enrich existing issue with extra context
/code:plan-issue #33 focus on the storage layer

# Use a spec file
/code:plan-issue @SPEC.md
```

This researches your codebase, creates or updates a GitHub issue, and registers native tasks. Each task includes:

| Field            | Purpose                                               |
| ---------------- | ----------------------------------------------------- |
| **Subject**      | What to implement (imperative form)                   |
| **Description**  | Detailed steps with `file:line` references            |
| **Metadata**     | `issueNumber`, `verification` command, `feature` name |
| **Dependencies** | `blockedBy` relationships to other tasks              |

### Existing Issue Mode

When you pass `#<number>`, plan-issue fetches the issue body and comments, creates native tasks, and updates the issue in-place. Ideal for bridging `@claude` agent mode: `@claude` investigates → `/code:plan-issue #33` creates tasks → `/code:implement #33` executes.

### Viewing Tasks

Press `ctrl+t` to see all tasks and their status in the terminal. Tasks persist across sessions when `CLAUDE_CODE_TASK_LIST_ID` is set.

### Task Dependencies

Tasks can depend on each other:

```
Task 1: "Create auth types"
Task 2: "Create auth context" (blockedBy: Task 1)
Task 3: "Add login page" (blockedBy: Task 2)
```

Blocked tasks stay pending until their dependencies complete, then auto-unblock.

---

## Implementing

### Starting Implementation

```bash
/clear                   # Free up context from planning
/code:implement #42      # Start executing tasks
```

Always `/clear` before implementing — the planning phase consumes tokens that the orchestrator doesn't need.

### Execution Modes

| Mode                   | When                            | How                                                                |
| ---------------------- | ------------------------------- | ------------------------------------------------------------------ |
| **Subagent** (default) | < 4 tasks, or many dependencies | Orchestrator spawns one implementer per task in isolated worktrees |
| **Agent Swarm**        | 4+ independent tasks            | Main session leads, teammates claim tasks in parallel              |

Auto-detection picks the right mode. Override with flags:

```bash
/code:implement #42 --team      # Force swarm
/code:implement #42 --no-team   # Force subagent
```

### What Happens During Execution

1. Issue is validated (must be open)
2. Feature branch is created
3. Tasks run in dependency order (up to 5 concurrent)
4. Each task: implement → verify (tests) → auto-commit
5. Simplify pass runs when all tasks complete
6. Orchestrator reports final status

### Resuming Interrupted Work

If a session crashes or you need to stop:

```bash
/code:implement #42
```

Run the same command again. Both modes reconstruct state from the task list — completed tasks are skipped, in-progress tasks resume.

---

## Deploying

Deployment commands work with Bun + GCP Cloud Run projects created via `/code:bun-init`.

### Staging

```bash
/code:bun-deploy-staging
```

Builds and deploys to GCP Cloud Run staging (1 CPU, 512Mi, 0-3 instances). Requires `GCP_PROJECT_STAGING`, `GCP_REGION`, and `SERVICE_NAME` in `.env`.

### Production

```bash
/code:bun-deploy-production yes
```

Requires explicit "yes" confirmation. Staging must exist and tests must pass. Deploys with 2 CPU, 1Gi, 1-10 instances.

### When to Deploy

- Deploy to **staging** after merging a feature to main
- Test on staging, then deploy to **production** when satisfied
- Never deploy directly to production without staging verification

---

## Agent Swarm

See [Agent Swarm Guide](agent-swarm.md) for setup and usage of parallel multi-session execution.

---

## Maintenance

### Cleanup

```bash
/code:cleanup
```

Refactors `CLAUDE.md` files and organizes auto-memory:

- Detects contradictions and redundancies
- Creates `.claude/rules/` structure for detailed rules
- Targets < 50 lines for root `CLAUDE.md`
- Deduplicates auto-memory entries

### Simplify

```bash
/code:simplify              # Whole project
/code:simplify src/utils.ts # Specific file
```

Analyzes code for simplification opportunities and potential bugs. Runs automatically at the end of `/code:implement`, but you can run it manually anytime.

### Keeping CLAUDE.md Lean

- Run `/code:cleanup` periodically (monthly or after major features)
- Move detailed rules to `.claude/rules/` — root `CLAUDE.md` should be a brief index
- Let auto-memory handle session-specific learnings

---

## Tips & Troubleshooting

### Common Issues

**Tasks aren't persisting across sessions**
Set `CLAUDE_CODE_TASK_LIST_ID` in `.claude/settings.json`. Each project needs a unique ID.

**Implementation seems stuck**
Press `ctrl+t` to check task status. If a task is blocked, it needs manual intervention — read the task description for context.

**Verification gate failing**
The plugin runs your test command after each task. If tests fail, the implementer retries. Check the test output for the actual failure.

**Context getting too large**
The plugin auto-compacts at 70% context usage. If you're doing manual work and hitting limits, use `/clear` between phases (planning → implementing).

### Best Practices

- **One feature at a time** — keep scope small and focused
- **Trust the process** — tests run automatically, failures get retried
- **Clear between phases** — `/clear` before `/code:implement` frees context
- **Use spec files for complex features** — `@SPEC.md` gives better task breakdowns
- **Check `ctrl+t` for progress** — the task list is your dashboard

### Getting Help

- Plugin repo: [github.com/NOGIT007/innovation-basement](https://github.com/NOGIT007/innovation-basement)
- Claude Code issues: [github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues)

---

_Part of the [Innovation Basement Coding Plugin](https://github.com/NOGIT007/innovation-basement)_
