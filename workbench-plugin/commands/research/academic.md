Search academic papers and research on a topic using ArXiv and SSRN.

Use Jina Searcher to find academic research on: $ARGUMENTS

## Research Sources

1. **ArXiv** - For technical papers (AI, ML, physics, math, CS)
   - Use `mcp__jina__search_arxiv` tool

2. **SSRN** - For social sciences, economics, law, finance
   - Use `mcp__jina__search_ssrn` tool

## Output Format

Structure findings as:

```markdown
## Academic Research: [Topic]

### Key Papers

1. **[Paper Title]** ([Year])
   - Authors: [Names]
   - Abstract summary: [2-3 sentences]
   - Key findings: [Bullet points]
   - Link: [URL]

2. **[Paper Title]** ([Year])
   ...

### Research Themes
- [Theme 1]: [Papers that address this]
- [Theme 2]: [Papers that address this]

### Gaps in Literature
- [What hasn't been studied yet]

### Recommended Reading Order
1. Start with: [Paper] - foundational
2. Then: [Paper] - builds on #1
3. Deep dive: [Paper] - advanced
```

Save to `/Users/kennetkusk/Documents/Output/{topic}/research/{topic}_academic.md`
