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

## Phase 1.5: Content Specification

Before planning, you MUST have **exact content** for every change.

### Rule: Read Before Write (No Exceptions)

For EVERY file you'll modify (including trivial changes like imports/typos):
1. Read the current content with `Read` tool
2. Find similar patterns in codebase (if creating new)
3. Draft exact before/after content

**No exceptions.** Even imports, typos, and renames need before/after.

**If you can't write exact content → you haven't researched enough. Go back to Phase 1.**

### For New Files

```markdown
**Create:** `path/to/new-file.ts`

**Full content:**
\`\`\`typescript
// Complete file content - NOT a summary or placeholder
export function newFunction(param: Type): ReturnType {
  // Actual implementation code
  return result;
}
\`\`\`

**Pattern source:** Based on `similar-file.ts:15-40`
```

### For Modifications

```markdown
**Modify:** `path/to/file.ts:42-55`

**Before:**
\`\`\`typescript
// Exact current content copied from file
export function existing() {
  return oldBehavior();
}
\`\`\`

**After:**
\`\`\`typescript
// Exact replacement content
export function existing(newParam: Type) {
  return newBehavior(newParam);
}
\`\`\`
```

### Validation Checklist

Before proceeding to Phase 2:
- [ ] Every modified file has been read with `Read` tool
- [ ] Every new file has complete content (not placeholders)
- [ ] Every modification shows exact before/after code
- [ ] Patterns sourced from existing codebase

## Phase 2: Plan (Using Specified Content)

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
| `file1.ts` | 42-50 | Modify `functionName()` |
| `file2.ts` | 15-20 | Update interface `TypeName` |

**Exact Changes:**

<details>
<summary><code>file1.ts:42</code> - Modify functionName</summary>

**Before:**
```typescript
export function functionName() {
  return oldLogic();
}
```

**After:**
```typescript
export function functionName(newParam: Type) {
  validateParam(newParam);
  return newLogic(newParam);
}
```

</details>

<details>
<summary><code>file2.ts:15</code> - Update TypeName interface</summary>

**Before:**
```typescript
interface TypeName {
  existingField: string;
}
```

**After:**
```typescript
interface TypeName {
  existingField: string;
  newField: Type;
}
```

</details>

**Tasks:**
- [ ] Apply change to `functionName()` at `file1.ts:42`
- [ ] Add `newField` to `TypeName` at `file2.ts:15`
- [ ] Update imports at `file3.ts:5`

**Verification:**
- [ ] `bun run typecheck` passes
- [ ] `bun run test` passes

### Phase 2: [name]
**Files:**
| File | Lines | Change |
|------|-------|--------|
| `file3.ts` | new | Add new function |

**Exact Changes:**

<details>
<summary><code>file3.ts</code> - Create newFunction</summary>

**Create:**
```typescript
// Full implementation - not a placeholder
export function newFunction(input: InputType): OutputType {
  const processed = transform(input);
  return { result: processed };
}
```

**Pattern source:** `utils.ts:23-35`

</details>

**Tasks:**
- [ ] Create `newFunction()` in `file3.ts`

**Verification:**
- [ ] [Specific test or check]

## Risks & Edge Cases
- [ ] Risk: [description] - Mitigation: [approach]
- [ ] Edge case: [description] at `file.ts:line`

---

Created with `/plan-issue` (LSP-precise)
```

Output issue URL for `/code/implement #<number>`.
