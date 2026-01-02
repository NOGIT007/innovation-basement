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

### coding-plugin v2.9

Structured coding workflow with phased development and spec interviews.

**Philosophy:** Interview -> Plan -> Implement (no code until plan approved).

**Features:**
- Spec interviews to develop vague ideas into 1.0 specs
- Project constitution for guiding principles
- LSP-precise planning with file:line references
- Lessons learning from commits
- Session handover/resume

**Commands:**
- `/code:interview <spec>` - Interview to develop vague ideas into specs
- `/code:constitution` - Create project principles (constitution.md)
- `/code:plan-issue <feature>` - Research with LSP, create GitHub issue
- `/code:implement #<number>` - Execute phases from issue
- `/code:handover` - Save session state
- `/code:resume` - Continue from handover
- `/code:lessons [N]` - Analyze commits, update LESSONS.md

## Installation

### Step 1: Clone the marketplace locally

```bash
mkdir -p ~/.claude/plugins/marketplaces
cd ~/.claude/plugins/marketplaces
git clone https://github.com/NOGIT007/innovation-basement.git
```

### Step 2: Add marketplace in Claude Code

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

## License

MIT
