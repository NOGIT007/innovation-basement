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
   - `CHANGELOG.md` (root) - add new version entry at top

3. CHANGELOG entry format:
   - Add `## [X.Y.Z] - YYYY-MM-DD` section below the header
   - Use subsections: `### Added` / `### Changed` / `### Removed` / `### Fixed` (only relevant ones)
   - Write descriptive bullets (what changed and why)
   - Update compare link at bottom of file

4. Commit format: `🔖 v1.2.3: description`
