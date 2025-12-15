---
description: Start the Research phase for a coding task. Creates GitHub issue and sets context.
---

Start RESEARCH phase for: $ARGUMENTS

## Phase Protocol

1. **Create GitHub Issue**
   Run: `gh issue create --title "[Research] $ARGUMENTS" --label "phase:research" --body "Research phase for: $ARGUMENTS"`

2. **Research Objectives**
   - Verify all assumptions about the task
   - Explore existing codebase patterns
   - Document API/library requirements
   - Identify potential challenges

3. **Use Research Agent**
   Delegate to research-agent for:
   - API documentation review
   - Codebase exploration
   - Dependency verification

4. **Output Requirements**
   Create research summary with:
   - Verified facts (with sources)
   - Relevant code references (file:line)
   - Identified risks/gotchas
   - Recommended approach

5. **Phase Completion**
   - Present findings to user
   - Get explicit approval before proceeding to PLAN phase
   - Update GitHub issue with findings
