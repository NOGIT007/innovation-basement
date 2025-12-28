# Project: innovation-basement

**Repo:** https://github.com/NOGIT007/innovation-basement

## Structure
- `coding-plugin/` - Main Claude Code plugin
- `workbench-plugin/` - Secondary plugin
- `.claude-plugin/` - Plugin configuration

## Versioning

Bump version on every push:
- Patch (x.x.X): Bug fixes, small changes
- Minor (x.X.0): New features
- Major (X.0.0): Breaking changes

Include version in commit message: `✨ v2.8.0: feature description`

**Source of truth:** `coding-plugin/.claude-plugin/plugin.json`

Update ALL version locations:
1. `coding-plugin/.claude-plugin/plugin.json` ← Claude Code reads this
2. `coding-plugin/README.md` (title)
3. `coding-plugin/rules/coding-workflow.md` (frontmatter)
