---
context: fork
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(mkdir:*), Read, Write, AskUserQuestion
description: Generate deployment scripts based on detected project stack
---

# Init Deployment

Generate deployment scripts for Firebase Hosting or GCP Cloud Run based on detected project stack.

## Phase 1: Detect Stack

```bash
echo "═══════════════════════════════════════════════════"
echo "🔍 Detecting stack..."
echo "═══════════════════════════════════════════════════"
echo ""

# Package manager
ls bun.lock 2>/dev/null && echo "✅ Bun detected (bun.lock)"
ls package-lock.json 2>/dev/null && echo "✅ npm detected (package-lock.json)"
ls pnpm-lock.yaml 2>/dev/null && echo "✅ pnpm detected (pnpm-lock.yaml)"

# Framework
ls next.config.* 2>/dev/null && echo "✅ Next.js detected (next.config.*)"
ls vite.config.* 2>/dev/null && echo "✅ Vite detected (vite.config.*)"

# Deployment targets
ls firebase.json 2>/dev/null && echo "✅ Firebase detected (firebase.json)"
ls Dockerfile 2>/dev/null && echo "✅ Docker detected (Dockerfile)"

# Frontend directory
ls -d web/ 2>/dev/null && echo "📁 Frontend directory: web/"
ls -d app/ 2>/dev/null && echo "📁 Frontend directory: app/"
ls -d src/ 2>/dev/null && echo "📁 Source directory: src/"
```

## Phase 2: Interactive Prompts

Use AskUserQuestion to get deployment preferences:

1. **Deployment target?**
   - Firebase Hosting (if firebase.json detected)
   - GCP Cloud Run

2. **Require TypeScript check before production?** [Y/n]

3. **Create Dockerfile?** (if Cloud Run selected and no Dockerfile exists) [Y/n]

## Phase 3: Generate Scripts

Create `scripts/` directory with deployment scripts based on selections.

### Firebase Hosting Scripts

**scripts/dev.sh:**

```bash
#!/bin/bash
set -e

echo "🔥 Starting Firebase development server..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  bun install
fi

# Start development
bun run dev
```

**scripts/deploy-staging.sh:**

```bash
#!/bin/bash
set -e

echo "🚀 Deploying to Firebase Hosting (staging)..."

# Build
bun run build

# Deploy to staging
firebase deploy --only hosting:staging

echo "✅ Staging deployment complete"
```

**scripts/deploy-production.sh:**

```bash
#!/bin/bash
set -e

# Safety gate
if [[ "$1" != "yes" ]]; then
  echo "⚠️  Production deployment requires explicit confirmation"
  echo "Usage: ./scripts/deploy-production.sh yes"
  exit 1
fi

echo "🚀 Deploying to Firebase Hosting (production)..."

# TypeScript check (if enabled)
# bun run typecheck

# Build
bun run build

# Deploy to production
firebase deploy --only hosting:production

echo "✅ Production deployment complete"
```

### GCP Cloud Run Scripts

**scripts/dev.sh:**

```bash
#!/bin/bash
set -e

echo "🔧 Starting local development server..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  bun install
fi

# Start development
bun run dev
```

**scripts/deploy-staging.sh:**

```bash
#!/bin/bash
set -e

# Load environment
source .env 2>/dev/null || true

SERVICE_NAME="${SERVICE_NAME:-my-service}"
GCP_REGION="${GCP_REGION:-europe-west1}"
GCP_PROJECT="${GCP_PROJECT_STAGING:-}"

if [ -z "$GCP_PROJECT" ]; then
  echo "❌ GCP_PROJECT_STAGING not set in .env"
  exit 1
fi

echo "🚀 Deploying to GCP Cloud Run (staging)..."
echo "   Service: ${SERVICE_NAME}-staging"
echo "   Region: ${GCP_REGION}"
echo "   Project: ${GCP_PROJECT}"

gcloud run deploy "${SERVICE_NAME}-staging" \
  --source . \
  --region "$GCP_REGION" \
  --project "$GCP_PROJECT" \
  --allow-unauthenticated \
  --cpu 1 \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 3

echo "✅ Staging deployment complete"
```

**scripts/deploy-production.sh:**

```bash
#!/bin/bash
set -e

# Safety gate
if [[ "$1" != "yes" ]]; then
  echo "⚠️  Production deployment requires explicit confirmation"
  echo "Usage: ./scripts/deploy-production.sh yes"
  exit 1
fi

# Load environment
source .env 2>/dev/null || true

SERVICE_NAME="${SERVICE_NAME:-my-service}"
GCP_REGION="${GCP_REGION:-europe-west1}"
GCP_PROJECT="${GCP_PROJECT_PROD:-}"

if [ -z "$GCP_PROJECT" ]; then
  echo "❌ GCP_PROJECT_PROD not set in .env"
  exit 1
fi

echo "🚀 Deploying to GCP Cloud Run (production)..."
echo "   Service: ${SERVICE_NAME}"
echo "   Region: ${GCP_REGION}"
echo "   Project: ${GCP_PROJECT}"

# TypeScript check (if enabled)
# bun run typecheck

# Run tests
bun test

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$GCP_REGION" \
  --project "$GCP_PROJECT" \
  --min-instances 1 \
  --max-instances 10 \
  --cpu 2 \
  --memory 1Gi \
  --cpu-boost

echo "✅ Production deployment complete"
```

## Phase 4: Make Scripts Executable

```bash
chmod +x scripts/*.sh
```

## Phase 5: Update Project CLAUDE.md

Append deployment documentation to `.claude/CLAUDE.md`:

```markdown
## Deployment

| Command                              | Environment | Notes              |
| ------------------------------------ | ----------- | ------------------ |
| `./scripts/dev.sh`                   | Local       | Hot reload enabled |
| `./scripts/deploy-staging.sh`        | Staging     | Preview/test       |
| `./scripts/deploy-production.sh yes` | Production  | Requires "yes"     |
```

## Output

```
═══════════════════════════════════════════════════
✅ Deployment scripts generated
═══════════════════════════════════════════════════

Created:
  📄 scripts/dev.sh
  📄 scripts/deploy-staging.sh
  📄 scripts/deploy-production.sh

Updated:
  📄 .claude/CLAUDE.md (deployment docs)

Next steps:
  1. Review scripts in scripts/
  2. Set environment variables in .env (if using Cloud Run)
  3. Run ./scripts/dev.sh to start development
```
