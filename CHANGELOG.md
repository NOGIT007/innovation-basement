# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.8.0] - 2026-02-14

### Added

- Task quality gate in implementer agent — tasks must pass a self-review before being marked complete
- Structured debugging workflow in implementer agent for systematic issue resolution
- Smarter BLOCKED recovery in orchestrator — automatically retries with adjusted approach

### Changed

- Enhanced plan-issue command with deeper codebase analysis and more detailed issue output

## [2.7.0] - 2026-02-06

### Changed

- Migrated from manual lessons-learned workflow to Claude Code auto-memory
- Simplified cleanup command to focus on progressive disclosure refactoring
- Streamlined plan-issue command (reduced redundant steps)
- Trimmed README to essential quick-start content

### Removed

- `interview` command (replaced by plan-issue's built-in clarification)
- `lessons` command and lessons-learned template (replaced by auto-memory)
- `quick-tasks` and `run-tasks` commands (merged into orchestrator agent)
- Error-logging hook and `log-error.sh` script

## [2.6.1] - 2026-02-02

### Added

- `quick-tasks` command for rapid multi-task execution without GitHub issues
- `run-tasks` command for executing task lists from existing plans
- Fast-path diagram in README showing when to use quick-tasks vs plan-issue

### Fixed

- `quick-tasks.md` frontmatter (added missing `context: fork`)

### Changed

- Expanded orchestrator agent with improved task delegation and status tracking

[2.8.0]: https://github.com/NOGIT007/innovation-basement/compare/3dd7f52...59444a2
[2.7.0]: https://github.com/NOGIT007/innovation-basement/compare/e5a45d6...3dd7f52
[2.6.1]: https://github.com/NOGIT007/innovation-basement/compare/57d9a32...e5a45d6
