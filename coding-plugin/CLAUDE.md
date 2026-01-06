# Coding Plugin

See [rules/architecture.md](rules/architecture.md) for structure.

🏗️ = Architecture updated after commit

## Project Memory

### Documentation Updates (ALWAYS - DO NOT SKIP)

**Any change to workflow, commands, or features requires ALL of these:**

1. `.claude-plugin/plugin.json` - bump version (source of truth)
2. `rules/coding-workflow.md` - update frontmatter version
3. `README.md`:
   - Update title version
   - Add "What's New in vX.X" section if new feature
   - Update commands table if commands changed

**Version bumps:**
- Patch (x.x.X): Bug fixes, docs-only changes
- Minor (x.X.0): New features, workflow additions
- Major (X.0.0): Breaking changes

Commit all version updates together with the feature.

### File Conventions

- `.handover.md` - Session state file (gitignored, overwritten)
- `LESSONS.md` - Learning from commits (project root)
- Commands in `commands/` - One file per command
