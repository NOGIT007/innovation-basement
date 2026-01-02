# coding-plugin v2.9.0

Simple, phased coding workflow for Claude Code. Part of the innovation-basement marketplace.

## What's New in v2.9

- **Spec Interview** - `/code:interview <spec>` develops vague ideas into comprehensive 1.0 specs
- **Project Constitution** - `/code:constitution` creates project principles via interview
- **Plan-issue integration** - Auto-reads `constitution.md` for context

## v2.8 Features

- **Handover/Resume workflow** - `/code:handover [description]` saves to `handover.md`, `/code:resume` continues
- **Enhanced plan-issue** - Detailed code references, file tables, before/after snippets
- **Session persistence** - No copy/paste needed between sessions

## v2.6 Features

- **LSP-precise planning** - Uses typescript-lsp for exact file:line references
- **Lessons learning** - `/code:lessons` analyzes commits, maintains LESSONS.md
- **Senior→Junior handoff** - Issues detailed enough for any LLM to implement
- **Quality checklist** - Edge cases, security, backward compat built into planning

## Installation

```bash
/plugin marketplace add NOGIT007/innovation-basement
/plugin install coding-plugin@innovation-basement
```

## Workflow

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                              CODING PLUGIN WORKFLOW                                    │
├───────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   PHASE 1: IDEATION          PHASE 2: PLANNING           PHASE 3: EXECUTION           │
│                                                                                        │
│   ┌──────────────┐          ┌──────────────┐            ┌──────────────┐              │
│   │  /interview  │          │ /plan-issue  │            │  /implement  │              │
│   │              │          │              │            │    #123      │              │
│   │  Spec File   │───────▶  │   Creates    │─────────▶  │              │              │
│   │  Interview   │          │ GitHub Issue │  Issue #   │   Code It    │              │
│   └──────────────┘          └──────────────┘            └──────────────┘              │
│          │                         ▲                           │                       │
│          ▼                         │                           ▼                       │
│   ┌──────────────┐                 │                    ┌──────────────┐              │
│   │/constitution │                 │                    │  /handover   │              │
│   │              │─────────────────┤                    │              │              │
│   │   Project    │   (auto-reads)  │                    │ Save State   │              │
│   │  Principles  │                 │                    └──────────────┘              │
│   └──────────────┘                 │                           │                       │
│                                    │                           ▼                       │
│   ┌──────────────┐                 │                    ┌──────────────┐              │
│   │   /lessons   │─────────────────┘                    │   /resume    │              │
│   │              │   (auto-reads)                       │              │              │
│   │   Learned    │                                      │  Continue    │              │
│   │   Patterns   │                                      └──────────────┘              │
│   └──────────────┘                                                                     │
│         ▲                                                                              │
│         │ (run after commits)                                                          │
│         │                                                                              │
│   ┌─────┴────────┐                                                                     │
│   │  Commits     │                                                                     │
│   └──────────────┘                                                                     │
│                                                                                        │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

*Interview and constitution are optional. Plan-issue auto-reads constitution.md and LESSONS.md if they exist.*

### Commands

| Command | Description |
|---------|-------------|
| `/code:interview <spec>` | Interview to develop vague ideas into comprehensive specs |
| `/code:constitution` | Interview to create project principles (constitution.md) |
| `/code:plan-issue <feature>` | Research with LSP, plan phases, create GitHub issue |
| `/code:implement #<number>` | Implement from GitHub issue, work through phases |
| `/code:handover` | Save session state to `handover.md` |
| `/code:resume` | Continue from `handover.md` |
| `/code:lessons [N]` | Analyze last N commits, update LESSONS.md |

## Usage

### 1. Plan Feature

```bash
/code:plan-issue add user authentication
```

Creates GitHub issue with:
- Summary (what and why)
- Data flow (Entry → Transform → Exit with file:line)
- Changes table (File:Line | Current | New)
- Verification steps

### 2. Implement

```bash
/code:implement #123
```

- Reads issue phases
- Verifies plan still applies (Task Explore)
- Implements at file:line
- Updates checkboxes on completion
- Commits changes

### 3. Session Handover

```bash
/code:handover
```

Saves session state to `handover.md`:
- Issue and branch context
- Key files with status
- Resume instructions

### 4. Resume Work

```bash
/code:resume
```

Loads `handover.md` and continues exactly where you left off. File is deleted when task completes.

## Rules

| Rule | Purpose |
|------|---------|
| [architecture](rules/architecture.md) | Auto-generated codebase structure |
| [vibe-coding](rules/vibe-coding.md) | Simplicity-first philosophy |
| [frontend-design](rules/frontend-design.md) | Avoid generic AI aesthetics |
| [coding-workflow](rules/coding-workflow.md) | Phase discipline |

## Requirements

- GitHub CLI (`gh`)
- Git

## License

MIT
