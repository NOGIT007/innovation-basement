---
name: architecture
generated: 2025-12-26
---

## Structure

coding-plugin/
├── commands/          # /code:plan-issue, implement, handover, lessons
├── rules/             # vibe-coding, frontend-design, coding-workflow
├── scripts/           # log-error, check-context
├── hooks/hooks.json   # PostToolUse, Stop hooks
└── templates/         # lessons-learned.md

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
