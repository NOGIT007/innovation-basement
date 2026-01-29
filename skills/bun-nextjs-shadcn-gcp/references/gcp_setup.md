# GCP Cloud Run Setup Guide

## Prerequisites

1. Google Cloud Account with billing
2. gcloud CLI installed
3. Docker (optional, for local testing)

## Setup

```bash
# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

## Deploy Commands

```bash
# Deploy from source
gcloud run deploy SERVICE_NAME --source . --region europe-west1

# Get service URL
gcloud run services describe SERVICE_NAME --region europe-west1 --format "value(status.url)"
```

## Rollback

```bash
# List revisions
gcloud run revisions list --service SERVICE_NAME --region europe-west1

# Rollback
gcloud run services update-traffic SERVICE_NAME --region europe-west1 --to-revisions REVISION_NAME=100
```

## Useful Commands

```bash
# View logs
gcloud run services logs read SERVICE_NAME --region europe-west1

# Delete service
gcloud run services delete SERVICE_NAME --region europe-west1
```
