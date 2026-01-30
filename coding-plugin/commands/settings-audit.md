---
context: fork
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(grep:*), Read, Write
description: Audit repository and generate Claude Code settings.json for Bun + Firebase stack
---

# Settings Audit

Analyze repository and generate recommended `.claude/settings.json` permissions.

## Phase 1: Detect Stack

```bash
echo "🔍 Detecting stack..."

# Bun
ls bun.lock 2>/dev/null && echo "✅ Bun detected"

# Firebase
ls firebase.json 2>/dev/null && echo "🔥 Firebase detected"

# Vite
ls vite.config.ts 2>/dev/null && echo "⚡ Vite detected"

# TypeScript
ls tsconfig.json 2>/dev/null && echo "📘 TypeScript detected"
```

## Phase 2: Detect Services

```bash
echo ""
echo "🔍 Detecting services..."

# Firestore
grep -l "firestore" firebase.json 2>/dev/null && echo "🗄️ Firestore detected"

# Cloud Functions
ls functions/package.json 2>/dev/null && echo "⚙️ Cloud Functions detected"

# Stripe
grep -rl "stripe" functions/src/ 2>/dev/null && echo "💳 Stripe integration detected"
```

## Phase 3: Check Existing Settings

```bash
echo ""
echo "📋 Current settings.json:"
cat .claude/settings.json 2>/dev/null || echo "No settings.json found"
```

## Phase 4: Generate Recommendations

Based on your Firebase + Bun stack, recommended `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(bun:*)",
      "Bash(bunx:*)",
      "Bash(bun test:*)",
      "Bash(bun run:*)",
      "Bash(firebase:*)",
      "Bash(firebase deploy:*)",
      "Bash(firebase emulators:*)",
      "Bash(tsc:*)",
      "Bash(vite:*)",
      "Bash(git:*)",
      "Bash(gh:*)"
    ],
    "deny": ["Bash(firebase projects:delete:*)", "Bash(rm -rf:*)"]
  }
}
```

## Output

```
✅ Settings audit complete

Stack detected:
  - Bun (runtime)
  - Firebase (backend)
  - Vite (frontend)
  - TypeScript

Recommendations:
  - Allow: bun, firebase, vite, tsc, git
  - Deny: destructive firebase commands, rm -rf
```
