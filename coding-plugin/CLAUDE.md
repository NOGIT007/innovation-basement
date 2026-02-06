# Coding Plugin

🏗️ = Architecture updated after commit

## Architecture

```
coding-plugin/
├── agents/        # orchestrator, implementer
├── commands/      # plan-issue, implement, finalizer, cleanup, etc.
├── hooks/         # Stop, SessionEnd, SubagentStop, PreCompact
└── scripts/       # check-context, verify-gate, session-end, pre-compact
```

## Task Storage

Tasks use Claude Code's **native Task tools**:

- **TaskCreate** - Create tasks with metadata.issueNumber
- **TaskList** - List all tasks, filter by issueNumber
- **TaskUpdate** - Update status (pending → in_progress → completed)

View tasks with `ctrl+t` in Claude Code terminal.

## Required Environment

Project `.claude/settings.json`:

```json
{
  "plansDirectory": "plans",
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70",
    "CLAUDE_CODE_TASK_LIST_ID": "<your-project-name>-tasks"
  }
}
```

## Hooks

| Hook         | Trigger           | Script           |
| ------------ | ----------------- | ---------------- |
| Stop         | Session pause     | check-context.sh |
| SessionEnd   | Session ends      | session-end.sh   |
| SubagentStop | Agent done        | verify-gate.sh   |
| PreCompact   | Before compaction | pre-compact.sh   |

## File Conventions

- `.handover.md` - Session state (gitignored, overwritten)
- Auto-memory at `~/.claude/projects/*/memory/` - Persistent learnings
- Commands in `commands/` - One file per command
