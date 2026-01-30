# GCP Safety Rules

> Prevent accidental resource deletion and billing surprises

## Deletion Protection

**NEVER delete GCP resources without explicit user approval.**

### Prohibited Without Approval

| Resource Type       | Command                           | Risk Level |
| ------------------- | --------------------------------- | ---------- |
| Cloud Run services  | `gcloud run services delete`      | 🔴 High    |
| Cloud SQL instances | `gcloud sql instances delete`     | 🔴 High    |
| GCS buckets         | `gsutil rm -r gs://`              | 🔴 High    |
| Compute instances   | `gcloud compute instances delete` | 🔴 High    |
| IAM policies        | `gcloud iam ... remove`           | 🔴 High    |
| Secrets             | `gcloud secrets delete`           | 🟡 Medium  |
| Container images    | `gcloud artifacts docker delete`  | 🟡 Medium  |

### Before Any Deletion

1. **Ask user explicitly**: "Delete [resource]? This cannot be undone."
2. **Require "yes" confirmation** in user response
3. **Never batch delete** without listing each resource

```bash
# ❌ NEVER do this automatically
gcloud run services delete my-service --quiet

# ✅ Always ask first, then execute with confirmation
gcloud run services delete my-service
# (prompts for confirmation)
```

## Billing Safety

### Cost Alerts

Before deploying to production, verify:

- [ ] Budget alerts configured
- [ ] Billing account linked
- [ ] Resource quotas set

### Resource Sizing

| Environment | CPU | Memory | Min Instances |
| ----------- | --- | ------ | ------------- |
| Staging     | 1   | 512Mi  | 0             |
| Production  | 2   | 1Gi    | 1             |

**Rule:** Start small, scale up based on metrics.

## Environment Separation

| Check           | Staging       | Production                 |
| --------------- | ------------- | -------------------------- |
| Project ID      | `*-staging`   | `*-prod` or `*-production` |
| Service account | Limited roles | Minimal required roles     |
| VPC             | Separate      | Isolated                   |

**Rule:** Never deploy to production without explicit "production" or "prod" in command.

## IAM Safety

### Prohibited Actions

- Granting `roles/owner` programmatically
- Removing billing admin access
- Modifying organization policies

### Safe Patterns

```bash
# ✅ Service-specific, minimal role
gcloud run services add-iam-policy-binding SERVICE \
  --member="serviceAccount:SA" \
  --role="roles/run.invoker"

# ❌ Too broad
gcloud projects add-iam-policy-binding PROJECT \
  --member="user:EMAIL" \
  --role="roles/editor"
```

## Flags

- Any `delete` command without user confirmation
- `--quiet` or `-q` flags that skip confirmations
- Production deployments without explicit approval
- IAM changes granting broad permissions
