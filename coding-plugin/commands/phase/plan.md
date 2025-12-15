---
description: Start the Planning phase. Creates detailed implementation plan with code/file references.
---

Start PLAN phase for: $ARGUMENTS

## Phase Protocol

1. **Create GitHub Issue**
   Run: `gh issue create --title "[Plan] $ARGUMENTS" --label "phase:plan" --body "Planning phase for: $ARGUMENTS"`

2. **Prerequisites**
   - Research phase MUST be complete
   - All assumptions MUST be verified

3. **Planning Requirements**
   Create detailed plan including:
   - Numbered steps
   - Specific file paths to create/modify
   - Code snippets ready for implementation
   - Test cases to write
   - Documentation to update

4. **Plan Format**

```markdown
## Implementation Plan: {Feature}

### Prerequisites
- [ ] Research complete and approved
- [ ] Dependencies identified

### Steps

#### Step 1: {Description}
**Files:** `path/to/file.ts`
**Action:** Create | Modify | Delete
**Code:**
```typescript
// Code snippet
```

#### Step 2: {Description}
...

### Tests
- [ ] Test case 1: {description}
- [ ] Test case 2: {description}

### Documentation
- [ ] Update: {doc file}
```

5. **CRITICAL: NO CODE UNTIL APPROVED**
   - Present plan to user
   - Get explicit "approved" or "proceed" confirmation
   - Do NOT write any code until approval received
