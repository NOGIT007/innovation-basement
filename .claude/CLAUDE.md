# Project: innovation-basement

**Repo:** https://github.com/NOGIT007/innovation-basement

## Structure
- `coding-plugin/` - Main Claude Code plugin
- `.claude-plugin/` - Plugin configuration
- `claude-files/` - Example user config (for learning)

## Versioning

Bump version on every push:
- Patch (x.x.X): Bug fixes, small changes
- Minor (x.X.0): New features
- Major (X.0.0): Breaking changes

Include version in commit message: `v1.2.3: feature description`

**Source of truth:** `coding-plugin/.claude-plugin/plugin.json`

**ALWAYS update ALL version locations on every version bump:**
1. `coding-plugin/.claude-plugin/plugin.json` - Claude Code reads this
2. `README.md` (root) - title
3. `coding-plugin/rules/coding-workflow.md` (frontmatter)
4. `.claude-plugin/marketplace.json` (metadata.version)
