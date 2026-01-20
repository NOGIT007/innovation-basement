# Coding Plugin v1.2.1

**Build apps with AI, even if you can't code.**

A Claude Code plugin that turns your ideas into working software through a simple two-step process: **Plan → Implement**.

---

## How It Works

```
Your Idea → Plan (creates GitHub issue) → Implement (writes the code)
```

The plugin handles the complexity. You focus on what you want to build.

---

## Two Ways to Start

### Option A: Start in Any AI Chat (Recommended for Beginners)

Use Claude.ai, ChatGPT, or any AI to develop your idea first. This is the "interview method" - the AI asks questions, you answer, and together you create a spec.

**Step 1: Interview your idea**

Paste this prompt into any AI chat:

```
Ask me one question at a time so we can develop a thorough, step-by-step spec
for this idea. Each question should build on my previous answers, and our end
goal is to have a detailed specification I can hand off to a developer.
Let's do this iteratively and dig into every relevant detail.
Remember, only one question at a time.

Here's the idea: [describe your idea]
```

**Step 2: Save the spec**

When the AI finishes asking questions and outputs your spec, save it as `SPEC.md` in your project root folder.

**Step 3: Create the plan**

In Claude Code, run:
```
/code:plan-issue @SPEC.md
```

The plugin reads your spec and creates a GitHub issue with implementation phases.

**Step 4: Build it**

```
/code:implement #123
```

The plugin writes the code, phase by phase, until it's done.

---

### Option B: Use Claude Code's Plan Mode

If you're already in Claude Code, use the built-in `/plan` command to explore your idea, then convert it to an issue.

**Step 1: Plan in Claude Code**
```
/plan add a dark mode toggle to the app
```

**Step 2: Create the issue**
```
/code:plan-issue add dark mode toggle
```

**Step 3: Build it**
```
/code:implement #123
```

---

### Quick Fixes (No Plugin Needed)

For small bugs or one-line changes, skip the full workflow. Just tell Claude what's wrong:

```
Fix the typo in the login button text
```

or

```
The submit button doesn't disable after clicking - fix it
```

Claude will find and fix it directly. **Use the plugin for features, not fixes.**

**Tip:** If you started `/plan` mode and want to exit, press `Shift+Tab` or type `/plan` again.

---

## The Simple Workflow

| Step | Command | What Happens |
|------|---------|--------------|
| 1 | `/code:plan-issue <feature>` | Creates GitHub issue with phases |
| 2 | `/code:implement #<number>` | Builds it automatically |

That's it. Two commands.

---

## What Makes This Different

**Context Management** — The plugin automatically handles long-running work by saving progress and continuing where it left off.

**Verification Built-In** — Code is tested before moving forward. No broken builds.

**GitHub as Memory** — Your progress is tracked in GitHub issues. Close the session, come back tomorrow, pick up where you left off.

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `/code:plan-issue <feature>` | Research codebase, create GitHub issue with phases |
| `/code:implement #<number>` | Execute phases from issue (runs until complete) |
| `/code:commit` | Generate conventional commit from staged changes |
| `/code:pr` | Create GitHub PR with auto-generated description |
| `/code:handover` | Save session state (optional - auto-managed) |
| `/code:continue` | Resume from handover |
| `/code:finish <issue> <pr>` | Close issue, merge PR, update local main |
| `/code:simplify` | Clean up code after implementation |
| `/code:lessons [N]` | Analyze recent commits, update LESSONS.md |

### Building Project Knowledge

**Start with `/init`** — Run this in any new project to create a `CLAUDE.md` file. This tells Claude about your project structure, tech stack, and preferences.

**Run `/code:lessons` periodically** — After completing 3-5 issues (or significant changes), run:

```
/code:lessons
```

This analyzes your recent commits, identifies patterns that worked, mistakes to avoid, and project quirks. The output goes into `LESSONS.md` which the plugin reads on future `/code:plan-issue` runs — so it learns from your project history.

---

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Git configured

### Install the Plugin

**Step 1: Clone the plugin**
```bash
mkdir -p ~/.claude/plugins/marketplaces
cd ~/.claude/plugins/marketplaces
git clone https://github.com/NOGIT007/innovation-basement.git
```

**Step 2: Add the marketplace**
```
/plugin marketplace add ~/.claude/plugins/marketplaces/innovation-basement
```

**Step 3: Install**
```
/plugin install coding-plugin@innovation-basement
```

Choose your scope:
- **User scope**: Available in all your projects
- **Project scope**: Shared with collaborators (via git)
- **Local scope**: This repo only, not shared

**Step 4: Restart Claude Code**

Restart to load the plugin, then verify with `/plugin` → Installed tab.

---

## Recommended Plugins

Install from `claude-plugins-official` to enhance the workflow:

```bash
/plugin install frontend-design@claude-plugins-official
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
```

## Recommended MCP Servers

Add these to your project's `.mcp.json` or user-level config:

| Server | Purpose | Config |
|--------|---------|--------|
| `shadcn` | UI component library | `npx shadcn@latest mcp` |
| `Homebrew` | Package manager (macOS) | `brew mcp-server` |

---

## Example: Building a Todo App

### Using Option A (Start in Any AI)

1. **Chat with Claude.ai or ChatGPT** using the interview prompt
2. **Save the output** as `SPEC.md` in your project
3. **In Claude Code:**
   ```
   /code:plan-issue @SPEC.md
   ```
4. **Review the GitHub issue** it creates
5. **Build it:**
   ```
   /code:implement #1
   ```

### Using Option B (Claude Code Only)

1. **Plan:**
   ```
   /plan build a simple todo app with add, complete, and delete
   ```
2. **Create issue:**
   ```
   /code:plan-issue build simple todo app
   ```
3. **Build:**
   ```
   /code:implement #1
   ```

---

## Tips for Non-Coders

**Run `/init` first** — In any new project, run `/init` to create a `CLAUDE.md` file. This teaches Claude about your project.

**Keep scope small** — Start with one feature. The AI will suggest many features. Say no. Build the minimum first.

**Trust the process** — The plugin runs tests automatically. If something breaks, it fixes it before moving on.

**Don't worry about the code** — Focus on describing what you want clearly. The plugin handles the how.

**Use GitHub issues as your memory** — The checkboxes in the issue track progress. Come back anytime.

**Run `/code:lessons` periodically** — After 3-5 completed issues, let the plugin learn from your project.

---

## User Config Backup

The `claude-files/` folder contains example user-level Claude Code config:

```
claude-files/
├── CLAUDE.md              # Core instructions + emoji stacks
├── settings.json          # Plugins, hooks, permissions
├── statusline-command.sh  # Custom status line
└── rules/
    ├── git-workflow.md    # Heredoc workaround
    └── ui.md              # Shadcn/React/Bun
```

To restore: `cp -r claude-files/* ~/.claude/`

---

## Optional: Frontend Stack Rules

For frontend projects using Bun/Shadcn/TypeScript, add this to your project's `CLAUDE.md`:

```markdown
# Frontend Stack Rules
@coding-plugin/rules/frontend.md
```

Or copy the content directly from `coding-plugin/rules/frontend.md` into your project's `CLAUDE.md`.

---

## Troubleshooting

**"No plan found"** — Create a `SPEC.md` file and reference it with `@SPEC.md`, or use `/plan` mode first.

**Tests failing** — The plugin will keep trying to fix them. If stuck, it will ask you.

**Lost progress** — Run `/code:implement #<number>` again. It reads the checkboxes to know where you left off.

---

## Philosophy

This plugin follows the "vibe coding" approach:

- **Simplicity first** — 10 lines of code beats 20 lines
- **Working beats perfect** — Ship something, improve later
- **Delete more than you add** — Less code = fewer bugs

---

## License

MIT

---

Created by Kennet Kusk.
