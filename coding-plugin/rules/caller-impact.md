# Caller Impact Rules

> Auto-loaded by `/code:plan-issue`

## When to Check for Callers

Before modifying any function/method, check if changes affect callers:

| Change Type                | Impact                         |
| -------------------------- | ------------------------------ |
| Parameter added/removed    | All callers must update        |
| Parameter type changed     | Callers may pass wrong type    |
| Return type changed        | Callers may handle incorrectly |
| Function renamed           | All imports/calls break        |
| Exception behavior changed | Callers may not catch          |

## Finding Callers

Use grep before making breaking changes:

```bash
# Find all callers of a function
grep -r "functionName(" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" .
```

## Required Actions

1. **Before changing signature:** Run grep to count callers
2. **If callers exist:** Update all call sites in same commit
3. **If many callers:** Consider adding new function, deprecate old

## Flags

- Breaking function signature without updating callers
- Renaming without searching for usages
- Changing return type without checking consumers
