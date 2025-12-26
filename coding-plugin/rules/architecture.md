---
name: architecture
generated: 2025-12-26
---

## Structure

coding-plugin/
├── commands/          # /code:plan-issue, implement, handover
├── rules/             # vibe-coding, frontend-design, coding-workflow
├── scripts/           # log-error, check-context, update-architecture
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
