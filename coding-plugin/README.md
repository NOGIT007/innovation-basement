# coding-plugin

Structured coding workflow plugin for Claude Code. Part of the innovation-basement marketplace.

**[📖 Read the Full User Guide](./GUIDE.md)** - Complete guide with copy-paste commands and examples.

## Features

- **Phased Workflow**: Research -> Plan -> Implement
- **GitHub Integration**: Auto-create issues for each phase
- **Context Hygiene**: Warnings at 60%/80% context usage
- **Bug Fix Tracking**: Warn after 3+ failed attempts
- **Auto Error Logging**: Build institutional knowledge
- **vibe-coding Rules**: Simplicity-first coding philosophy
- **frontend-design Rules**: Avoid generic AI aesthetics for UI work
- **Sub-agents**: Research and documentation specialists

## Installation

```bash
/plugin marketplace add NOGIT007/innovation-basement
/plugin install coding-plugin@innovation-basement
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `/start <description>` | Initialize new workflow |
| `/research <topic>` | Start research phase |
| `/plan <feature>` | Start planning phase |
| `/implement <feature>` | Start implementation |
| `/status` | Check current status |
| `/complete` | Mark phase complete |
| `/nuke` | Generate summary for fresh chat |

See [GUIDE.md](./GUIDE.md) for detailed usage and examples.

## Workflow

```
Research → Plan → Implement
```

1. **Start**: `/start "Add user authentication"`
2. **Research**: Automatically begins, creates GitHub issue with `phase:research` label
3. **Plan**: `/plan` - After research approval, creates detailed plan
4. **Implement**: `/implement` - After plan approval, executes plan exactly
5. **Complete**: `/complete` - Mark phase done, move to next

## Core Principles

### Research -> Plan -> Implement

Every task follows this mandatory sequence:
- **Research**: Verify ground truth, never guess
- **Plan**: Detailed steps with file:line references, NO CODE until approved
- **Implement**: Follow the plan exactly, commit within phases

### vibe-coding (Always Active)

Simplicity-first coding philosophy:
- **10 lines > 20 lines** - Prefer simpler code
- **Working > Perfect** - Don't fix what isn't broken
- **Delete > Add** - Optimize by removing
- **One File First** - Extend existing files before creating new ones

See `rules/vibe-coding.md` for full philosophy.

### frontend-design (UI Work Only)

Activates for UI/frontend work - avoids generic AI aesthetics:
- Choose **bold aesthetic direction** (brutalist, luxury, minimal, playful, etc.)
- Avoid AI clichés: Inter/Space Grotesk fonts, purple gradients, generic layouts
- **Code complexity matches design**: Minimal design = simple code, Elaborate design = elaborate code OK

See `rules/frontend-design.md` for full guidelines.

### Context Hygiene ("Avoid the Dumb Zone")

- Warns at 60% context usage
- Strongly suggests "Chat Nuke" at 80%
- Tracks consecutive failed bug fix attempts (warns at 3+)

### Critical Thinking

- No blind compliance - challenge bad plans
- List missing requirements before starting
- Lead Engineer mindset: consider performance, security, maintainability

## Configuration

### Hooks

The plugin uses hooks to:
- Auto-log errors to `docs/lessons-learned.md`
- Monitor context usage
- Track bug fix attempts

### GitHub Labels

Create these labels in your repo for best experience:
- `phase:research`
- `phase:plan`
- `phase:implement`

## Rules

The plugin includes two rule files that guide behavior:

- **`rules/vibe-coding.md`**: Always-active simplicity-first philosophy
- **`rules/frontend-design.md`**: UI-specific creative direction (activates for UI work)
- **`rules/coding-workflow.md`**: Phased workflow enforcement

See individual rule files for complete guidance.

## Requirements

- GitHub CLI (`gh`) - for issue creation
- Git - for version control
- jq - for JSON parsing in scripts

## License

MIT
