---
allowed-tools: Bash(gcloud:*), Bash(docker:*), Read
description: Deploy to GCP Cloud Run staging environment
---

# Deploy to Staging

Deploy current project to GCP Cloud Run staging environment.

## Step 1: Verify Environment

```bash
# Check for required files
if [ ! -f "Dockerfile" ]; then
  echo "❌ Error: Dockerfile not found"
  exit 1
fi

if [ ! -f ".env.example" ]; then
  echo "⚠️ Warning: .env.example not found"
fi
```

## Step 2: Load Configuration

Read `.env.example` or `.env.staging` for:

- `GCP_PROJECT_STAGING` - GCP project ID
- `GCP_REGION` - Deployment region (default: europe-west1)
- `SERVICE_NAME` - Cloud Run service name

```bash
# Verify gcloud is configured
gcloud config get-value project
gcloud config get-value account
```

## Step 3: Build Container

```bash
# Build with Cloud Build (recommended)
gcloud builds submit --tag gcr.io/$GCP_PROJECT_STAGING/$SERVICE_NAME

# Or build locally and push
docker build -t gcr.io/$GCP_PROJECT_STAGING/$SERVICE_NAME .
docker push gcr.io/$GCP_PROJECT_STAGING/$SERVICE_NAME
```

## Step 4: Deploy to Cloud Run

```bash
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$GCP_PROJECT_STAGING/$SERVICE_NAME \
  --platform managed \
  --region $GCP_REGION \
  --allow-unauthenticated \
  --cpu 1 \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 3 \
  --port 8080
```

## Step 5: Verify Deployment

```bash
# Get service URL
gcloud run services describe $SERVICE_NAME \
  --region $GCP_REGION \
  --format "value(status.url)"

# Check service status
gcloud run services list --filter="SERVICE:$SERVICE_NAME"
```

## Output

Report:

- ✅ Service URL
- 📊 Resource allocation (CPU, memory)
- 🔄 Revision name
- ⏱️ Deployment time

## Rules

- Staging uses minimal resources (1 CPU, 512Mi)
- Allow unauthenticated for easier testing
- Min instances = 0 to save costs
- Always verify deployment succeeded
