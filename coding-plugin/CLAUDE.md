# Coding Plugin

🏗️ = Architecture updated after commit

## Architecture

```
coding-plugin/
├── agents/        # orchestrator, implementer
├── commands/      # plan-issue, implement, finalizer, cleanup, etc.
├── hooks/         # Stop, SessionEnd, SubagentStop, PreCompact, TeammateIdle, TaskCompleted
└── scripts/       # check-context, verify-gate, session-end, pre-compact, teammate-idle, team-task-complete
```

## Task Storage

Tasks use Claude Code's **native Task tools**:

- **TaskCreate** - Create tasks with metadata.issueNumber
- **TaskList** - List all tasks, filter by issueNumber
- **TaskUpdate** - Update status (pending → in_progress → completed)

View tasks with `ctrl+t` in Claude Code terminal.

## Execution Modes

`/code:implement` supports two execution modes:

| Mode                | Trigger             | Flow                                    | Token Cost |
| ------------------- | ------------------- | --------------------------------------- | ---------- |
| Subagent (default)  | Auto or `--no-team` | implement → orchestrator → implementers | Lower      |
| Team (experimental) | Auto or `--team`    | implement = lead → teammates            | Higher     |

Team mode requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json env.
Auto-detection uses team mode when 4+ tasks exist with 60%+ having no blockers.

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

| Hook          | Trigger                    | Script                |
| ------------- | -------------------------- | --------------------- |
| Stop          | Session pause              | check-context.sh      |
| SessionEnd    | Session ends               | session-end.sh        |
| SubagentStop  | Agent done                 | verify-gate.sh        |
| PreCompact    | Before compaction          | pre-compact.sh        |
| TeammateIdle  | Teammate idle (team mode)  | teammate-idle.sh      |
| TaskCompleted | Task completed (team mode) | team-task-complete.sh |

## File Conventions

- `.handover.md` - Session state (gitignored, overwritten)
- Auto-memory at `~/.claude/projects/*/memory/` - Persistent learnings
- Commands in `commands/` - One file per command
