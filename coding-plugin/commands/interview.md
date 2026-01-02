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
- Project name/title
- What's already defined (skip in interview)
- What's vague or missing (focus here)

## Step 2: Interview Phase

Interview across 6 categories using AskUserQuestion with multi-choice options.

For each category:
1. Check what spec already covers → skip those
2. Ask 2-4 probing questions
3. Follow up on vague answers

### Category 1: Core Vision

Skip if already clear. Otherwise ask:

```
Question: "What problem does this solve?"
Options:
- Automates manual process
- Enables new capability
- Improves existing workflow
- Other (describe)
```

```
Question: "Who is the primary user?"
Options:
- Developers
- End users/consumers
- Internal team
- Other (describe)
```

```
Question: "What's the single most important outcome for 1.0?"
Options:
- Working MVP (feature complete)
- Production ready (stable, tested)
- User validated (feedback incorporated)
- Other (describe)
```

### Category 2: User Experience

Skip if already clear. Otherwise ask:

```
Question: "What's the primary user flow?"
Options:
- Single action (click/command → result)
- Multi-step wizard
- Dashboard/monitoring
- Other (describe)
```

```
Question: "What happens when something goes wrong?"
Options:
- Show error message, user retries
- Automatic retry with fallback
- Fail silently, log for later
- Other (describe)
```

### Category 3: Technical Boundaries

Skip if already clear. Otherwise ask:

```
Question: "What's explicitly OUT of scope for 1.0?"
Options:
- Multi-user/auth
- Mobile support
- Offline mode
- Other (describe)
```

```
Question: "Platform constraints?"
Options:
- Web only
- CLI/terminal
- Desktop app
- Cross-platform
```

```
Question: "Performance requirements?"
Options:
- Fast (< 1s response)
- Moderate (< 5s acceptable)
- Background processing OK
- No specific requirements
```

### Category 4: Risks & Tradeoffs

Skip if already clear. Otherwise ask:

```
Question: "Biggest risk to this project?"
Options:
- Technical complexity
- Unclear requirements
- External dependencies
- Time constraints
- Other (describe)
```

```
Question: "What tradeoffs are acceptable for 1.0?"
Options:
- Less features, more stability
- Manual steps over automation
- Limited scale initially
- Other (describe)
```

### Category 5: Dependencies

Skip if already clear. Otherwise ask:

```
Question: "What must exist before this works?"
Options:
- Nothing (standalone)
- Existing API/service
- Database/storage
- Other system (describe)
```

```
Question: "External services needed?"
Options:
- None
- Auth provider (OAuth, etc)
- Cloud storage
- Third-party API
- Other (describe)
```

### Category 6: Verification

Skip if already clear. Otherwise ask:

```
Question: "How will you know 1.0 is complete?"
Options:
- All tests pass
- Manual QA checklist
- User acceptance sign-off
- Demo to stakeholders
```

```
Question: "What does a successful demo look like?"
Options:
- Single feature walkthrough
- Full user journey
- Performance benchmark
- Other (describe)
```

## Step 3: Write Improved Spec

Determine output path:
- Input: `path/to/idea.md`
- Output: `path/to/idea-spec.md`

Write comprehensive spec:

```markdown
# [Project Name] - 1.0 Specification

*Generated from interview on [date]*
*Source: [original-file]*

## Vision

[1-2 paragraphs synthesized from Category 1]

## Success Criteria

- [ ] [Measurable outcome from interview]
- [ ] [Measurable outcome from interview]

## User Stories

### Primary Flow
[From Category 2: step-by-step]

### Error Handling
[From Category 2: what happens when wrong]

## Technical Scope

### In Scope (1.0)
[Features that ARE in 1.0]

### Out of Scope (Future)
[From Category 3: explicit exclusions]

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Platform | [From interview] | [Why] |
| [Other] | [Choice] | [Why] |

## Dependencies & Assumptions

### Prerequisites
[From Category 5]

### Assumptions
[Things assumed true]

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [From Category 4] | High/Medium/Low | [Approach] |

## Verification Plan

- [ ] [From Category 6: how to test]
- [ ] [Demo criteria]

## Open Questions

- [ ] [Unresolved items from interview]

---

*Ready for `/plan-issue` to create implementation phases*
```

## Step 4: Summary

State:
- "Improved spec written to: [output-path]"
- Brief summary of key insights (2-3 bullets)
- "Next step: `/plan-issue [feature-summary]`"

## Rules

- **Non-destructive**: Never overwrite original spec
- **Skip answered**: Don't ask what's clear in spec
- **Multi-choice**: Use AskUserQuestion with options
- **15-25 questions max**: Respect user's time
- **Actionable output**: Spec ready for `/plan-issue`
