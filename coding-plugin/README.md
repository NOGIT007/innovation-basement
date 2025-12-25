# coding-plugin

Simple, phased coding workflow for Claude Code. Part of the innovation-basement marketplace.

## Installation

```bash
/plugin marketplace add NOGIT007/innovation-basement
/plugin install coding-plugin@innovation-basement
```

## Workflow

```
/code:plan-issue → /code:implement → /code:handover
     ↓                   ↓                ↓
  GitHub Issue    Work phases      Next session
```

### Commands

| Command | Description |
|---------|-------------|
| `/code:plan-issue <feature>` | Research codebase, plan phases, create GitHub issue |
| `/code:implement #<number>` | Implement from GitHub issue, work through phases |
| `/code:handover` | Generate handover for next session |

## Usage

### 1. Plan Feature

```bash
/code:plan-issue add user authentication
```

Creates GitHub issue with:
- Goal
- Implementation phases
- Checkboxes for each task

### 2. Implement

```bash
/code:implement #123
```

- Reads issue phases
- Works through unchecked tasks
- Updates checkboxes on completion
- Commits changes

### 3. Session Handover

When ending a session:

```bash
/code:handover
```

Generates concise handover text for next session.

### 4. Continue Next Session

Start new session, paste handover, then:

```bash
/code:implement #123
```

Picks up where you left off (reads checkboxes).

## Rules

The plugin includes coding rules:

- **vibe-coding**: Simplicity-first philosophy (always active)
- **frontend-design**: Avoid generic AI aesthetics (UI work)
- **coding-workflow**: Phase discipline

## Requirements

- GitHub CLI (`gh`)
- Git

## License

MIT
