# Coding Plugin User Guide

**Never memorize commands again!** This guide is your quick reference for the coding-plugin workflow.

## Quick Start (Copy-Paste Commands)

### Common Scenarios

#### I want to add a feature
```
/start Add user authentication system
```

#### I want to build a UI component
```
/start Create landing page hero section
```

#### I want to fix a bug
```
/start Fix login validation error
```

#### Check current status
```
/status
```

#### Mark current phase done
```
/complete
```

#### Start fresh chat (when context is full)
```
/nuke
```

---

## How The Workflow Works

```
Research → Plan → Implement
```

### The Three Phases

**1. Research Phase**
- Verifies ground truth - never guesses about APIs, libraries, or code
- Reads documentation and explores codebase
- Creates GitHub issue labeled `phase:research`
- Output: Research summary with verified facts

**2. Plan Phase**
- Creates detailed, step-by-step implementation plan
- Includes specific file paths and code references
- **NO CODE WRITTEN** until plan is explicitly approved
- Creates GitHub issue labeled `phase:plan`
- Output: Numbered steps with file:line references

**3. Implement Phase**
- Follows approved plan exactly
- Commits changes within the phase
- Creates GitHub issue labeled `phase:implement`
- Requests approval before marking complete

### Typical Flow

```bash
# 1. Start workflow
/start Add user authentication

# Claude asks setup questions and starts research phase automatically

# 2. Review research, then plan
/plan

# Claude creates implementation plan and waits for your approval

# 3. After approving plan, implement
/implement

# Claude executes the plan step by step

# 4. Mark phase complete when done
/complete
```

---

## All Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/start <description>` | Initialize new workflow | `/start Add dark mode` |
| `/research <topic>` | Begin research phase | `/research User auth libraries` |
| `/plan <feature>` | Create implementation plan | `/plan Dark mode toggle` |
| `/implement <feature>` | Execute approved plan | `/implement Dark mode` |
| `/status` | Check current phase and progress | `/status` |
| `/complete` | Mark current phase as done | `/complete` |
| `/nuke` | Generate summary for fresh chat | `/nuke` |

---

## Rules Explained

The plugin has two main rule files that guide coding behavior:

### vibe-coding (Always Active)

**Core philosophy: Keep it simple, keep it working**

Key principles:
- **Simplicity First**: 10 lines > 20 lines
- **Working > Perfect**: Don't fix what isn't broken
- **Delete > Add**: Optimize by removing code
- **One File First**: Add to existing files before creating new ones
- **Small Steps**: Break work into minimal logical changes
- **Follow Patterns**: Match the project's existing style

**Stop signals** - Don't do these without asking:
- Create new files without being asked
- Add tests without request
- Create "comprehensive" anything
- Restructure file organization
- Use phrases like "refactor for organization" or "best practices"

### frontend-design (UI Work Only)

**Activates when**: Building UI components, pages, styling, animations

**Core philosophy: Bold aesthetic choices that avoid generic AI design**

Key principles:
- **Choose Bold Direction**: Pick distinctive aesthetic (brutalist, luxury, playful, minimal, etc.)
- **Avoid AI Clichés**:
  - Fonts: Inter, Roboto, Arial, Space Grotesk
  - Colors: Purple gradients on white
  - Layouts: Generic, predictable patterns
- **Typography**: Use characterful fonts, pair display + body
- **Motion**: Well-orchestrated moments > scattered micro-interactions
- **Match Code to Design**: Minimalist design → simple code, Elaborate design → elaborate code OK

### How Rules Work Together

When doing UI work, **BOTH rules apply** with this bridge:

```
Code complexity should match design ambition:
  - Minimalist design → simple code (vibe-coding wins)
  - Elaborate design → elaborate animations/effects OK (frontend-design wins)
  - Key: INTENTIONALITY, not complexity
```

---

## Common Patterns

### Pattern 1: Adding a New Feature

```bash
# Start
/start Add password reset functionality

# Claude asks:
# - "Do you need documentation?"
# - "What does 'done' look like?"
# - Starts research phase automatically

# After research approval
/plan

# After plan approval
/implement

# When done
/complete
```

### Pattern 2: Building UI Component

```bash
# Start (triggers frontend-design rule)
/start Create product card component

# Claude will:
# - Ask about aesthetic direction
# - Research existing design patterns
# - Propose bold visual approach
# - Avoid generic AI aesthetics

# Continue with plan → implement → complete
```

### Pattern 3: Bug Fix

```bash
# Start
/start Fix checkout cart calculation bug

# Claude will:
# - Research the issue thoroughly
# - Identify root cause
# - Plan minimal fix (vibe-coding: simple > complex)
# - Track if multiple attempts fail (warns after 3 attempts)

# If stuck after 3 tries, Claude suggests:
/nuke  # Fresh perspective
```

---

## Context Hygiene ("Avoid the Dumb Zone")

The plugin monitors context usage to prevent degraded performance:

### Context Warnings

- **60% context**: Warning message
- **80% context**: Strong suggestion to use `/nuke`
- **3+ failed bug fixes**: "Consider fresh perspective" warning

### Chat Nuke Protocol

When context is exhausted, use `/nuke` to generate a summary:

```bash
/nuke
```

Claude generates:
- Current task and goal
- What has been tried (successes and failures)
- Key file references (file:line)
- Next steps

Copy this summary and start a fresh chat with it.

---

## Tips for No-Memory Usage

### Bookmark This Guide

Add this to your browser bookmarks:
```
file:///Users/kennetkusk/code/Claude_plugin/innovation-basement/coding-plugin/GUIDE.md
```

### Shell Aliases (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Coding plugin aliases
alias cstart="echo '/start'" # Copy start command
alias cstatus="echo '/status'"
alias cplan="echo '/plan'"
alias cimplement="echo '/implement'"
alias ccomplete="echo '/complete'"
alias cnuke="echo '/nuke'"

# Quick guide access
alias cguide="cat /Users/kennetkusk/code/Claude_plugin/innovation-basement/coding-plugin/GUIDE.md"
```

### Keep Commands Tab Open

Keep a terminal tab open with common commands ready to copy:

```bash
# Common commands - copy as needed
/start Add feature name
/status
/plan
/implement
/complete
/nuke
```

---

## Requirements

The plugin requires these tools:

- **GitHub CLI** (`gh`) - For issue creation
- **Git** - For version control
- **jq** - For JSON parsing in scripts

Install missing tools:
```bash
# macOS
brew install gh jq

# Check versions
gh --version
git --version
jq --version
```

---

## GitHub Setup

### Labels

Create these labels in your repo for best experience:

```bash
gh label create "phase:research" --color "0E8A16"
gh label create "phase:plan" --color "1D76DB"
gh label create "phase:implement" --color "5319E7"
```

Or manually in GitHub:
- `phase:research` (green)
- `phase:plan` (blue)
- `phase:implement` (purple)

---

## Troubleshooting

### Plugin not found
```bash
# Add marketplace
/plugin marketplace add NOGIT007/innovation-basement

# Install plugin
/plugin install coding-plugin@innovation-basement
```

### Commands don't work
```bash
# Check installed plugins
/plugin list

# Reinstall if needed
/plugin uninstall coding-plugin
/plugin install coding-plugin@innovation-basement

# Restart Claude Code
```

### Rules not activating

Rules activate automatically based on context:
- **vibe-coding**: Always active
- **frontend-design**: Activates when UI/design work detected

To verify rules are loaded:
```bash
# Check plugin status
/plugin list
```

---

## Advanced Usage

### Custom Workflow

You can use commands independently without `/start`:

```bash
# Direct research
/research Next.js App Router patterns

# Direct planning
/plan User authentication flow

# Direct implementation
/implement Login form component
```

### Documentation Control

The plugin asks before creating docs. To control:

- Answer "yes" when starting: Claude creates/updates docs
- Answer "no": No documentation created
- Manual control: Create docs yourself, Claude follows pattern

### Sub-Agents

The plugin can spawn specialized agents:
- **research-agent**: Deep technical research
- **doc-agent**: Documentation creation

These are managed automatically, but you can request them:
```
/research Use doc-agent to create API docs
```

---

## Philosophy

The coding-plugin embodies:

1. **Structured workflow** - Research before planning, plan before coding
2. **Context hygiene** - Fresh perspective when stuck
3. **Critical thinking** - Challenge bad plans, list missing requirements
4. **Git discipline** - Commit frequently, use branches, descriptive messages
5. **Simple code** - Working > perfect, 10 lines > 20 lines
6. **Bold UI** - When doing design, commit fully to distinctive vision

---

## Quick Reference Card

Print or screenshot this:

```
┌─────────────────────────────────────────┐
│       CODING PLUGIN QUICK REF           │
├─────────────────────────────────────────┤
│ /start <desc>  → Start workflow         │
│ /research      → Research phase         │
│ /plan          → Plan phase             │
│ /implement     → Implement phase        │
│ /status        → Check progress         │
│ /complete      → Finish phase           │
│ /nuke          → Fresh chat summary     │
├─────────────────────────────────────────┤
│ Workflow: Research → Plan → Implement   │
├─────────────────────────────────────────┤
│ Rules:                                  │
│ • vibe-coding (always on)               │
│ • frontend-design (UI work)             │
└─────────────────────────────────────────┘
```

---

## Getting Help

- **Issues**: Report bugs at [GitHub](https://github.com/NOGIT007/innovation-basement/issues)
- **Guide**: You're reading it!
- **README**: See `README.md` for technical details
- **Rules**: See `rules/` folder for full rule text

---

**Remember**: You don't need to memorize anything. Bookmark this guide and copy-paste commands as needed. The plugin handles the workflow, you focus on coding.
