---
context: fork
allowed-tools: Bash(gh issue view:*), Bash(gh issue edit:*), Bash(git:*), Read, Grep, Glob, Edit, Write, Task, Skill
description: Start implementation from a GitHub issue URL
argument-hint: #<issue-number> or <issue-url>
---

# Implement from GitHub Issue

Issue: $ARGUMENTS

## Step 1: Fetch Issue

```bash
gh issue view <number> --json title,body,state
```

Parse the issue body to extract:
- **Goal**: What we're building
- **Phases**: Implementation phases with checkboxes
- **Current phase**: First unchecked phase

## Step 2: Identify Current Phase

Look for the first phase with unchecked `- [ ]` tasks.

If all phases complete → proceed to **Step 6: Completion**.

## Step 2.5: Load Agent Context

Before executing, prepare for verification:

1. **Read implementer agent definition:**
   - Load `${CLAUDE_PLUGIN_ROOT}/agents/implementer.md`
   - Internalize the **HARD VERIFICATION GATE** rules

2. **Detect test command** (in order):
   - `package.json` with `"test"` script -> `bun test` or `npm test`
   - `Makefile` with `test:` target -> `make test`
   - `pyproject.toml` -> `uv run pytest` or `pytest`
   - `Cargo.toml` -> `cargo test`
   - `.claude/CLAUDE.md` with `## Verification` section -> use specified command
   - If none found: Ask user for test command

## Step 3: Execute Phase via Subagent

**Auto-Phase Management:** Spawn a fresh subagent for each phase to maintain clean context.

```
For each phase with unchecked [ ] tasks:
  1. Spawn Task(implementer subagent) with phase context
  2. Subagent implements tasks, monitors context usage
  3. If context ≥55% → Skill("handover") → return → spawn continue
  4. When phase complete → subagent returns → next phase
```

### Spawn Implementer Subagent

Use the Task tool with `subagent_type: coding-plugin:implementer`:

```
Task(
  subagent_type: "coding-plugin:implementer",
  prompt: """
  Issue #<number>: <title>

  Current Phase: <phase-name>

  Tasks:
  - [ ] Task 1
  - [ ] Task 2
  ...

  Files: <file-list>

  Test command: <detected-command>

  Implement all tasks in this phase. Monitor context usage.
  If context reaches 55%, call Skill("coding-plugin:handover") and return.
  """
)
```

### Context Monitoring (Inside Subagent)

The implementer subagent monitors `context_window.used_percentage`:

- **Below 55%**: Continue implementing
- **At 55%**:
  1. Stop current work cleanly
  2. Call `Skill("coding-plugin:handover")` to save state
  3. Return summary to caller

Caller spawns fresh subagent to continue (effective context clear).

### Phase Execution Flow

For the current phase:
1. **Read the tasks** - ALWAYS READ CODE BEFORE CHANGING: Search thoroughly for key facts, patterns, and conventions
2. **Identify files** - Check the `Files:` line for affected files
3. **Implement** - Complete each task in order
4. **Test (VERIFICATION GATE)** - Run test command, verify exit code 0
   - If tests **fail**: Fix issues, re-run tests, repeat until passing
   - If tests **pass**: Log "Tests passed" with summary
   - **GATE: Cannot mark [x] until tests pass**
5. **Commit** - Use descriptive commit message (only after tests pass)

### Verification Gate

```
+-------------------------------------------+
| VERIFICATION GATE                         |
+-------------------------------------------+
| Test command: <detected>                  |
| Status: PASSING / FAILING                 |
| Result: <test output summary>             |
+-------------------------------------------+
| BLOCKED until tests pass                  |
+-------------------------------------------+
```

**Rule:** NEVER mark a task `[x]` without passing tests. No exceptions.

### Git Discipline

- Branch: `feature/<issue-number>-<short-desc>` (if not already on it)
- Commits: Small, atomic, descriptive
- Format: `✨ <description>` for features, `🐛 <description>` for fixes
- **Smart Commit:** Use `/commit` for auto-generated conventional commits

## Step 4: Update Issue

After completing phase tasks:

### ⚠️ Always Use --body-file

**Never use `--body "..."`** — fails with special characters in sandbox.

1. Write updated body to `.claude-issue-body.md` using Write tool
2. Update issue:
   ```bash
   gh issue edit <number> --body-file .claude-issue-body.md
   ```

Mark completed tasks with `[x]`.

## Step 5: Report Progress

Tell user:
- What was completed
- What's next (next phase or done)
- Any blockers encountered

## Step 6: Completion

After all phases are marked `[x]`:

1. **Run auto-simplify** (unless `--no-simplify` in `$ARGUMENTS`):
   ```
   Skill("coding-plugin:simplify")
   ```
   Report: files simplified, issues created (if any)

2. **Ask user:** "All phases complete. Close issue #<number>?"

3. **Wait for explicit "yes"** before running `gh issue close`

4. **Never auto-close** - user approval required

## Rules

- **Follow the plan** - Don't deviate from the issue phases
- **One phase at a time** - Complete current phase before moving on
- **Update checkboxes** - Keep issue in sync with progress
- **Ask if unclear** - Don't guess, ask the user
