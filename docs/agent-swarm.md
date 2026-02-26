# Agent Swarm

**Experimental** — Agent Swarm is an advanced feature for complex, multi-task features. Most users should start with the default subagent mode.

Agent Swarm lets `/code:implement` use multiple independent Claude Code sessions instead of subagents. **One developer, many agents** — you become the lead, Claude spawns a swarm of coding agents that parallelize your work.

---

## What Is Agent Swarm?

You (single user) run one Claude Code session that becomes the **lead** (coordinator). Claude spawns multiple independent sessions (agents) that claim tasks from a shared task list, implement them in parallel, and self-coordinate.

This is NOT a multi-user team feature. It's one person leveraging multiple parallel Claude instances to move faster on complex features.

## How It Works

```
You (lead session)
  │
  ├─ Teammate 1 → claims Task A → implements → verifies → commits
  ├─ Teammate 2 → claims Task B → implements → verifies → commits
  ├─ Teammate 3 → claims Task C → implements → verifies → commits
  └─ ...up to 5 teammates
  │
  Shared TaskList ← self-coordination
  │
  Teammates message each other directly when needed
```

- **Your session** = lead (monitors progress, updates GitHub issue)
- **Teammate sessions** = workers (claim tasks, implement, verify, commit)
- **Shared TaskList** = coordination layer (tasks auto-unblock as dependencies complete)
- **Direct messaging** = teammates can message each other for cross-task coordination

---

## Enable Agent Swarm

Add to your project's `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_TASK_LIST_ID": "<your-project-name>-tasks",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## When Does Agent Swarm Activate?

| Scenario                                      | Mode                             |
| --------------------------------------------- | -------------------------------- |
| Env var not set                               | Always subagent (default)        |
| Env var set + < 4 tasks                       | Subagent (auto-detected)         |
| Env var set + 4+ tasks with 60%+ independence | Swarm (auto-detected)            |
| `--team` flag                                 | Swarm (forced, requires env var) |
| `--no-team` flag                              | Subagent (forced, always works)  |

## Using Agent Swarm

```bash
# Let auto-detection decide
/code:implement #42

# Force swarm mode for a complex cross-layer feature
/code:implement #42 --team

# Force subagent mode when you want lower token usage
/code:implement #42 --no-team
```

---

## Display Modes

### In-process (default)

Works in any terminal. All agents run in the same terminal window.

```json
{ "teammateMode": "in-process" }
```

Or via CLI: `claude --teammate-mode in-process`

Use `Shift+Down` to cycle between agents and view/message them.

### Split-pane

Each agent gets its own terminal pane. Requires tmux or iTerm2.

```json
{ "teammateMode": "tmux" }
```

Or via CLI: `claude --teammate-mode tmux`

---

## Configure tmux for Split-Pane Mode (macOS)

Install tmux:

```bash
brew install tmux
```

Create `~/.tmux.conf`:

```bash
# Mouse support
set -g mouse on

# Scrollback buffer
set -g history-limit 10000

# Start windows and panes at 1
set -g base-index 1
setw -g pane-base-index 1

# Pane navigation with Alt+Arrow
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Status bar theme
set -g status-style 'bg=#1a1a2e fg=#e0e0e0'
set -g status-left '#[fg=#00d4aa,bold] #S '
set -g status-right '#[fg=#666]%H:%M'

# Split shortcuts
bind | split-window -h
bind - split-window -v

# Reload config
bind r source-file ~/.tmux.conf \; display "Config reloaded"

# Cheat sheet
bind h run-shell "~/.tmux/cheatsheet.sh"
```

Create `~/.tmux/cheatsheet.sh`:

```bash
#!/bin/bash
tmux display-popup -w 60 -h 20 -E "echo '
  tmux Cheat Sheet
  ════════════════════════════
  Alt+Arrow    Navigate panes
  Prefix + |   Vertical split
  Prefix + -   Horizontal split
  Prefix + r   Reload config
  Prefix + h   This cheat sheet
  Prefix + z   Toggle zoom pane
  Scroll       Mouse wheel
  ════════════════════════════
  Prefix = Ctrl+B (default)
' && read -n 1"
```

```bash
chmod +x ~/.tmux/cheatsheet.sh
```

Start Agent Swarm in tmux mode:

```bash
claude --teammate-mode tmux
```

> **Note:** Split-pane works best on macOS. Linux may need adjustments to the tmux config.

---

## Keyboard Shortcuts

| Shortcut     | Action                  |
| ------------ | ----------------------- |
| `Shift+Down` | Cycle to next agent     |
| `Shift+Up`   | Cycle to previous agent |
| `Ctrl+T`     | View shared task list   |
| `Escape`     | Interrupt current agent |

### Interacting with Agents

1. Press `Shift+Down` to select the agent you want to talk to
2. Type your message — redirect their approach, give additional instructions, or ask for status
3. Each agent maintains its own context and continues where it left off

---

## Quality Gates

The plugin ships hooks that enforce verification in swarm mode:

- **`TeammateIdle` hook** — when a teammate finishes a task and goes idle, the hook directs them to pick up the next available task from TaskList
- **`TaskCompleted` hook** — runs the detected test command before accepting task completion. Uses exit code 2 to reject if tests fail (task stays in_progress for retry)

Agents cannot skip verification. The hooks run automatically.

---

## Token Usage

Each teammate is a separate Claude instance. Agent Swarm uses significantly more tokens than subagent mode. Use it for complex features with 4+ independent tasks where parallel work justifies the cost.

---

## Limitations

- **No session resumption** — if a teammate crashes, it cannot be resumed. The lead will detect the stalled task and can re-dispatch
- **One swarm per session** — you can only run one Agent Swarm at a time
- **No nested swarms** — teammates cannot spawn their own swarms
- **Lead is fixed** — the session that starts the swarm is always the lead, cannot be transferred

---

_Part of the [Innovation Basement Coding Plugin](https://github.com/NOGIT007/innovation-basement)_
