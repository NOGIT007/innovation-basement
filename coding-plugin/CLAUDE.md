# Coding Plugin

🏗️ = Architecture updated after commit

## Architecture

```
coding-plugin/
├── agents/        # orchestrator, implementer
├── commands/      # plan-issue, implement, finalizer, lessons, etc.
├── hooks/         # PostToolUse, Stop, SessionEnd, SubagentStop, PreCompact
├── scripts/       # log-error, check-context, verify-gate, etc.
└── templates/     # lessons-learned
```

## Task Storage

Tasks are stored using Claude Code's **native Task tools**:

- **TaskCreate** - Create tasks with metadata.issueNumber
- **TaskList** - List all tasks, filter by issueNumber
- **TaskUpdate** - Update status (pending → in_progress → completed)
- **TaskGet** - Get full task details

View tasks with `ctrl+t` in Claude Code terminal.

## Required Environment

Project `.claude/settings.json`:

```json
{
  "plansDirectory": "plans",
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70",
    "CLAUDE_CODE_TASK_LIST_ID": "coding-plugin-tasks"
  }
}
```

| Setting                           | Purpose                                       |
| --------------------------------- | --------------------------------------------- |
| `plansDirectory`                  | Store plans in `plans/` folder                |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Auto-compact at 70% (agents never hit limits) |
| `CLAUDE_CODE_TASK_LIST_ID`        | Persist tasks across sessions                 |

| Hook         | Trigger           | Script           |
| ------------ | ----------------- | ---------------- |
| PostToolUse  | After Bash        | log-error.sh     |
| Stop         | Session pause     | check-context.sh |
| SessionEnd   | Session ends      | session-end.sh   |
| SubagentStop | Agent done        | verify-gate.sh   |
| PreCompact   | Before compaction | pre-compact.sh   |

## Project Memory

### Documentation Updates (ALWAYS - DO NOT SKIP)

**Any change to workflow, commands, or features requires ALL of these:**

1. `.claude-plugin/plugin.json` - bump version (source of truth)
2. `README.md` (in coding-plugin/):
   - Update title version
   - Add "What's New in vX.X" section if new feature
   - Update commands table if commands changed
3. `README.md` (root) - update title version

**Version bumps:**

- Patch (x.x.X): Bug fixes, docs-only changes
- Minor (x.X.0): New features, workflow additions
- Major (X.0.0): Breaking changes

Commit all version updates together with the feature.

### File Conventions

- `.handover.md` - Session state file (gitignored, overwritten)
- `LESSONS.md` - Learning from commits (project root)
- Commands in `commands/` - One file per command
