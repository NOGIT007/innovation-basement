---
allowed-tools: Bash(gh issue create:*), Bash(gh issue list:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Read, Grep, Glob, Task, AskUserQuestion, mcp__typescript-lsp__*
description: Research codebase with LSP precision, plan feature with phases, create GitHub issue
argument-hint: [feature-description] [@spec-file]
---

# Feature Planning & GitHub Issue Creation

Feature to plan: $ARGUMENTS

> 💡 **Tip:** Include `@file` references to provide specs or context (e.g., `/plan-issue add auth @spec.md`)

## Step 0: Verify Target Repo

Check current project repo (issue will be created here):
```bash
git remote -v
```

## Step 0.5: Load Existing Plan

Check for plan sources in order:

**1. File reference in arguments:**
If `$ARGUMENTS` contains `@SPEC.md` or similar file reference:
- Claude Code expands `@file` automatically
- Use the expanded content as primary context
- Skip Phase 1 research

**2. Project SPEC.md:**
```bash
cat SPEC.md 2>/dev/null
```

If found:
- Read the file
- Use as primary context for issue
- Skip Phase 1 research

**3. Claude Code plan file:**
```bash
ls ~/.claude/plans/*.md 2>/dev/null
```

If found:
- Read the most recent file
- Use as primary context for issue
- Skip Phase 1 research

**If NONE found:**
- Proceed to Phase 1 research (explore codebase)
- Generate plan from scratch based on `$ARGUMENTS`

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

## Phase 1: Research (LSP-Precise) — Skip if plan exists

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

**Rules:**
1. **Read First:** MUST read every file you intend to modify (no exceptions)
2. **No Placeholders:** New files have full executable content. No `// ... rest`
3. **Exact Diffs:** Modifications show exact before/after from actual file content
4. **No Summaries:** Markdown files have complete content, no `[placeholder]` text
5. **Sizing:** Each phase fits within 55% context window

**If you can't write exact content → research more (Phase 1).**

**Validation (all must be true before Phase 2):**
- [ ] Every modified file read with `Read` tool
- [ ] Every new file has complete content
- [ ] Every modification has exact before/after
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

Create in **current project repo**.

### ⚠️ CRITICAL: No Heredocs

Heredocs fail silently in sandbox → empty issue body. **Use Write tool instead.**

### Step 4.1: Write Body File (Use Write Tool)

Use Claude's **Write tool** to create `.claude-issue-body.md` with full issue content (see format below).

**Do NOT use heredocs or `cat <<EOF`** — they fail silently.

### Step 4.2: Validate Body (REQUIRED)

Before creating, verify the file exists and isn't empty:

```bash
if [ ! -s .claude-issue-body.md ]; then
  echo "❌ ERROR: .claude-issue-body.md is empty or missing."
  echo "Use Write tool to create the file first."
  exit 1
fi
echo "✅ Body validated ($(wc -l < .claude-issue-body.md) lines)"
```

**If validation fails:** Use Write tool to create `.claude-issue-body.md`, then retry.

### Step 4.3: Create Issue with Body File

```bash
gh issue create --title "[Feature] $ARGUMENTS" --body-file .claude-issue-body.md
```

> **Note:** `.claude-issue-body.md` is gitignored and overwritten each time. No cleanup needed.

Issue format:
```markdown
## Goal
[1-2 sentences]

## Context

### From LESSONS.md
- Avoid: [relevant lesson if applicable]
- Pattern: [relevant pattern if applicable]

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

## Phase 4.5: Create Feature Branch

After issue created:

1. Extract issue number from URL
2. Create branch:
   ```bash
   ISSUE_NUM=<from issue URL>
   SLUG=$(echo "$ARGUMENTS" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | cut -c1-30)
   BRANCH="feature/${ISSUE_NUM}-${SLUG}"
   git checkout -b "$BRANCH"
   git push -u origin "$BRANCH"
   ```
3. Output: "Created branch: $BRANCH"

## Phase Sizing Guidance

When creating phases, aim for ~55% context usage per phase:
- Each phase should be completable within 55% of context window
- Enables auto-handover without mid-phase interruption
- If a phase is too large, split into sub-phases

## Next Steps

After branch is created, implement with `/implement #<number>`.

**Git Commands Available:**
- `/commit` - Auto-generate conventional commit from staged changes
- `/pr` - Create PR with auto-generated description

Output issue URL for `/code/implement #<number>`.
