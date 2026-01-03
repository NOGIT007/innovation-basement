# coding-plugin v3.3.0

Simple, phased coding workflow for Claude Code. Part of the innovation-basement marketplace.

## Recommended Plugins

Install from `claude-plugins-official` marketplace to enhance the workflow:

| Plugin | Purpose |
|--------|---------|
| `typescript-lsp` | LSP-precise code analysis for TypeScript |
| `pyright-lsp` | LSP-precise code analysis for Python |
| `frontend-design` | Create distinctive, production-grade frontend interfaces |

```bash
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
```

## Tip: Use /plan mode

Claude Code's built-in `/plan` mode can be used to explore and design changes before running `/code:plan-issue`.

## What's New in v3.0

- **Focused on coding** - Removed workbench-plugin, single-purpose workflow
- **Smart handover** - `/code:handover` now auto-detects issue from branch/context and parses phases

## v2.9 Features

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

## Workflow Overview

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

---

## Command Flow Detail

```
                                    USER HAS VAGUE IDEA
                                           │
                                           ▼
                              ┌────────────────────────┐
                              │    idea.md (rough)     │
                              │                        │
                              │  "I want auth system"  │
                              └────────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────┐
                    │         /code:interview idea.md          │
                    ├──────────────────────────────────────────┤
                    │                                          │
                    │  ┌─────────────────────────────────────┐ │
                    │  │      AskUserQuestion Loop           │ │
                    │  │                                     │ │
                    │  │  Category 1: Core Vision            │ │
                    │  │    ├─ What problem?                 │ │
                    │  │    ├─ Who is user?                  │ │
                    │  │    └─ Success metric?               │ │
                    │  │                                     │ │
                    │  │  Category 2: User Experience        │ │
                    │  │    ├─ Primary flow?                 │ │
                    │  │    └─ Error handling?               │ │
                    │  │                                     │ │
                    │  │  Category 3: Technical Boundaries   │ │
                    │  │    ├─ Out of scope?                 │ │
                    │  │    └─ Constraints?                  │ │
                    │  │                                     │ │
                    │  │  Category 4: Risks & Tradeoffs      │ │
                    │  │  Category 5: Dependencies           │ │
                    │  │  Category 6: Verification           │ │
                    │  └─────────────────────────────────────┘ │
                    │                                          │
                    └──────────────────────────────────────────┘
                                           │
                                           ▼
                              ┌────────────────────────┐
                              │   idea-spec.md (rich)  │
                              │                        │
                              │  - Vision              │
                              │  - Success Criteria    │
                              │  - User Stories        │
                              │  - Technical Scope     │
                              │  - Risks               │
                              │  - Verification Plan   │
                              └────────────────────────┘
                                           │
                           ┌───────────────┴───────────────┐
                           │                               │
                           ▼                               ▼
              ┌────────────────────────┐      ┌────────────────────────┐
              │   /code:constitution   │      │    /code:plan-issue    │
              │      (optional)        │      │                        │
              └────────────────────────┘      └────────────────────────┘
                           │                               │
                           ▼                               │
              ┌────────────────────────┐                   │
              │    constitution.md     │───────────────────┤ (auto-read)
              │                        │                   │
              │  - Core Principles     │                   │
              │  - Boundaries          │                   │
              │  - Decision Framework  │                   │
              │  - Non-Negotiables     │                   │
              └────────────────────────┘                   │
                                                           │
              ┌────────────────────────┐                   │
              │      LESSONS.md        │───────────────────┤ (auto-read)
              │                        │                   │
              │  - Patterns            │                   │
              │  - Mistakes to avoid   │                   │
              └────────────────────────┘                   │
                           ▲                               │
                           │ (updated by /lessons)        │
                           │                               ▼
                           │                  ┌────────────────────────┐
                           │                  │   GitHub Issue #123    │
                           │                  │                        │
                           │                  │  - Goal                │
                           │                  │  - Context (from files)│
                           │                  │  - Implementation      │
                           │                  │    Phases              │
                           │                  └────────────────────────┘
                           │                               │
                           │                               ▼
                           │                  ┌────────────────────────┐
                           │                  │  /code:implement #123  │
                           │                  │                        │
                           │                  │  Work through phases   │
                           │                  └────────────────────────┘
                           │                               │
                           │                               ▼
                           │                        ┌─────────────┐
                           └────────────────────────│   Commits   │
                                                    └─────────────┘
```

---

## File Relationships

```
PROJECT ROOT
│
├── idea.md                    ◄── Input: Your rough idea
│
├── idea-spec.md               ◄── Output: /interview (comprehensive spec)
│
├── constitution.md            ◄── Output: /constitution (project principles)
│                                  Read by: /plan-issue
│
├── LESSONS.md                 ◄── Output: /lessons (learned patterns)
│                                  Read by: /plan-issue
│                                  Updated after commits
│
├── handover.md                ◄── Output: /handover (session state, gitignored)
│                                  Read by: /resume
│
└── GitHub Issue #123          ◄── Output: /plan-issue
                                   Read by: /implement #123
```

---

## Interview Question Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    /code:interview <spec>                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Read spec file                                         │
│  ─────────────────────                                          │
│  • Parse existing content                                       │
│  • Identify what's already defined (skip these)                 │
│  • Identify gaps (focus here)                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Interview (AskUserQuestion with multi-choice)          │
│  ─────────────────────────────────────────────────────          │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   VISION    │  │     UX      │  │  TECHNICAL  │              │
│  │             │  │             │  │             │              │
│  │ • Problem?  │  │ • Flow?     │  │ • Scope?    │              │
│  │ • Users?    │  │ • Errors?   │  │ • Platform? │              │
│  │ • Success?  │  │ • MVP?      │  │ • Perf?     │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │                │                │                      │
│         ▼                ▼                ▼                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │    RISKS    │  │    DEPS     │  │   VERIFY    │              │
│  │             │  │             │  │             │              │
│  │ • Biggest?  │  │ • Prereqs?  │  │ • Done?     │              │
│  │ • Tradeoffs?│  │ • External? │  │ • Demo?     │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                  │
│  15-25 questions total, skip what's already in spec             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Write <spec>-spec.md                                   │
│  ────────────────────────────                                   │
│  Comprehensive spec with all insights                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Constitution Question Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      /code:constitution                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Check if constitution.md exists                        │
│  ───────────────────────────────────────                        │
│  • If exists: Ask "Overwrite?" (Yes/No)                         │
│  • If no: abort                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Interview (AskUserQuestion with multi-choice)          │
│  ─────────────────────────────────────────────────────          │
│                                                                  │
│  ┌──────────────────────┐    ┌──────────────────────┐           │
│  │     CORE VALUES      │    │      BOUNDARIES      │           │
│  │                      │    │                      │           │
│  │ • What matters most? │    │ • In scope?          │           │
│  │   □ Simplicity       │    │ • Out of scope?      │           │
│  │   □ Correctness      │    │                      │           │
│  │   □ User experience  │    │                      │           │
│  │   □ Stability        │    │                      │           │
│  └──────────────────────┘    └──────────────────────┘           │
│              │                          │                        │
│              ▼                          ▼                        │
│  ┌──────────────────────┐    ┌──────────────────────┐           │
│  │      PRIORITIES      │    │   NON-NEGOTIABLES    │           │
│  │                      │    │                      │           │
│  │ When tradeoffs:      │    │ Rules that never     │           │
│  │ 1. First wins        │    │ bend:                │           │
│  │ 2. Second if equal   │    │ □ Tests must pass    │           │
│  │ 3. Tiebreaker        │    │ □ No breaking changes│           │
│  └──────────────────────┘    └──────────────────────┘           │
│                                                                  │
│  8-12 questions total                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Write constitution.md to project root                  │
│  ─────────────────────────────────────────────                  │
│  /plan-issue will auto-read this for context                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Complete Workflow Example

```
DAY 1: Ideation
══════════════════════════════════════════════════════════════════

  You have a rough idea...

  $ echo "I want to add user auth to my app" > ideas/auth.md

  $ /code:interview ideas/auth.md

  [Interview: 15-25 questions across 6 categories]

  Output: ideas/auth-spec.md (comprehensive 1.0 spec)


DAY 2: Principles (Optional)
══════════════════════════════════════════════════════════════════

  Define project principles once...

  $ /code:constitution

  [Interview: 8-12 questions across 4 categories]

  Output: constitution.md (project principles)


DAY 3: Planning
══════════════════════════════════════════════════════════════════

  Create actionable GitHub issue...

  $ /code:plan-issue add user authentication

  [Reads: LESSONS.md + constitution.md for context]
  [LSP research: file:line precision]

  Output: GitHub Issue #123 with implementation phases


DAY 4+: Implementation
══════════════════════════════════════════════════════════════════

  Work through phases...

  $ /code:implement #123

  [Work through phases, commit changes]

  $ /code:handover       # Save state if stopping
  $ /code:resume         # Continue later


ONGOING: Learning
══════════════════════════════════════════════════════════════════

  After commits, update lessons...

  $ /code:lessons

  [Analyzes recent commits]
  [Updates LESSONS.md with patterns/mistakes]

  Output: LESSONS.md (auto-read by future /plan-issue)
```

---

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
