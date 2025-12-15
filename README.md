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

```bash
# Add the marketplace
/plugin marketplace add NOGIT007/innovation-basement

# Install workbench plugin (research, documents)
/plugin install workbench-plugin@innovation-basement

# Install coding plugin (phased development)
/plugin install coding-plugin@innovation-basement
```

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
