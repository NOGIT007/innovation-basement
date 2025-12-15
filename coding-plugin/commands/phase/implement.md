---
description: Start the Implementation phase. Follows approved plan exactly.
---

Start IMPLEMENT phase for: $ARGUMENTS

## Phase Protocol

1. **Create GitHub Issue**
   Run: `gh issue create --title "[Implement] $ARGUMENTS" --label "phase:implement" --body "Implementation phase for: $ARGUMENTS"`

2. **Prerequisites**
   - Plan phase MUST be complete
   - Plan MUST be explicitly approved by user

3. **Implementation Rules**
   - Follow the approved plan EXACTLY
   - If plan needs changes, STOP and discuss
   - Commit after each logical unit of work
   - Use branch: `feature/{issue-number}-{short-desc}`

4. **Git Discipline**
   - Create feature branch
   - Commit message format: `[Implement] Step N: {description}`
   - Keep commits atomic and focused

5. **Quality Checks**
   - Run tests after each step
   - Check for lint errors
   - Verify functionality works

6. **Phase Completion**
   - All plan steps complete
   - Tests passing
   - Documentation updated
   - User explicitly approves
   - Merge/close GitHub issue
