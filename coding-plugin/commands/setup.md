---
context: fork
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(grep:*), Bash(mkdir:*), Bash(chmod:*), Read, Write, AskUserQuestion
description: Detect project stack, generate settings.json permissions and deployment scripts
---

# Project Setup

Detect project stack and configure both Claude Code settings and deployment scripts.

## Phase 1: Detect Stack

```bash
echo "═══════════════════════════════════════════════════"
echo "🔍 Detecting project stack..."
echo "═══════════════════════════════════════════════════"
echo ""

# Package manager
ls bun.lock 2>/dev/null && echo "✅ Bun detected"
ls package-lock.json 2>/dev/null && echo "✅ npm detected"
ls pnpm-lock.yaml 2>/dev/null && echo "✅ pnpm detected"
ls pyproject.toml 2>/dev/null && echo "🐍 Python detected"
ls Cargo.toml 2>/dev/null && echo "🦀 Rust detected"
ls go.mod 2>/dev/null && echo "🐹 Go detected"

# Framework
ls next.config.* 2>/dev/null && echo "✅ Next.js detected"
ls vite.config.* 2>/dev/null && echo "✅ Vite detected"

# Deployment targets
ls firebase.json 2>/dev/null && echo "🔥 Firebase detected"
ls Dockerfile 2>/dev/null && echo "🐳 Docker detected"

# TypeScript
ls tsconfig.json 2>/dev/null && echo "📘 TypeScript detected"

# Existing settings
echo ""
echo "📋 Current settings.json:"
cat .claude/settings.json 2>/dev/null || echo "No settings.json found"
```

## Phase 2: Generate Settings

Based on detected stack, generate recommended `.claude/settings.json` permissions.

**Stack → Permissions mapping:**

| Stack       | Allow                                                     | Deny                         |
| ----------- | --------------------------------------------------------- | ---------------------------- |
| Bun         | `bun:*`, `bunx:*`, `bun test:*`, `bun run:*`              | —                            |
| npm         | `npm:*`, `npx:*`                                          | —                            |
| Python (uv) | `uv:*`, `uv run:*`                                        | —                            |
| Firebase    | `firebase:*`, `firebase deploy:*`, `firebase emulators:*` | `firebase projects:delete:*` |
| Docker      | `docker:*`, `docker compose:*`                            | `docker system prune:*`      |
| GCP         | `gcloud:*`                                                | `gcloud projects delete:*`   |
| General     | `git:*`, `gh:*`, `tsc:*`                                  | `rm -rf:*`                   |

Always include the required environment variables:

```json
{
  "plansDirectory": "plans",
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70",
    "CLAUDE_CODE_TASK_LIST_ID": "<project-name>-tasks"
  }
}
```

## Phase 3: Deployment Scripts

Use AskUserQuestion to ask:

1. **Generate deployment scripts?** [Yes / No]
2. If yes: **Deployment target?**
   - Firebase Hosting (if firebase.json detected)
   - GCP Cloud Run
   - Skip (manual deployment)

If user wants deployment scripts, create `scripts/` directory with:

- `scripts/dev.sh` — Local development
- `scripts/deploy-staging.sh` — Staging deployment
- `scripts/deploy-production.sh` — Production (requires "yes" confirmation)

### Firebase Hosting Scripts

**scripts/dev.sh:**

```bash
#!/bin/bash
set -e
echo "🔥 Starting Firebase development server..."
if [ ! -d "node_modules" ]; then bun install; fi
bun run dev
```

**scripts/deploy-staging.sh:**

```bash
#!/bin/bash
set -e
echo "🚀 Deploying to Firebase Hosting (staging)..."
bun run build
firebase deploy --only hosting:staging
echo "✅ Staging deployment complete"
```

**scripts/deploy-production.sh:**

```bash
#!/bin/bash
set -e
if [[ "$1" != "yes" ]]; then
  echo "⚠️  Production deployment requires explicit confirmation"
  echo "Usage: ./scripts/deploy-production.sh yes"
  exit 1
fi
echo "🚀 Deploying to Firebase Hosting (production)..."
bun run build
firebase deploy --only hosting:production
echo "✅ Production deployment complete"
```

### GCP Cloud Run Scripts

**scripts/dev.sh:**

```bash
#!/bin/bash
set -e
echo "🔧 Starting local development server..."
if [ ! -d "node_modules" ]; then bun install; fi
bun run dev
```

**scripts/deploy-staging.sh:**

```bash
#!/bin/bash
set -e
source .env 2>/dev/null || true
SERVICE_NAME="${SERVICE_NAME:-my-service}"
GCP_REGION="${GCP_REGION:-europe-west1}"
GCP_PROJECT="${GCP_PROJECT_STAGING:-}"
if [ -z "$GCP_PROJECT" ]; then echo "❌ GCP_PROJECT_STAGING not set in .env"; exit 1; fi
echo "🚀 Deploying to GCP Cloud Run (staging)..."
gcloud run deploy "${SERVICE_NAME}-staging" --source . --region "$GCP_REGION" --project "$GCP_PROJECT" --allow-unauthenticated --cpu 1 --memory 512Mi --min-instances 0 --max-instances 3
echo "✅ Staging deployment complete"
```

**scripts/deploy-production.sh:**

```bash
#!/bin/bash
set -e
if [[ "$1" != "yes" ]]; then
  echo "⚠️  Production deployment requires explicit confirmation"
  echo "Usage: ./scripts/deploy-production.sh yes"
  exit 1
fi
source .env 2>/dev/null || true
SERVICE_NAME="${SERVICE_NAME:-my-service}"
GCP_REGION="${GCP_REGION:-europe-west1}"
GCP_PROJECT="${GCP_PROJECT_PROD:-}"
if [ -z "$GCP_PROJECT" ]; then echo "❌ GCP_PROJECT_PROD not set in .env"; exit 1; fi
echo "🚀 Deploying to GCP Cloud Run (production)..."
bun test
gcloud run deploy "$SERVICE_NAME" --source . --region "$GCP_REGION" --project "$GCP_PROJECT" --min-instances 1 --max-instances 10 --cpu 2 --memory 1Gi --cpu-boost
echo "✅ Production deployment complete"
```

After generating scripts:

```bash
chmod +x scripts/*.sh
```

## Phase 4: Update CLAUDE.md

If deployment scripts were generated, append deployment docs to `.claude/CLAUDE.md`.

## Output

```
═══════════════════════════════════════════════════
✅ Project setup complete
═══════════════════════════════════════════════════

Settings:
  📄 .claude/settings.json (permissions generated)

Deployment:
  📄 scripts/dev.sh
  📄 scripts/deploy-staging.sh
  📄 scripts/deploy-production.sh

Next steps:
  1. Review .claude/settings.json
  2. Set environment variables in .env (if using Cloud Run)
  3. Run ./scripts/dev.sh to start development
```
