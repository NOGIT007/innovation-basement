---
description: Initialize a new coding workflow. Sets up project context and asks initial questions.
---

Initialize new coding workflow for: $ARGUMENTS

## Initialization Protocol

1. **Context Setup**
   - Identify project repository
   - Check for existing `docs/lessons-learned.md`
   - Review recent git history

2. **Documentation Check**
   ASK USER:
   - "Do you need documentation for this feature?"
   - "Should I update existing docs?"
   - "Is there an architecture decision to record?"

3. **Scope Definition**
   ASK USER:
   - "What is the specific goal?"
   - "Are there constraints or requirements?"
   - "What does 'done' look like?"

4. **Git Setup**
   - Verify clean working tree
   - Identify base branch
   - Plan feature branch name

5. **Begin Research Phase**
   After setup, automatically transition to Research phase.
