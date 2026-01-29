---
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
description: Deep requirement clarification for plan refinement
argument-hint: [plan-file]
---

# Interview: Deep Requirement Clarification

Clarify ambiguous requirements through structured questioning. Use between `/plan` and `/code:plan-issue`.

## Step 1: Find Plan File

Find the most recent plan in the plans directory:

```
Glob: plans/*.md
```

**If no plans found:**

```
ERROR: No plan files found in plans/ directory.

Run `/plan <your idea>` first to create a plan, then run `/code:interview` to clarify requirements.
```

Stop here if no plan exists.

**If multiple plans found:**

Select the most recently modified file (by modification date).

**If argument provided:**

If `$ARGUMENTS` contains a specific file path, use that plan instead.

## Step 2: Load Context

1. **Read the plan file** - Get full content
2. **Note conversation context** - Any relevant discussion from current session
3. **Merge contexts** - If both exist, note any conflicts to ask about

**If context conflict detected:**

Add to first round of questions: "The plan says X but you mentioned Y earlier. Which should we follow?"

## Step 3: Analyze for Ambiguities

Perform breadth-first analysis. Scan the entire plan for areas needing clarification:

### Categories to Check

| Category        | Look For                                                 |
| --------------- | -------------------------------------------------------- |
| **Scope**       | Vague boundaries, "etc.", "and more", undefined limits   |
| **Technical**   | Unspecified tech choices, missing architecture decisions |
| **Data**        | Undefined formats, storage unclear, validation rules     |
| **UI/UX**       | Missing interaction details, layout gaps, state handling |
| **Edge Cases**  | Error handling unclear, boundary conditions              |
| **Integration** | API contracts, external dependencies, auth flows         |
| **Performance** | Scale requirements, optimization needs                   |

Build a list of ambiguous areas, prioritized by:

1. Blocking decisions (can't proceed without answer)
2. High-impact choices (affects multiple tasks)
3. Clarifications (nice to have detail)

## Step 4: Interview Loop

### Question Strategy

- **Questions per round:** 2-3 related questions grouped together
- **Style:** Breadth first - touch all ambiguous areas, then cycle back for depth
- **Inference:** Moderate - infer related concerns from mentioned items

### Asking Questions

For each round, use **AskUserQuestion** with 2-3 related questions:

```
AskUserQuestion:
  questions:
    - question: "[Clear, specific question]?"
      header: "[Category]"
      options:
        - label: "[Option A]"
          description: "[What this means]"
        - label: "[Option B]"
          description: "[What this means]"
        - label: "[Option C] (if needed)"
          description: "[What this means]"
      multiSelect: false
```

**Question guidelines:**

- Be specific, not abstract
- Provide concrete options when possible
- Adjust technical language to match user's apparent expertise
- Group related questions in the same round

### Handling "Other" Selection

If user selects "Other" and provides custom input:

1. Ask a follow-up clarifying question to ensure understanding
2. Confirm interpretation: "So you mean [interpretation]?"
3. Only proceed when clarified

### Stopping Condition

Continue until user explicitly says one of:

- `done`
- `stop`
- `enough`

Do NOT auto-detect when "enough" questions have been asked. Keep cycling through ambiguous areas until explicit stop command.

## Step 5: Update Plan

When user says stop:

### Merge Strategy

1. **Read existing plan** - Check for existing `## Details` section
2. **If exists:** Merge new answers into existing section
   - Keep existing content that wasn't contradicted
   - Add new information
   - Update changed items
3. **If not exists:** Create new `## Details` section

### Output Format

Add/update `## Details` section in the plan file:

```markdown
## Details

### [Category 1]

- **[Question topic]:** [Answer/decision]
- **[Question topic]:** [Answer/decision]

### [Category 2]

- **[Question topic]:** [Answer/decision]
```

**Rules:**

- Clean output, no source tracking
- Simple section name (`## Details`)
- Natural integration with existing plan structure
- Only save on completion (not partial saves)

## Step 6: Completion

Minimal confirmation:

```
✓ Plan updated with interview details.

[N] questions answered across [M] categories.

Next: Run `/code:plan-issue` to create the GitHub issue.
```

## Rules

- **Require plan file** - Error with guidance if none found
- **Breadth first** - Touch all areas before going deep
- **Explicit stop only** - No auto-detection of completion
- **No plan-issue enforcement** - Interview is optional, don't warn if skipped
- **Save on completion** - Don't save partial interview state
- **Merge intelligently** - Preserve existing Details, add/update
