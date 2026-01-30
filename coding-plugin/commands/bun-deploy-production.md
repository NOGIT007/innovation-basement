---
allowed-tools: Bash(gcloud:*), Bash(docker:*), Read
description: Deploy to GCP Cloud Run production (requires "yes" confirmation)
argument-hint: [yes]
---

# Deploy to Production

Deploy current project to GCP Cloud Run production environment.

## ⚠️ Production Safety

**This command requires explicit "yes" confirmation.**

```bash
CONFIRM="$ARGUMENTS"
if [ "$CONFIRM" != "yes" ]; then
  echo "❌ Production deployment requires explicit confirmation"
  echo ""
  echo "Usage: /code:bun-deploy-production yes"
  echo ""
  echo "This will deploy to PRODUCTION. Make sure:"
  echo "  ✅ Staging deployment tested"
  echo "  ✅ All tests passing"
  echo "  ✅ Version bumped"
  exit 1
fi
```

## Step 1: Pre-deployment Checks

```bash
# Verify staging was deployed first
echo "🔍 Checking staging deployment..."
gcloud run services describe $SERVICE_NAME \
  --project $GCP_PROJECT_STAGING \
  --region $GCP_REGION \
  --format "value(status.url)" 2>/dev/null || {
    echo "❌ Error: Deploy to staging first"
    exit 1
  }

# Verify tests pass
echo "🧪 Running tests..."
bun test || {
  echo "❌ Error: Tests failed. Fix before deploying to production."
  exit 1
}
```

## Step 2: Load Configuration

Read `.env.example` or `.env.production` for:

- `GCP_PROJECT_PRODUCTION` - GCP project ID
- `GCP_REGION` - Deployment region
- `SERVICE_NAME` - Cloud Run service name

## Step 3: Build Container

```bash
# Build with Cloud Build
gcloud builds submit \
  --project $GCP_PROJECT_PRODUCTION \
  --tag gcr.io/$GCP_PROJECT_PRODUCTION/$SERVICE_NAME
```

## Step 4: Deploy to Cloud Run

```bash
gcloud run deploy $SERVICE_NAME \
  --project $GCP_PROJECT_PRODUCTION \
  --image gcr.io/$GCP_PROJECT_PRODUCTION/$SERVICE_NAME \
  --platform managed \
  --region $GCP_REGION \
  --no-allow-unauthenticated \
  --cpu 2 \
  --memory 1Gi \
  --min-instances 1 \
  --max-instances 10 \
  --port 8080 \
  --cpu-boost \
  --session-affinity
```

## Step 5: Verify Deployment

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --project $GCP_PROJECT_PRODUCTION \
  --region $GCP_REGION \
  --format "value(status.url)")

echo "🚀 Production URL: $SERVICE_URL"

# Check revision
gcloud run revisions list \
  --project $GCP_PROJECT_PRODUCTION \
  --service $SERVICE_NAME \
  --region $GCP_REGION \
  --limit 3
```

## Output

Report:

- 🚀 Production URL
- 📊 Resource allocation (2 CPU, 1Gi)
- 🔄 Active revision
- 📈 Traffic split (if gradual rollout)

## Rules

- **Requires "yes" argument** - No silent deployments
- **Staging first** - Must have staging deployment
- **Tests must pass** - No broken deployments
- Production uses more resources (2 CPU, 1Gi)
- Auth required (no-allow-unauthenticated)
- Min instances = 1 for fast cold starts
- CPU boost enabled for startup performance
