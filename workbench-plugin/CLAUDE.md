# Workbench Plugin - Daily Assistant Toolbox

**Skills first, agents for research, manual code last.**

## Output Folders

**Base path:** `~/Documents/Output/{topic}/`

| Folder | Purpose |
|--------|---------|
| `{topic}/research/` | Raw research from agents |
| `{topic}/analysis/` | Synthesized reports |
| `{topic}/final/` | Deliverables (PDF, PPTX) |

**Naming:** Topic -> folder name (lowercase, underscores). Example: "AI SaaS" -> `ai_saas/`

---

## Agent Routing

| You say... | Use this agent | Output to |
|------------|----------------|-----------|
| "Research X market/pricing/competitors" | Market Researcher | `{topic}/research/` |
| "Analyze X architecture/tech stack" | Technical Analyst | `{topic}/research/` |
| "Get latest info on X" / "Read this URL" | Jina Searcher | `{topic}/research/` |
| "Second opinion on this" | Gemini Analyst | - |
| "Compare X, Y, Z" | Market Researcher | `{topic}/analysis/` |

**When NOT to use:**

- Market Researcher: NOT for technical "how it works" -> use Technical Analyst
- Technical Analyst: NOT for pricing/market share -> use Market Researcher
- Jina Searcher: NOT for deep analysis -> use Market/Technical Researcher

---

## Skill Routing

| You need... | Use this skill |
|-------------|----------------|
| Report/document to read | **PDF** |
| Presentation for meetings/board | **PPTX** + Theme Factory |
| Editable document for collaboration | **DOCX** |
| Data tables/calculations | **XLSX** or Data Analyzer |
| Charts from data | **Data Analyzer** |
| Visual poster/artwork | **Canvas Design** |
| Internal communications | **Internal Comms** |

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `/research market [topic]` | Market/competitive research |
| `/research technical [topic]` | Technical architecture analysis |
| `/research quick [topic]` | Quick web lookup |
| `/research academic [topic]` | ArXiv/SSRN paper search |
| `/analyze compare [options]` | Structured comparison |
| `/workflow quick-report [topic]` | Research -> PDF in one go |
| `/workflow competitive-intel [competitors]` | Full competitive pipeline with SWOT |
| `/workflow deep-research [topic]` | Multi-angle deep research |
