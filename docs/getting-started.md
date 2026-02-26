# Getting Started

**Install the plugin, configure a project, and build your first feature with AI agents — in about 10 minutes.**

---

## What You'll Build

By the end of this guide, you'll have:

1. Installed the Coding Plugin
2. Configured a project for task-driven development
3. Planned, implemented, and shipped your first feature using AI agents

---

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Git configured with a remote repository
- **Recommended:** LSP servers and companion plugins (see [Recommended Plugins](../README.md#recommended-plugins))

---

## Step 1: Install the Plugin

See [Installation](../README.md#installation) in the README for marketplace or manual install.

---

## Step 2: Set Up Your Project

Run the setup command inside your project:

```bash
/code:setup
```

This detects your project stack (Bun, npm, Python, etc.) and generates:

- `.claude/settings.json` — permissions tailored to your stack
- Deployment scripts (if applicable)

Then add a unique task list ID to `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_TASK_LIST_ID": "my-project-tasks"
  }
}
```

This lets tasks persist across sessions. Press `ctrl+t` at any time to view them.

---

## Step 3: Plan Your First Feature

Use plan mode to explore the idea before committing to it:

```bash
/plan add a dark mode toggle
```

Or press `Shift+Tab` to toggle plan mode manually. In plan mode, Claude explores your codebase read-only — no changes are made. Iterate until the approach feels right.

---

## Step 4: Create the Issue

Turn your plan into a GitHub issue with tasks:

```bash
/code:plan-issue add a dark mode toggle
```

Output:

```
✅ Issue #42 created: "Add dark mode toggle"
   3 tasks registered
```

Press `ctrl+t` to see the tasks and their status.

> **Tip:** Already have a GitHub issue (e.g. from `@claude` investigation)? Enrich it directly:
>
> ```bash
> /code:plan-issue #33
> ```
>
> This fetches the issue body + comments, creates native tasks, and updates the issue in-place.

---

## Step 5: Implement

Clear context (the planning phase used tokens), then start implementation:

```bash
/clear
/code:implement #42
```

What happens next:

1. **Orchestrator** validates the issue and creates a feature branch
2. **Implementer agents** spawn — one per task, each in its own git worktree
3. Each agent implements, runs verification (tests), and **auto-commits**
4. When all tasks pass, a **simplify pass** cleans up the code
5. Orchestrator reports completion

Watch progress with `ctrl+t`. The whole process runs autonomously.

**Interrupted?** Run `/code:implement #42` again. Tasks track their own state — completed work isn't repeated.

---

## Step 6: Finalize

When implementation is complete, choose how to ship:

### Create a PR for review (recommended)

```bash
/code:finalizer --pr
```

Creates a pull request with a summary of changes, links to the issue, and `Closes #42` so the issue auto-closes on merge.

### Ship directly to main

```bash
/code:finalizer
```

Merges to main, closes the issue, and deletes the feature branch.

---

## What's Next?

- **[User Guide](user-guide.md)** — Deeper coverage of each workflow stage, tips, and troubleshooting
- **[Agent Swarm](agent-swarm.md)** — Parallel execution with multiple Claude sessions
- **[Git Workflow Guide](git-workflow-guide.md)** — When to commit, PR, or merge

---

_Part of the [Innovation Basement Coding Plugin](https://github.com/NOGIT007/innovation-basement)_
