# Coding Plugin v3.5.1

A Claude Code plugin for structured development workflow by Kennet Kusk.

## What's New in v3.5.0

### Hard Verification Gate
- Tests **must pass** before marking any task `[x]`
- Auto-detects test commands (bun, npm, pytest, cargo, make)
- No exceptions - enforced by Implementer Agent

### Specialized Agents
- **Planner**: LSP-precise research and phase creation
- **Implementer**: Code execution with verification gate
- **Reviewer**: Code quality review (separate from tests)

### New Hooks
- `SessionEnd`: Warn about uncommitted changes
- `SubagentStop`: Trigger verification after agent phases
- `PreCompact`: Save state before context compaction

### Constitution Enhancement
- New "Verification Strategy" section in interview
- Captures test requirements and commands

> **Tip:** Use Claude Code's `/plan` mode to explore changes before `/code:plan-issue`

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
│   ║   IDEATION                 PLANNING                    EXECUTION                   ║ │
│   ║   (optional)               (required)                  (required)                  ║ │
│   ║                                                                                    ║ │
│   ║   ┌──────────────┐        ┌──────────────┐            ┌──────────────┐            ║ │
│   ║   │  /interview  │        │ /plan-issue  │            │  /implement  │            ║ │
│   ║   │              │        │              │            │    #123      │            ║ │
│   ║   │  idea.md ──▶ │───────▶│   Creates    │───────────▶│              │            ║ │
│   ║   │  spec.md     │        │ GitHub Issue │  Issue #   │   Code It    │            ║ │
│   ║   └──────────────┘        └──────────────┘            └──────────────┘            ║ │
│   ║          │                       ▲                           │                     ║ │
│   ║          ▼                       │                           ▼                     ║ │
│   ║   ┌──────────────┐               │                    ┌──────────────┐            ║ │
│   ║   │/constitution │               │                    │   Commits    │            ║ │
│   ║   │              │───────────────┤                    └──────┬───────┘            ║ │
│   ║   │constitution.md│  (auto-read) │                           │                     ║ │
│   ║   └──────────────┘               │                           ▼                     ║ │
│   ║                                  │                    ┌──────────────┐            ║ │
│   ║   ┌──────────────┐               │                    │  /handover   │            ║ │
│   ║   │   /lessons   │───────────────┘                    │              │            ║ │
│   ║   │              │   (auto-read)                      │ .handover.md │            ║ │
│   ║   │  LESSONS.md  │◀──────────────────────────────────┐└──────────────┘            ║ │
│   ║   └──────────────┘  (run after commits)              │       │                     ║ │
│   ║                                                      │       ▼                     ║ │
│   ║                                                      │┌──────────────┐            ║ │
│   ║                                                      ││   /resume    │            ║ │
│   ║                                                      ││              │            ║ │
│   ║                                                      └│  Continue    │            ║ │
│   ║                                                       └──────────────┘            ║ │
│   ║                                                                                    ║ │
│   ╚═══════════════════════════════════════════════════════════════════════════════════╝ │
│                                                                                          │
│   Philosophy: Interview → Plan → Implement (no code until plan approved)                 │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Commands

| Command | Description |
|---------|-------------|
| `/code:interview <spec>` | Develop vague ideas into comprehensive specs |
| `/code:constitution` | Create project principles (constitution.md) |
| `/code:plan-issue <feature>` | Research with LSP, create GitHub issue |
| `/code:implement #<number>` | Execute phases from issue |
| `/code:handover` | Save session state with issue progress |
| `/code:resume` | Continue from handover |
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
/plugin install commit-commands@claude-plugins-official
/plugin install code-review@claude-plugins-official
/plugin install pr-review-toolkit@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
```

## User Config Backup

The `claude-files/` folder contains a backup of user-level Claude Code config (Boris approach):

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
- Homebrew (macOS package manager)

## Included MCP Servers

The plugin includes these MCP servers (project-level via `.mcp.json`):

| Server | Purpose | Prerequisite |
|--------|---------|--------------|
| `chrome-devtools` | Browser automation | Node.js |
| `shadcn` | UI component library | Node.js |
| `Homebrew` | Package manager | Homebrew installed |
| `jina` | Web reader (SSE) | None |

These are automatically available when the plugin is installed - no user-level config needed.

## License

MIT
