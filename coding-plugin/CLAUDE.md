# Coding Plugin

See [rules/architecture.md](rules/architecture.md) for structure.

🏗️ = Architecture updated after commit

## Project Memory

### Documentation Updates (ALWAYS)

When modifying commands or workflow:
1. Update `rules/coding-workflow.md` - version + workflow changes
2. Update `README.md` - version, what's new, commands table
3. Update `.claude-plugin/plugin.json` - version bump
4. Commit all docs together

### File Conventions

- `.handover.md` - Session state file (gitignored, overwritten)
- `LESSONS.md` - Learning from commits (project root)
- Commands in `commands/` - One file per command
