# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.12.0] - 2026-02-20

### Added

- **Auto-close tmux teammates** — when teammates finish all tasks and go idle, the `TeammateIdle`
  hook now instructs them to `/exit` their session instead of just notifying the lead. This
  automatically closes tmux panes without manual cleanup.

- **Tmux pane cleanup safety net** — after all tasks complete in team mode, the lead waits 10
  seconds for graceful exits, then force-kills any remaining tmux panes (preserving the lead pane).
  Guarded by `$TMUX` check so it's a no-op in in-process mode.

- **`Bash(tmux:*)` permission** for `/code:implement` — enables the lead to run tmux cleanup
  commands after team completion.

- **LSP MCP server prerequisites** — README and Getting Started guide now recommend installing
  `typescript-lsp` and `python-lsp` MCP servers for LSP-powered codebase research in
  `/code:plan-issue`.

## [2.11.0] - 2026-02-20

### Added

- **Default `settings.json` ships with plugin** — zero-config onboarding. New users get
  `plansDirectory`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, git/gh permissions, and custom spinner
  tips automatically. Only project-specific settings (like `CLAUDE_CODE_TASK_LIST_ID`) need
  to be added manually.

- **Custom spinner tips** — plugin-specific tips shown during loading (e.g., "Press ctrl+t
  to view task progress", "Use --team flag for Agent Swarm mode").

- **Worktree isolation for implementers** — each implementer agent runs in its own git worktree
  (`isolation: worktree`), preventing file conflicts when multiple tasks execute in parallel.
  Orchestrator handles merge-back conflicts by marking tasks as BLOCKED.

- **Background orchestrator** — orchestrator agent uses `background: true` frontmatter, running
  explicitly as a background task.

- **`last_assistant_message` parsing in hooks** — `verify-gate.sh` and `team-task-complete.sh`
  now read hook input from stdin. When an implementer/teammate reports BLOCKED, tests are
  skipped instead of running unnecessarily.

- **`ConfigChange` hook** — validates `.claude/settings.json` when modified mid-session. Warns
  if `plansDirectory` or `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` are missing.

- **`/code:plan-issue #<number>` accepts existing GitHub issues** — instead of always creating
  a new issue, you can now pass `#33` to fetch an existing issue's body + comments, create
  native tasks from the investigation findings, and update the issue in-place. This bridges
  GitHub's `@claude` agent mode findings with `/code:implement` — run
  `/code:plan-issue #33` then `/code:implement #33` without losing context. Mixed usage
  supported: `/code:plan-issue #33 focus on storage` adds extra context alongside the issue.

- **Agent Swarm documentation** — comprehensive README section covering: what it is, how it
  works, display modes, tmux setup, keyboard shortcuts, agent interaction, quality gates,
  token usage, and limitations.

- **Task Workflow documentation** — new README section explaining task lifecycle, creation,
  execution, dependencies, and verification gates.

### Changed

- Renamed "Agent Teams" → "Agent Swarm" throughout README for consistent branding
- README Required Configuration split into "Base Settings (ships with plugin)" and
  "Project-Specific Settings (you add)"
- Architecture diagram updated to show worktree isolation and background orchestrator
- `coding-plugin/CLAUDE.md` updated with base settings info, ConfigChange hook, and
  worktree isolation note
- `/code:implement` Done section notes worktree isolation behavior

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

[2.12.0]: https://github.com/NOGIT007/innovation-basement/compare/v2.11.0...HEAD
[2.11.0]: https://github.com/NOGIT007/innovation-basement/compare/v2.10.0...v2.11.0
[2.10.0]: https://github.com/NOGIT007/innovation-basement/compare/v2.9.0...v2.10.0
[2.9.0]: https://github.com/NOGIT007/innovation-basement/compare/e855fbb...v2.9.0
[2.8.0]: https://github.com/NOGIT007/innovation-basement/compare/3dd7f52...59444a2
[2.7.0]: https://github.com/NOGIT007/innovation-basement/compare/e5a45d6...3dd7f52
[2.6.1]: https://github.com/NOGIT007/innovation-basement/compare/57d9a32...e5a45d6
