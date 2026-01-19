# Coding Plugin v1.0.0

A Claude Code plugin for structured development workflow.

## Philosophy: Plan → Implement

**No code until plan approved.** This plugin enforces a two-step workflow:

1. **Plan** - Use `/code:plan-issue` to research with LSP precision and create a GitHub issue
2. **Implement** - Use `/code:implement #123` to execute the plan phase by phase

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              CODING PLUGIN WORKFLOW                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ╔═══════════════════════════════════════════════════════════════════════════════════╗ │
│   ║  WEB/DESKTOP (Quick Mode)                                                          ║ │
│   ║  • Bug triage • TODO fixes • Exploration • Parallel sessions                       ║ │
│   ╚═══════════════════════════════════════════════════════════════════════════════════╝ │
│                          │                                                               │
│                          │ complex task?                                                 │
│                          ▼                                                               │
│   ╔═══════════════════════════════════════════════════════════════════════════════════╗ │
│   ║  CLI (Full Mode)                                                                   ║ │
│   ╠═══════════════════════════════════════════════════════════════════════════════════╣ │
│   ║                                                                                    ║ │
│   ║                       PLANNING                    EXECUTION                       ║ │
│   ║                                                                                    ║ │
│   ║                      ┌──────────────┐            ┌──────────────┐                 ║ │
│   ║                      │ /plan-issue  │            │  /implement  │                 ║ │
│   ║                      │              │            │    #123      │                 ║ │
│   ║                      │   Creates    │───────────▶│              │                 ║ │
│   ║                      │ GitHub Issue │  Issue #   │   Code It    │                 ║ │
│   ║                      └──────────────┘            └──────────────┘                 ║ │
│   ║                                                                                    ║ │
│   ╚═══════════════════════════════════════════════════════════════════════════════════╝ │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Commands

| Command | Description |
|---------|-------------|
| `/code:plan-issue <feature> [@spec]` | Research with LSP, create GitHub issue. Accepts `@file` refs |
| `/code:implement #<number>` | Execute phases from issue |
| `/code:simplify [focus]` | Simplify code, create issues for bugs |
| `/code:handover` | Save session state with issue progress |
| `/code:continue` | Continue from handover |
| `/code:lessons [N]` | Analyze commits, update LESSONS.md |

## Installation

### Step 1: Clone the marketplace locally

```bash
mkdir -p ~/.claude/plugins/marketplaces
cd ~/.claude/plugins/marketplaces
git clone https://github.com/NOGIT007/innovation-basement.git
```

### Step 2: Add marketplace in Claude Code

```
/plugin marketplace add ~/.claude/plugins/marketplaces/innovation-basement
```

### Step 3: Install plugins

```
/plugin install coding-plugin@innovation-basement
```

Choose your scope:
- **User scope**: Available in all your projects
- **Project scope**: Shared with collaborators (via git)
- **Local scope**: This repo only, not shared

### Step 4: Restart Claude Code

Restart to load the plugin, then verify with `/plugin` → Installed tab.

## Recommended Plugins

Install from `claude-plugins-official` to enhance the workflow:

```bash
/plugin install frontend-design@claude-plugins-official
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
```

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

## Requirements

- GitHub CLI (`gh`)
- Git
- Node.js (for npx - used by MCP servers)

## Recommended MCP Servers

Add these to your project's `.mcp.json` or user-level config:

| Server | Purpose | Config |
|--------|---------|--------|
| `shadcn` | UI component library | `npx shadcn@latest mcp` |
| `Homebrew` | Package manager (macOS) | `brew mcp-server` |

## License

MIT
