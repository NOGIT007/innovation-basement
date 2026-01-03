---
allowed-tools: Read, Write, AskUserQuestion, Glob
description: Interview user to develop vague ideas into comprehensive 1.0 specs
argument-hint: <spec-file-path>
---

# Interview: Develop Idea into 1.0 Spec

Spec file: $ARGUMENTS

## Step 1: Load Source Spec

Read the input file:
```
Read $ARGUMENTS
```

If file doesn't exist: Error "File not found: $ARGUMENTS"

Extract:
- What's already defined (context for interview)
- What's vague or missing (focus interview here)

## Step 2: Interview

Read the spec and interview me in detail using AskUserQuestion about literally anything:
- Technical implementation
- UI & UX decisions
- Concerns and risks
- Tradeoffs and edge cases
- Dependencies and assumptions
- Verification criteria

Rules:
- Questions must NOT be obvious
- Be very in-depth
- Continue interviewing until the spec is complete

## Step 3: Write Spec

Output: `interview_YYYY-MM-DD.md` in project root

```markdown
# [Project Name] - 1.0 Specification

*Generated from interview on [date]*
*Source: [original-file]*

## Vision

[1-2 paragraphs synthesized from interview]

## Success Criteria

- [ ] [Measurable outcome from interview]
- [ ] [Measurable outcome from interview]

## User Stories

### Primary Flow
[Step-by-step from interview]

### Error Handling
[What happens when things go wrong]

## Technical Scope

### In Scope (1.0)
[Features that ARE in 1.0]

### Out of Scope (Future)
[Explicit exclusions]

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Platform | [From interview] | [Why] |
| [Other] | [Choice] | [Why] |

## Dependencies & Assumptions

### Prerequisites
[What must exist before this works]

### Assumptions
[Things assumed true]

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [From interview] | High/Medium/Low | [Approach] |

## Verification Plan

- [ ] [How to test]
- [ ] [Demo criteria]

## Open Questions

- [ ] [Unresolved items from interview]

---

*Ready for `/plan-issue` to create implementation phases*
```

State: "Spec written to: interview_YYYY-MM-DD.md"

## Rules

- **Non-destructive**: Never overwrite original spec
- **Deep questions**: No surface-level/obvious questions
- **Continue until done**: No question limit
- **Actionable output**: Spec ready for `/plan-issue`
