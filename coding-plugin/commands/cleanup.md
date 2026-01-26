---
allowed-tools: Read, Write, Glob, Grep, Edit, AskUserQuestion, Bash(mkdir:*)
description: Refactor CLAUDE.md and LESSONS.md for progressive disclosure
---

# Cleanup Context Files

Refactor CLAUDE.md and LESSONS.md using progressive disclosure. Keep root files lean, move detailed rules to `.claude/rules/`.

## Step 1: Find Context Files

Find all CLAUDE.md and LESSONS.md files in the project:

```
Glob: **/CLAUDE.md
Glob: **/LESSONS.md
```

Read each file found.

## Step 2: Detect Contradictions

Scan for contradictory instructions. Examples:

- "Always use X" vs "Never use X"
- Different values for same setting
- Conflicting patterns or approaches

**For each contradiction found:**

```
AskUserQuestion: "Found contradiction:
- File A says: [instruction 1]
- File B says: [instruction 2]
Which should be kept?"
Options: [Keep first, Keep second, Keep both (clarify context), Delete both]
```

## Step 3: Categorize Instructions

Group all instructions into categories:

| Category   | Description                       | Destination                   |
| ---------- | --------------------------------- | ----------------------------- |
| Essential  | Project identity, critical rules  | Root CLAUDE.md                |
| TypeScript | Type conventions, import patterns | `.claude/rules/typescript.md` |
| Testing    | Test patterns, mocking, coverage  | `.claude/rules/testing.md`    |
| Git        | Commit format, branch naming      | `.claude/rules/git.md`        |
| API        | Endpoints, auth patterns          | `.claude/rules/api.md`        |
| Delete     | Redundant, stale, obvious         | (removed)                     |

## Step 4: Flag Items for Deletion

Identify items that should be removed:

- **Redundant**: Duplicated elsewhere
- **Stale**: References removed files/deps
- **Obvious**: Standard practices Claude already knows (e.g., "use meaningful variable names")

**For each flagged item:**

```
AskUserQuestion: "Should this be deleted?
[quoted instruction]
Reason: [redundant/stale/obvious]"
Options: [Delete, Keep in root, Move to rules]
```

## Step 5: Create Rules Structure

```bash
mkdir -p .claude/rules
```

Create rule files based on categorized content. Each file follows this format:

```markdown
# [Category] Rules

_Loaded when working on [category] files_

## [Section]

- [Specific rule]
- [Specific rule]
```

## Step 6: Write Minimal Root CLAUDE.md

Target: **Under 50 lines**

Include only:

1. Project name/purpose (1-2 lines)
2. Key architecture summary (5-10 lines)
3. Critical rules that apply everywhere (10-15 lines)
4. Reference to `.claude/rules/` for detailed rules

Template:

```markdown
# [Project Name]

[One-line description]

## Architecture

[Brief structure - max 10 lines]

## Critical Rules

- [Rule 1]
- [Rule 2]

## Detailed Rules

See `.claude/rules/` for context-specific rules:

- `typescript.md` - Type conventions
- `testing.md` - Test patterns
- `git.md` - Commit/branch rules
```

## Step 7: Archive LESSONS.md

Don't delete LESSONS.md content - archive it:

```bash
mkdir -p .claude/archive
```

Move to: `.claude/archive/lessons-YYYY-MM-DD.md`

Create fresh LESSONS.md with:

```markdown
# Project Lessons

_Last updated: [date]_

## Active Lessons

(migrated from cleanup - [date])

[Keep only lessons still relevant]
```

## Step 8: Report Summary

Output statistics:

```
## Cleanup Summary

**Before:**
- CLAUDE.md: [X] lines
- LESSONS.md: [Y] lines
- Total instructions: [Z]

**After:**
- CLAUDE.md: [X'] lines (target: <50)
- Rules files created: [N]
- Items deleted: [M]
- LESSONS.md archived to: [path]

**Created:**
- .claude/rules/typescript.md
- .claude/rules/testing.md
- .claude/rules/git.md

**User decisions:**
- Contradictions resolved: [N]
- Items confirmed for deletion: [M]
```

## Rules

- **Never delete without asking** - Always get user confirmation
- **Archive, don't destroy** - LESSONS.md content is preserved
- **Progressive disclosure** - Root file is entry point, details in rules/
- **Keep it lean** - Root CLAUDE.md under 50 lines
- **Be specific** - Each rule file has clear scope
