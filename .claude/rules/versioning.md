# Versioning Rules

_Loaded when pushing changes_

## Version Bump Required

**Before any `git push`:**

1. Determine version type:
   - Patch (x.x.X): Bug fixes, small changes
   - Minor (x.X.0): New features
   - Major (X.0.0): Breaking changes

2. Update ALL version locations:
   - `coding-plugin/.claude-plugin/plugin.json` (source of truth)
   - `README.md` (root) - title
   - `.claude-plugin/marketplace.json` (metadata.version)

3. Commit format: `🔖 v1.2.3: description`
