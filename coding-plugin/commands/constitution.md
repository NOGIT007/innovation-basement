---
allowed-tools: Read, Write, AskUserQuestion, Bash(ls:*)
description: Interview user to create project principles (constitution.md)
argument-hint: (no arguments)
---

# Constitution: Define Project Principles

Creates `constitution.md` at project root via interview.

## Step 1: Check Existing

```bash
ls constitution.md 2>/dev/null
```

If exists:
- Ask: "constitution.md already exists. Overwrite?"
- Options: Yes (continue) / No (abort)

If no: abort with "Keeping existing constitution.md"

## Step 2: Get Project Name

```
Question: "What's the project name?"
Options:
- [Infer from folder name]
- [Infer from package.json/pyproject.toml if exists]
- Other (enter name)
```

## Step 3: Interview - Core Values

```
Question: "What matters most for this project?"
Options:
- Simplicity over features
- Correctness over speed
- User experience over technical elegance
- Stability over innovation
- Other (describe)
multiSelect: true (pick up to 3)
```

```
Question: "How should decisions be made?"
Options:
- Smallest change wins
- User benefit drives choice
- Technical debt avoided at all costs
- Ship fast, fix later
- Other (describe)
```

## Step 4: Interview - Boundaries

```
Question: "What's explicitly IN scope?"
Options:
- Core functionality only
- Full feature set
- MVP then iterate
- Other (describe)
```

```
Question: "What's explicitly OUT of scope?"
Options:
- Advanced/power-user features
- Multiple platform support
- Backwards compatibility
- Performance optimization
- Other (describe)
multiSelect: true
```

## Step 5: Interview - Priorities

```
Question: "When facing tradeoffs, what wins?"
Options:
- Working > Perfect
- Simple > Powerful
- Stable > Fast
- Documented > Clever
- Other (describe)
```

```
Question: "Second priority?"
Options:
- [Remaining from above]
```

```
Question: "Third priority?"
Options:
- [Remaining from above]
```

## Step 6: Interview - Non-Negotiables

```
Question: "What rules never bend?"
Options:
- Tests must pass before commit
- No breaking changes without migration
- All code reviewed before merge
- Documentation required for public APIs
- Security issues fixed immediately
- Other (describe)
multiSelect: true
```

## Step 6.5: Interview - Verification Strategy

```
Question: "How should code be verified before completion?"
Options:
- Tests must pass (automated)
- Manual testing sufficient
- Type checking only
- No verification needed
- Other (describe)
```

```
Question: "What test framework does this project use?"
Options:
- Jest / Vitest (JavaScript)
- Bun test
- Pytest (Python)
- Cargo test (Rust)
- Make test
- None / Will set up later
- Other (describe)
```

```
Question: "When should tests run?"
Options:
- Before every commit
- Before marking tasks complete
- Before merging PRs only
- Manually when needed
- Other (describe)
```

## Step 7: Write Constitution

Write to project root: `constitution.md`

```markdown
# [Project Name] Constitution

## Core Principles

### 1. [First Value]
[What this means: when X happens, we do Y]

### 2. [Second Value]
[What this means: when X happens, we do Y]

### 3. [Third Value]
[What this means: when X happens, we do Y]

## Boundaries

### In Scope
- [What we do]
- [What we do]

### Out of Scope
- [What we explicitly don't do]
- [What we explicitly don't do]

## Decision Framework

When facing tradeoffs:
1. [First priority] - always wins
2. [Second priority] - if first is equal
3. [Third priority] - tiebreaker

## Non-Negotiables

These rules never bend:
- [Hard rule 1]
- [Hard rule 2]
- [Hard rule 3]

## Verification Strategy

### Test Requirement
[From interview: automated/manual/type-only/none]

### Test Command
```bash
[detected or specified test command]
```

### Verification Points
- [When tests must run]
- [What must pass before completion]

---

Version: 1.0 | Created: [date]
```

## Step 8: Summary

State:
- "Constitution written to: constitution.md"
- "Key principles: [2-3 bullet summary]"
- "`/plan-issue` will now auto-read this for context"

## Rules

- **One per project**: Only one constitution.md at root
- **Multi-choice**: Use AskUserQuestion with options
- **Short interview**: 8-12 questions max
- **Actionable output**: Principles that guide `/plan-issue`
