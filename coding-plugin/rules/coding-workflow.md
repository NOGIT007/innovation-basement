---
name: coding-workflow
description: Enforces structured coding workflow with phased development, context hygiene, and critical thinking.
---

# Coding Workflow Rules

## Core Principles

### 1. Mandatory Workflow: Research -> Plan -> Implement

Every coding task MUST follow this sequence:

**Phase 1: RESEARCH**
- Verify ground truth - NEVER guess about APIs, libraries, or existing code
- Read documentation, explore codebase, test assumptions
- Output: Research summary with verified facts and code references

**Phase 2: PLAN**
- Create detailed, step-by-step implementation plan
- Include specific file paths and code snippets ready for implementation
- NO CODE WRITTEN until plan is explicitly approved by user
- Output: Numbered steps with file:line references

**Phase 3: IMPLEMENT**
- Follow the approved plan exactly
- Commit all changes within the phase
- Request user approval before marking phase complete

### 2. GitHub Issues for Every Phase

When starting any phase:
1. Create a GitHub issue using `gh issue create`
2. Title format: `[Phase N] {phase-name}: {description}`
3. Label with phase type: `phase:research`, `phase:plan`, `phase:implement`
4. Link to parent issue if exists

### 3. Git Tree Discipline

- Always use git for version control
- Commit frequently within phases
- Commit message format: `[Phase N] {description}`
- Never commit broken code
- Use branches for features: `feature/{issue-number}-{short-desc}`

### 4. Documentation Requirements

Before any implementation, ASK the user:
- "Do you need documentation for this feature?"
- "Should I update the docs/ folder?"
- "Are there API docs or README updates needed?"

Maintain `docs/` folder with:
- API documentation
- Architecture decisions
- Usage examples

### 5. Context Hygiene ("Avoid the Dumb Zone")

**Bug Fix Tracking:**
- Track consecutive failed bug fix attempts
- After 3+ failed attempts, WARN: "We've tried 3 approaches. Consider fresh perspective."
- Suggest: "Chat Nuke - start fresh chat with summary of attempts"

**Context Estimation:**
- Monitor approximate context usage
- At 60%+ estimated context, WARN: "Context is getting full."
- At 80%+, STRONGLY SUGGEST: "Time for Chat Nuke"

**Chat Nuke Protocol:**
When context is exhausted:
1. Generate high-signal summary of:
   - Current task and goal
   - What has been tried (successes and failures)
   - Key file references
   - Next steps
2. Format for copy-paste into new chat

### 6. Amplification and Critical Thinking

**No Blind Compliance:**
- Challenge plans that seem incomplete or risky
- Ask clarifying questions before implementing unclear requirements
- Flag potential issues proactively

**Lead Engineer Mindset:**
- List missing requirements before starting
- Identify edge cases and error scenarios
- Consider performance, security, maintainability
- Prioritize correctness over speed

### 7. Sub-Agent Mindset

When using sub-agents for research or documentation:
- Request high-signal summaries, not data dumps
- Specify output format and length constraints
- Focus on actionable insights

### 8. Error Logging (Automatic)

All significant errors are automatically logged to:
- `docs/lessons-learned.md` - Institutional knowledge
- Format: Date, Error Type, Context, Resolution/Workaround

### 9. Phase Completion Checklist

Before marking any phase complete:
- [ ] All tasks in GitHub issue addressed
- [ ] Code committed (if applicable)
- [ ] Tests pass (if applicable)
- [ ] Documentation updated (if required)
- [ ] User explicitly approves completion
