# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.10.0] - 2026-02-17

### Added

- **Agent Teams support** in `/code:implement` — experimental alternative execution mode where
  the main session leads a team of independent Claude Code sessions instead of using the
  orchestrator/implementer subagent pattern. Each teammate is a full Claude session that claims
  tasks from the shared TaskList, implements them, runs verification, and commits independently.
  Teammates can communicate with each other directly, enabling cross-layer coordination.

- **`--team` / `--no-team` flags** for `/code:implement` to override auto-detection:
  - `--team` forces Agent Teams mode (requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
  - `--no-team` forces the proven subagent orchestrator mode
  - Without flags: auto-detects based on task count and independence ratio

- **Auto-detection heuristic** that analyzes TaskList to choose execution mode:
  - Uses team mode when 4+ tasks exist with 60%+ having no blockers (high independence)
  - Falls back to subagent mode for sequential/dependent task chains or small task counts
  - Only activates when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set

- **`TeammateIdle` hook** (`teammate-idle.sh`) — guides idle teammates to pick up the next
  available task from TaskList instead of stopping. Uses exit code 2 to send feedback.

- **`TaskCompleted` hook** (`team-task-complete.sh`) — verification gate for team mode that
  runs detected test command before accepting task completion. Uses exit code 2 to reject
  completion when tests fail (same pattern as `verify-gate.sh` for subagent mode).

- **Agent Teams setup guide** in README with prerequisites, configuration, and usage examples

### Changed

- `/code:implement` now accepts optional `--team` / `--no-team` flags alongside issue number
- `/code:implement` frontmatter adds `TaskGet, TaskUpdate` to allowed-tools for lead monitoring
- Updated architecture diagram in README to show both execution paths
- Updated `coding-plugin/CLAUDE.md` with execution modes table and new hooks

## [2.9.0] - 2026-02-15

### Fixed

- `verify-gate.sh` now actually runs detected test command and exits non-zero on failure (was a no-op)
- `session-end.sh` and `pre-compact.sh` — removed dead `/handover` references (command removed in v2.7.0)
- `check-context.sh` — removed reference to non-existent `/workflow status` command

### Changed

- Consolidated `settings-audit` + `init-deployment` into single `/code:setup` command (12 → 11 commands)
- `/code:setup` detects any project stack (Bun, npm, Python, Rust, Go) and generates both settings and deployment scripts

### Removed

- `settings-audit` command (merged into `/code:setup`)
- `init-deployment` command (merged into `/code:setup`)

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

[2.10.0]: https://github.com/NOGIT007/innovation-basement/compare/v2.9.0...HEAD
[2.9.0]: https://github.com/NOGIT007/innovation-basement/compare/e855fbb...v2.9.0
[2.8.0]: https://github.com/NOGIT007/innovation-basement/compare/3dd7f52...59444a2
[2.7.0]: https://github.com/NOGIT007/innovation-basement/compare/e5a45d6...3dd7f52
[2.6.1]: https://github.com/NOGIT007/innovation-basement/compare/57d9a32...e5a45d6
