# Coding Plugin User Guide v1.0.0

Simple workflow: **Plan → Implement** (auto-manages context)

## Quick Start

```bash
# 1. Plan a feature (creates GitHub issue + branch)
/code:plan-issue add dark mode toggle

# 2. Implement - runs autonomously until done
/code:implement #42
```

**That's it!** `/implement` now handles everything:
- Spawns fresh subagent per phase (clean context)
- Auto-handover at 55% context → spawns continue
- Loops until all phases complete
- No manual `/handover` needed

### Manual Flow (still supported)

```bash
# End session manually
/code:handover

# Continue next session
/code:continue
```

## Commands

### `/code:plan-issue <feature>`

Research codebase and create a GitHub issue with phases.

```bash
/code:plan-issue add user authentication
```

**What happens:**
1. Researches your codebase (patterns, files, dependencies)
2. Creates implementation plan with phases
3. Asks for confirmation
4. Creates GitHub issue with checkboxes

**Output:** GitHub issue URL like `#123`

### `/code:implement #<number>`

Work through phases from a GitHub issue.

```bash
/code:implement #123
```

**What happens:**
1. Fetches issue and parses phases
2. Identifies current phase (first unchecked)
3. Implements tasks in order
4. Updates checkboxes when done
5. Reports progress

**Between sessions:** Just run `/code:implement #123` again - it reads the checkboxes to know where you left off.

### `/code:handover`

Generate handover text for next session.

```bash
/code:handover
```

**Output:**
```
## Handover

**Issue:** #123 - Add dark mode toggle
**Phase:** Phase 2 - Theme context
**Branch:** feature/123-dark-mode
**Status:** Phase 1 complete, starting theme context

### Next Steps
- [ ] Create ThemeContext provider
```

Copy this and paste at the start of your next session.

## Typical Flow

### Day 1: Start Feature

```bash
# Plan and create issue
/code:plan-issue add export to CSV feature

# Start implementing
/code:implement #45

# ... work through Phase 1 ...

# End session
/code:handover
```

### Day 2: Continue

```bash
# Paste yesterday's handover, then:
/code:implement #45

# ... continues from Phase 2 ...
```

### Day 3: Finish

```bash
/code:implement #45

# All phases complete - issue auto-closes
```

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

## Tips

### Clear Sessions Often

Your workflow supports clearing sessions between phases. The GitHub issue tracks progress, not the chat.

### Keep Issues Updated

If you manually change something, update the issue checkboxes so `/code:implement` knows the current state.

### One Issue at a Time

Focus on one feature issue. Complete it before starting another.

## Quick Reference

```
┌─────────────────────────────────────────────┐
│         CODING PLUGIN v1.0.0                │
├─────────────────────────────────────────────┤
│ /code:plan-issue <desc>  Plan + Issue       │
│ /code:implement #<num>   Auto-loop phases   │
├─────────────────────────────────────────────┤
│ Flow: Plan → Implement (auto until done)    │
│                                             │
│ Manual: /handover + /continue (optional)    │
└─────────────────────────────────────────────┘
```
