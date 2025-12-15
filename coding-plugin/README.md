# coding-plugin

Structured coding workflow plugin for Claude Code. Part of the innovation-basement marketplace.

## Features

- **Phased Workflow**: Research -> Plan -> Implement
- **GitHub Integration**: Auto-create issues for each phase
- **Context Hygiene**: Warnings at 60%/80% context usage
- **Bug Fix Tracking**: Warn after 3+ failed attempts
- **Auto Error Logging**: Build institutional knowledge
- **Sub-agents**: Research and documentation specialists

## Installation

```bash
/plugin marketplace add NOGIT007/innovation-basement
/plugin install coding-plugin@innovation-basement
```

## Commands

### Phase Commands
- `/phase research <topic>` - Start research phase
- `/phase plan <feature>` - Start planning phase
- `/phase implement <feature>` - Start implementation phase

### Workflow Commands
- `/workflow start <project>` - Initialize new workflow
- `/workflow status` - Check current status
- `/workflow complete` - Mark phase complete
- `/workflow nuke` - Generate summary for fresh chat

## Workflow

1. **Start**: `/workflow start "Add user authentication"`
2. **Research**: Automatically begins research phase, creates GitHub issue
3. **Plan**: After research approval, create detailed implementation plan
4. **Implement**: After plan approval, execute the plan exactly

## Core Principles

### Research -> Plan -> Implement

Every task follows this mandatory sequence:
- **Research**: Verify ground truth, never guess
- **Plan**: Detailed steps with file:line references, NO CODE until approved
- **Implement**: Follow the plan exactly, commit within phases

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

## Sub-agents

- **research-agent**: Technical research and verification
- **doc-agent**: Documentation creation and updates

## Requirements

- GitHub CLI (`gh`) - for issue creation
- Git - for version control
- jq - for JSON parsing in scripts

## License

MIT
