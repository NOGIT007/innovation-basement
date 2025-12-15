Quick research-to-PDF pipeline: research a topic and deliver a polished PDF in one go.

Run the quick report pipeline for: $ARGUMENTS

## Pipeline Steps

### Step 1: Research
Use Market Researcher or Technical Analyst (based on topic type) to gather comprehensive information.
- Market/business topics → Market Researcher
- Technical/architecture topics → Technical Analyst

Save research to `/Users/kennetkusk/Documents/Output/{topic}/research/{topic}.md`

### Step 2: Structure
Organize findings into a well-structured report with:
- Executive Summary
- Key Findings (with sources)
- Analysis/Implications
- Recommendations (if applicable)
- Sources

Save structured report to `/Users/kennetkusk/Documents/Output/{topic}/analysis/{topic}_report.md`

### Step 3: Convert to PDF
Use the PDF skill to create a polished deliverable.
Save to `/Users/kennetkusk/Documents/Output/{topic}/final/{topic}_report.pdf`

### Step 4: Confirm
Tell the user the PDF is ready and provide the path.
