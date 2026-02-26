# Coding Plugin

## Architecture

```
coding-plugin/
├── agents/        # orchestrator, implementer
├── commands/      # plan-issue, implement, finalizer, cleanup, etc.
├── hooks/         # Stop, SessionEnd, SubagentStop, PreCompact, TeammateIdle, TaskCompleted, ConfigChange
└── scripts/       # check-context, verify-gate, session-end, pre-compact, teammate-idle, team-task-complete, config-validate
```

## Base Settings

The plugin ships default settings via `coding-plugin/.claude-plugin/settings.json`:

- `plansDirectory: "plans"` — store plans in plans/ folder
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "70"` — auto-compact at 70% context
- `Bash(git:*)`, `Bash(gh:*)` — git and GitHub CLI permissions
- Custom spinner tips for plugin workflow guidance

Users only need to add project-specific settings (like `CLAUDE_CODE_TASK_LIST_ID`) to their `.claude/settings.json`.

## Task Storage

Tasks use Claude Code's **native Task tools**:

- **TaskCreate** - Create tasks with metadata.issueNumber
- **TaskList** - List all tasks, filter by issueNumber
- **TaskUpdate** - Update status (pending → in_progress → completed)

View tasks with `ctrl+t` in Claude Code terminal.

## Execution Modes

`/code:implement` supports two execution modes:

| Mode                | Trigger             | Flow                                    |
| ------------------- | ------------------- | --------------------------------------- |
| Subagent (default)  | Auto or `--no-team` | implement → orchestrator → implementers |
| Team (experimental) | Auto or `--team`    | implement = lead → teammates            |

Team mode requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json env.
Auto-detection uses team mode when 4+ tasks exist with 60%+ having no blockers.

**Worktree isolation:** Implementers run in separate git worktrees (`isolation: worktree`), preventing file conflicts during parallel execution.

## Required Environment

Project `.claude/settings.json` (only project-specific settings needed):

```json
{
  "env": {
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
| ConfigChange  | Settings modified          | config-validate.sh    |

## File Conventions

- `.handover.md` - Session state (gitignored, overwritten)
- Auto-memory at `~/.claude/projects/*/memory/` - Persistent learnings
- Commands in `commands/` - One file per command
