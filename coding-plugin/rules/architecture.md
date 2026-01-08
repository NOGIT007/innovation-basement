---
name: architecture
generated: 2025-01-08
---

## Structure

coding-plugin/
├── agents/            # Specialized agents: planner, implementer, reviewer
├── commands/          # /code:plan-issue, implement, handover, lessons, etc.
├── rules/             # vibe-coding, frontend-design, coding-workflow
├── scripts/           # log-error, check-context, verify-gate, pre-compact, session-end
├── hooks/hooks.json   # PostToolUse, Stop, SessionEnd, SubagentStop, PreCompact
└── templates/         # lessons-learned.md

## Agents

| Agent | Responsibility | Key Feature |
|-------|---------------|-------------|
| `planner.md` | LSP research, phase creation | File:line precision |
| `implementer.md` | Code execution | **Hard verification gate** |
| `reviewer.md` | Code quality review | Pattern checking |

## Hooks

| Hook | Trigger | Script |
|------|---------|--------|
| PostToolUse | After Bash | log-error.sh |
| Stop | Session pause | check-context.sh |
| SessionEnd | Session ends | session-end.sh |
| SubagentStop | Agent completes | verify-gate.sh |
| PreCompact | Before compaction | pre-compact.sh |

## Commit Conventions

| Emoji | Type |
|-------|------|
| ✨ | Feature |
| 🐛 | Bug fix |
| ♻️ | Refactor |
| 📝 | Docs |
| 🧪 | Tests |

## Workflow

/code:plan-issue → GitHub Issue → /code:implement → /code:handover
                                        ↓
                              [Implementer Agent]
                                        ↓
                              HARD VERIFICATION GATE
                                        ↓
                              Tests pass → Mark [x]
