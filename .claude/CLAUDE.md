# Project: innovation-basement

**Repo:** https://github.com/NOGIT007/innovation-basement

## Structure

- `coding-plugin/` - Main Claude Code plugin
- `.claude-plugin/` - Plugin configuration
- `claude-files/` - Example user config (for learning)

## Versioning

**⛔ CANNOT push without version bump.** Before any `git push`:

1. Determine version type:
   - Patch (x.x.X): Bug fixes, small changes
   - Minor (x.X.0): New features
   - Major (X.0.0): Breaking changes

2. Update ALL version locations:
   - `coding-plugin/.claude-plugin/plugin.json` (source of truth)
   - `README.md` (root) - title
   - `.claude-plugin/marketplace.json` (metadata.version)

3. Include version in commit: `🔖 v1.2.3: description`
