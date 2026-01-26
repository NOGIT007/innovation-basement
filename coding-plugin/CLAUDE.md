# Coding Plugin

🏗️ = Architecture updated after commit

## Architecture

```
coding-plugin/
├── agents/        # orchestrator, implementer
├── commands/      # plan-issue, implement, finalizer, lessons, etc.
├── hooks/         # PostToolUse, Stop, SessionEnd, SubagentStop, PreCompact
├── scripts/       # log-error, check-context, verify-gate, etc.
└── templates/     # lessons-learned, rules/
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
| PostToolUse  | After Bash        | log-error.sh     |
| Stop         | Session pause     | check-context.sh |
| SessionEnd   | Session ends      | session-end.sh   |
| SubagentStop | Agent done        | verify-gate.sh   |
| PreCompact   | Before compaction | pre-compact.sh   |

## File Conventions

- `.handover.md` - Session state (gitignored, overwritten)
- `LESSONS.md` - Learning from commits (project root)
- Commands in `commands/` - One file per command
