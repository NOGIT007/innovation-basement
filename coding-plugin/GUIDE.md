# Coding Plugin User Guide v2.0.1

Simple workflow: **Plan → Implement → Finalize** (fully autonomous)

## Quick Start

```bash
# 1. Plan a feature (creates GitHub issue + task manifest)
/code:plan-issue add dark mode toggle

# 2. Implement - orchestrator runs all tasks autonomously
/code:implement #42

# 3. Finalize - merge or create PR
/code:finalizer --pr   # Create PR for review
/code:finalizer        # Merge directly to main
```

**That's it!** The orchestrator handles everything:

- Spawns implementer per task (isolated context)
- Auto-compact at 55% → continues seamlessly
- Commits after each task
- Updates GitHub issue status
- Runs simplify automatically
- No manual handover needed

## What's New in v2.0.0

| Feature      | Before (v1.x)             | Now (v2.0)                  |
| ------------ | ------------------------- | --------------------------- |
| Architecture | Commands control tasks    | Tasks control agents        |
| Context      | Manual handover           | Auto-compact at 55%         |
| Resume       | `/handover` → `/continue` | Just run `/implement` again |
| State        | GitHub checkboxes         | Task manifest JSON          |
| Finalize     | `/finish`                 | `/finalizer [--pr]`         |

## Commands

### `/code:plan-issue <feature>`

Research codebase and create a GitHub issue with task manifest.

```bash
/code:plan-issue add user authentication
```

**What happens:**

1. Researches your codebase (patterns, files, dependencies)
2. Creates task list with verification commands
3. Asks for confirmation
4. Creates GitHub issue with task headlines
5. Writes task manifest to `.claude/tasks/<issue>/manifest.json`

**Output:** GitHub issue URL + manifest path

### `/code:implement #<number>`

Launch orchestrator to execute all tasks.

```bash
/code:implement #123
```

**What happens:**

1. Validates issue is open
2. Ensures feature branch exists
3. Reads task manifest
4. Spawns orchestrator agent
5. Orchestrator loops through tasks:
   - Spawns implementer for each task
   - Commits after each task
   - Updates GitHub issue status
6. Runs simplify when all tasks complete
7. Reports: "Run `/code:finalizer [--pr]` to finish"

**Resume:** Just run `/code:implement #123` again. The orchestrator reads the manifest and continues from where it left off.

### `/code:finalizer [--pr] [issue-number]`

Finalize the feature: merge or create PR, close issue, cleanup.

```bash
/code:finalizer --pr   # Create pull request for review
/code:finalizer        # Merge directly to main
```

**What happens:**

1. Verifies all tasks complete
2. Creates PR (if `--pr`) or merges to main
3. Closes GitHub issue
4. Deletes feature branch (local + remote)

### `/code:commit`

Generate conventional commit from staged changes.

```bash
/code:commit
```

### `/code:pr`

Create GitHub PR with auto-generated description.

```bash
/code:pr
```

### `/code:simplify`

Clean up code after implementation.

```bash
/code:simplify
```

### `/code:lessons [N]`

Analyze recent commits and update LESSONS.md.

```bash
/code:lessons       # Analyze last 5 commits
/code:lessons 10    # Analyze last 10 commits
```

## Typical Flow

### Day 1: Start Feature

```bash
# Plan and create issue
/code:plan-issue add export to CSV feature

# Start implementing - runs autonomously
/code:implement #45

# ... orchestrator runs all tasks ...
# Output: "All tasks complete. Run /code:finalizer [--pr]"

# Create PR
/code:finalizer --pr
```

### Interrupted Session

If you need to stop mid-implementation:

```bash
# Next session - just run implement again
/code:implement #45

# Orchestrator reads manifest, continues from last task
```

No handover file needed. The manifest tracks progress.

## Architecture

```
User → /implement #42 (thin launcher)
         ↓
    Task(orchestrator) - Master controller
         ↓
         ├── Task(implementer) - Task 1
         ├── Task(implementer) - Task 2
         ├── Task(implementer) - Task 3
         └── Task(simplifier) - Cleanup
         ↓
    "Run /finalizer [--pr]"
```

**Key principle:** Intelligence lives in agents, not commands.

## Agents

| Agent          | Purpose                                  |
| -------------- | ---------------------------------------- |
| `orchestrator` | Controls task lifecycle, spawns workers  |
| `implementer`  | Implements single task with verification |

## Task Storage

```
.claude/tasks/
└── <issue-number>/
    └── manifest.json
```

The manifest tracks:

- Task list with status (pending/in_progress/completed)
- Dependencies (blockedBy/blocks)
- Verification commands
- File references

## Rules

### vibe-coding (Always Active)

- **10 lines > 20 lines** - Simpler is better
- **Working > Perfect** - Don't over-engineer
- **Delete > Add** - Remove unused code
- **One File First** - Extend before creating

### frontend-design (UI Work)

- **Bold direction** - Pick distinctive aesthetic
- **Avoid AI clichés** - No Inter font, purple gradients
- **Match complexity** - Simple design = simple code

## Required Configuration

Add to your project's `.claude/settings.json`:

```json
{
  "plansDirectory": "plans",
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "65"
  }
}
```

This enables auto-compact at 65% context, allowing agents to run indefinitely.

## Quick Reference

```
┌─────────────────────────────────────────────────────┐
│              CODING PLUGIN v2.0.1                   │
├─────────────────────────────────────────────────────┤
│ /code:plan-issue <desc>    Plan + Issue + Manifest  │
│ /code:implement #<num>     Orchestrator runs tasks  │
│ /code:finalizer [--pr]     Merge or PR + cleanup    │
├─────────────────────────────────────────────────────┤
│ Flow: Plan → Implement → Finalizer (autonomous)     │
│                                                     │
│ Resume: Just run /implement again (reads manifest)  │
└─────────────────────────────────────────────────────┘
```
