# Coding Plugin v3.0.1

A Claude Code plugin for structured development workflow by Kennet Kusk.

> **Tip:** Use Claude Code's `/plan` mode to explore changes before `/code:plan-issue`

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                           CODING PLUGIN WORKFLOW                              │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│   IDEATION              PLANNING                EXECUTION                     │
│                                                                               │
│   ┌──────────────┐     ┌──────────────┐       ┌──────────────┐               │
│   │  /interview  │     │ /plan-issue  │       │  /implement  │               │
│   │              │────▶│              │──────▶│    #123      │               │
│   │  Spec File   │     │ GitHub Issue │       │   Code It    │               │
│   └──────────────┘     └──────────────┘       └──────────────┘               │
│          │                    ▲                      │                        │
│          ▼                    │                      ▼                        │
│   ┌──────────────┐            │               ┌──────────────┐               │
│   │/constitution │────────────┤               │  /handover   │               │
│   │              │ (auto-read)│               │              │               │
│   │  Principles  │            │               │ Save State   │               │
│   └──────────────┘            │               └──────────────┘               │
│                               │                      │                        │
│   ┌──────────────┐            │                      ▼                        │
│   │   /lessons   │────────────┘               ┌──────────────┐               │
│   │              │ (auto-read)                │   /resume    │               │
│   │   Patterns   │                            │  Continue    │               │
│   └──────────────┘                            └──────────────┘               │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Philosophy:** Interview → Plan → Implement (no code until plan approved)

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
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
```

## Requirements

- GitHub CLI (`gh`)
- Git

## License

MIT
