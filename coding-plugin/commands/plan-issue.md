---
allowed-tools: Bash(gh issue create:*), Bash(gh issue list:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Read, Grep, Glob, Task, AskUserQuestion, mcp__typescript-lsp__*
description: Research codebase with LSP precision, plan feature with phases, create GitHub issue
argument-hint: [feature-description]
---

# Feature Planning & GitHub Issue Creation

Feature to plan: $ARGUMENTS

## Step 0: Verify Target Repo

Check current project repo (issue will be created here):
```bash
git remote -v
```

## Step 0.5: Capture Existing Plan from Session

If a plan already exists in the **current conversation context** (e.g., from plan mode):

### Detection Criteria
Look for ANY of these in conversation:
- File paths with line numbers (`src/file.ts:42`)
- Function/type references (`functionName()`, `interface X`)
- Implementation phases or steps
- Plan mode output or architecture decisions

### Extraction Process (CRITICAL)
When plan exists, **extract and preserve ALL details**:

1. **Code References** - Capture every `file:line` mention
   ```
   Example: src/api/handler.ts:42 → processData()
   ```

2. **Type Information** - Preserve interface/type details
   ```
   Example: interface UserData at types/user.ts:15
   ```

3. **Code Snippets** - Include relevant code blocks from plan
   ```typescript
   // Example snippet that was discussed
   function existingPattern() { ... }
   ```

4. **Dependencies** - Note all file relationships discovered

5. **Risks/Edge Cases** - Carry forward any warnings

### Output Format for Issue
Transform plan into structured issue content:

```markdown
## Research Summary (from plan mode)

### Files Analyzed
| File | Lines | Purpose |
|------|-------|---------|
| `src/file.ts` | 42-58 | Entry point for feature |
| `types/index.ts` | 15 | Type definitions |

### Key Code References
- `processData()` at `src/handler.ts:42` - needs modification
- `UserData` interface at `types/user.ts:15` - extend with new field

### Discovered Patterns
\`\`\`typescript
// Pattern found at src/utils.ts:23
export function existingPattern() {
  // Follow this style
}
\`\`\`
```

State: "Using existing plan from this session. Preserving X file references."

If no existing plan in session → proceed with full research workflow.

## Step 0.6: Read Project Lessons

Check for LESSONS.md in project root:
```bash
cat LESSONS.md 2>/dev/null
```

If exists:
- Note patterns to follow
- Note mistakes to avoid
- Include relevant lessons in issue context

## Step 0.7: Check Lessons Age

If LESSONS.md older than 30 days:
```bash
stat -f "%Sm" LESSONS.md 2>/dev/null
```

Suggest: "LESSONS.md is stale. Run `/code:lessons` to refresh."

## Step 0.8: Read Project Constitution

Check for constitution.md in project root:
```bash
cat constitution.md 2>/dev/null
```

If exists:
- Note core principles to follow
- Note boundaries (in/out scope)
- Note non-negotiables
- Include relevant principles in issue "Context" section

## Phase 1: Research (LSP-Precise) — Skip if plan exists in session

Research the **current project** codebase with LSP precision:

1. **Find entry points** - Grep for feature patterns
2. **LSP: Go to definition** - Use typescript-lsp to trace exact types/functions
3. **LSP: Find references** - Locate all usages of affected code
4. **Trace data flow** - Document: Entry → Transform → Exit with file:line
5. **Check types** - Use LSP to understand interfaces/types involved
6. **Find patterns** - Look for similar implementations to follow

Document with **file:line precision**:
- Exact locations: `src/api/handler.ts:42`
- Function signatures: `processData(input: InputType): OutputType`
- Type definitions: `interface UserData` at `types/user.ts:15`
- Dependencies and imports
- Risks and edge cases

## Phase 2: Plan

Break into phases:
- Each phase = independently testable
- Order by dependency
- List specific files per phase

## Phase 3: Confirm

Show plan to user. Ask: **"Create issue in [repo-name]?"**

Wait for confirmation.

## Phase 4: Create Issue

Create in **current project repo**:

```bash
gh issue create --title "[Feature] $ARGUMENTS" --body "..."
```

Issue format:
```markdown
## Goal
[1-2 sentences]

## Context

### From LESSONS.md
- Avoid: [relevant lesson if applicable]
- Pattern: [relevant pattern if applicable]

### From constitution.md (if exists)
- Principles: [relevant principles]
- Boundaries: [in/out scope constraints]

## Research Summary

### Files Analyzed
| File | Lines | Purpose |
|------|-------|---------|
| `src/file.ts` | 42-58 | [what this file does] |
| `types/index.ts` | 15-30 | [type definitions] |

### Key Code References
- `functionName()` at `src/handler.ts:42` - [what needs to change]
- `InterfaceName` at `types/user.ts:15` - [how to extend]

### Existing Patterns to Follow
```typescript
// Found at src/utils.ts:23-30
// Copy this pattern for consistency
export function existingPattern(input: Type): ReturnType {
  // implementation details
}
```

## Data Flow
```
Entry: `file.ts:line` (functionName)
  → Transform: `file.ts:line` (processData)
  → Exit: `file.ts:line` (returnHandler)
```

## Implementation Phases

### Phase 1: [name]
**Files:**
| File | Lines | Change |
|------|-------|--------|
| `file1.ts` | 42 | Modify `functionName()` to add X |
| `file2.ts` | 15-20 | Update interface `TypeName` |

**Code Changes:**
```typescript
// file1.ts:42 - Before
export function functionName() { ... }

// file1.ts:42 - After
export function functionName(newParam: Type) { ... }
```

**Tasks:**
- [ ] Modify `functionName()` at `file1.ts:42` to accept new parameter
- [ ] Add `newField: Type` to `TypeName` at `file2.ts:15`
- [ ] Update imports at `file3.ts:5`

**Verification:**
- [ ] `bun run typecheck` passes
- [ ] `bun run test` passes

### Phase 2: [name]
**Files:**
| File | Lines | Change |
|------|-------|--------|
| `file3.ts` | 10 | Add new function |

**Tasks:**
- [ ] Create `newFunction()` following pattern at `utils.ts:23`

**Verification:**
- [ ] [Specific test or check]

## Risks & Edge Cases
- [ ] Risk: [description] - Mitigation: [approach]
- [ ] Edge case: [description] at `file.ts:line`

---

Created with `/plan-issue` (LSP-precise)
```

Output issue URL for `/code/implement #<number>`.
