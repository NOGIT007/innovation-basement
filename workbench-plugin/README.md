# Workbench Plugin

A Claude Code plugin for research, document generation, and analysis. Part of the innovation-basement marketplace.

## Philosophy

**Skills first, agents for research, manual code last.**

This plugin packages non-coding capabilities for daily productivity:
- Research and competitive intelligence
- Document creation (PDF, PPTX, DOCX, XLSX)
- Data analysis and visualization
- Internal communications

## Installation

```bash
/plugin marketplace add NOGIT007/innovation-basement
/plugin install workbench-plugin@innovation-basement
```

## Requirements

- Claude Code >= 1.0.0
- MCP Jina server (for web research)
- Gemini CLI (optional, for second opinions)
- Pandoc (for PDF conversion)
- LibreOffice (for PPTX editing)

## Quick Start

### Research a Market
```
/research market AI coding assistants 2025
```

### Create a Competitive Analysis
```
/workflow competitive-intel Vercel, Netlify, Cloudflare Pages
```

### Generate a Report
```
/workflow quick-report state of AI coding assistants
```

## Agents

| Agent | Best For |
|-------|----------|
| Market Researcher | WHO, WHAT, HOW MUCH |
| Technical Analyst | HOW (architecture) |
| Jina Searcher | Quick lookups, URLs |
| Gemini Analyst | Second opinions |

## Skills

| Skill | Purpose |
|-------|---------|
| PDF | Document creation |
| PPTX | Presentations |
| DOCX | Editable documents |
| XLSX | Spreadsheets |
| Theme Factory | 10 professional themes |
| Data Analyzer | CSV/JSON/Parquet analysis |
| Internal Comms | Status reports, newsletters |
| Canvas Design | Posters, artwork |

## Output Structure

All outputs go to `~/Documents/Output/{topic}/`:
- `research/` - Raw research
- `analysis/` - Synthesized reports
- `final/` - Deliverables

## Commands

### Research Commands
- `/research market [topic]` - Deep market research
- `/research technical [topic]` - Technical architecture analysis
- `/research quick [topic]` - Quick web lookup
- `/research academic [topic]` - ArXiv/SSRN paper search

### Analysis Commands
- `/analyze compare [options]` - Structured comparison

### Workflow Commands
- `/workflow quick-report [topic]` - Research to PDF pipeline
- `/workflow deep-research [topic]` - Multi-angle comprehensive research
- `/workflow competitive-intel [competitors]` - Full competitive intelligence with SWOT

## License

MIT
