# coding-plugin v2.5

Simple, phased coding workflow for Claude Code. Part of the innovation-basement marketplace.

## What's New in v2.5

- **Architecture auto-update** - `rules/architecture.md` regenerates after commits
- **Streamlined rules** - Simplified user rules with Ground Rules enforcement
- **Data flow tracing** - Plan issues now require file:line references
- **Quality checklist** - Edge cases, security, backward compat built into planning

## Installation

```bash
/plugin marketplace add NOGIT007/innovation-basement
/plugin install coding-plugin@innovation-basement
```

## Workflow

```
/code:plan-issue → /code:implement → /code:handover
     ↓                   ↓                ↓
  GitHub Issue    Work phases      Next session
```

### Commands

| Command | Description |
|---------|-------------|
| `/code:plan-issue <feature>` | Research codebase, plan phases, create GitHub issue |
| `/code:implement #<number>` | Implement from GitHub issue, work through phases |
| `/code:handover` | Generate handover for next session |
| `/code:update-architecture` | Regenerate architecture.md |

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

Generates concise handover text for next session.

## Architecture Auto-Update

After each commit, `rules/architecture.md` regenerates via git hook.

### Install in This Project

```bash
cp scripts/post-commit .git/hooks/ && chmod +x .git/hooks/post-commit
```

### Install in Any Project

```bash
# From your project root
mkdir -p scripts rules

# Create update-architecture.sh
cat > scripts/update-architecture.sh << 'EOF'
#!/bin/bash
ARCH="rules/architecture.md"
[ -f "$ARCH" ] && [ $(($(date +%s) - $(stat -f %m "$ARCH"))) -lt 3600 ] && exit 0
echo "🏗️ Updating architecture..."
claude -p "/code:update-architecture" --allowed-tools "Read,Glob,Write,Bash(ls:*)" &
EOF

# Create post-commit hook
cat > scripts/post-commit << 'EOF'
#!/bin/bash
./scripts/update-architecture.sh 2>/dev/null || true
EOF

# Make executable and install
chmod +x scripts/update-architecture.sh scripts/post-commit
cp scripts/post-commit .git/hooks/
```

Shows 🏗️ emoji when updating. Rate-limited to once per hour.

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
