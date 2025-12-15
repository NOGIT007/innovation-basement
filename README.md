# Innovation Basement

A Claude Code marketplace with productivity plugins by Kennet Kusk.

## Plugins

### workbench-plugin

Daily assistant toolbox for research, document generation, and analysis.

**Philosophy:** Skills first, agents for research, manual code last.

**Features:**
- 4 research agents (Market Researcher, Technical Analyst, Jina Searcher, Gemini Analyst)
- 8 slash commands for research and workflows
- Document skills (PDF, PPTX, DOCX, XLSX)
- Theme Factory with 10 professional themes
- Data Analyzer, Canvas Design, Internal Comms

### coding-plugin

Structured coding workflow with phased development.

**Philosophy:** Research -> Plan -> Implement (no code until plan approved).

**Features:**
- GitHub issue creation for each phase
- Context hygiene warnings (60%/80% thresholds)
- Bug fix tracking (warns after 3+ failed attempts)
- Auto error logging to lessons-learned.md
- Chat Nuke for fresh starts

## Installation

### Step 1: Clone the marketplace locally

```bash
# In your terminal (not Claude Code)
mkdir -p ~/.claude/plugins/marketplaces
cd ~/.claude/plugins/marketplaces
git clone https://github.com/NOGIT007/innovation-basement.git
```

### Step 2: Add marketplace in Claude Code

In Claude Code chat, type:
```
/plugin marketplace add ~/.claude/plugins/marketplaces/innovation-basement
```

### Step 3: Install plugins

```
/plugin install coding-plugin@innovation-basement
```

Choose your scope:
- **User scope**: Available in all your projects
- **Project scope**: Shared with collaborators (via git)
- **Local scope**: This repo only, not shared

### Step 4: Restart Claude Code

Restart to load the plugin, then verify with `/plugin` → Installed tab.

## Requirements

### workbench-plugin
- GitHub CLI (`gh`) + Git
- MCP Jina server (for web research)
- Gemini CLI (optional)
- Pandoc, LibreOffice (for document conversion)

### coding-plugin
- GitHub CLI (`gh`)
- Git
- jq

## License

MIT
