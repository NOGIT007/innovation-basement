# GCP Safety Policy

## ⚠️ CRITICAL: No Deletions Without Approval

This skill will **NEVER** perform destructive operations on GCP without explicit user approval.

## Blocked Operations

The following gcloud commands are **FORBIDDEN** in all scripts:

```bash
# NEVER executed by this skill:
gcloud run services delete
gcloud run revisions delete
gcloud projects delete
gcloud storage rm
gcloud storage buckets delete
gcloud compute instances delete
gcloud sql instances delete
gcloud functions delete
```

## What This Skill CAN Do

✅ **Allowed operations:**

- Deploy new services
- Update existing services
- List services and revisions
- Describe service details
- View logs
- Traffic routing between revisions (for rollback)

## What Requires YOUR Manual Approval

❌ **Must be done manually by user:**

- Deleting Cloud Run services
- Deleting revisions
- Deleting projects
- Deleting storage buckets/objects
- Deleting databases
- Modifying IAM permissions
- Any destructive operation

## Rollback vs Delete

**Rollback** (allowed) - Routes traffic to previous revision:

```bash
gcloud run services update-traffic SERVICE --to-revisions OLD_REVISION=100
```

**Delete** (BLOCKED) - Removes the service entirely:

```bash
# This script will NEVER run this command
gcloud run services delete SERVICE
```

## If You Need to Delete Something

Run the command manually in your terminal:

```bash
# Delete a Cloud Run service (manual only)
gcloud run services delete SERVICE_NAME --region REGION --project PROJECT

# Delete old revisions (manual only)
gcloud run revisions delete REVISION_NAME --region REGION --project PROJECT
```

## Environment Protection

The scripts enforce:

1. Staging and Production use separate GCP projects
2. Production requires typing "yes" to deploy
3. Tests must pass before production deployment
4. No delete commands are ever generated or executed
